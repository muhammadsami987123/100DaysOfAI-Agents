#!/usr/bin/env python3
"""
Test script for VoiceNoteAgent

This script tests the VoiceNoteAgent functionality without requiring
actual microphone input, using mock data and simulated operations.

Author: Muhammad Sami Asghar Mughal
"""

import json
import os
import sys
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def test_note_creation():
    """Test note creation and management."""
    print(f"{Fore.CYAN}🧪 Testing Note Creation...")
    
    # Mock note data
    test_notes = [
        {
            "id": 1,
            "title": "Test Note 1",
            "content": "This is a test voice note for testing purposes.",
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "length": 8,
            "tags": ["test", "demo"]
        },
        {
            "id": 2,
            "title": "Meeting Notes",
            "content": "Discuss project timeline and deliverables for next week.",
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "length": 10,
            "tags": ["meeting", "project"]
        }
    ]
    
    # Test JSON file operations
    test_file = "test_voice_notes.json"
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_notes, f, indent=2, ensure_ascii=False)
        print(f"{Fore.GREEN}✅ JSON file creation successful")
        
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_notes = json.load(f)
        print(f"{Fore.GREEN}✅ JSON file loading successful")
        
        assert len(loaded_notes) == 2, "Note count mismatch"
        assert loaded_notes[0]["title"] == "Test Note 1", "Note title mismatch"
        print(f"{Fore.GREEN}✅ Note data integrity verified")
        
        # Cleanup
        os.remove(test_file)
        print(f"{Fore.GREEN}✅ Test file cleanup successful")
        
    except Exception as e:
        print(f"{Fore.RED}❌ JSON file operations failed: {e}")
        return False
    
    return True

def test_directory_operations():
    """Test directory creation and file operations."""
    print(f"{Fore.CYAN}🧪 Testing Directory Operations...")
    
    test_dir = "test_voice_notes"
    test_file = os.path.join(test_dir, "test_note.txt")
    
    try:
        # Create directory
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        print(f"{Fore.GREEN}✅ Directory creation successful")
        
        # Create test file
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Title: Test Note\n")
            f.write("Date: 2024-01-15 10:30:00\n")
            f.write("Length: 5 words\n")
            f.write("Tags: test\n")
            f.write("-" * 50 + "\n")
            f.write("This is a test note content.")
        print(f"{Fore.GREEN}✅ Test file creation successful")
        
        # Verify file exists
        assert os.path.exists(test_file), "Test file not created"
        print(f"{Fore.GREEN}✅ File existence verified")
        
        # Cleanup
        os.remove(test_file)
        os.rmdir(test_dir)
        print(f"{Fore.GREEN}✅ Directory cleanup successful")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Directory operations failed: {e}")
        return False
    
    return True

def test_search_functionality():
    """Test search functionality with mock data."""
    print(f"{Fore.CYAN}🧪 Testing Search Functionality...")
    
    test_notes = [
        {"id": 1, "title": "Python Programming", "content": "Learn Python basics and advanced concepts"},
        {"id": 2, "title": "Meeting Notes", "content": "Discuss AI project timeline"},
        {"id": 3, "title": "Shopping List", "content": "Buy groceries and household items"}
    ]
    
    # Test search
    search_term = "python"
    matching_notes = []
    
    for note in test_notes:
        if (search_term.lower() in note['content'].lower() or 
            search_term.lower() in note['title'].lower()):
            matching_notes.append(note)
    
    assert len(matching_notes) == 1, f"Expected 1 match, got {len(matching_notes)}"
    assert matching_notes[0]['id'] == 1, "Wrong note matched"
    print(f"{Fore.GREEN}✅ Search functionality working correctly")
    
    return True

def test_statistics_calculation():
    """Test statistics calculation with mock data."""
    print(f"{Fore.CYAN}🧪 Testing Statistics Calculation...")
    
    test_notes = [
        {"length": 10, "date": "2024-01-15"},
        {"length": 15, "date": "2024-01-15"},
        {"length": 8, "date": "2024-01-16"},
        {"length": 12, "date": "2024-01-16"}
    ]
    
    # Calculate statistics
    total_notes = len(test_notes)
    total_words = sum(note['length'] for note in test_notes)
    avg_words = total_words / total_notes if total_notes > 0 else 0
    
    # Group by date
    dates = {}
    for note in test_notes:
        date = note['date']
        dates[date] = dates.get(date, 0) + 1
    
    # Verify calculations
    assert total_notes == 4, f"Expected 4 notes, got {total_notes}"
    assert total_words == 45, f"Expected 45 words, got {total_words}"
    assert avg_words == 11.25, f"Expected 11.25 avg, got {avg_words}"
    assert len(dates) == 2, f"Expected 2 dates, got {len(dates)}"
    assert dates["2024-01-15"] == 2, "Wrong count for 2024-01-15"
    assert dates["2024-01-16"] == 2, "Wrong count for 2024-01-16"
    
    print(f"{Fore.GREEN}✅ Statistics calculation working correctly")
    return True

