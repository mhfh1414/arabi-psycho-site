from flask import Flask, render_template_string

app = Flask(__name__)

# HTML قالب الصفحة الرئيسية
HOME_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Arabi Psycho</title>
    <style>
        body {
            font-family: "Tahoma", sans-serif;
            background: linear-gradient(to right, #2c3e50, #3498db);
            color: white;
            text-align: center;
            padding: 50px;
        }
        h1 {
            font-size: 40px;
            margin-bottom: 10px;
        }
        p {
            font-size: 20px;
            margin-bottom: 40px;
        }
        .btn {
            display: inline-block;
            background: #e74c3c;
            color: white;
            padding: 15px 30px;
            margin: 10px;
            border-radius: 10px;
            font-size: 18px;
            text-decoration: none;
            transition: 0.3s;
        }
        .btn:hover {
            background: #c0392b;
        }
        footer {
            margin-top: 50px;
            font-size: 14px;
            color: #bdc3c7;
        }
    </style>
</head>
<body>
    <h1>مرحباً بك في Arabi Psycho</h1>
    <p>منصة متكاملة للاختبارات والتشخيص النفسي</p>

    <a href="/dsm" class="btn">📘 تشخيص DSM</a>
    <a href="/cbt" class="btn">🧠 العلاج المعرفي السلوكي CBT</a>
    <a href="/addiction" class="btn">🚭 علاج الإدمان</a>

    <footer>
        <p>برعاية البطل موسى الذكي 💡</p>
    </footer>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_PAGE)

# صفحات فرعية للتجربة (يمكنك ربطها بالملفات)
@app.route("/dsm")
def dsm_page():
    return "<h2>📘 صفحة DSM شغالة</h2>"

@app.route("/cbt")
def cbt_page():
    return "<h2>🧠 صفحة CBT شغالة</h2>"

@app.route("/addiction")
def addiction_page():
    return "<h2>🚭 صفحة علاج الإدمان شغالة</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
