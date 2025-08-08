from __future__ import annotations

from typing import Optional

from colorama import Fore, Style, init as colorama_init
import sys
import threading
import time

from config import CONFIG
from assistant_service import AssistantService
from faq_matcher import FAQMatcher
from logger import QALogger, make_log_entry
from stt_service import STTService
from tts_service import TTSService


class VoiceAssistantCLI:
    def __init__(self) -> None:
        colorama_init(autoreset=True)
        self.stt = STTService()
        self.tts = TTSService()
        self.matcher = FAQMatcher()
        self.logger = QALogger()
        self.ai: Optional[AssistantService] = None
        if CONFIG.openai_api_key:
            try:
                self.ai = AssistantService()
            except Exception:
                self.ai = None
        self._spinner_stop = threading.Event()

    def print_header(self) -> None:
        print(f"{Fore.CYAN}🎧 VoiceAssistantLite (Day 8){Style.RESET_ALL}")
        print("Press Enter to start listening, or type a question.")
        print("Type 'exit' or 'quit' to stop.\n")

    def loop(self) -> None:
        self.print_header()
        while True:
            try:
                user_input = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                break

            if user_input.lower() in {"exit", "quit"}:
                print("👋 Goodbye!")
                break

            if user_input == "":
                print("🎙️  Continuous voice mode. Press Ctrl+C to stop.")
                try:
                    while True:
                        text, lang = self._capture_voice()
                        if not text:
                            print(f"{Fore.YELLOW}⚠️  Didn't catch that. Try again.{Style.RESET_ALL}")
                            continue
                        if self.ai is not None:
                            print(f"📝 You said: {text}")
                            spinner_thread = threading.Thread(target=self._spinner, args=("Thinking",))
                            self._spinner_stop.clear()
                            spinner_thread.start()
                            try:
                                answer = self.ai.ask(text)
                            except Exception as e:
                                print(f"{Fore.RED}Assistant error: {e}{Style.RESET_ALL}")
                                answer = "Sorry, there was an error answering your question."
                            finally:
                                self._spinner_stop.set()
                                spinner_thread.join()
                            print(f"💬 AI Answer: {answer}")
                            self.tts.speak(answer)
                            if self.logger:
                                self.logger.log(make_log_entry(text, "assistant", 100, answer, lang))
                        else:
                            faq, score, matched_text = self.matcher.best_match(text)
                            if faq is None:
                                print(f"{Fore.YELLOW}🔎 No close FAQ match found (score={score}).{Style.RESET_ALL}")
                                self.tts.speak("Sorry, I do not have an answer for that yet.")
                                if self.logger:
                                    self.logger.log(make_log_entry(text, matched_text, score, "", lang))
                                continue
                            print(f"📝 You said: {text}")
                            print(f"🔎 Best match: {faq.question}  ({score}%)")
                            print(f"💬 Answer: {faq.answer}")
                            self.tts.speak(faq.answer)
                            if self.logger:
                                self.logger.log(make_log_entry(text, faq.question, score, faq.answer, lang))
                except (KeyboardInterrupt, EOFError):
                    print("\n🛑 Stopped voice mode.")
                continue
            else:
                text, lang = user_input, CONFIG.language

                # If OpenAI is configured, route to Assistants API for dynamic answer
                if self.ai is not None:
                    print(f"📝 You said: {text}")
                    spinner_thread = threading.Thread(target=self._spinner, args=("Thinking",))
                    self._spinner_stop.clear()
                    spinner_thread.start()
                    try:
                        answer = self.ai.ask(text)
                    except Exception as e:
                        print(f"{Fore.RED}Assistant error: {e}{Style.RESET_ALL}")
                        answer = "Sorry, there was an error answering your question."
                    finally:
                        self._spinner_stop.set()
                        spinner_thread.join()
                    print(f"💬 AI Answer: {answer}")
                    self.tts.speak(answer)
                    if self.logger:
                        self.logger.log(make_log_entry(text, "assistant", 100, answer, lang))
                else:
                    # Fallback to local FAQ matching
                    faq, score, matched_text = self.matcher.best_match(text)
                    if faq is None:
                        print(f"{Fore.YELLOW}🔎 No close FAQ match found (score={score}).{Style.RESET_ALL}")
                        self.tts.speak("Sorry, I do not have an answer for that yet.")
                        if self.logger:
                            self.logger.log(make_log_entry(text, matched_text, score, "", lang))
                        continue

                    print(f"📝 You said: {text}")
                    print(f"🔎 Best match: {faq.question}  ({score}%)")
                    print(f"💬 Answer: {faq.answer}")
                    self.tts.speak(faq.answer)
                    if self.logger:
                        self.logger.log(make_log_entry(text, faq.question, score, faq.answer, lang))

    def _capture_voice(self) -> tuple[str, str]:
        print("🎙️  Listening... speak now")
        try:
            audio = self.stt.listen(phrase_time_limit=8.0)
        except Exception as e:
            print(f"{Fore.RED}Microphone error: {e}{Style.RESET_ALL}")
            return "", CONFIG.language
        print(f"🧠 Transcribing ({CONFIG.stt_provider}, {CONFIG.language})...")
        text, used_lang = self.stt.transcribe(audio)
        return text.strip(), used_lang

    def _spinner(self, label: str = "Working") -> None:
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        idx = 0
        while not self._spinner_stop.is_set():
            frame = frames[idx % len(frames)]
            sys.stdout.write(f"\r{Fore.BLUE}{frame} {label}...{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.08)
            idx += 1
        # clear the line
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()


