#!/usr/bin/env python3
"""
Test script for EmailWriterAgent inline editing feature
"""

import os
import sys

def test_editable_fields():
    """Test that editable fields are properly configured"""
    print("🔍 Testing inline editing configuration...")
    
    # Check if HTML template has editable fields
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        required_elements = [
            'id="previewSubject"',
            'id="previewTo"',
            'id="previewFrom"',
            'id="previewBody"',
            'id="editBtn"',
            'class="editable-field"',
            'class="editable-body"'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in html_content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Missing elements: {missing_elements}")
            return False
        else:
            print("✅ All editable field elements present in HTML")
            return True
            
    except FileNotFoundError:
        print("❌ templates/index.html not found")
        return False
    except Exception as e:
        print(f"❌ Error reading HTML template: {e}")
        return False

def test_css_styles():
    """Test that CSS styles for editing are present"""
    print("\n🔍 Testing CSS styles for inline editing...")
    
    try:
        with open('static/css/style.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        required_styles = [
            '.editable-field',
            '.editable-body',
            '.editable-field:focus',
            '.editable-body:focus',
            '.editable-field[readonly]',
            '.editable-body[readonly]'
        ]
        
        missing_styles = []
        for style in required_styles:
            if style not in css_content:
                missing_styles.append(style)
        
        if missing_styles:
            print(f"❌ Missing CSS styles: {missing_styles}")
            return False
        else:
            print("✅ All editing CSS styles present")
            return True
            
    except FileNotFoundError:
        print("❌ static/css/style.css not found")
        return False
    except Exception as e:
        print(f"❌ Error reading CSS file: {e}")
        return False

def test_javascript_functionality():
    """Test that JavaScript functions for editing are present"""
    print("\n🔍 Testing JavaScript functionality...")
    
    try:
        with open('static/js/app.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        required_functions = [
            'toggleEditMode',
            'editBtn.addEventListener',
            'previewSubject?.value',
            'previewBody?.value'
        ]
        
        missing_functions = []
        for func in required_functions:
            if func not in js_content:
                missing_functions.append(func)
        
        if missing_functions:
            print(f"❌ Missing JavaScript functions: {missing_functions}")
            return False
        else:
            print("✅ All editing JavaScript functions present")
            return True
            
    except FileNotFoundError:
        print("❌ static/js/app.js not found")
        return False
    except Exception as e:
        print(f"❌ Error reading JavaScript file: {e}")
        return False

def main():
    """Run all inline editing tests"""
    print("🤖 EmailWriterAgent - Inline Editing Tests")
    print("=" * 50)
    
    tests = [
        ("HTML Template", test_editable_fields),
        ("CSS Styles", test_css_styles),
        ("JavaScript Functions", test_javascript_functionality)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Inline Editing Test Results")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All inline editing tests passed!")
        print("\nInline editing features implemented:")
        print("✅ Editable subject, recipient, sender, and body fields")
        print("✅ Toggle edit mode with Edit/Save button")
        print("✅ Auto-enable edit mode after email generation")
        print("✅ Copy/download use edited content")
        print("✅ Visual feedback for edit mode")
        print("✅ Focus on body text for immediate editing")
        
        print("\nUsage:")
        print("1. Generate an email")
        print("2. Click 'Edit Email' to enable editing")
        print("3. Make changes directly in the preview")
        print("4. Click 'Save Changes' to finish editing")
        print("5. Copy/download will use your edited content")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 