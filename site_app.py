# --- Arabi Psycho - Royal Navy & Gold ---
# واجهة الموقع الأساسية

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>عربي سايكو</title>
        <style>
            body {
                font-family: 'Tahoma', sans-serif;
                background: linear-gradient(135deg, #0a0f3c, #1a237e);
                color: #ffd700;
                text-align: center;
                padding: 50px;
            }
            h1 {
                font-size: 48px;
                margin-bottom: 20px;
                text-shadow: 2px 2px 8px #000;
            }
            p {
                font-size: 22px;
                margin-bottom: 40px;
            }
            .btn {
                display: inline-block;
                background: #ffd700;
                color: #0a0f3c;
                padding: 15px 30px;
                margin: 10px;
                border-radius: 10px;
                text-decoration: none;
                font-size: 20px;
                font-weight: bold;
                transition: 0.3s;
            }
            .btn:hover {
                background: #fff176;
                transform: scale(1.1);
            }
        </style>
    </head>
    <body>
        <h1>🌟 عربي سايكو 🌟</h1>
        <p>الراحة النفسية تبدأ من هنا</p>
        <a href="/dsm" class="btn">DSM-5</a>
        <a href="/cbt" class="btn">العلاج السلوكي المعرفي CBT</a>
        <a href="/tests" class="btn">الاختبارات النفسية</a>
        <a href="/contact" class="btn">تواصل معنا</a>
    </body>
    </html>
    """

@app.route("/dsm")
def dsm():
    return "<h2>📘 DSM-5</h2><p>هنا سيتم ربط قاعدة بيانات DSM للمساعدة في التشخيص.</p>"

@app.route("/cbt")
def cbt():
    return "<h2>🧠 العلاج السلوكي المعرفي CBT</h2><p>تمارين وأدوات لمساعدة العميل على التغيير.</p>"

@app.route("/tests")
def tests():
    return "<h2>📝 الاختبارات النفسية</h2><p>مجموعة من الاختبارات النفسية المخصصة.</p>"

@app.route("/contact")
def contact():
    return "<h2>☎️ تواصل معنا</h2><p>يمكنك التواصل مع معالجك النفسي من هنا.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
