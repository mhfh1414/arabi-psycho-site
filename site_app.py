from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1 style='text-align:center; color:blue;'>مرحباً بك في موقع Arabi Psycho 🌿</h1><p style='text-align:center;'>الموقع شغال بنجاح 🚀</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
