import google.generativeai as genai
import os
import requests
from bs4 import BeautifulSoup
from docx import Document

class TextCleanerAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-001')

    def _clean_with_gemini(self, text: str) -> str:
        """Sends text to Gemini API for cleaning and returns the polished version."""
        prompt = f"""
        You are TextCleanerAgent, an intelligent assistant powered by Google's Gemini API. Your job is to take messy, unstructured, or poorly written text and return a polished, grammatically correct, and well-formatted version.

        You must:
        - Correct grammar, punctuation, and spelling
        - Improve sentence structure and coherence
        - Remove unnecessary symbols or line breaks
        - Maintain the original meaning
        - Format content into clean, readable paragraphs

        Here is the text to clean:
        {text}
        """
        response = self.model.generate_content(prompt)
        return response.text

    def clean_text(self, text: str, summarize: bool = False, provide_diff: bool = False) -> str:
        """Cleans the given text using Gemini API."""
        cleaned_text = self._clean_with_gemini(text)

        output = ""
        if provide_diff:
            output += "Original Text:\n"
            output += "--------------------\n"
            output += text + "\n\n"
            output += "Cleaned Text:\n"
            output += "--------------------\n"
        output += cleaned_text

        if summarize:
            output += "\n\nSummary:\n"
            output += "--------------------\n"
            output += self._summarize_with_gemini(cleaned_text)

        return output

    def _summarize_with_gemini(self, text: str) -> str:
        """Summarizes the given text using Gemini API."""
        prompt = f"""
        Please summarize the following text concisely and clearly:
        {text}
        """
        response = self.model.generate_content(prompt)
        return response.text

    def _read_docx(self, file_path: str) -> str:
        """Reads content from a .docx file."""
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

    def _read_txt(self, file_path: str) -> str:
        """Reads content from a .txt file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _fetch_url_content(self, url: str) -> str:
        """Fetches and extracts main text content from a URL."""
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from common content containers
            paragraphs = soup.find_all('p')
            text_content = [para.get_text() for para in paragraphs]
            return '\n'.join(text_content)
        except requests.exceptions.RequestException as e:
            return f"Error fetching URL: {e}"
