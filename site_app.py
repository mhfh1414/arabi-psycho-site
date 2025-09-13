# === Arabi Psycho - Royal Navy & Gold Theme ===
# Colors: Navy Blue + Shiny Gold
# File: site_app.py

from flask import Flask, render_template_string

app = Flask(__name__)

# ======================
# الصفحة الرئيسية
# ======================
@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>عربي سايكو</title>
    <style>
        body {
            margin: 0;
            font-family: "Cairo", sans-serif;
            background: linear-gradient(to right, #0a0f2c, #1b1f3a);
            color: #f5d76e;
            text-align: center;
        }
        header {
            padding: 25px;
            background: #0a0f2c;
            color: #f5d76e;
            font-size: 28px;
            font-weight: bold;
            letter-spacing: 1px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.6);
        }
        .btn {
            display: inline-block;
            margin: 12px;
            padding: 14px 28px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            border: 2px solid #f5d76e;
            background: transparent;
            color: #f5d76e;
            transition: 0.3s;
        }
        .btn:hover {
            background: #f5d76e;
            color: #0a0f2c;
            cursor: pointer;
            transform: scale(1.1);
            box-shadow: 0 0 15px #f5d76e;
        }
        section {
            padding: 40px;
        }
        footer {
            background: #0a0f2c;
            padding: 15px;
            font-size: 14px;
            color: #f5d76e;
            margin-top: 50px;
            box-shadow: 0 -2px 15px rgba(0,0,0,0.6);
        }
    </style>
</head>
<body>
    <header>🌟 عربي سايكو | راحتك النفسية تبدأ من هنا 🌟</header>

    <section>
        <h2>اختر خدمتك</h2>
        <a class="btn" href="/dsm">DSM-5</a>
        <a class="btn" href="/cbt">العلاج السلوكي CBT</a>
        <a class="btn" href="/tests">اختبارات نفسية</a>
        <a class="btn" href="/contact">تواصل معنا</a>
    </section>

    <footer>
        ⓒ 2025 Arabi Psycho | Navy & Gold Edition
    </footer>
</body>
</html>
    """)

# ======================
# تشغيل التطبيق
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
