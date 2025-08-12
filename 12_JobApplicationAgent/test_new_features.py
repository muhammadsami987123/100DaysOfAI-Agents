#!/usr/bin/env python3
"""
Test script to verify new JobApplicationAgent features
"""

import sys
import os
from pathlib import Path

def test_url_extractor():
    """Test URL extraction functionality"""
    print("Testing URL extraction...")
    
    try:
        from url_extractor import JobURLExtractor
        
        extractor = JobURLExtractor()
        
        # Test supported sites
        sites = extractor.get_supported_sites()
        print(f"✅ Supported job sites: {list(sites.keys())}")
        
        # Test URL validation
        valid_url = "https://www.linkedin.com/jobs/view/123456"
        invalid_url = "not-a-url"
        
        assert extractor._is_valid_url(valid_url) == True
        assert extractor._is_valid_url(invalid_url) == False
        print("✅ URL validation working correctly")
        
        # Test job site identification
        linkedin_url = "https://www.linkedin.com/jobs/view/123456"
        indeed_url = "https://www.indeed.com/viewjob?jk=123456"
        
        assert extractor._identify_job_site(linkedin_url) == "linkedin"
        assert extractor._identify_job_site(indeed_url) == "indeed"
        print("✅ Job site identification working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ URL extraction test failed: {e}")
        return False

def test_additional_documents():
    """Test additional document functionality"""
    print("\nTesting additional documents...")
    
    try:
        from config import ADDITIONAL_DOCUMENTS, PROMPT_TEMPLATES
        
        # Check if all document types are defined
        expected_docs = [
            "personal_statement", "reference_page", "thank_you_note", 
            "motivation_letter", "linkedin_bio"
        ]
        
        for doc_type in expected_docs:
            assert doc_type in ADDITIONAL_DOCUMENTS, f"Missing {doc_type}"
            assert doc_type in PROMPT_TEMPLATES, f"Missing prompt for {doc_type}"
        
        print(f"✅ All additional document types defined: {list(ADDITIONAL_DOCUMENTS.keys())}")
        
        # Check prompt templates
        for doc_type, prompt in PROMPT_TEMPLATES.items():
            if doc_type in expected_docs:
                assert "{resume_analysis}" in prompt, f"Missing resume_analysis in {doc_type}"
                assert "{job_analysis}" in prompt, f"Missing job_analysis in {doc_type}"
                assert "{language}" in prompt, f"Missing language in {doc_type}"
        
        print("✅ All prompt templates properly formatted")
        
        return True
        
    except Exception as e:
        print(f"❌ Additional documents test failed: {e}")
        return False

def test_document_generator():
    """Test document generator improvements"""
    print("\nTesting document generator improvements...")
    
    try:
        from document_generator import DocumentGenerator
        
        generator = DocumentGenerator()
        
        # Test additional document generation method
        test_content = "This is a test document content."
        
        # Test that the method exists
        assert hasattr(generator, 'generate_additional_document'), "Missing generate_additional_document method"
        
        # Test supported formats
        formats = generator.get_supported_formats()
        assert "pdf" in formats, "PDF format not supported"
        assert "docx" in formats, "DOCX format not supported"
        
        print("✅ Document generator improvements working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Document generator test failed: {e}")
        return False

def test_job_agent():
    """Test job agent new features"""
    print("\nTesting job agent new features...")
    
    try:
        from job_agent import JobApplicationAgent
        
        # Test that new methods exist
        agent = JobApplicationAgent()
        
        assert hasattr(agent, 'extract_job_from_url'), "Missing extract_job_from_url method"
        assert hasattr(agent, 'get_additional_documents'), "Missing get_additional_documents method"
        assert hasattr(agent, 'get_supported_job_sites'), "Missing get_supported_job_sites method"
        
        # Test additional documents getter
        additional_docs = agent.get_additional_documents()
        assert isinstance(additional_docs, dict), "get_additional_documents should return dict"
        
        # Test supported job sites getter
        job_sites = agent.get_supported_job_sites()
        assert isinstance(job_sites, dict), "get_supported_job_sites should return dict"
        
        print("✅ Job agent new features working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Job agent test failed: {e}")
        return False

def main():
    """Run all new feature tests"""
    print("=" * 50)
    print("JobApplicationAgent - New Features Test")
    print("=" * 50)
    
    tests = [
        ("URL Extraction", test_url_extractor),
        ("Additional Documents", test_additional_documents),
        ("Document Generator", test_document_generator),
        ("Job Agent Features", test_job_agent)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All new features are working correctly!")
        print("\nNew features available:")
        print("✅ URL extraction from job posting sites")
        print("✅ Additional document generation (5 new types)")
        print("✅ Improved document formatting")
        print("✅ Enhanced UI with new options")
    else:
        print("\n⚠️  Some new feature tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
