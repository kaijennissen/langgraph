import io
import logging
from typing import Union

import docx2txt
import pypdf
from PIL import Image


def extract_text_from_pdf(file_obj: Union[str, io.BytesIO]) -> str:
    """Extract text from PDF file."""
    try:
        pdf = pypdf.PdfReader(file_obj)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise


def extract_text_from_docx(file_obj: Union[str, io.BytesIO]) -> str:
    """Extract text from DOCX file."""
    try:
        text = docx2txt.process(file_obj)
        return text.strip()
    except Exception as e:
        logging.error(f"Error extracting text from DOCX: {e}")
        raise


def process_document(file_obj: io.BytesIO, file_type: str = None) -> str:
    """Process uploaded document and extract text."""
    if file_type is None:
        file_type = file_obj.name.split(".")[-1].lower()

    if file_type == "pdf":
        return extract_text_from_pdf(file_obj)
    elif file_type in ["docx", "doc"]:
        return extract_text_from_docx(file_obj)
    elif file_type == "txt":
        return file_obj.read().decode("utf-8").strip()
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
