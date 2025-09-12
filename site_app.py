from flask import Flask, render_template_string

app = Flask(__name__)

# صفحة رئيسية
@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>عربي سايكو | المنصة النفسية</title>
        <style>
            body {
                font-family: 'Tahoma', sans-serif;
                background: linear-gradient(120deg, #74ebd5, #ACB6E5);
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #222;
                font-size: 36px;
                margin-bottom: 20px;
            }
            p {
                color: #333;
                font-size: 18px;
                margin-bottom: 40px;
            }
            .btn {
                display: inline-block;
                padding: 15px 25px;
                margin: 10px;
                font-size: 18px;
                border: none;
                border-radius: 12px;
                background-color: #007BFF;
                color: white;
                text-decoration: none;
                transition: 0.3s;
            }
            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>مرحباً بك في <span style="color:#007BFF;">عربي سايكو</span></h1>
        <p>منصة نفسية متكاملة لخدمة الأفراد في مجالات العلاج، الاختبارات، والتطوير.</p>
        
        <a href="/dsm" class="btn">اضطرابات DSM-5</a>
        <a href="/cbt" class="btn">العلاج السلوكي المعرفي CBT</a>
        <a href="/addiction" class="btn">علاج الإدمان</a>
    </body>
    </html>
    """)

# مسارات تجريبية
@app.route("/dsm")
def dsm():
    return "📘 هنا ستجد محتوى DSM-5"

@app.route("/cbt")
def cbt():
    return "🧠 هنا ستجد محتوى CBT"

@app.route("/addiction")
def addiction():
    return "🚭 هنا ستجد محتوى علاج الإدمان"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
