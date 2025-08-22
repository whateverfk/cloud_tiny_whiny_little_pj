from urllib import response
from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv
from pdf_reader import auto_correct
from flask import Flask, render_template, request, redirect, url_for
from model import db, User, History
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
class FlaskApp:
    def __init__(self):
        load_dotenv()
        self.app = Flask(__name__)
        #self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///app.db")
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
        db.init_app(self.app)
        login_manager = LoginManager()
        login_manager.init_app(self.app)
        login_manager.user_loader(self.load_user)
        self.API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

        self.setup_routes()

    def load_user(self, user_id):
        return User.query.get(int(user_id))


    def setup_routes(self):
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            ai_response = ""
            user_input = ""
            file_upload =""  
            history_id = request.form.get("history_id")
            
            if request.method == "POST":
                
                user_input = request.form.get("user_input", "")
                language = request.form.get("language", "vi")
                style = request.form.get("style", "basic")
                translate = request.form.get("translate")
                uploaded_file = request.files.get("text_files")


                if uploaded_file:
                    file_upload = auto_correct(uploaded_file)
                    user_input += file_upload

                if not uploaded_file and not user_input and not history_id:
                    return render_template("index.html", ai_response="Không có gì xử lý cả, đừng ấn bừa nhé! :V  ")
                elif history_id and not user_input:
                    history = History.query.filter_by(id=history_id, user_id=current_user.id).first()
                    if history:
                        ai_response = history.content
                        histories = History.query.filter_by(user_id=current_user.id).order_by(History.timestamp.desc()).limit(10).all()
                    return render_template("index.html", ai_response=ai_response, histories=histories)

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


                response = requests.post(self.OPENROUTER_API_URL, json=payload, headers=headers)
                try:
                    response_json = response.json()
                except Exception as e:
                    ai_response = f"Hãy thử lại vì API không trả về JSON hợp lệ: {e}\nNội dung: {response.text}"

                else:
                    if response.ok:
                        if response.status_code == 200:
                            data = response.json()
                        if "choices" in data:
                            ai_response = response.json()["choices"][0]["message"]["content"]
                        else:
                            ai_response = "Phản hồi không hợp lệ từ API."
                        # Lưu lịch sử nếu người dùng đã đăng nhập
                        if current_user.is_authenticated:
                            existing = History.query.filter_by(user_id=current_user.id, content=ai_response).first()
                            if not existing:
                                history = History(user_id=current_user.id, content=ai_response)
                                db.session.add(history)
                                db.session.commit()
                    else:
                        ai_response = f" thử lại vì API Error: {response_json.get('error', {}).get('message', 'Unknown error')}"



            histories = []
            if current_user.is_authenticated:
                histories = History.query.filter_by(user_id=current_user.id).order_by(History.timestamp.desc()).limit(10).all()
            return render_template("index.html", ai_response=ai_response , histories=histories)
            #return render_template("index.html", file_upload=file_upload, ai_response=ai_response if user_input else "                   Chúc mừng đoạn trắng tinh của bạn không sai gì cả / Congratulations, your NOTHING have nothing wrong with it"  )

        @self.app.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                username = request.form["username"]
                password = request.form["password"]
                user = User.query.filter_by(username=username).first()
                if user and check_password_hash(user.password, password):
                    login_user(user)
                    return redirect("/")
                return render_template("login.html", error="Sai thông tin đăng nhập")
            return render_template("login.html")

        @self.app.route("/register", methods=["GET", "POST"])
        def register():
            if request.method == "POST":
                username = request.form["username"]
                password = generate_password_hash(request.form["password"])
                if User.query.filter_by(username=username).first():
                    return render_template("register.html", error="Tên người dùng đã tồn tại")
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect("/")
            return render_template("register.html")

        @self.app.route("/logout")
        @login_required
        def logout():
            logout_user()
            return redirect("/")

        @self.app.route("/delete_history", methods=["POST"])
        @login_required
        def delete_history():
            history_id = request.form.get("history_id")
            history = History.query.filter_by(id=history_id, user_id=current_user.id).first()
            if history:
                db.session.delete(history)
                db.session.commit()
            return redirect("/")


    def get_app(self):
        return self.app
app = FlaskApp().get_app()
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
