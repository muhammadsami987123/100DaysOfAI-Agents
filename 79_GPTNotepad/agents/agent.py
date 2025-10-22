import os
import io
import requests
import bs4
import PyPDF2
import docx
import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI
from config import Config

load_dotenv()

class GPTSummarizerAgent:
    def __init__(self):
        self.model_choice = Config.LLM_MODEL.lower()
        self.openai_client = None
        self.gemini_client = None
        self.gemini_model = None
        
        self._init_clients()

        self.prompt_template = self._load_prompt_template()

    # --- FILE and URL TEXT EXTRACTION ---
    def extract_text_from_file(self, file, file_bytes):
        filename = file.filename.lower()
        if filename.endswith(".txt"):
            try:
                return file_bytes.decode("utf-8", errors="replace")
            except Exception:
                return file_bytes.decode("latin1", errors="replace")
        elif filename.endswith(".pdf"):
            return self._extract_from_pdf(file_bytes)
        elif filename.endswith(".docx"):
            return self._extract_from_docx(file_bytes)
        else:
            return "[Unsupported file type: only .txt, .pdf, .docx supported]"
    def _extract_from_pdf(self, file_bytes):
        try:
            pdf = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            return "\n".join([page.extract_text() or '' for page in pdf.pages])
        except Exception as e:
            return f"[Error reading PDF: {e}]"
    def _extract_from_docx(self, file_bytes):
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            return f"[Error reading DOCX: {e}]"
    def extract_text_from_url(self, url):
        try:
            resp = requests.get(url, timeout=10)
            soup = bs4.BeautifulSoup(resp.content, "html.parser")
            # Use boilerplate/dominant content, fallback: big blocks of text
            [s.decompose() for s in soup(['script', 'style', 'footer', 'nav', 'aside', 'form'])]
            blocks = [t.get_text(strip=True, separator=' ') for t in soup.find_all(['p','li','article','section','main','div']) if t.get_text(strip=True)]
            text = "\n".join([b for b in blocks if len(b) > 50])
            if not text:
                text = soup.get_text(separator=' ', strip=True)
            return text
        except Exception as e:
            return f"[Error fetching page: {e}]"

    # --- SUMMARIZATION INTERFACE ---
    def summarize_with_notes(self, note_text: str) -> dict:
        # The summary (bullets/short) and notes (full, cleaned)
        summary = self.summarize_only(note_text)
        notes = note_text.strip() if note_text else "[No note content found]"
        return {
            "summary": summary,
            "notes": notes
        }

    # UNIVERSAL SUMMARIZER (fallback between LLMs)
    def summarize_only(self, text: str):
        prompt = self.prompt_template.format(user_input=text)
        summary_text = ""

        # Prefer Gemini
        if self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                summary_text = (response.text or "").strip()
                out = self._parse_summary(summary_text)
                if out: return out
            except Exception as e:
                print(f"Gemini summarization failed: {e}")
        # Fallback OpenAI
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are GPTNotepad. Summarize notes concisely."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.4
                )
                summary_text = response.choices[0].message.content.strip()
                out = self._parse_summary(summary_text)
                if out: return out
            except Exception as e:
                print(f"OpenAI summarization failed: {e}")
        return ["Unable to generate summary."]

    def _init_clients(self):
        if self.model_choice == "gemini" and Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL)
                self.gemini_client = genai
                print("✅ GPTSummarizerAgent initialized with Gemini")
            except Exception as e:
                print(f"❌ Error initializing Gemini client: {e}")
                self.gemini_client = None
                self.gemini_model = None
        
        if self.model_choice == "openai" and Config.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                print("✅ GPTSummarizerAgent initialized with OpenAI")
            except Exception as e:
                print(f"❌ Error initializing OpenAI client: {e}")
                self.openai_client = None
        
        # Fallback if preferred model is not available or explicitly not set
        if not self.gemini_client and Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL)
                self.gemini_client = genai
                print("✅ GPTSummarizerAgent initialized with Gemini (fallback)")
            except Exception as e:
                print(f"❌ Error initializing Gemini fallback: {e}")
                self.gemini_client = None
                self.gemini_model = None
        
        if not self.openai_client and Config.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                print("✅ GPTSummarizerAgent initialized with OpenAI (fallback)")
            except Exception as e:
                print(f"❌ Error initializing OpenAI fallback: {e}")
                self.openai_client = None
        
        if not self.gemini_client and not self.openai_client:
            print("⚠️ Warning: No valid API keys provided for any LLM. Summarization will not work.")

    def _load_prompt_template(self):
        script_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(script_dir, "..", Config.SUMMARIZER_PROMPT_PATH)
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Prompt file not found at {prompt_path}")
            return "You are GPTNotepad. Summarize the following note in 3–6 short bullet points. Focus only on the key ideas, events, actions, or thoughts. Do not add or assume anything. Use professional, neutral tone.\n\nNote: {user_input}"

    def _parse_summary(self, summary_text: str):
        # Attempt to split into bullet points, handling various formats
        if summary_text.startswith('-') or summary_text.startswith('*'):
            return [point.strip() for point in summary_text.split('\n') if point.strip()]
        else:
            # If it's a single paragraph, wrap it as a single bullet point
            return [summary_text]
