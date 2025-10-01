# app.py — Flask web (Purple/Gold)
import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>عربي سايكو — واجهة بنفسجي وذهبي</title>
  <style>
    :root{
      --purple:#4B0082;   /* البنفسجي */
      --gold:#FFD700;     /* الذهبي */
      --white:#ffffff;
    }
    body{
      margin:0;
      min-height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      background:var(--purple);
      font-family:"Tajawal","Segoe UI",system-ui,sans-serif;
      color:var(--white);
    }
    .card{
      background:var(--gold);
      color:var(--purple);
      padding:40px 60px;
      border-radius:20px;
      box-shadow:0 8px 25px rgba(0,0,0,0.3);
      text-align:center;
    }
    .card h1{margin:0 0 10px; font-size:2rem}
    .btn{
      display:inline-block; margin-top:14px; padding:12px 18px;
      border-radius:14px; background:var(--purple); color:var(--white);
      text-decoration:none; font-weight:700;
    }
    .btn:hover{opacity:0.85}
  </style>
</head>
<body>
  <main class="card">
    <h1>مرحباً بك في عربي سايكو</h1>
    <p>واجهة بسيطة بلون بنفسجي × ذهبي.</p>
    <a class="btn" href="/">ابدأ الآن</a>
  </main>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(HTML)

@app.get("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
