"""
Tool for loading and extracting text from PDFs.
"""
from pypdf import PdfReader
from loguru import logger

def load_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Failed to load PDF {file_path}: {e}")
        return ""
