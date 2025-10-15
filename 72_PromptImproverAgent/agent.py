# PromptImproverAgent main class
import json
from utils.llm_service import LLMService

class PromptImproverAgent:
    def __init__(self, model_service=None):
        self.model_service = model_service or LLMService()

    def improve_prompt(self, raw_prompt: str, tone: str = None) -> dict:
        """
        Takes a rough/unclear prompt and returns:
        - improved version
        - 2–3 variations (formal, creative, concise, etc.)
        - optional explanation
        """
        response = self.model_service.improve_prompt(raw_prompt, tone)
        alternatives = response.get('alternatives', []) or []
        normalized_alts = []
        for item in alternatives:
            if isinstance(item, str):
                normalized_alts.append(item)
            elif isinstance(item, dict):
                if 'prompt' in item and isinstance(item['prompt'], str):
                    normalized_alts.append(item['prompt'])
                elif 'text' in item and isinstance(item['text'], str):
                    normalized_alts.append(item['text'])
                else:
                    normalized_alts.append(json.dumps(item, ensure_ascii=False))
            elif isinstance(item, list):
                normalized_alts.append(' '.join(str(x) for x in item))
            else:
                normalized_alts.append(str(item))

        return {
            'improved_prompt': response.get('improved', ''),
            'variations': normalized_alts,
            'explanation': response.get('explanation', '')
        }
