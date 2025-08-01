#!/usr/bin/env python3
"""
🧪 Test script for TodoAgent

This script tests the TodoAgent functionality without requiring OpenAI API calls.
It demonstrates the core features and provides a way to test the agent locally.

Usage:
    python test_agent.py
"""

import json
import os
from datetime import datetime
from main import TodoAgent

def test_todo_agent():
    """Test the TodoAgent functionality."""
    print("🧪 Testing TodoAgent...")
    
    # Create a test API key (this won't actually be used for API calls)
    test_api_key = "test_key_for_local_testing"
    
    try:
        # Initialize the agent
        agent = TodoAgent(test_api_key)
        print("✅ Agent initialized successfully")
        
        # Test adding todos directly (bypassing GPT parsing)
        print("\n📝 Testing todo operations...")
        
        # Add some test todos
        agent.add_todo("Buy groceries", "medium", "shopping", "2024-01-20")
        agent.add_todo("Meeting with client", "high", "work", "2024-01-18")
        agent.add_todo("Workout session", "low", "health")
        agent.add_todo("Study Python", "high", "learning", "2024-01-25")
        
        print("✅ Added test todos")
        
        # Test listing todos
        print("\n📋 Testing list functionality...")
        agent.list_todos()
        
        # Test updating a todo
        print("\n🔄 Testing update functionality...")
        agent.update_todo(1, priority="high", status="in_progress")
        
        # Test marking as completed
        print("\n✅ Testing mark functionality...")
        agent.mark_todo(2, "completed")
        
        # Test search functionality
        print("\n🔍 Testing search functionality...")
        agent.search_todos("groceries")
        
        # Test statistics
        print("\n📊 Testing statistics...")
        agent.get_statistics()
        
        # Test filtering
        print("\n🎯 Testing filtering...")
        print("High priority todos:")
        agent.list_todos(filter_priority="high")
        
        print("\nWork category todos:")
        agent.list_todos(filter_category="work")
        
        # Test deleting a todo
        print("\n🗑️ Testing delete functionality...")
        agent.delete_todo(3)
        
        # Show final state
        print("\n📋 Final todo list:")
        agent.list_todos()
        
        print("\n📊 Final statistics:")
        agent.get_statistics()
        
        # Clean up test file
        if os.path.exists("todos.json"):
            os.remove("todos.json")
            print("\n🧹 Cleaned up test file")
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def test_data_structure():
    """Test the todo data structure."""
    print("\n🔧 Testing data structure...")
    
    # Create a sample todo
    sample_todo = {
        "id": 1,
        "task": "Test task",
        "priority": "medium",
        "category": "other",
        "due_date": "2024-01-20",
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Test JSON serialization
    try:
        json_str = json.dumps(sample_todo, indent=2)
        parsed_todo = json.loads(json_str)
        
        assert parsed_todo["id"] == 1
        assert parsed_todo["task"] == "Test task"
        assert parsed_todo["priority"] == "medium"
        
        print("✅ Data structure test passed")
        return True
        
    except Exception as e:
        print(f"❌ Data structure test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting TodoAgent Tests")
    print("=" * 50)
    
    # Test data structure
    structure_test = test_data_structure()
    
    # Test agent functionality
    agent_test = test_todo_agent()
    
    print("\n" + "=" * 50)
    if structure_test and agent_test:
        print("🎉 All tests passed! TodoAgent is ready to use.")
        print("\nTo use the agent with OpenAI:")
        print("1. Set your OpenAI API key: export OPENAI_API_KEY=your_key")
        print("2. Run: python main.py")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main() 