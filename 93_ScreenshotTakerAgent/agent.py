import speech_recognition as sr
import pyautogui
import os
import datetime
import time
import sys
from PIL import Image
from mss import mss
from utils.llm_service import LLMService
from config import Config
from colorama import Fore, Style

class ScreenshotTakerAgent:
    """
    An agent that takes screenshots based on voice commands.
    """
    def __init__(self):
        """
        Initializes the ScreenshotTakerAgent.
        """
        self.recognizer = sr.Recognizer()
        self.screenshots_dir = Config.SCREENSHOTS_DIR
        Config.ensure_screenshots_dir_exists()
        self.llm_service = LLMService(provider="gemini") # Default to Gemini
        self.last_screenshot_filepath = None
        self.prompt_template = self._load_prompt_template("prompts/screenshot_prompt.txt")

    def _load_prompt_template(self, filepath):
        """
        Loads the prompt template from a file.
        """
        with open(filepath, "r") as f:
            return f.read()

    def listen_for_command(self):
        """
        Listens for a voice command from the user.
        """
        with sr.Microphone() as source:
            print(f"{Fore.CYAN}Listening for command...{Style.RESET_ALL}")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio).lower()
            print(f"{Fore.YELLOW}User said: {command}{Style.RESET_ALL}")
            return command
        except sr.UnknownValueError:
            print(f"{Fore.RED}Sorry, I did not understand that.{Style.RESET_ALL}")
            return None
        except sr.RequestError as e:
            print(f"{Fore.RED}Could not request results from Google Speech Recognition service; {e}{Style.RESET_ALL}")
            return None

    def take_screenshot(self, window=False):
        """
        Takes a screenshot of the entire screen or the active window.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{'window_' if window else ''}{timestamp}.png"
        filepath = os.path.join(self.screenshots_dir, filename)

        if window:
            try:
                active_window = pyautogui.getActiveWindow()
                if active_window:
                    # Capture the active window using its coordinates
                    with mss() as sct:
                        monitor = {
                            "top": active_window.top,
                            "left": active_window.left,
                            "width": active_window.width,
                            "height": active_window.height,
                        }
                        sct_img = sct.grab(monitor)
                        # Convert to PIL Image and save
                        Image.frombytes("RGB", sct_img.size, sct_img.rgb).save(filepath)
                    print(f"{Fore.GREEN}Window screenshot saved: {filepath}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}No active window found. Taking a full screenshot instead.{Style.RESET_ALL}")
                    pyautogui.screenshot(filepath)
            except Exception as e:
                print(f"{Fore.RED}Could not capture active window ({e}). Taking a full screenshot instead.{Style.RESET_ALL}")
                pyautogui.screenshot(filepath)
        else:
            pyautogui.screenshot(filepath)
        
        print(f"{Fore.GREEN}Screenshot saved: {filepath}{Style.RESET_ALL}")
        return filepath

    def save_screenshot(self, filepath, new_name=None):
        """
        Saves the screenshot with a new name if provided.
        """
        if new_name:
            new_filepath = os.path.join(self.screenshots_dir, f"{new_name}.png")
            os.rename(filepath, new_filepath)
            print(f"{Fore.GREEN}Screenshot saved as: {new_filepath}{Style.RESET_ALL}")
            return new_filepath
        return filepath

    def open_last_screenshot(self):
        """
        Opens the most recent screenshot.
        """
        files = os.listdir(self.screenshots_dir)
        if not files:
            print(f"{Fore.YELLOW}No screenshots found.{Style.RESET_ALL}")
            return

        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.screenshots_dir, f)))
        filepath = os.path.join(self.screenshots_dir, latest_file)
        
        try:
            # Using os.startfile for Windows compatibility
            os.startfile(filepath)
            print(f"{Fore.GREEN}Opening screenshot: {filepath}{Style.RESET_ALL}")
        except AttributeError:
            # For non-Windows systems
            import subprocess
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filepath])
            print(f"{Fore.GREEN}Opening screenshot: {filepath}{Style.RESET_ALL}")


    def process_command(self, command):
        """
        Processes the given command.
        """
        if not command:
            return

        # Use LLM to interpret the command
        full_prompt = self.prompt_template.format(command=command)
        llm_response = self.llm_service.generate_response(full_prompt)
        print(f"{Fore.BLUE}LLM Response: {llm_response}{Style.RESET_ALL}")

        # Parse LLM response to determine intent and parameters
        intent = None
        name = None
        window = False

        for line in llm_response.split('\n'):
            if line.startswith("Intent:"):
                intent = line.split(":")[1].strip()
            elif line.startswith("Name:"):
                name = line.split(":")[1].strip()
            elif line.startswith("Window:"):
                window = line.split(":")[1].strip().lower() == "true"

        if intent == "take_screenshot":
            self.last_screenshot_filepath = self.take_screenshot(window=window)
        elif intent == "save_screenshot":
            if self.last_screenshot_filepath:
                self.save_screenshot(self.last_screenshot_filepath, new_name=name)
            else:
                print(f"{Fore.YELLOW}No screenshot to save. Please take a screenshot first.{Style.RESET_ALL}")
        elif intent == "open_last_screenshot":
            self.open_last_screenshot()
        else:
            print(f"{Fore.RED}Unknown command or intent not recognized by LLM.{Style.RESET_ALL}")

    def run(self):
        """
        Runs the agent's main loop.
        """
        while True:
            command = self.listen_for_command()
            self.process_command(command)
            time.sleep(1)

if __name__ == '__main__':
    agent = ScreenshotTakerAgent()
    agent.run()
