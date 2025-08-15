#!/usr/bin/env python3
"""
🧪 Test script for BrowserOpenerAgent

Tests the core functionality without requiring voice input.
"""

import sys
import os
from unittest.mock import patch, MagicMock

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import BrowserOpenerAgent


def test_url_validation():
    """Test URL validation functionality."""
    print("🧪 Testing URL validation...")
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    # Test valid URLs
    valid_urls = [
        "https://google.com",
        "http://example.com",
        "https://www.youtube.com",
        "https://github.com/user/repo"
    ]
    
    for url in valid_urls:
        assert agent.is_valid_url(url), f"URL should be valid: {url}"
    
    # Test invalid URLs
    invalid_urls = [
        "not-a-url",
        "google.com",  # Missing protocol
        "ftp://example.com",  # Unsupported protocol
        "https://",  # Missing domain
        ""
    ]
    
    for url in invalid_urls:
        assert not agent.is_valid_url(url), f"URL should be invalid: {url}"
    
    print("✅ URL validation tests passed!")


def test_site_mapping():
    """Test site name to URL mapping."""
    print("🧪 Testing site mapping...")
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    # Test common site mappings
    test_cases = [
        ("Open YouTube", ("youtube", None)),
        ("Go to Google", ("google", None)),
        ("Launch GitHub", ("github", None)),
        ("Visit OpenAI", ("openai", None)),
        ("Open Facebook", ("facebook", None)),
        ("Go to Wikipedia", ("wikipedia", None)),
    ]
    
    for command, expected_result in test_cases:
        result = agent.extract_site_and_search(command)
        assert result == expected_result, f"Expected {expected_result}, got {result} for command: {command}"
    
    print("✅ Site mapping tests passed!")


def test_smart_search():
    """Test smart search functionality."""
    print("🧪 Testing smart search...")
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    # Test search commands
    test_cases = [
        ("Open YouTube and search for lo-fi music", ("youtube", "lo-fi music")),
        ("Go to Google and search for AI tools", ("google", "ai tools")),
        ("Launch GitHub and search for python projects", ("github", "python projects")),
        ("Open Wikipedia and search for machine learning", ("wikipedia", "machine learning")),
    ]
    
    for command, expected_result in test_cases:
        result = agent.extract_site_and_search(command)
        assert result == expected_result, f"Expected {expected_result}, got {result} for command: {command}"
    
    print("✅ Smart search tests passed!")


def test_url_extraction():
    """Test URL extraction from commands."""
    print("🧪 Testing URL extraction...")
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    # Test direct URLs
    test_cases = [
        ("Open https://example.com", ("https://example.com", None)),
        ("Go to http://test.org", ("http://test.org", None)),
        ("Visit https://myportfolio.dev", ("https://myportfolio.dev", None)),
    ]
    
    for command, expected_result in test_cases:
        result = agent.extract_site_and_search(command)
        assert result == expected_result, f"Expected {expected_result}, got {result} for command: {command}"
    
    print("✅ URL extraction tests passed!")


def test_search_fallback():
    """Test Google search fallback for unknown sites."""
    print("🧪 Testing search fallback...")
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    # Test unknown sites that should trigger Google search
    test_cases = [
        ("Open my custom tutorials", (None, None)),
        ("Go to machine learning course", (None, None)),
        ("Visit my personal blog", (None, None)),
    ]
    
    for command, expected_result in test_cases:
        result = agent.extract_site_and_search(command)
        assert result == expected_result, f"Expected {expected_result}, got {result} for command: {command}"
    
    print("✅ Search fallback tests passed!")


