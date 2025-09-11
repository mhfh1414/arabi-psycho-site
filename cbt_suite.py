# -*- coding: utf-8 -*-
# home.py — واجهة رئيسية فخمة بأزرار دائرية ملونة

from flask import Flask, render_template_string
from cbt_suite import cbt_bp
from dsm_suite import dsm_bp
from addiction_suite import addiction_bp

app = Flask(__name__)

# تسجيل البلوبرنتات
app.register_blueprint(cbt_bp)
app.register_blueprint(dsm_bp)
app.register_blueprint(addiction_bp)

@app.route("/")
def index():
    return render_template_string("""
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>عربي سايكو | المنصة النفسية</title>
      <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
      <style>
        body {
          margin: 0;
          font-family: 'Tajawal', sans-serif;
          background: #f5f9ff;
          color: #222;
          text-align: center;
        }
        header {
          padding: 30px;
          background: linear-gradient(90deg, #1565c0, #42a5f5);
          color: white;
          border-bottom-left-radius: 30px;
          border-bottom-right-radius: 30px;
          box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        h1 {
          font-size: 2.5rem;
          margin-bottom: 10px;
        }
        p.tagline {
          font-size: 1.2rem;
          opacity: 0.95;
        }
        .buttons {
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          gap: 30px;
          padding: 50px 20px;
        }
        a.btn {
          width: 150px;
          height: 150px;
          border-radius: 50%;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          background: linear-gradient(145deg, #e3f2fd, #bbdefb);
          color: #0d47a1;
          font-size: 1.1rem;
          font-weight: bold;
          text-decoration: none;
          box-shadow: 0 6px 15px rgba(0,0,0,0.2);
          transition: all 0.3s ease-in-out;
        }
        a.btn:hover {
          transform: scale(1.08);
          background: linear-gradient(145deg, #bbdefb, #90caf9);
        }
        a.btn span.icon {
          font-size: 2.2rem;
          margin-bottom: 10px;
        }
        footer {
          margin-top: 40px;
          padding: 20px;
          font-size: 0.9rem;
          background: #e3f2fd;
          border-top: 1px solid #bbdefb;
        }
      </style>
    </head>
    <body>
      <header>
        <h1>🌟 عربي سايكو 🌟</h1>
        <p class="tagline">منصة نفسية متكاملة: تشخيص، علاج معرفي سلوكي، وخدمات الإدمان</p>
      </header>

      <div class="buttons">
        <a class="btn" href="/dsm"><span class="icon">📋</span> DSM</a>
        <a class="btn" href="/cbt"><span class="icon">🧠</span> CBT</a>
        <a class="btn" href="/addiction"><span class="icon">⚕️</span> الإدمان</a>
        <a class="btn" href="https://t.me/Mhfh1414" target="_blank"><span class="icon">✉️</span> تواصل</a>
      </div>

      <footer>
        © {{year}} عربي سايكو — منصة نفسية لكل المجتمع
      </footer>
    </body>
    </html>
    """, year=2025)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
