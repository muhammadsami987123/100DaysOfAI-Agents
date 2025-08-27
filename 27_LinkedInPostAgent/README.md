## Day 27 – LinkedInPostAgent (Pro Version)

Create, preview, schedule, and post LinkedIn content via CLI. Supports simulate mode (logs only) and Playwright automation to post through the LinkedIn UI.

### Features
- AI or manual post creation (topic → post, paste, or file input)
- Smart editor: tone, hashtags, emojis, 3k-char trimming
- Actions: Post now, Save as draft, Schedule (with background runner)
- Local history and logs with timestamps

### Setup
1) Python environment
```
pip install -r requirements.txt
```
2) Configure `.env` (at minimum set the mode)
```
# Text generation (stub works offline; key optional)
OPENAI_API_KEY=your_key_here

# Mode: simulate (default) or playwright
LINKEDIN_METHOD=simulate

# Optional for Playwright auto-login
LINKEDIN_USERNAME=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

### Usage
- Create a post (interactive CLI):
```
python agent.py create
```
- Schedule runner (executes scheduled posts):
```
python agent.py schedule-runner
```

### Simulate mode
- No real posting occurs. “Post now” writes to `logs/linkedin_actions.log`.
- Drafts are saved in `drafts/`. Scheduled items in `scheduled_posts.json`.

### Playwright mode
1) Install browsers once:
```
python -m playwright install
```
2) In `.env` set:
```
LINKEDIN_METHOD=playwright
# Optional: credentials to auto-login (or log in manually in the opened browser)
LINKEDIN_USERNAME=your_email@example.com
LINKEDIN_PASSWORD=your_password
```
3) Run create flow and choose Post now:
```
python agent.py create
```
Notes:
- The agent waits for the feed to be ready, opens the composer, types the post, and clicks Post.
- If UI text differs (e.g., localized), tell us the exact composer and post button text; we’ll add selectors.
- On failure, a screenshot is saved in `logs/` for debugging.

### Files & Folders
- `agent.py`: CLI entry and interactive flow
- `linkedin_service.py`: simulate and Playwright posting logic
- `openai_utils.py`: AI generation and enhancements (offline stub provided)
- `scheduler.py`: simple JSON-backed scheduler loop
- `drafts/`, `posts/`, `logs/`: outputs and logs


### Next Steps
- OpenAI integration:
  - Replace `_fake_ai_generate` with real OpenAI SDK calls.
  - Add rate limiting and error handling/retries.
  - Support system prompts for stricter tone/structure control.
- LinkedIn automation:
  - Implement Playwright login and post publishing flow.
  - Store session state/cookies securely to avoid re-login.
  - Add optional draft support if API/browser flows allow it.
- Scheduling service:
  - Run `schedule-runner` as a Windows service or background task.
  - Add command to list/cancel scheduled posts from CLI.
- Storage/history:
  - Persist posts in `posts/` and maintain `post_history.json` with richer metadata.
  - Add a `drafts list` and `drafts post <id>` CLI.
- Smart editor:
  - Enforce 3,000 char limit with a visual counter and soft-warnings.
  - Add rewrite options: shorten, expand, simplify, add CTA, add examples.
- Optional UI:
  - Minimal Flask/FastAPI web UI for preview and scheduling.
  - Local auth, logs view, and posts history table.
- Configuration:
  - Expand `.env` with timezone and method toggles.
  - Add schema validation and helpful startup diagnostics.
- Testing & CI:
  - Unit tests for parser, scheduler, and text utilities.
  - E2E tests for simulated posting; mock OpenAI calls.
  - Pre-commit hooks for formatting and linting.
- Packaging:
  - Add entry points for `linkedin-agent` CLI via `setup.py`/`pyproject.toml`.
  - Version and changelog, usage examples, and troubleshooting guide.


