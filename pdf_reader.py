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


def test_pdf_reading(file_path="Cau hoi on tap bai 4.pdf"):
    """
    Hàm test: Đọc nội dung từ file PDF cục bộ và in ra màn hình.
    """
    try:
        with open(file_path, "rb") as f:

            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            print(text.strip())

    except Exception as e:
        print(f" Lỗi khi đọc file: {e}")

# ✅ Chạy test nếu file được gọi trực tiếp
if __name__ == "__main__":
    print(" Đang test đọc file PDF 2...")
    test_pdf_reading("Cau hoi on tap bai 4.pdf")  #  Thay bằng đường dẫn file PDF bạn muốn test
