from agent import BookSummaryAgent
from utils.llm_service import LLMService
from config import Config

print("Testing BookSummaryAgent directly...")
print(f"Gemini API Key: {'Set' if Config.GEMINI_API_KEY else 'Not set'}")
print(f"OpenAI API Key: {'Set' if Config.OPENAI_API_KEY else 'Not set'}")
print(f"Default LLM: {Config.DEFAULT_LLM}")

try:
    # Test LLM Service initialization
    llm_service = LLMService()
    print(f"LLM Service initialized. Current LLM: {llm_service.current_llm}")
    print(f"Gemini client: {'Available' if llm_service.gemini_client else 'Not available'}")
    print(f"OpenAI client: {'Available' if llm_service.openai_client else 'Not available'}")
    
    # Test agent initialization
    agent = BookSummaryAgent(llm_service=llm_service)
    print("BookSummaryAgent initialized successfully")
    
    # Test with a simple chapter
    test_chapter = "This is a test chapter about the importance of time management and provides practical strategies for organizing daily tasks effectively."
    
    print(f"\nTesting with chapter: {test_chapter}")
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