def test_voice_trigger_removal():
    """Test that voice triggers are properly removed from commands."""
    print("🧪 Testing voice trigger removal...")
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    # Test various voice triggers
    test_cases = [
        ("Please open YouTube", ("youtube", None)),
        ("Can you open Google", ("google", None)),
        ("Would you open GitHub", ("github", None)),
        ("I want to go to OpenAI", ("openai", None)),
        ("Navigate to Facebook", ("facebook", None)),
    ]
    
    for command, expected_result in test_cases:
        result = agent.extract_site_and_search(command)
        assert result == expected_result, f"Expected {expected_result}, got {result} for command: {command}"
    
    print("✅ Voice trigger removal tests passed!")


def test_clean_site_names():
    """Test clean site name generation."""
    print("🧪 Testing clean site names...")
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    test_cases = [
        ("youtube", "YouTube"),
        ("github", "GitHub"),
        ("stackoverflow", "Stack Overflow"),
        ("openai", "OpenAI"),
        ("google", "Google"),
        ("unknown", "Unknown"),
    ]
    
    for site_name, expected_clean_name in test_cases:
        clean_name = agent.get_clean_site_name(site_name)
        assert clean_name == expected_clean_name, f"Expected {expected_clean_name}, got {clean_name} for {site_name}"
    
    print("✅ Clean site names tests passed!")


@patch('webbrowser.open')
def test_browser_opening(mock_browser_open):
    """Test browser opening functionality."""
    print("🧪 Testing browser opening...")
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    # Mock the browser open function
    mock_browser_open.return_value = True
    
    # Test opening a URL
    result = agent.open_url("https://google.com", "google")
    
    # Verify the browser was called
    mock_browser_open.assert_called_once_with("https://google.com")
    assert result == True
    
    print("✅ Browser opening tests passed!")


@patch('webbrowser.open')
def test_smart_search_opening(mock_browser_open):
    """Test smart search URL opening."""
    print("🧪 Testing smart search opening...")
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    # Mock the browser open function
    mock_browser_open.return_value = True
    
    # Test opening a search URL
    result = agent.open_url("https://youtube.com/results?search_query=lo-fi+music", "youtube", "lo-fi music")
    
    # Verify the browser was called
    mock_browser_open.assert_called_once_with("https://youtube.com/results?search_query=lo-fi+music")
    assert result == True
    
    print("✅ Smart search opening tests passed!")


def test_agent_initialization():
    """Test agent initialization with different voice settings."""
    print("🧪 Testing agent initialization...")
    
    # Test with voice enabled
    agent1 = BrowserOpenerAgent(enable_voice=True)
    assert hasattr(agent1, 'speech_output')
    assert hasattr(agent1, 'speech_input')
    
    # Test with voice disabled
    agent2 = BrowserOpenerAgent(enable_voice=False)
    assert hasattr(agent2, 'speech_output')
    assert hasattr(agent2, 'speech_input')
    
    # Test site mappings are loaded with new structure
    assert len(agent1.site_mappings) > 0
    assert "youtube" in agent1.site_mappings
    assert "google" in agent1.site_mappings
    assert "github" in agent1.site_mappings
    
    # Test site mappings have URL and search_url
    for site_name, site_info in agent1.site_mappings.items():
        assert "url" in site_info
        assert isinstance(site_info["url"], str)
    
    # Test voice triggers are loaded
    assert len(agent1.voice_triggers) > 0
    assert "open" in agent1.voice_triggers
    assert "go to" in agent1.voice_triggers
    
    # Test search keywords are loaded
    assert len(agent1.search_keywords) > 0
    assert "search for" in agent1.search_keywords
    assert "find" in agent1.search_keywords
    
    print("✅ Agent initialization tests passed!")


def run_all_tests():
    """Run all tests."""
    print("🚀 Starting BrowserOpenerAgent tests...\n")
    
    try:
        test_agent_initialization()
        test_url_validation()
        test_site_mapping()
        test_smart_search()
        test_url_extraction()
        test_search_fallback()
        test_voice_trigger_removal()
        test_clean_site_names()
        test_browser_opening()
        test_smart_search_opening()
        
        print("\n🎉 All tests passed! BrowserOpenerAgent is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
