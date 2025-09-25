import speech_recognition as sr
import pyttsx3
import subprocess
import winreg
import wmi
import re
import os
from datetime import datetime

from config import (
    OPENAI_API_KEY,
    GREETING_MESSAGE,
    UNINSTALL_CONFIRMATION_PROMPT,
    APP_NOT_FOUND_MESSAGE,
    LIST_APPS_MESSAGE,
    UNINSTALL_SUCCESS_MESSAGE,
    UNINSTALL_FAILED_MESSAGE,
    NO_APPS_FOUND_MESSAGE,
    VOICE_INPUT_TIMEOUT,
    VOICE_INPUT_PHRASE_TIME_LIMIT
)

class AppUninstallerAgent:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.wmi_c = wmi.WMI()

    def speak(self, text):
        """Converts text to speech."""
        print(f"AI: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_for_command(self):
        """Listens for a voice command from the user."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.speak("Please say a command.")
            try:
                audio = self.recognizer.listen(source, timeout=VOICE_INPUT_TIMEOUT, phrase_time_limit=VOICE_INPUT_PHRASE_TIME_LIMIT)
                command = self.recognizer.recognize_google(audio).lower()
                return command
            except sr.WaitTimeoutError:
                self.speak("No speech detected. Please try again.")
                return None
            except sr.UnknownValueError:
                self.speak("Could not understand audio. Please try again.")
                return None
            except sr.RequestError as e:
                self.speak(f"Could not request results from Google Speech Recognition service; {e}")
                return None

    def get_installed_applications(self):
        """Retrieves a list of installed applications on Windows."""
        apps = []
        uninstall_keys = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]

        for uninstall_key in uninstall_keys:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key, 0, winreg.KEY_READ)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        
                        display_name = ""
                        uninstall_string = ""
                        install_date = ""
                        estimated_size = 0

                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        except FileNotFoundError:
                            pass

                        try:
                            uninstall_string = winreg.QueryValueEx(subkey, "UninstallString")[0]
                        except FileNotFoundError:
                            pass
                        
                        try:
                            install_date = winreg.QueryValueEx(subkey, "InstallDate")[0]
                        except FileNotFoundError:
                            pass

                        try:
                            estimated_size = winreg.QueryValueEx(subkey, "EstimatedSize")[0]
                        except FileNotFoundError:
                            pass
                        
                        if display_name and uninstall_string:
                            apps.append({
                                "name": display_name,
                                "uninstall_string": uninstall_string,
                                "install_date": install_date,
                                "estimated_size": estimated_size
                            })
                        
                        winreg.CloseKey(subkey)
                    except OSError:
                        continue
                winreg.CloseKey(key)
            except OSError:
                continue
        return apps

    def list_applications(self, filters=None):
        """Lists installed applications with optional filters."""
        apps = self.get_installed_applications()
        filtered_apps = []

        if not apps:
            self.speak(NO_APPS_FOUND_MESSAGE)
            return

        # Basic filtering (can be expanded)
        if filters:
            for app in apps:
                match = True
                if "name" in filters and filters["name"].lower() not in app["name"].lower():
                    match = False
                if "size_gt" in filters and app["estimated_size"] < filters["size_gt"]:
                    match = False
                if "last_used_days_gt" in filters and app["install_date"] and len(app["install_date"]) == 8:
                    try:
                        install_date = datetime.strptime(app["install_date"], "%Y%m%d")
                        if (datetime.now() - install_date).days > filters["last_used_days_gt"]:
                            pass
                        else:
                            match = False
                    except ValueError:
                        # Handle cases where InstallDate is not in YYYYMMDD format
                        match = False
                # Add more filter logic here (category)
                if match:
                    filtered_apps.append(app)
        else:
            filtered_apps = apps

        if filtered_apps:
            app_names = [app["name"] for app in filtered_apps]
            self.speak(LIST_APPS_MESSAGE + ", ".join(app_names))
        else:
            self.speak(NO_APPS_FOUND_MESSAGE)

    def uninstall_application(self, app_name, confirm=True):
        """Uninstalls a specified application."""
        apps = self.get_installed_applications()
        target_app = None

        for app in apps:
            if app_name.lower() in app["name"].lower():
                target_app = app
                break
        
        if not target_app:
            self.speak(APP_NOT_FOUND_MESSAGE.format(app_name))
            return

        if confirm:
            self.speak(UNINSTALL_CONFIRMATION_PROMPT.format(target_app["name"]))
            response = self.listen_for_command()
            if response and "yes" in response:
                pass
            else:
                self.speak("Uninstallation cancelled.")
                return

        uninstall_string = target_app["uninstall_string"]
        print(f"Attempting to uninstall {target_app['name']} using: {uninstall_string}")

        try:
            # Handle different uninstall command formats
            if "msiexec" in uninstall_string.lower():
                subprocess.run(uninstall_string, shell=True, check=True)
            else:
                # For other executables, try to run directly
                # Need to be careful with spaces in paths, often requires shell=True
                subprocess.run(uninstall_string, shell=True, check=True)
            self.speak(UNINSTALL_SUCCESS_MESSAGE.format(target_app["name"]))
        except subprocess.CalledProcessError as e:
            self.speak(UNINSTALL_FAILED_MESSAGE.format(target_app["name"]))
            print(f"Uninstallation failed: {e}")
        except Exception as e:
            self.speak(UNINSTALL_FAILED_MESSAGE.format(target_app["name"]))
            print(f"An error occurred: {e}")

    def process_command(self, command):
        """Processes the voice command and performs the corresponding action."""
        if "list apps" in command:
            self.list_applications()
        elif "uninstall" in command:
            app_name = command.replace("uninstall", "").strip()
            confirm = "without confirmation" not in command
            app_name = app_name.replace("without confirmation", "").strip()
            self.uninstall_application(app_name, confirm)
        elif "remove all games" in command:
            self.speak("This feature is not yet implemented.")
        elif "clear apps" in command and "days" in command:
            try:
                days = int(re.search(r'\d+', command).group())
                self.list_applications(filters={"last_used_days_gt": days})
            except (AttributeError, ValueError):
                self.speak("I couldn't understand the number of days. Please specify a number.")
        else:
            self.speak("I'm sorry, I don't understand that command.")
