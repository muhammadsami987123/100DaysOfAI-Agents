from agent import BookSummaryAgent
from utils.llm_service import LLMService

print("Testing with actual prompt template...")

try:
    # Test LLM Service initialization
    llm_service = LLMService()
    print(f"LLM Service initialized. Current LLM: {llm_service.current_llm}")
    
    # Test agent initialization
    agent = BookSummaryAgent(llm_service=llm_service)
    print("BookSummaryAgent initialized successfully")
    
    # Test with a simple chapter
    test_chapter = "This is a test chapter about the importance of time management and provides practical strategies for organizing daily tasks effectively."
    
    print(f"\nTesting with chapter: {test_chapter}")
    print("Calling agent.summarize_chapter...")
    
    result = agent.summarize_chapter(test_chapter, "concise")
    
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")
    
    if isinstance(result, dict) and "summary" in result:
        print("✅ Success! Summary generated:")
        print(f"Summary: {result['summary']}")
        print(f"Key points: {result.get('key_points', [])}")
    else:
        print("❌ Error: Invalid result format")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
