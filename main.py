from app import FlaskApp
from model import db, User, History
app_instance = FlaskApp()
app = app_instance.get_app()
with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)

