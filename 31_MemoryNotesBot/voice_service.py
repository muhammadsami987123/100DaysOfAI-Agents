import speech_recognition as sr
import pyttsx3
import logging
import threading
import time
from typing import Optional, Callable
from config import Config

logger = logging.getLogger(__name__)

class VoiceService:
    """Voice service for speech input and output"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = None
        self.is_listening = False
        self.listen_thread = None
        self.on_speech_detected: Optional[Callable] = None
        
        # Initialize TTS engine
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.8)  # Volume level
            logger.info("TTS engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
    
    def speak(self, text: str, block: bool = True):
        """Convert text to speech"""
        if not self.tts_engine:
            logger.warning("TTS engine not available")
            return
        
        try:
            if block:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # Run in separate thread to avoid blocking
                def speak_async():
                    try:
                        self.tts_engine.say(text)
                        self.tts_engine.runAndWait()
                    except Exception as e:
                        logger.error(f"Error in async speech: {e}")
                
                thread = threading.Thread(target=speak_async)
                thread.daemon = True
                thread.start()
                
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
    
    def listen(self, timeout: int = None, phrase_time_limit: int = None) -> Optional[str]:
        """Listen for speech input and convert to text"""
        if not Config.ENABLE_VOICE:
            logger.warning("Voice input is disabled")
            return None
        
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                logger.info("Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout or Config.VOICE_TIMEOUT,
                    phrase_time_limit=phrase_time_limit
                )
                
                logger.info("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized: {text}")
                return text
                
        except sr.WaitTimeoutError:
            logger.info("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            logger.info("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from speech recognition service: {e}")
            return None
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return None
    
    def start_continuous_listening(self, callback: Callable[[str], None]):
        """Start continuous listening for voice commands"""
        if self.is_listening:
            logger.warning("Already listening")
            return
        
        self.is_listening = True
        self.on_speech_detected = callback
        
        def listen_loop():
            while self.is_listening:
                try:
                    text = self.listen(timeout=1, phrase_time_limit=10)
                    if text and self.on_speech_detected:
                        self.on_speech_detected(text)
                    time.sleep(0.1)  # Small delay to prevent CPU overuse
                except Exception as e:
                    logger.error(f"Error in continuous listening: {e}")
                    time.sleep(1)  # Wait before retrying
        
        self.listen_thread = threading.Thread(target=listen_loop)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        logger.info("Started continuous voice listening")
    
    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
            self.listen_thread = None
        logger.info("Stopped continuous voice listening")
    
    def get_available_microphones(self) -> list:
        """Get list of available microphones"""
        try:
            return sr.Microphone.list_microphone_names()
        except Exception as e:
            logger.error(f"Error getting microphone list: {e}")
            return []
    
    def set_microphone(self, device_index: int):
        """Set specific microphone device"""
        try:
            # This would require modifying the recognizer to use a specific device
            logger.info(f"Set microphone to device {device_index}")
        except Exception as e:
            logger.error(f"Error setting microphone: {e}")
    
    def get_voice_status(self) -> dict:
        """Get current voice service status"""
        return {
            "tts_available": self.tts_engine is not None,
            "listening": self.is_listening,
            "voice_enabled": Config.ENABLE_VOICE,
            "microphones": self.get_available_microphones()
        }
    
    def test_voice(self) -> dict:
        """Test voice input and output"""
        result = {
            "tts_test": False,
            "stt_test": False,
            "error": None
        }
        
        # Test TTS
        try:
            self.speak("Voice test successful", block=True)
            result["tts_test"] = True
        except Exception as e:
            result["error"] = f"TTS test failed: {e}"
            return result
        
        # Test STT
        try:
            self.speak("Please say 'test' in 3 seconds", block=True)
            time.sleep(1)
            text = self.listen(timeout=5, phrase_time_limit=3)
            if text and "test" in text.lower():
                result["stt_test"] = True
            else:
                result["error"] = "STT test failed: No speech detected or incorrect text"
        except Exception as e:
            result["error"] = f"STT test failed: {e}"
        
        return result

class VoiceCommandProcessor:
    """Process voice commands for the MemoryNotesBot"""
    
    def __init__(self, memory_store, ai_service):
        self.memory_store = memory_store
        self.ai_service = ai_service
        self.voice_service = VoiceService()
        
        # Voice command patterns
        self.command_patterns = {
            "remember": self._handle_remember_command,
            "what is": self._handle_what_is_command,
            "show me": self._handle_show_command,
            "delete": self._handle_delete_command,
            "forget": self._handle_forget_command,
            "help": self._handle_help_command
        }
    
    def process_voice_command(self, text: str) -> str:
        """Process voice command and return response"""
        text_lower = text.lower().strip()
        
        # Find matching command pattern
        for pattern, handler in self.command_patterns.items():
            if pattern in text_lower:
                try:
                    return handler(text)
                except Exception as e:
                    logger.error(f"Error processing voice command '{text}': {e}")
                    return f"Sorry, I encountered an error processing your command: {e}"
        
        # Default: treat as a memory to remember
        return self._handle_remember_command(text)
    
    def _handle_remember_command(self, text: str) -> str:
        """Handle 'remember' commands or general memory storage"""
        # Extract the content to remember
        if text.lower().startswith("remember"):
            content = text[9:].strip()  # Remove "remember" prefix
        else:
            content = text
        
        if not content:
            return "What would you like me to remember?"
        
        # Use AI to enhance the memory
        ai_enhancement = self.ai_service.enhance_memory_content(content)
        
        if ai_enhancement.get("enhanced"):
            suggestions = ai_enhancement["suggestions"]
            memory = self.memory_store.add_memory(
                content=content,
                memory_type=suggestions.get("memory_type", "long_term"),
                tags=suggestions.get("tags", []),
                category=suggestions.get("category"),
                priority=suggestions.get("priority", "medium")
            )
            return f"I've remembered: '{content}'. I've categorized it as {suggestions.get('category', 'general')} with priority {suggestions.get('priority', 'medium')}."
        else:
            # Fallback without AI enhancement
            memory = self.memory_store.add_memory(content=content)
            return f"I've remembered: '{content}'"
    
    def _handle_what_is_command(self, text: str) -> str:
        """Handle 'what is' queries"""
        query = text.lower().replace("what is", "").replace("what's", "").strip()
        
        if not query:
            return "What would you like me to look up?"
        
        # Search for memories
        results = self.memory_store.search_memories(query, limit=3)
        
        if results:
            response = f"Here's what I found about '{query}':\n"
            for i, result in enumerate(results, 1):
                memory = result.memory
                response += f"{i}. {memory.content}\n"
            return response
        else:
            return f"I don't have any memories about '{query}'"
    
    def _handle_show_command(self, text: str) -> str:
        """Handle 'show me' commands"""
        query = text.lower().replace("show me", "").strip()
        
        if "recent" in query:
            memories = self.memory_store.get_recent_memories(5)
            if memories:
                response = "Here are your recent memories:\n"
                for i, memory in enumerate(memories, 1):
                    response += f"{i}. {memory.content[:50]}...\n"
                return response
            else:
                return "You don't have any recent memories"
        
        elif "tags" in query or "tagged" in query:
            # Extract tag from query
            tag = query.replace("tags", "").replace("tagged", "").replace("with", "").strip()
            if tag:
                memories = self.memory_store.get_memories_by_tag(tag)
                if memories:
                    response = f"Here are memories tagged '{tag}':\n"
                    for i, memory in enumerate(memories[:5], 1):
                        response += f"{i}. {memory.content[:50]}...\n"
                    return response
                else:
                    return f"No memories found with tag '{tag}'"
            else:
                return "Please specify which tag you'd like to see"
        
        else:
            return "I can show you recent memories or memories by tag. Try 'show me recent' or 'show me tagged with work'"
    
    def _handle_delete_command(self, text: str) -> str:
        """Handle delete commands"""
        query = text.lower().replace("delete", "").strip()
        
        if not query:
            return "What would you like me to delete?"
        
        # Search for memories to delete
        results = self.memory_store.search_memories(query, limit=5)
        
        if results:
            if len(results) == 1:
                memory = results[0].memory
                self.memory_store.delete_memory(memory.id)
                return f"I've deleted the memory: '{memory.content[:50]}...'"
            else:
                return f"I found {len(results)} memories matching '{query}'. Please be more specific."
        else:
            return f"I couldn't find any memories matching '{query}'"
    
    def _handle_forget_command(self, text: str) -> str:
        """Handle forget commands (same as delete)"""
        return self._handle_delete_command(text.replace("forget", "delete"))
    
    def _handle_help_command(self, text: str) -> str:
        """Handle help commands"""
        help_text = """
        I can help you with:
        - Remember things: "Remember my GitHub token is abc123"
        - Look up information: "What is my GitHub token?"
        - Show recent memories: "Show me recent"
        - Show tagged memories: "Show me tagged with work"
        - Delete memories: "Delete my old password"
        - Get help: "Help"
        """
        return help_text.strip()
    
    def start_voice_interface(self):
        """Start the voice interface"""
        def on_speech(text: str):
            response = self.process_voice_command(text)
            print(f"You said: {text}")
            print(f"Response: {response}")
            
            # Speak the response
            self.voice_service.speak(response, block=False)
        
        self.voice_service.start_continuous_listening(on_speech)
        print("Voice interface started. Say 'help' for commands or just speak naturally.")
    
    def stop_voice_interface(self):
        """Stop the voice interface"""
        self.voice_service.stop_continuous_listening()
        print("Voice interface stopped.")
