from datetime import datetime
from pathlib import Path
import time
import re

from config import get_linkedin_method, get_linkedin_username, get_linkedin_password


class LinkedInService:
    def __init__(self) -> None:
        self.method = get_linkedin_method()
        self.log_path = Path(__file__).resolve().parent / "logs" / "linkedin_actions.log"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def post_now(self, text: str) -> bool:
        if self.method == "simulate":
            return self._simulate_post(text)
        if self.method == "playwright":
            return self._playwright_post(text)
        # Fallback
        return self._simulate_post(text)

    def _simulate_post(self, text: str) -> bool:
        entry = f"[{datetime.now().isoformat()}] POST: {len(text)} chars\n{text}\n---\n"
        self.log_path.write_text(self.log_path.read_text(encoding="utf-8") + entry if self.log_path.exists() else entry, encoding="utf-8")
        return True

    def _append_log(self, message: str) -> None:
        entry = f"[{datetime.now().isoformat()}] {message}\n"
        self.log_path.write_text(self.log_path.read_text(encoding="utf-8") + entry if self.log_path.exists() else entry, encoding="utf-8")

    def _playwright_post(self, text: str) -> bool:
        try:
            from playwright.sync_api import sync_playwright
        except Exception as exc:
            self._append_log(f"Playwright not installed: {exc}")
            return False

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                page.set_default_timeout(60000)
                # Attempt login if credentials provided
                username = get_linkedin_username()
                password = get_linkedin_password()
                if username and password:
                    page.goto("https://www.linkedin.com/login")
                    # Wait for login inputs to be visible
                    page.wait_for_selector("input#username", state="visible", timeout=120000)
                    page.fill("input#username", username)
                    page.fill("input#password", password)
                    page.click("button[type='submit']")
                    # After submit, allow for redirects/MFA and wait for feed readiness
                    self._wait_for_login_or_mfa(page, overall_timeout_ms=240000)

                # Navigate to feed
                page.goto("https://www.linkedin.com/feed/")
                self._wait_for_feed_ready(page, overall_timeout_ms=180000)
                # Try to dismiss cookie or transient banners if present
                self._dismiss_banners(page)

                # Click start post (may vary by locale/DOM; selectors are best-effort)
                # Ensure we're at the top where the composer lives
                try:
                    page.evaluate("window.scrollTo(0,0)")
                except Exception:
                    pass
                clicked = self._retry_click(
                    page,
                    [
                        {"by": "text", "value": "Start a post"},
                        {"by": "text", "value": "Create a post"},
                        {"by": "text", "value": "Start post"},
                        {"by": "css", "value": "button[aria-label*='Start a post']"},
                        {"by": "css", "value": "button[aria-label*='Create a post']"},
                        {"by": "css", "value": "button[aria-label*='post']"},
                        {"by": "css", "value": "div.share-box-feed-entry__trigger"},
                        {"by": "css", "value": "button.share-box-feed-entry__trigger"},
                        {"by": "css", "value": "div[role='button']:has-text('Start a post')"},
                        {"by": "css", "value": "[placeholder='Start a post']"},
                        {"by": "css", "value": "[data-control-name='sharebox_trigger']"},
                        {"by": "css", "value": "button[data-test-reaction-bar-start-a-post-button]"},
                        {"by": "css", "value": "button[aria-label='Start a post']"},
                        {"by": "role", "value": ("button", "Start a post")},
                        {"by": "role", "value": ("button", "Create a post")},
                    ],
                    timeout_per_try_ms=15000,
                    max_tries=6,
                )
                if not clicked:
                    # As a last resort, click the center of the visible box that contains the text
                    try:
                        box = page.locator("text=Start a post").first.bounding_box()
                        if box:
                            page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
                            clicked = True
                    except Exception:
                        pass
                if not clicked:
                    # Fallback: use URL flag to open share composer
                    try:
                        page.goto("https://www.linkedin.com/feed/?shareActive=true")
                        self._wait_for_any_selector(page, [
                            "div[role='dialog']",
                            "div[aria-modal='true']",
                            "div.share-box__modal",
                        ], timeout_ms=60000)
                        clicked = True
                    except Exception:
                        pass
                if not clicked:
                    raise RuntimeError("Could not open post composer")

                # Wait for composer dialog and editor
                self._wait_for_any_selector(page, [
                    "div[role='dialog']",
                    "div[aria-modal='true']",
                    "div.share-box__modal" ,
                ], timeout_ms=120000)
                dialog = page.locator("div[role='dialog'], div[aria-modal='true'], div.share-box__modal").first
                self._wait_for_any_selector(dialog, [
                    "div[role='textbox']",
                    "div[contenteditable='true']",
                    "div[aria-label*='What do you want to talk about']",
                    "div.editor-content",
                ], timeout_ms=120000)
                editor = dialog.locator("div[role='textbox'], div[contenteditable='true'], div[aria-label*='What do you want to talk about'], div.editor-content").first
                editor.click()
                try:
                    editor.fill("")
                except Exception:
                    pass
                try:
                    editor.type(text, delay=5)
                except Exception:
                    # Fallback: use execCommand to insert text
                    try:
                        dialog.evaluate("(root, t) => { const el = root.querySelector(\"div[role='textbox'], div[contenteditable='true']\"); if (el) { el.focus(); document.execCommand('insertText', false, t); } }", text)
                    except Exception:
                        # Final fallback: paste via clipboard
                        try:
                            dialog.page.keyboard.insert_text(text)
                        except Exception:
                            raise

                # Click Post button
                posted = self._retry_click(
                    dialog,
                    [
                        {"by": "role", "value": ("button", "Post")},
                        {"by": "css", "value": "button:has-text('Post')"},
                        {"by": "css", "value": "button.share-actions__primary-action"},
                        {"by": "css", "value": "button[aria-label='Post']"},
                        {"by": "css", "value": "button[data-test-share-cta]"},
                        {"by": "css", "value": "button.artdeco-button--primary"},
                    ],
                    timeout_per_try_ms=15000,
                    max_tries=6,
                )
                if not posted:
                    raise RuntimeError("Failed to click Post button after retries")

                # Wait briefly for confirmation
                # Wait for toast/confirmation or post composer to close
                try:
                    page.wait_for_selector("div:has-text('Post successful')", timeout=5000)
                except Exception:
                    pass
                page.wait_for_timeout(3000)
                self._append_log("Playwright posted successfully (best-effort).")
                context.close()
                browser.close()
                return True
        except Exception as exc:
            # Save a screenshot on failure
            try:
                ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                shot = self.log_path.parent / f"playwright_error_{ts}.png"
                page.screenshot(path=str(shot))
                self._append_log(f"Playwright post error (screenshot saved {shot}): {exc}")
            except Exception:
                self._append_log(f"Playwright post error: {exc}")
            return False

    # --- Helpers ---
    def _wait_for_feed_ready(self, page, overall_timeout_ms: int = 120000) -> None:
        """Wait until the LinkedIn feed is ready by checking common UI anchors.

        We consider the page ready when one of these appears:
        - "Start a post" text
        - A button with aria-label containing "Start a post"
        - The global nav/home icon container (fallback)
        """
        deadline = time.time() + (overall_timeout_ms / 1000.0)
        while time.time() < deadline:
            try:
                if page.is_visible("text=Start a post"):
                    return
            except Exception:
                pass
            try:
                if page.is_visible("button[aria-label*='Start a post']"):
                    return
            except Exception:
                pass
            try:
                if page.is_visible("header.global-nav__nav"):
                    # Fallback readiness
                    return
            except Exception:
                pass
            # Wait for network to go idle briefly and try again
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass
        raise TimeoutError("Feed not ready within timeout")

    def _wait_for_login_or_mfa(self, page, overall_timeout_ms: int = 240000) -> None:
        """Wait until either feed is ready or MFA checkpoint is resolved."""
        deadline = time.time() + (overall_timeout_ms / 1000.0)
        while time.time() < deadline:
            # If feed is ready, we are done
            try:
                if page.url and re.search(r"linkedin\.com/(feed|feed/|/?$)", page.url):
                    try:
                        self._wait_for_feed_ready(page, overall_timeout_ms=30000)
                        return
                    except Exception:
                        pass
            except Exception:
                pass

            # Detect common MFA prompts and wait for user action
            try:
                if page.is_visible("input[name='pin']") or page.is_visible("text=/verification code/i"):
                    # Give user time to complete MFA, then proceed
                    try:
                        page.wait_for_load_state("networkidle", timeout=15000)
                    except Exception:
                        pass
            except Exception:
                pass

            # Progressively wait a bit and retry
            try:
                page.wait_for_timeout(2000)
            except Exception:
                pass
        # If we exit the loop, just return and let next steps try to open the feed
        return

    def _retry_click(self, page_or_locator, targets, timeout_per_try_ms: int, max_tries: int) -> bool:
        """Try multiple selectors/locators with retries."""
        for _ in range(max_tries):
            for tgt in targets:
                try:
                    if tgt["by"] == "text":
                        loc = page_or_locator.get_by_text(tgt["value"]).first
                        try:
                            loc.scroll_into_view_if_needed(timeout=timeout_per_try_ms)
                        except Exception:
                            pass
                        try:
                            loc.click(timeout=timeout_per_try_ms)
                        except Exception:
                            loc.click(timeout=timeout_per_try_ms, force=True)
                        return True
                    if tgt["by"] == "css":
                        loc = page_or_locator.locator(tgt["value"]).first
                        try:
                            loc.scroll_into_view_if_needed(timeout=timeout_per_try_ms)
                        except Exception:
                            pass
                        try:
                            loc.click(timeout=timeout_per_try_ms)
                        except Exception:
                            loc.click(timeout=timeout_per_try_ms, force=True)
                        return True
                    if tgt["by"] == "role":
                        role, name = tgt["value"]
                        loc = page_or_locator.get_by_role(role, name=name)
                        try:
                            loc.scroll_into_view_if_needed(timeout=timeout_per_try_ms)
                        except Exception:
                            pass
                        try:
                            loc.click(timeout=timeout_per_try_ms)
                        except Exception:
                            loc.click(timeout=timeout_per_try_ms, force=True)
                        return True
                except Exception:
                    continue
            # brief pause before next round
            try:
                # page_or_locator may be a Locator; use page from context if needed
                (page_or_locator.page if hasattr(page_or_locator, 'page') else page_or_locator).wait_for_timeout(1500)
            except Exception:
                pass
        return False

    def _dismiss_banners(self, page) -> None:
        # Try common cookie/consent/coachmark banners
        selectors = [
            {"by": "text", "value": "Accept"},
            {"by": "text", "value": "Accept all"},
            {"by": "text", "value": "Got it"},
            {"by": "css", "value": "button.artdeco-button--primary"},
        ]
        try:
            self._retry_click(page, selectors, timeout_per_try_ms=2000, max_tries=1)
        except Exception:
            pass


