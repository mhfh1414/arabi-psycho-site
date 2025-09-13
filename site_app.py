from flask import Flask
app = Flask(__name__)  # <-- لازم يكون اسم المتغيّر app

@app.route("/")
def home():
    return "شغال ✔"
