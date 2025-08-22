import os
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from config import Config


def save_post_to_file(text: str, platform: str, topic: str, tone: str) -> str:
    """Save generated social media post to a file for manual posting."""
    # Create posts directory if it doesn't exist
    posts_dir = Path(Config.POSTS_DIR)
    posts_dir.mkdir(exist_ok=True)
    
    # Create platform-specific subdirectory
    platform_dir = posts_dir / platform.lower().replace(" ", "_")
    platform_dir.mkdir(exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.replace(" ", "_").replace("/", "_")[:30]
    filename = f"{platform.lower()}_{timestamp}_{safe_topic}.md"
    filepath = platform_dir / filename
    
    # Get character limit for the platform
    char_limit = Config.PLATFORM_LIMITS.get(platform, 280)
    char_count = len(text)
    
    # Write post content in markdown format
    content = f"""# {platform} Post

**Topic:** {topic}  
**Tone:** {tone}  
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Character Count:** {char_count}/{char_limit}  
**Platform:** {platform}

---

{text}

---

## Instructions
Copy this text and paste it into {platform} to post manually.

## Character Status
{'✅ Within limit' if char_count <= char_limit else '⚠️ Exceeds limit'}
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return str(filepath)


def save_tweet_to_file(text: str, topic: str, tone: str) -> str:
    """Legacy function for backward compatibility - now calls save_post_to_file for Twitter"""
    return save_post_to_file(text, "Twitter", topic, tone)


def post_tweet_via_web(text: str, timeout: int = 30) -> bool:
    """Post tweet directly to X.com using web automation with existing profile."""
    try:
        # Setup Chrome options to use existing profile
        options = Options()
        
        # Use existing Chrome profile to access logged-in X.com session
        user_data_dir = os.path.expandvars(os.path.expanduser(str(Config.CHROME_PROFILE_PATH)))
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument(f"--profile-directory={Config.CHROME_PROFILE_NAME}")
        
        # Stability flags
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument("--remote-allow-origins=*")
        
        # Launch Chrome with existing profile
        driver = webdriver.Chrome(options=options)
        
        try:
            # Navigate to X.com compose page
            driver.get("https://x.com/compose/tweet")
            time.sleep(3)  # Wait for page to load
            
            # Wait for and find the tweet composer
            wait = WebDriverWait(driver, timeout)
            
            # Look for the tweet input field (X.com uses different selectors)
            tweet_input = None
            selectors = [
                "//div[@role='textbox']",
                "//div[@data-testid='tweetTextarea_0']",
                "//div[@contenteditable='true']",
                "//textarea[@data-testid='tweetTextarea_0']"
            ]
            
            for selector in selectors:
                try:
                    tweet_input = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not tweet_input:
                raise Exception("Could not find tweet input field")
            
            # Clear and type the tweet
            tweet_input.click()
            tweet_input.clear()
            tweet_input.send_keys(text)
            time.sleep(1)
            
            # Find and click the Tweet button
            tweet_button = None
            button_selectors = [
                "//div[@data-testid='tweetButtonInline']",
                "//div[@data-testid='tweetButton']",
                "//div[contains(text(), 'Tweet')]",
                "//button[contains(text(), 'Tweet')]"
            ]
            
            for selector in button_selectors:
                try:
                    tweet_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not tweet_button:
                raise Exception("Could not find Tweet button")
            
            # Click the tweet button
            tweet_button.click()
            time.sleep(3)  # Wait for tweet to post
            
            return True
            
        finally:
            # Keep browser open briefly to show the result, then close
            time.sleep(2)
            driver.quit()
            
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return False


