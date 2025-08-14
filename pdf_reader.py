from PyPDF2 import PdfReader
from docx import Document
#from transformers import pipeline
#import re
#import language_tool_python
#from langdetect import detect

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



# def split_text_by_length(text):
#     # Tách câu theo . ! ? hoặc xuống dòng, giữ dấu
#     sentences = re.findall(r'[^.!?\n]+[.!?]?', text)
#     chunks = [s.strip() for s in sentences if s.strip()]
#     return chunks



# def correct_Vn(Input_text):
#     sentences = split_text_by_length(Input_text)
#     VNspell_checker = pipeline(
#         "text2text-generation",
#         model="bmd1905/vietnamese-correction-v2"
#     )
    
#     result_lines = ["Các câu có thể sai và đã được sửa:"]
#     for sentence in sentences:
#         pred = VNspell_checker(sentence, max_length=128)[0]['generated_text']
#         result_lines.append(f"- {sentence} => {pred}")
#     return "\n".join(result_lines)



    


# def correct_english(text):
#     # try:
#     tool = language_tool_python.LanguageTool('en-US')
#     # except Exception as e:   
#     #     tool = language_tool_python.LanguageToolPublicAPI('en-US')

#     corrected_sentences = []

#     for sentence in split_text_by_length(text):
#         matches = tool.check(sentence)
#         corrected = language_tool_python.utils.correct(sentence, matches)
#         corrected_sentences.append(corrected)

#     # Ghép lại thành đoạn văn hoàn chỉnh
#     tool.close()
#     return ' '.join(corrected_sentences)

def auto_correct(file_obj):
    try:
        filename = file_obj.filename.lower()

        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_obj)
            return text
        elif filename.endswith(".txt"):
            text = extract_text_from_txt(file_obj)
            return text
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(file_obj)
            return text
        else:
            return "[Unsupported file type]"

        # lang = detect(text)
        # if lang == 'en':
        #     #return correct_english(text)
        # elif lang == 'vi':
        #     #return correct_Vn(text)
        # else:
        #     return f"[Unsupported language: {lang}] {text}"

    except Exception as e:
        return f"[Có lỗi khi xử lý file] {str(e)}"


# if __name__ == "__main__":

#     text_en = """
#     She dont has any idear how to solve the problam. When I watched the anime, " 
#     "I knew that they made a real song for episode 11. And when I searched on youtube, I was amazed.  Outstanding move, Waseda-san
#     seriously？you made a whole manga and  anime just right for advertising  your song? well it's the coolest thing i‘ve ever met.good song by the way.
#     """


#     text_vi = """
#     Tôi di học vào ngáy hôm qua nhưng quên mang sách.kinh tế viet nam dang dứng truoc 1 thoi ky đổi mơi chưa tung có tienf lệ trong lịch sử

#     """

#     print(" EN:", auto_correct(text_en))
#     print(" VI:", auto_correct(text_vi))





