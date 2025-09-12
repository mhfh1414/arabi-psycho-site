# -*- coding: utf-8 -*-
# site.py — ملف التشغيل الرئيسي لموقع عربي سايكو

from flask import Flask, render_template_string, redirect

app = Flask(__name__)

HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | منصة الصحة النفسية</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body {
      margin:0; font-family:'Tajawal',sans-serif;
      background: linear-gradient(135deg,#0a3a75,#0a65b0);
      color:#fff; line-height:1.6;
    }
    header {
      display:flex; justify-content:space-between; align-items:center;
      padding:20px; background:rgba(0,0,0,0.4);
      border-bottom:2px solid #f4b400;
    }
    .logo { font-size:28px; font-weight:900; color:#f4b400; }
    .privacy { font-size:14px; color:#cfe0ff; font-weight:600; }
    .hero {
      text-align:center; padding:60px 20px;
    }
    .hero h1 { font-size:3rem; margin-bottom:20px; }
    .hero p { font-size:1.2rem; color:#cfe0ff; }
    .cards {
      display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
      gap:20px; max-width:1200px; margin:40px auto; padding:20px;
    }
    .card {
      background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.2);
      border-radius:16px; padding:20px; text-align:center;
      transition:0.3s;
    }
    .card:hover { transform:translateY(-5px); box-shadow:0 8px 20px rgba(0,0,0,0.4); }
    .card i { font-size:40px; color:#f4b400; margin-bottom:15px; }
    .card h3 { margin-bottom:10px; }
    .btn {
      display:inline-block; margin-top:15px; padding:12px 20px;
      background:linear-gradient(145deg,#ffd86a,#f4b400); color:#2b1b02;
      border-radius:12px; font-weight:700; text-decoration:none;
    }
    footer {
      text-align:center; padding:20px; background:rgba(0,0,0,0.5);
      margin-top:40px; font-size:14px; color:#cfe0ff;
    }
  </style>
</head>
<body>
  <header>
    <div class="logo">💛 عربي سايكو</div>
    <div class="privacy">🔒 خصوصية وسرية تامة</div>
  </header>

  <section class="hero">
    <h1>منصة عربي سايكو للصحة النفسية</h1>
    <p>هنا تجد التشخيص الدقيق (DSM)، العلاج السلوكي المعرفي (CBT)، وخدمات علاج الإدمان<br>
    ✨ نرافقك في رحلة التعافي بخبرة واحترافية</p>
  </section>

  <section class="cards">
    <div class="card">
      <i class="fas fa-brain"></i>
      <h3>التشخيص وفق DSM</h3>
      <p>إدخال دراسة الحالة وتحليل الأعراض لإصدار التشخيص المرجّح بدقة.</p>
      <a class="btn" href="/dsm">ابدأ التشخيص</a>
    </div>
    <div class="card">
      <i class="fas fa-clipboard-check"></i>
      <h3>العلاج السلوكي المعرفي CBT</h3>
      <p>اختبارات مقننة + أدوات CBT عملية: سجل الأفكار، التنشيط السلوكي، خطة جلسات.</p>
      <a class="btn" href="/cbt">ادخل إلى لوحة CBT</a>
    </div>
    <div class="card">
      <i class="fas fa-prescription-bottle-alt"></i>
      <h3>علاج الإدمان</h3>
      <p>برامج تقييم وتأهيل شاملة مع خطط فردية للتعافي المستدام.</p>
      <a class="btn" href="/addiction">ابدأ التقييم</a>
    </div>
    <div class="card">
      <i class="fas fa-headset"></i>
      <h3>تواصل معنا</h3>
      <p>اختر وسيلة التواصل المناسبة: واتساب، تلجرام، أو البريد الإلكتروني.</p>
      <a class="btn" href="/contact">خيارات التواصل</a>
    </div>
  </section>

  <footer>
    © {{year}} عربي سايكو — منصة نفسية تخدم الجميع باحترافية
  </footer>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML, year=2025)

@app.route("/dsm")
def dsm_redirect():
    return redirect("/dsm")  # DSM blueprint لازم يكون مسجل

@app.route("/cbt")
def cbt_redirect():
    return redirect("/cbt")

@app.route("/addiction")
def addiction_redirect():
    return redirect("/addiction")

@app.route("/contact")
def contact_redirect():
    return redirect("https://wa.me/9665XXXXXXX")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
