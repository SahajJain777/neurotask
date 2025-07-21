# file_manager/reader.py
import os
from PyPDF2 import PdfReader
from docx import Document

def read_first_page(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return read_pdf(path)
    elif ext == ".docx":
        return read_docx(path)
    elif ext == ".txt":
        return read_txt(path)
    else:
        return ""

def read_pdf(path):
    try:
        reader = PdfReader(path)
        if reader.pages:
            return reader.pages[0].extract_text()
    except Exception as e:
        print(f"PDF read error: {e}")
    return ""

def read_docx(path):
    try:
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs[:10]])
    except Exception as e:
        print(f"DOCX read error: {e}")
    return ""

def read_txt(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read(2048)
    except Exception as e:
        print(f"TXT read error: {e}")
    return ""
