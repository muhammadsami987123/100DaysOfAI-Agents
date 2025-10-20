#!/usr/bin/env python3
"""
Demo script for GPTConfigGenerator showcasing various configuration types
"""

import json
from agent import GPTConfigGenerator

def demo_basic_configs():
    """Demo basic configuration generation"""
    print("🚀 GPTConfigGenerator Demo - Basic Configurations")
    print("=" * 60)
    
    agent = GPTConfigGenerator()
    
    # Example configurations to generate
    examples = [
        {
            "request": "Create a JSON config for a Node.js Express app with port 3000 and MongoDB",
            "type": "app_settings",
            "format": "json",
            "title": "Express.js App Configuration"
        },
        {
            "request": "Generate a docker-compose.yml file with PostgreSQL and Redis services",
            "type": "devops",
            "format": "yaml",
            "title": "Docker Compose Configuration"
        },
        {
            "request": "Create a .prettierrc JSON config using 2-space tabs, no semicolons",
            "type": "linting",
            "format": "json",
            "title": "Prettier Configuration"
        },
        {
            "request": "Generate a vite.config.js file with React and Tailwind CSS",
            "type": "build_tools",
            "format": "js",
            "title": "Vite Configuration"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n📝 Example {i}: {example['title']}")
        print("-" * 40)
        print(f"Request: {example['request']}")
        print(f"Type: {example['type']}, Format: {example['format']}")
        print("\nGenerated Configuration:")
        
        try:
            result = agent.generate_config(
                user_request=example['request'],
                config_type=example['type'],
                format=example['format']
            )
            
            if result['success']:
                print(result['config_content'])
            else:
                print(f"⚠️  Fallback configuration (AI unavailable):")
                print(result['config_content'])
                
        except Exception as e:
            print(f"❌ Error generating config: {e}")
        
        print("\n" + "=" * 60)

def demo_config_types():
    """Demo different configuration types"""
    print("\n🎯 Available Configuration Types")
    print("=" * 40)
    
    agent = GPTConfigGenerator()
    config_types = agent.get_config_types()
    
    for type_key, type_info in config_types.items():
        print(f"\n📁 {type_info['name']}")
        print(f"   Examples: {', '.join(type_info['examples'])}")

def demo_supported_formats():
    """Demo supported formats"""
    print("\n📄 Supported Formats")
    print("=" * 30)
    
    agent = GPTConfigGenerator()
    formats = agent.get_supported_formats()
    
    for format_type in formats:
        print(f"✅ {format_type.upper()}")

def demo_suggestions():
    """Demo configuration suggestions"""
    print("\n💡 Configuration Suggestions")
    print("=" * 35)
    
    agent = GPTConfigGenerator()
    
    # Get suggestions for different types
    for config_type in ["app_settings", "devops", "linting"]:
        suggestions = agent.get_suggestions(config_type, "json")
        print(f"\n🔧 {config_type.replace('_', ' ').title()} Suggestions:")
        for suggestion in suggestions[:3]:  # Show first 3 suggestions
            print(f"   • {suggestion}")

def demo_default_values():
    """Demo default configuration values"""
    print("\n⚙️  Default Configuration Values")
    print("=" * 40)
    
    agent = GPTConfigGenerator()
    defaults = agent.get_default_values()
    
    for key, value in defaults.items():
        print(f"   {key}: {value}")

def main():
    """Run all demos"""
    print("🎉 GPTConfigGenerator - Day 77 of #100DaysOfAI-Agents")
    print("Transform natural language into structured configuration files!")
    print("=" * 80)
    
    try:
        # Run demos
        demo_basic_configs()
        demo_config_types()
        demo_supported_formats()
        demo_suggestions()
        demo_default_values()
        
        print("\n🎊 Demo completed successfully!")
        print("\nTo use GPTConfigGenerator:")
        print("   1. Web Interface: python main.py")
        print("   2. CLI Interface: python cli.py 'your request'")
        print("   3. API: Use the FastAPI endpoints directly")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Make sure you have installed all dependencies and configured your API keys")

if __name__ == "__main__":
    main()
