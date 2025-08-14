from PyPDF2 import PdfReader
from docx import Document
from transformers import pipeline
import re
import language_tool_python
from langdetect import detect

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


def split_text_by_length(text, max_length=300):
    # Tách văn bản thành các câu
    sentences = re.findall(r'[^.!?]+[.!?]?', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def correct_Vn(Input_text):

    text_chunks = split_text_by_length(Input_text)

 
    VNspell_checker = pipeline("text2text-generation", model="bmd1905/vietnamese-correction-v2")


    corrected_chunks = VNspell_checker(text_chunks, max_length=512)

    
    corrected_text = ' '.join([chunk['generated_text'] for chunk in corrected_chunks])

    
    return corrected_text


def correct_english(text):
    # try:
    tool = language_tool_python.LanguageTool('en-US')
    # except Exception as e:   
    #     tool = language_tool_python.LanguageToolPublicAPI('en-US')

    corrected_sentences = []

    for sentence in split_text_by_length(text):
        matches = tool.check(sentence)
        corrected = language_tool_python.utils.correct(sentence, matches)
        corrected_sentences.append(corrected)

    # Ghép lại thành đoạn văn hoàn chỉnh
    return ' '.join(corrected_sentences)

def auto_correct(text):
    try:
        lang = detect(text)
        if lang == 'en':
            return correct_english(text)
        elif lang == 'vi':
            return correct_Vn(text)
        else:
            return f"[Unsupported language: {lang}] {text}"
    except Exception as e:
        return f"[Error detecting language] {str(e)}"

if __name__ == "__main__":

    text_en = "She dont has any idear how to solve the problam."
    text_vi = "Tooi di học vào ngáy hôm qua nhưng quên mang sách."

    print(" EN:", auto_correct(text_en))
    print(" VI:", auto_correct(text_vi))





