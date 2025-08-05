#!/usr/bin/env python3
"""
TranslatorAgent - Day 5 of #100DaysOfAI-Agents
AI-powered translation tool with voice capabilities
"""

import argparse
import sys
import logging
from typing import Optional
from colorama import init, Fore, Style

from translator_agent import TranslatorAgent
from voice_service import VoiceService
from config import TranslatorConfig

# Initialize colorama for cross-platform colored output
init()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_banner():
    """Print application banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    🌍 TranslatorAgent - Day 5                        ║
║                #100DaysOfAI-Agents Challenge                        ║
║                                                                    ║
║  Instant translation with AI-powered accuracy and voice capabilities ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def print_colored(text: str, color: str = Fore.WHITE, style: str = ""):
    """Print colored text"""
    print(f"{color}{style}{text}{Style.RESET_ALL}")

def run_web_interface(host: str, port: int):
    """Run web interface"""
    print_colored("🚀 Starting TranslatorAgent Web Interface...", Fore.GREEN)
    print_colored(f"📍 Server will be available at: http://{host}:{port}", Fore.YELLOW)
    print_colored("🛑 Press Ctrl+C to stop the server", Fore.RED)
    print()
    
    try:
        from web_app import app
        import uvicorn
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=False
        )
    except KeyboardInterrupt:
        print_colored("\n👋 Shutting down TranslatorAgent...", Fore.YELLOW)
    except Exception as e:
        print_colored(f"❌ Error starting web interface: {str(e)}", Fore.RED)
        sys.exit(1)

def run_terminal_interface():
    """Run terminal interface"""
    print_colored("🌍 Starting TranslatorAgent Terminal Interface...", Fore.GREEN)
    print_colored("💡 Type 'help' for commands, 'quit' to exit", Fore.CYAN)
    print()
    
    try:
        translator = TranslatorAgent()
        voice_service = VoiceService()
        
        print_colored("✅ TranslatorAgent initialized successfully!", Fore.GREEN)
        print()
        
        while True:
            try:
                command = input(f"{Fore.CYAN}🌍 TranslatorAgent> {Style.RESET_ALL}").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print_colored("👋 Goodbye!", Fore.YELLOW)
                    break
                
                elif command.lower() == 'help':
                    show_help()
                
                elif command.lower() == 'languages':
                    show_languages(translator)
                
                elif command.lower() == 'history':
                    show_history(translator)
                
                elif command.lower().startswith('translate '):
                    handle_translate_command(command, translator, voice_service)
                
                elif command.lower().startswith('detect '):
                    handle_detect_command(command, translator)
                
                elif command.lower().startswith('speak '):
                    handle_speak_command(command, voice_service)
                
                elif command.lower().startswith('listen'):
                    handle_listen_command(command, voice_service)
                
                else:
                    print_colored("❌ Unknown command. Type 'help' for available commands.", Fore.RED)
                    
            except KeyboardInterrupt:
                print_colored("\n👋 Goodbye!", Fore.YELLOW)
                break
            except Exception as e:
                print_colored(f"❌ Error: {str(e)}", Fore.RED)
                
    except Exception as e:
        print_colored(f"❌ Failed to initialize TranslatorAgent: {str(e)}", Fore.RED)
        sys.exit(1)

def show_help():
    """Show help information"""
    help_text = f"""
{Fore.CYAN}📚 Available Commands:{Style.RESET_ALL}

{Fore.GREEN}Translation Commands:{Style.RESET_ALL}
  translate "text" to language    - Translate text to specified language
  translate "text" from lang to lang  - Translate with specific source language
  
{Fore.GREEN}Language Detection:{Style.RESET_ALL}
  detect "text"                  - Detect language of text
  
{Fore.GREEN}Voice Commands:{Style.RESET_ALL}
  speak "text" [language]        - Speak text (optional language)
  listen [language]              - Listen for speech and convert to text
  
{Fore.GREEN}Utility Commands:{Style.RESET_ALL}
  languages                      - Show supported languages
  history                        - Show translation history
  help                           - Show this help
  quit                           - Exit the program

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  translate "Hello world" to Spanish
  translate "Bonjour le monde" from French to English
  detect "Hola mundo"
  speak "Hello world" Spanish
  listen English
