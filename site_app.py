# === Arabi Psycho - Royal Navy & Gold ===
import json
import os

app = Flask(__name__)

# === Arabi Psycho - Royal Navy & Gold ===
# Colors: Navy Blue + Shiny Gold
# File: site_app.py

# تحميل ملف DSM كامل
def load_dsm():
    try:
        with open(os.path.join("data", "dsm_rules.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return """
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <title>عربي سايكو</title>
        <style>
            body {
                background-color: #0a0f2c; /* كحلي */
                color: #FFD700; /* ذهبي */
                font-family: 'Tahoma', sans-serif;
                text-align: center;
                padding: 50px;
            }
            h1 {
                font-size: 36px;
                margin-bottom: 20px;
            }
            p {
                font-size: 20px;
                margin-bottom: 30px;
            }
            a.button {
                background: #FFD700;
                color: #0a0f2c;
                padding: 15px 25px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 10px;
                margin: 10px;
                display: inline-block;
            }
            a.button:hover {
                background: #e6c200;
            }
        </style>
    </head>
    <body>
        <h1>🌟 عربي سايكو 🌟</h1>
        <p>مرحبًا بك في منصتك للصحة النفسية والدعم المتكامل</p>
        <a class="button" href="/dsm">📘 DSM-5</a>
        <a class="button" href="/about">ℹ️ عن الموقع</a>
    </body>
    </html>
    """

@app.route("/about")
def about():
    return "<h2>ℹ️ هذا الموقع يهدف لتقديم أدوات نفسية، اختبارات، وملفات DSM بلغة عربية ميسّرة.</h2>"

@app.route("/dsm")
def dsm():
    rules = load_dsm()
    return jsonify(rules)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
