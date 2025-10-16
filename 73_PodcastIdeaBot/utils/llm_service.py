import os
import json
from typing import Optional, Dict, Any

from config import LLM_MODEL, GEMINI_API_KEY, OPENAI_API_KEY


class LLMService:
	def __init__(self):
		self.model_choice = (LLM_MODEL or 'gemini').lower()
		self.gemini_client = None
		self.gemini_model = None
		self.openai_client = None
		self._init_clients()

	def _init_clients(self) -> None:
		if self.model_choice == 'gemini' and GEMINI_API_KEY:
			try:
				import google.generativeai as genai
				genai.configure(api_key=GEMINI_API_KEY)
				model_name = os.environ.get('GEMINI_MODEL_NAME', 'gemini-2.0-flash')
				self.gemini_model = genai.GenerativeModel(model_name)
				self.gemini_client = genai
			except Exception:
				self.gemini_client = None
				self.gemini_model = None
		elif self.model_choice in ('gpt', 'openai') and OPENAI_API_KEY:
			try:
				from openai import OpenAI
				self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
			except Exception:
				self.openai_client = None

	def _parse_json(self, text: str) -> Dict[str, Any]:
		try:
			return json.loads(text)
		except Exception:
			start = text.find('{')
			end = text.rfind('}')
			if start != -1 and end != -1 and end > start:
				snippet = text[start:end+1]
				try:
					return json.loads(snippet)
				except Exception:
					pass
			return {}

	def ideate_podcast(self, prompt: str) -> Dict[str, Any]:
		# Try Gemini
		if self.model_choice == 'gemini' and self.gemini_model is not None:
			try:
				result = self.gemini_model.generate_content(prompt)
				text = (result.text or '').strip()
				data = self._parse_json(text)
				if data:
					return data
			except Exception:
				pass
		# Try OpenAI
		if self.openai_client is not None:
			try:
				model_name = os.environ.get('OPENAI_MODEL_NAME', 'gpt-4o-mini')
				resp = self.openai_client.chat.completions.create(
					model=model_name,
					messages=[
						{ 'role': 'system', 'content': 'You are PodcastIdeaBot. Reply ONLY in strict JSON.' },
						{ 'role': 'user', 'content': prompt },
					],
					temperature=0.5,
				)
				text = (resp.choices[0].message.content or '').strip()
				data = self._parse_json(text)
				if data:
					return data
			except Exception:
				pass
		# Fallback
		return {}


