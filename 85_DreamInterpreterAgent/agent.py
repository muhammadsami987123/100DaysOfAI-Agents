from typing import Dict, Any, List, Optional
from utils.llm_service import LLMService
import re


class DreamInterpreterAgent:
    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm = llm_service or LLMService()

    def interpret(self, dream_text: str) -> Dict[str, Any]:
        """Primary entry: attempt LLM-based interpretation, fall back to local symbolic analysis."""
        prompt_template = self.llm._read_template("interpreter_prompt.txt")
        prompt = prompt_template.replace("{dream_text}", dream_text)

        # Try LLM
        result = self.llm.generate_content(prompt)
        # If LLM returned a dict with expected keys, pass through
        if isinstance(result, dict) and ("interpretation" in result or "summary" in result):
            # normalize keys
            interpretation = result.get("interpretation") or result.get("summary") or ""
            symbols = result.get("symbols") or result.get("key_points") or []
            message = result.get("message") or ""
            return {"interpretation": interpretation, "symbols": symbols, "message": message}

        # Fallback to local analysis
        return self._local_interpret(dream_text)

    def _local_interpret(self, dream: str) -> Dict[str, Any]:
        symbols = self._extract_symbols(dream)
        emotions = self._detect_emotions(dream)
        interpretation = self._compose_interpretation(dream, symbols, emotions)
        message = self._compose_message(emotions)
        return {"interpretation": interpretation, "symbols": symbols, "message": message}

    def _extract_symbols(self, dream: str) -> List[Dict[str, str]]:
        mapping = {
            "flying": "Freedom, ambition, perspective",
            "falling": "Fear, loss of control, anxiety",
            "water": "Emotions, subconscious, purification",
            "teeth": "Anxiety about appearance or power",
            "death": "Endings, transformation, change",
            "chase": "Avoidance, stress, conflict",
            "house": "Self, inner life, security",
            "baby": "New beginnings, vulnerability",
            "fire": "Passion, anger, transformation",
            "road": "Life path, choices",
        }

        found = []
        text = dream.lower()
        for k, meaning in mapping.items():
            if re.search(r"\b" + re.escape(k) + r"\b", text):
                found.append({"symbol": k, "meaning": meaning})
        return found

    def _detect_emotions(self, dream: str) -> List[str]:
        emotions = []
        e_map = {
            "anx": ["anxious", "anxiety", "anxiousness"],
            "fear": ["afraid", "scared", "fear"],
            "joy": ["happy", "joy", "excited"],
            "sad": ["sad", "down", "depressed"],
        }
        t = dream.lower()
        for label, words in e_map.items():
            for w in words:
                if w in t:
                    emotions.append(label)
                    break
        return emotions

    def _compose_interpretation(self, dream: str, symbols: List[Dict[str, str]], emotions: List[str]) -> str:
        parts = []
        if symbols:
            parts.append("Key symbols in your dream suggest: ")
            symbol_texts = [f"{s['symbol']} ({s['meaning']})" for s in symbols]
            parts.append(", ".join(symbol_texts) + ".")

        if emotions:
            parts.append("Emotionally, the dream feels: " + ", ".join(emotions) + ".")

        parts.append("A gentle takeaway: this dream may be reflecting your inner concerns and hopes. Consider what in waking life maps to these symbols and emotions.")
        return "\n\n".join(parts)

    def _compose_message(self, emotions: List[str]) -> str:
        if "anx" in emotions or "fear" in emotions:
            return "Ground yourself with small routines and breathe — your instincts are signaling care is needed."
        if "joy" in emotions:
            return "Celebrate this energy and consider how to expand it in waking life."
        return "Reflect kindly: dreams are symbolic and meant to help, not to worry you."
