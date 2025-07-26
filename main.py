from flask import Flask, request, render_template
import requests
import json
from dotenv import load_dotenv
import os
import steeamlit as st
app = Flask(__name__)


load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

choice1= "chỉ tạo 1 phiên bản sửa lôi chính tả và ngữ pháp, không tạo thêm bất kỳ thông tin nào khác,không đưa đoạn văn bản về ngôn ngữ khác. Chỉ trả về phiên bản đã sửa lỗi chính tả và ngữ pháp."

@app.route("/", methods=["GET", "POST"])
def index():
    ai_response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]

        payload = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [{"role": "user", "content": "Bạn hãy sửa lỗi ngữ pháp và chính tả trong đoạn văn sau và :  "  + choice1 + user_input}]
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        if response.ok:
            ai_response = response.json()["choices"][0]["message"]["content"]

    return render_template("index.html", ai_response=ai_response)

if __name__ == "__main__":
    app.run(debug=True)
