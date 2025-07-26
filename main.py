from app import FlaskApp

app_instance = FlaskApp()
app = app_instance.get_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)

