# === Arabi Psycho - Royal Navy & Gold Theme ===
# Colors: Navy Blue + Shiny Gold
# File: site_app.py

from flask import Flask, render_template_string

app = Flask(__name__)

# صفحة رئيسية بواجهة أنيقة (كحلي + ذهبي)
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
            font-family: 'Tahoma', sans-serif;
            background: linear-gradient(135deg, #0a1a33, #001f3f);
            color: #FFD700;
            margin: 0;
            padding: 0;
            text-align: center;
        }
        header {
            padding: 40px;
            background-color: #001f3f;
            color: #FFD700;
            font-size: 32px;
            font-weight: bold;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.6);
        }
        .btn {
            display: inline-block;
            margin: 15px;
            padding: 15px 30px;
            border: 2px solid #FFD700;
            border-radius: 12px;
            background-color: transparent;
            color: #FFD700;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease-in-out;
        }
        .btn:hover {
            background-color: #FFD700;
            color: #001f3f;
            transform: scale(1.1);
        }
        footer {
            margin-top: 40px;
            padding: 20px;
            font-size: 14px;
            background-color: #0a1a33;
            color: #ccc;
        }
    </style>
</head>
<body>
    <header>🌟 عربي سايكو | Arabi Psycho 🌟</header>
    <h2>مرحباً بك في منصتك للصحة النفسية</h2>
    <p>ابدأ رحلتك مع اختبارات نفسية، DSM-5، العلاج السلوكي المعرفي (CBT)، وخدمات الدعم.</p>

    <div>
        <a href="#" class="btn">📘 DSM-5</a>
        <a href="#" class="btn">🧠 CBT</a>
        <a href="#" class="btn">📝 اختبارات</a>
        <a href="#" class="btn">❤️ الإدمان</a>
        <a href="#" class="btn">📞 التواصل</a>
    </div>

    <footer>
        جميع الحقوق محفوظة © 2025 - عربي سايكو  
    </footer>
</body>
</html>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
