import pdfplumber
from loguru import logger


class PDFParser:
    """Extract text from PDF resumes."""

    def extract_text(self, file) -> str:
        """Extract text from uploaded PDF file."""
        try:
            text = ""

            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            return text.strip()

        except Exception as e:
            logger.error(f"PDF parsing failed: {e}")
            raise ValueError("Failed to parse PDF")