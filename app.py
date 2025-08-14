from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv
from pdf_reader import auto_correct
class FlaskApp:
    def __init__(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            ai_response = ""
            user_input = ""
            file_upload =""  
                
            if request.method == "POST":
                
                user_input = request.form.get("user_input", "")
                language = request.form.get("language", "vi")
                style = request.form.get("style", "basic")
                translate = request.form.get("translate")
                uploaded_file = request.files.get("text_files")

                # Tạo prompt động
                prompt = "Hãy sửa lỗi chính tả và ngữ pháp trong đoạn văn sau. "
                if style == "formal":
                    prompt += "Biến văn phong thành trang trọng. "
                elif style == "funny":
                    prompt += "Biến văn phong thành hài hước dí dỏm. "
                elif style == "multiple":
                    prompt += "Trả về nhiều phiên bản khác nhau theo các văn phong khác nhau. "
                prompt += "Không thay đổi ngôn ngữ gốc trừ khi được yêu cầu. "
                if translate:
                    prompt += f"Sau mỗi phiên bản, dịch sang ngôn ngữ '{language}' bên dưới. "

                full_content = f"{prompt}\n\nĐoạn văn:\n{user_input}"

                payload = {
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "messages": [{"role": "user", "content": full_content}]
                }

                headers = {
                    "Authorization": f"Bearer {self.API_KEY}",
                    "Content-Type": "application/json"
                }
                            

                    # Nếu có file PDF được tải lên
                if uploaded_file:
                    file_upload = auto_correct(uploaded_file)
                elif not uploaded_file and not user_input:
                    return render_template("index.html", ai_response="Không có gì xử lý cả, đừng ấn bừa nhé! :V  ")

                
                response = requests.post(self.OPENROUTER_API_URL, json=payload, headers=headers)
                 
                if response.ok:
                    ai_response = response.json()["choices"][0]["message"]["content"]

            return render_template("index.html", file_upload=file_upload, ai_response=ai_response if user_input else "                   Chúc mừng đoạn trắng tinh của bạn không sai gì cả / Congratulations, your NOTHING have nothing wrong with it"  )


    def get_app(self):
        return self.app
app = FlaskApp().get_app()