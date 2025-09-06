# -*- coding: utf-8 -*-
from flask import url_for, render_template_string

# عدّل الروابط كما يناسبك
WA_LINK = "https://wa.me/9665XXXXXXXX"       # رقم واتساب دولي
TG_LINK = "https://t.me/USERNAME"            # يوزر تيليجرام
EMAIL_LINK = "mailto:info@arabipsycho.com"   # بريدك

def render_home():
    html = """
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
      <meta charset="utf-8">
      <title>عربي سايكو | الرئيسية</title>
      <meta name="viewport" content="width=device-width, initial-scale=1"/>
      <style>
        body{margin:0;font-family:"Tajawal",system-ui,Segoe UI,Arial;-webkit-font-smoothing:antialiased;
             background:radial-gradient(1200px 600px at 80% -10%, #1a4bbd22, transparent),
             linear-gradient(135deg,#0b3b78 0%,#08244a 60%, #061a34 100%);color:#fff}
        .wrap{max-width:1100px;margin:auto;padding:28px}
        header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
        .brand{display:flex;gap:12px;align-items:center}
        .brand h1{margin:0;font-size:28px}
        .brand small{color:#cfe0ff}
        .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
        @media(max-width:900px){.grid{grid-template-columns:1fr}}
        .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px;backdrop-filter:blur(6px)}
        a.btn{display:inline-block;background:#f4b400;color:#2b1b02;border-radius:14px;padding:12px 16px;font-weight:800;text-decoration:none}
        .links a{display:inline-block;margin-inline:6px;color:#ffe28a;text-decoration:none}
        .hero{margin:18px 0 24px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.15);border-radius:18px;padding:20px}
      </style>
    </head>
    <body>
      <div class="wrap">
        <header>
          <div class="brand">
            <img src="https://dummyimage.com/44x44/0b3b78/ffffff&text=AS" alt="Arabipsycho" width="44" height="44" style="border-radius:10px;border:1px solid #ffffff33"/>
            <div>
              <h1>عربي سايكو</h1>
              <small>مركز عربي سايكو يرحب بكم — نخدمك أينما كنت</small>
            </div>
          </div>
          <div class="links">
            <a href="{{ url_for('contact_whatsapp') }}">واتساب</a> •
            <a href="{{ url_for('contact_telegram') }}">تلجرام</a> •
            <a href="{{ url_for('contact_email') }}">إيميل</a>
          </div>
        </header>

        <section class="hero">
          <p style="margin:0 0 12px">ابدأ هنا:</p>
          <a class="btn" href="{{ url_for('dsm') }}">🗂️ دراسة حالة + تشخيص (DSM)</a>
          <a class="btn" href="{{ url_for('cbt') }}">💡 العلاج السلوكي المعرفي + الاختبارات</a>
          <a class="btn" href="{{ url_for('addiction') }}">🚭 علاج الإدمان</a>
        </section>

        <div class="grid">
          <div class="card">
            <h3>📖 DSM-5</h3>
            <p>قائمة اضطرابات + مطابقة كلمات لتشخيص مبدئي فوري.</p>
            <a class="btn" href="{{ url_for('dsm') }}">ابدأ الآن</a>
          </div>
          <div class="card">
            <h3>🧪 الاختبارات</h3>
            <p>PHQ-9 | GAD-7 | PCL-5 | BDI-II | Big Five وغيرها.</p>
            <a class="btn" href="{{ url_for('cbt') }}">افتح لوحة الاختبارات</a>
          </div>
          <div class="card">
            <h3>🚭 الإدمان</h3>
            <p>تقييم أولي ومسارات علاجية وإحالة عند الحاجة.</p>
            <a class="btn" href="{{ url_for('addiction') }}">ابدأ التقييم</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    return render_template_string(html)
