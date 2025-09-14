from flask import Flask, render_template_string

app = Flask(__name__)

# === Arabi Psycho - Royal Navy & Gold ===

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>عربي سايكو</title>
    <style>
        body {
            margin: 0;
            font-family: 'Cairo', sans-serif;
            background: linear-gradient(135deg, #001f3f, #003366);
            color: #f5f5f5;
            text-align: center;
        }
        header {
            background-color: #001a33;
            padding: 20px;
            color: gold;
            font-size: 28px;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0,0,0,0.5);
        }
        .container {
            margin: 40px auto;
            max-width: 900px;
            padding: 20px;
            background: rgba(0,0,0,0.4);
            border-radius: 20px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.6);
        }
        h1 {
            color: gold;
            margin-bottom: 20px;
        }
        p {
            font-size: 20px;
            line-height: 1.8;
            margin-bottom: 30px;
        }
        .btn {
            display: inline-block;
            margin: 12px;
            padding: 14px 28px;
            font-size: 18px;
            font-weight: bold;
            color: #001a33;
            background: gold;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            text-decoration: none;
        }
        .btn:hover {
            background: #ffcc00;
            transform: scale(1.05);
        }
        footer {
            margin-top: 50px;
            padding: 15px;
            font-size: 16px;
            background: #001a33;
            color: #f5f5f5;
            border-top: 2px solid gold;
        }
    </style>
</head>
<body>
    <header>🌟 عربي سايكو 🌟</header>
    <div class="container">
        <h1>مرحبا بك في عالم الراحة النفسية</h1>
        <p>من هنا تبدأ رحلتك نحو التوازن النفسي. تصفح أدلة DSM-5، جرب اختبارات شخصية، واطلع على برامج العلاج السلوكي المعرفي CBT.</p>
        <a href="/dsm" class="btn">DSM-5</a>
        <a href="/cbt" class="btn">العلاج السلوكي المعرفي</a>
        <a href="/tests" class="btn">الاختبارات النفسية</a>
        <a href="/addiction" class="btn">الإدمان وعلاجه</a>
        <a href="/contact" class="btn">تواصل معنا</a>
    </div>
    <footer>حقوق النشر © 2025 عربي سايكو | تصميم بلون كحلي وذهبي لامع</footer>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
