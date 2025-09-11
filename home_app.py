# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, url_for

app = Flask(__name__)

# =====================[ HTML BASE ]=====================
BASE_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    body {
      margin: 0;
      font-family: 'Tajawal', sans-serif;
      background: linear-gradient(135deg, #0b3a75, #0a65b0);
      color: #fff;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .container {
      text-align: center;
      max-width: 800px;
      padding: 20px;
    }
    h1 {
      font-size: 2.4rem;
      margin-bottom: 10px;
      color: #ffd86a;
      text-shadow: 1px 1px 3px #000;
    }
    p {
      font-size: 1.2rem;
      line-height: 1.8;
      margin-bottom: 30px;
    }
    .btn-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 15px;
    }
    a.btn {
      display: block;
      padding: 14px;
      font-size: 1.1rem;
      font-weight: bold;
      border-radius: 12px;
      text-decoration: none;
      background: linear-gradient(180deg,#ffd86a,#f4b400);
      color: #2b1b02;
      box-shadow: 0 4px 10px rgba(0,0,0,0.3);
      transition: 0.2s;
    }
    a.btn:hover {
      transform: scale(1.05);
      background: linear-gradient(180deg,#ffe699,#ffbb33);
    }
    footer {
      margin-top: 40px;
      font-size: 0.9rem;
      opacity: 0.8;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>💙 منصة عربي سايكو</h1>
    <p>
      خدمات نفسية متكاملة: <br>
      التشخيص حسب معايير DSM-5، العلاج السلوكي المعرفي (CBT)، <br>
      برامج الإدمان والتعافي، وأدوات طبية حديثة لدعم صحتك النفسية.
    </p>
    <div class="btn-grid">
      <a href="/dsm" class="btn">🧾 التشخيص ودراسة الحالة (DSM)</a>
      <a href="/cbt" class="btn">🧠 العلاج السلوكي المعرفي (CBT)</a>
      <a href="/addiction" class="btn">🚭 الإدمان والتعافي</a>
      <a href="https://t.me/Mhfh1414" target="_blank" class="btn">📲 تواصل مع الأخصائي</a>
    </div>
    <footer>© 2025 منصة عربي سايكو — الصحة النفسية أولويتنا</footer>
  </div>
</body>
</html>
"""

# =====================[ ROUTES ]=====================
@app.route("/")
def home():
    return render_template_string(BASE_HTML)

# =====================[ RUN LOCAL ]=====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
