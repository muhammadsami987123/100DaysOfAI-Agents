import os
from docx import Document
from pypdf import PdfReader

class ResumeParser:
    def read_file(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return ""

        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension == ".pdf":
            return self._read_pdf(file_path)
        elif file_extension == ".docx":
            return self._read_docx(file_path)
        elif file_extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return ""

    def _read_pdf(self, file_path: str) -> str:
        text = ""
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            # In a real scenario, log this error via a proper logger
            print(f"Error reading PDF: {e}")
        return text

    def _read_docx(self, file_path: str) -> str:
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            # In a real scenario, log this error via a proper logger
            print(f"Error reading DOCX: {e}")
        return text
