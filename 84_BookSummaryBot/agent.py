from typing import Dict, Any, Optional
from utils.llm_service import LLMService

class BookSummaryAgent:
    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm_service = llm_service or LLMService()

    def summarize_chapter(self, chapter_text: str, summary_type: str = "concise") -> Dict[str, Any]:
        prompt_template = self.llm_service._read_template("summary_prompt.txt")
        # Use string replacement instead of .format() to avoid issues with JSON braces
        formatted_prompt = prompt_template.replace("{chapter_text}", chapter_text)
        
        summary_result = self.llm_service.generate_content(formatted_prompt)
        return summary_result