"""
    print(help_text)

def show_languages(translator: TranslatorAgent):
    """Show supported languages"""
    try:
        languages = translator.get_supported_languages()
        print_colored(f"\n🌍 Supported Languages ({len(languages)}):", Fore.CYAN)
        print()
        
        # Group by first letter
        grouped = {}
        for lang in languages:
            first_letter = lang["name"][0].upper()
            if first_letter not in grouped:
                grouped[first_letter] = []
            grouped[first_letter].append(lang)
        
        for letter in sorted(grouped.keys()):
            print_colored(f"{letter}:", Fore.YELLOW)
            for lang in grouped[letter]:
                print(f"  {lang['code']} - {lang['name']} ({lang['native']})")
            print()
            
    except Exception as e:
        print_colored(f"❌ Error getting languages: {str(e)}", Fore.RED)

def show_history(translator: TranslatorAgent):
    """Show translation history"""
    try:
        history = translator.get_translation_history()
        if not history:
            print_colored("📝 No translation history found.", Fore.YELLOW)
            return
        
        print_colored(f"\n📝 Translation History ({len(history)} entries):", Fore.CYAN)
        print()
        
        for i, entry in enumerate(history[-10:], 1):  # Show last 10
            print_colored(f"{i}. {entry['timestamp']}", Fore.GREEN)
            print(f"   From: {entry['source_lang']} → To: {entry['target_lang']}")
            print(f"   Original: {entry['original_text'][:50]}...")
            print(f"   Translation: {entry['translation'][:50]}...")
            print()
            
    except Exception as e:
        print_colored(f"❌ Error getting history: {str(e)}", Fore.RED)

def handle_translate_command(command: str, translator: TranslatorAgent, voice_service: VoiceService):
    """Handle translate command"""
    try:
        # Parse command: translate "text" to language
        parts = command.split('"')
        if len(parts) < 3:
            print_colored("❌ Invalid format. Use: translate \"text\" to language", Fore.RED)
            return
        
        text = parts[1]
        remaining = parts[2].strip()
        
        if remaining.startswith('to '):
            target_lang = remaining[3:].strip()
            source_lang = "auto"
        elif remaining.startswith('from ') and ' to ' in remaining:
            # Format: from lang to lang
            from_part = remaining[6:]  # Remove "from "
            source_lang, target_lang = from_part.split(' to ', 1)
            source_lang = source_lang.strip()
            target_lang = target_lang.strip()
        else:
            print_colored("❌ Invalid format. Use: translate \"text\" to language", Fore.RED)
            return
        
        print_colored(f"🔄 Translating: \"{text}\"", Fore.YELLOW)
        
        result = translator.translate_text(text, source_lang, target_lang)
        
        if result["success"]:
            print_colored("✅ Translation:", Fore.GREEN)
            print(f"   Original: {result['original_text']}")
            print(f"   Translation: {result['translation']}")
            print(f"   From: {result['source_name']} → To: {result['target_name']}")
            
            # Ask if user wants to hear it
            response = input(f"\n{Fore.CYAN}🗣️  Speak translation? (y/n): {Style.RESET_ALL}").lower()
            if response in ['y', 'yes']:
                voice_result = voice_service.speak_text(result['translation'], target_lang)
                if voice_result["success"]:
                    print_colored("🔊 Speaking translation...", Fore.GREEN)
                else:
                    print_colored(f"❌ Voice error: {voice_result['error']}", Fore.RED)
        else:
            print_colored(f"❌ Translation failed: {result['error']}", Fore.RED)
            
    except Exception as e:
        print_colored(f"❌ Error: {str(e)}", Fore.RED)

def handle_detect_command(command: str, translator: TranslatorAgent):
    """Handle detect command"""
    try:
        # Parse command: detect "text"
        parts = command.split('"')
        if len(parts) < 3:
            print_colored("❌ Invalid format. Use: detect \"text\"", Fore.RED)
            return
        
        text = parts[1]
        print_colored(f"🔍 Detecting language: \"{text}\"", Fore.YELLOW)
        
        result = translator.detect_language(text)
        
        if result["success"]:
            print_colored("✅ Language Detection:", Fore.GREEN)
            print(f"   Text: {result['text']}")
            print(f"   Detected Language: {result['language_name']} ({result['detected_language']})")
            print(f"   Confidence: {result['confidence']:.2f}")
        else:
            print_colored(f"❌ Detection failed: {result['error']}", Fore.RED)
            
    except Exception as e:
        print_colored(f"❌ Error: {str(e)}", Fore.RED)

def handle_speak_command(command: str, voice_service: VoiceService):
    """Handle speak command"""
    try:
        # Parse command: speak "text" [language]
        parts = command.split('"')
        if len(parts) < 3:
            print_colored("❌ Invalid format. Use: speak \"text\" [language]", Fore.RED)
            return
        
        text = parts[1]
        remaining = parts[2].strip()
        language = remaining if remaining else "en"
        
        print_colored(f"🗣️  Speaking: \"{text}\" in {language}", Fore.YELLOW)
        
        result = voice_service.speak_text(text, language)
        
        if result["success"]:
            print_colored("🔊 Speaking...", Fore.GREEN)
        else:
            print_colored(f"❌ Speech error: {result['error']}", Fore.RED)
            
    except Exception as e:
        print_colored(f"❌ Error: {str(e)}", Fore.RED)

def handle_listen_command(command: str, voice_service: VoiceService):
    """Handle listen command"""
    try:
        # Parse command: listen [language]
        parts = command.split()
        language = parts[1] if len(parts) > 1 else "en"
        
        print_colored(f"👂 Listening for speech in {language}...", Fore.YELLOW)
        print_colored("💬 Speak now (press Ctrl+C to cancel)", Fore.CYAN)
        
        result = voice_service.listen_for_speech(language)
        
        if result["success"]:
            print_colored("✅ Speech Recognition:", Fore.GREEN)
            print(f"   Text: {result['text']}")
            print(f"   Language: {result['language']}")
            print(f"   Confidence: {result['confidence']:.2f}")
        else:
            print_colored(f"❌ Speech recognition failed: {result['error']}", Fore.RED)
            
    except KeyboardInterrupt:
        print_colored("\n❌ Listening cancelled", Fore.YELLOW)
    except Exception as e:
        print_colored(f"❌ Error: {str(e)}", Fore.RED)

def quick_translate(text: str, source_lang: str, target_lang: str, voice: bool = False):
    """Quick translation without interactive interface"""
    try:
        translator = TranslatorAgent()
        voice_service = VoiceService() if voice else None
        
        print_colored(f"🔄 Translating: \"{text}\"", Fore.YELLOW)
        print_colored(f"   From: {source_lang} → To: {target_lang}", Fore.CYAN)
        
        result = translator.translate_text(text, source_lang, target_lang)
        
        if result["success"]:
            print_colored("✅ Translation:", Fore.GREEN)
            print(f"   {result['translation']}")
            
            if voice and voice_service:
                voice_result = voice_service.speak_text(result['translation'], target_lang)
                if voice_result["success"]:
                    print_colored("🔊 Speaking translation...", Fore.GREEN)
                else:
                    print_colored(f"❌ Voice error: {voice_result['error']}", Fore.RED)
        else:
            print_colored(f"❌ Translation failed: {result['error']}", Fore.RED)
            sys.exit(1)
            
    except Exception as e:
        print_colored(f"❌ Error: {str(e)}", Fore.RED)
        sys.exit(1)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="TranslatorAgent - AI-powered translation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --web                    # Start web interface
  python main.py --terminal               # Start terminal interface
  python main.py --quick "Hello" --target es  # Quick translation
  python main.py --detect "Hola mundo"   # Detect language
  python main.py --voice "Hello" --target fr  # Voice translation
        """
    )
    
    # Interface options
    parser.add_argument("--web", action="store_true", help="Start web interface")
    parser.add_argument("--terminal", action="store_true", help="Start terminal interface")
    
    # Quick translation options
    parser.add_argument("--quick", type=str, help="Quick translation text")
    parser.add_argument("--detect", type=str, help="Detect language of text")
    parser.add_argument("--voice", type=str, help="Voice translation text")
    
    # Language options
    parser.add_argument("--source", type=str, default="auto", help="Source language (default: auto)")
    parser.add_argument("--target", type=str, default="en", help="Target language (default: en)")
    
    # Server options
    parser.add_argument("--host", type=str, default=TranslatorConfig.HOST, help="Web server host")
    parser.add_argument("--port", type=int, default=TranslatorConfig.PORT, help="Web server port")
    
    # Voice options
    parser.add_argument("--enable-voice", action="store_true", help="Enable voice features")
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check if OpenAI API key is available
    if not TranslatorConfig.OPENAI_API_KEY:
        print_colored("❌ OpenAI API key not found!", Fore.RED)
        print_colored("💡 Set your API key using one of these methods:", Fore.YELLOW)
        print_colored("   1. Environment variable: export OPENAI_API_KEY=your_key", Fore.CYAN)
        print_colored("   2. .env file: Create .env file with OPENAI_API_KEY=your_key", Fore.CYAN)
        print_colored("   3. Command line: python main.py --web your_api_key", Fore.CYAN)
        sys.exit(1)
    
    # Handle different modes
    if args.web:
        run_web_interface(args.host, args.port)
    elif args.terminal:
        run_terminal_interface()
    elif args.quick:
        quick_translate(args.quick, args.source, args.target, args.enable_voice)
    elif args.detect:
        try:
            translator = TranslatorAgent()
            result = translator.detect_language(args.detect)
            if result["success"]:
                print_colored("✅ Language Detection:", Fore.GREEN)
                print(f"   Text: {result['text']}")
                print(f"   Detected Language: {result['language_name']} ({result['detected_language']})")
                print(f"   Confidence: {result['confidence']:.2f}")
            else:
                print_colored(f"❌ Detection failed: {result['error']}", Fore.RED)
                sys.exit(1)
        except Exception as e:
            print_colored(f"❌ Error: {str(e)}", Fore.RED)
            sys.exit(1)
    elif args.voice:
        try:
            translator = TranslatorAgent()
            voice_service = VoiceService()
            
            result = translator.translate_text(args.voice, args.source, args.target)
            if result["success"]:
                print_colored("✅ Translation:", Fore.GREEN)
                print(f"   {result['translation']}")
                
                voice_result = voice_service.speak_text(result['translation'], args.target)
                if voice_result["success"]:
                    print_colored("🔊 Speaking translation...", Fore.GREEN)
                else:
                    print_colored(f"❌ Voice error: {voice_result['error']}", Fore.RED)
            else:
                print_colored(f"❌ Translation failed: {result['error']}", Fore.RED)
                sys.exit(1)
        except Exception as e:
            print_colored(f"❌ Error: {str(e)}", Fore.RED)
            sys.exit(1)
    else:
        # Default to terminal interface
        run_terminal_interface()

if __name__ == "__main__":
    main() 