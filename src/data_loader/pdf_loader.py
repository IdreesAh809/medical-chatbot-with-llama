import os
from PyPDF2 import PdfReader

class PDFLoader:
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF not found at {file_path}")
        self.file_path = file_path

    def load(self):
        """Load text from PDF"""
        reader = PdfReader(self.file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
