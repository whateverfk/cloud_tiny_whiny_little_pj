from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(file_stream):
    """
    Nhận file stream (từ Flask request.files) và trích xuất nội dung văn bản từ PDF.
    """
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_txt(file_stream):
    return file_stream.read().decode("utf-8")  # hoặc "utf-8-sig" nếu có BOM



def extract_text_from_docx(file_stream):
    doc = Document(file_stream)
    return "\n".join([para.text for para in doc.paragraphs])





