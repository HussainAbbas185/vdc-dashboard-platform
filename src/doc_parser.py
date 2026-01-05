import os
import re
import pandas as pd
from pypdf import PdfReader
from docx import Document

def extract_text_from_pdf(file_path_or_buffer):
    """Extracts text from a PDF file."""
    reader = PdfReader(file_path_or_buffer)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path_or_buffer):
    """Extracts text from a DOCX file."""
    doc = Document(file_path_or_buffer)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def parse_document(file_name, file_buffer):
    """
    Parses a document (PDF/DOCX) and attempts to extract basic metadata 
    (Name, Email) using simple heuristics. Returns a dictionary.
    """
    file_ext = file_name.split('.')[-1].lower()
    text = ""
    
    try:
        if file_ext == 'pdf':
            text = extract_text_from_pdf(file_buffer)
        elif file_ext in ['docx', 'doc']:
            text = extract_text_from_docx(file_buffer)
        else:
            return None
    except Exception as e:
        print(f"Error parsing {file_name}: {e}")
        return None

    # heuristic extraction
    email = None
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        email = email_match.group(0)

    # Name heuristic: First line that looks like a name (2-3 words, capitalized)
    # This is very basic, but serves the "Intelligent" demo purpose.
    name = "Unknown"
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines[:5]: # Check first 5 lines
        words = line.split()
        if 2 <= len(words) <= 3 and all(w[0].isupper() for w in words if w[0].isalpha()):
            name = line
            break
            
    return {
        "filename": file_name,
        "extracted_name": name,
        "extracted_email": email,
        "full_text": text,
        "file_type": file_ext
    }
