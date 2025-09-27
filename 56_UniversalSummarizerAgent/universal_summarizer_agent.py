import google.generativeai as genai
from config import Config
import requests
from bs4 import BeautifulSoup
from docx import Document
import PyPDF2

class UniversalSummarizerAgent:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL_NAME)
        self.prompt_template = """You are UniversalSummarizerAgent, an advanced multi-input summarization tool designed to generate clean, concise, and context-aware summaries from various types of content.

Your job is to summarize the provided content. You can summarize:
- Plain text pasted by the user
- Uploaded files (.pdf, .docx, .txt)
- Public URLs (e.g., news articles, blogs, research papers)
- Extracted text from scanned images or OCR content
- Notes or book pages

Content to Summarize:
{content}

Output Format: {summary_format}
Language: {language}

Generated Summary:"""

    def _extract_text_from_url(self, url: str) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = ' '.join([para.get_text() for para in paragraphs])
            return text
        except requests.exceptions.RequestException as e:
            return f"Error fetching URL: {e}"
        except Exception as e:
            return f"Error parsing URL content: {e}"

    def _extract_text_from_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
            return text
        except Exception as e:
            return f"Error reading PDF file: {e}"

    def _extract_text_from_docx(self, file_path: str) -> str:
        text = ""
        try:
            document = Document(file_path)
            for paragraph in document.paragraphs:
                text += paragraph.text + '\n'
            return text
        except Exception as e:
            return f"Error reading DOCX file: {e}"

    def summarize_content(self, content: str, summary_format: str, language: str, content_type: str = "text") -> str:
        extracted_content = ""
        if content_type == "url":
            extracted_content = self._extract_text_from_url(content)
        elif content_type == "pdf":
            extracted_content = self._extract_text_from_pdf(content)
        elif content_type == "docx":
            extracted_content = self._extract_text_from_docx(content)
        elif content_type == "txt" or content_type == "email" or content_type == "text":
            extracted_content = content
        else:
            return "Unsupported content type."

        if "Error" in extracted_content: # Handle extraction errors
            return extracted_content

        prompt = self.prompt_template.format(
            content=extracted_content,
            summary_format=Config.SUMMARY_FORMATS.get(summary_format, "Bullet Points"),
            language=Config.LANGUAGE_OPTIONS.get(language, "English")
        )
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=Config.TEMPERATURE,
                max_output_tokens=Config.MAX_TOKENS
            )
        )
        return response.text