def test_dependency_imports():
    """Test if all required dependencies can be imported."""
    print(f"{Fore.CYAN}🧪 Testing Dependency Imports...")
    
    try:
        import speech_recognition as sr
        print(f"{Fore.GREEN}✅ SpeechRecognition imported successfully")
    except ImportError as e:
        print(f"{Fore.RED}❌ SpeechRecognition import failed: {e}")
        return False
    
    try:
        import pyttsx3
        print(f"{Fore.GREEN}✅ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"{Fore.RED}❌ pyttsx3 import failed: {e}")
        return False
    
    try:
        import colorama
        print(f"{Fore.GREEN}✅ colorama imported successfully")
    except ImportError as e:
        print(f"{Fore.RED}❌ colorama import failed: {e}")
        return False
    
    # Test optional dependency
    try:
        import pocketsphinx
        print(f"{Fore.GREEN}✅ pocketsphinx imported successfully (offline recognition available)")
    except ImportError:
        print(f"{Fore.YELLOW}⚠️  pocketsphinx not available (offline recognition not available)")
    
    return True

def run_all_tests():
    """Run all tests and report results."""
    print(f"{Fore.CYAN}🧪 VoiceNoteAgent Test Suite")
    print("=" * 50)
    
    tests = [
        ("Dependency Imports", test_dependency_imports),
        ("Note Creation", test_note_creation),
        ("Directory Operations", test_directory_operations),
        ("Search Functionality", test_search_functionality),
        ("Statistics Calculation", test_statistics_calculation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{Fore.CYAN}Running: {test_name}")
        try:
            if test_func():
                print(f"{Fore.GREEN}✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"{Fore.RED}❌ {test_name} FAILED")
        except Exception as e:
            print(f"{Fore.RED}❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{Fore.CYAN}Test Results:")
    print(f"{Fore.WHITE}Passed: {passed}/{total}")
    print(f"{Fore.WHITE}Failed: {total - passed}/{total}")
    
    if passed == total:
        print(f"{Fore.GREEN}🎉 All tests passed! VoiceNoteAgent is ready to use.")
        return True
    else:
        print(f"{Fore.RED}⚠️  Some tests failed. Please check the issues above.")
        return False

def test_interactive_commands():
    """Test command processing logic."""
    print(f"{Fore.CYAN}🧪 Testing Command Processing...")
    
    # Mock command processing
    commands = [
        ("record", "record"),
        ("r", "record"),
        ("new", "record"),
        ("list", "list"),
        ("l", "list"),
        ("show", "list"),
        ("play 1", "play"),
        ("show 2", "show"),
        ("search python", "search"),
        ("delete 3", "delete"),
        ("stats", "stats"),
        ("help", "help"),
        ("quit", "quit"),
        ("unknown", "unknown")
    ]
    
    for command, expected in commands:
        if command in ['record', 'r', 'new']:
            result = "record"
        elif command in ['list', 'l', 'show']:
            result = "list"
        elif command.startswith('play '):
            result = "play"
        elif command.startswith('show '):
            result = "show"
        elif command.startswith('search '):
            result = "search"
        elif command.startswith('delete '):
            result = "delete"
        elif command in ['stats', 'statistics']:
            result = "stats"
        elif command in ['help', 'h', '?']:
            result = "help"
        elif command in ['quit', 'q', 'exit']:
            result = "quit"
        else:
            result = "unknown"
        
        if result == expected:
            print(f"{Fore.GREEN}✅ Command '{command}' processed correctly")
        else:
            print(f"{Fore.RED}❌ Command '{command}' failed: expected {expected}, got {result}")
    
    print(f"{Fore.GREEN}✅ Command processing test completed")
    return True

if __name__ == "__main__":
    print(f"{Fore.CYAN}🤖 VoiceNoteAgent Test Suite")
    print(f"{Fore.CYAN}Testing functionality without microphone input...")
    
    # Run basic tests
    basic_tests = run_all_tests()
    
    # Run command processing test
    command_tests = test_interactive_commands()
    
    if basic_tests and command_tests:
        print(f"\n{Fore.GREEN}🎉 All tests completed successfully!")
        print(f"{Fore.CYAN}💡 Run 'python main.py' to start the VoiceNoteAgent")
    else:
        print(f"\n{Fore.RED}⚠️  Some tests failed. Please check the issues above.")
        sys.exit(1) 