#!/usr/bin/env python3
"""
Demo script for Weather Speaker Agent
Shows the agent capabilities without the web interface
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def demo_weather_agent():
    """Demonstrate the Weather Speaker Agent capabilities"""
    
    print("🌤️ Weather Speaker Agent - Demo")
    print("=" * 50)
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OpenAI API key not found!")
        print("Please set OPENAI_API_KEY in your .env file")
        return
    
    try:
        from ai_agent import WeatherAgent
        from weather_service import WeatherService
        from tts_service import TTSService
        
        # Initialize services
        print("🚀 Initializing Weather Speaker Agent...")
        agent = WeatherAgent()
        weather_service = WeatherService()
        tts_service = TTSService()
        
        # Demo cities
        demo_cities = ["New York", "London", "Tokyo", "Sydney"]
        
        for city in demo_cities:
            print(f"\n📍 Getting weather for {city}...")
            
            # Get weather data
            weather_data, error = await weather_service.get_weather_data(city)
            
            if error:
                print(f"❌ Error: {error}")
                continue
            
            # Display weather information
            current = weather_data['current']
            forecast = weather_data['forecast']
            
            print(f"✅ Weather data retrieved for {weather_data['city']}, {weather_data['country']}")
            print(f"🌡️  Temperature: {current['temperature']}°C (feels like {current['feels_like']}°C)")
            print(f"💧 Humidity: {current['humidity']}%")
            print(f"💨 Wind: {current['wind_speed']} km/h")
            print(f"📈 Today's High: {forecast['today_max']}°C")
            print(f"📉 Today's Low: {forecast['today_min']}°C")
            
            # Get AI response
            print("\n🤖 Getting AI-enhanced response...")
            response = await agent.get_weather_response(city, include_voice=False)
            
            if response['success']:
                print("💬 AI Response:")
                print(f"   {response['ai_response']}")
                
                # Get weather tips
                print("\n💡 Getting weather tips...")
                tips = await agent.get_weather_tips(weather_data)
                print(f"   {tips}")
            else:
                print(f"❌ AI Error: {response['error']}")
            
            print("-" * 50)
            
            # Small delay between cities
            await asyncio.sleep(1)
        
        # Voice demo (optional)
        print("\n🔊 Voice Demo")
        print("Would you like to hear a voice weather report? (y/n): ", end="")
        
        try:
            # For demo purposes, we'll simulate user input
            # In a real scenario, you'd use input()
            user_input = "n"  # Change to "y" to enable voice demo
            
            if user_input.lower() == 'y':
                print("🎤 Speaking weather report...")
                voice_text = tts_service.create_weather_speech(weather_data)
                print(f"📢 Speaking: {voice_text}")
                await tts_service.speak_text(voice_text)
            else:
                print("⏭️  Skipping voice demo")
                
        except KeyboardInterrupt:
            print("\n⏹️  Voice demo interrupted")
        
        print("\n🎉 Demo completed!")
        print("\n💡 To run the full web interface:")
        print("   python main.py")
        print("   Then open: http://localhost:8000")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function"""
    try:
        asyncio.run(demo_weather_agent())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    main() 