# -*- coding: utf-8 -*-
from flask import url_for, render_template_string

# عدّل الروابط كما يناسبك
WA_LINK = "https://wa.me/9665XXXXXXXX"        # رقم واتساب دولي
TG_LINK = "https://t.me/USERNAME"             # يوزر تيليجرام
EMAIL_LINK = "mailto:info@arabipsycho.com"    # بريدك

def render_home():
    html = """
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
      <meta charset="utf-8">
      <title>عربي سايكو | الرئيسية</title>
      <meta name="viewport" content="width=device-width, initial-scale=1"/>
      <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
      <style>
        :root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400;--white:#fff}
        *{box-sizing:border-box}
        body{margin:0;font-family:"Tajawal",system-ui;-webkit-font-smoothing:antialiased;
             background:
              radial-gradient(900px 480px at 85% -10%, #1a4bbd22, transparent),
              linear-gradient(135deg,var(--bg1),var(--bg2)); color:var(--white)}
        .wrap{max-width:1200px;margin:auto;padding:28px}
        header{display:flex;align-items:center;justify-content:space-between;gap:16px}
        .brand{display:flex;align-items:center;gap:14px}
        .badge{width:52px;height:52px;border-radius:14px;background:#0d2c54;border:1px solid #ffffff33;display:grid;place-items:center;font-weight:800}
        .title{margin:0;font-size:30px}
        .subtitle{margin:0;color:#cfe0ff}
        .actions a{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-weight:800;
                   padding:10px 14px;border-radius:12px;border:1px solid #ffffff22;background:rgba(255,255,255,.06);color:#fff}
        .actions a:hover{background:rgba(255,255,255,.12)}
        .hero{margin:24px 0;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.15);border-radius:18px;padding:24px}
        .btn{display:inline-flex;align-items:center;gap:10px;background:var(--gold);color:#2b1b02;border-radius:14px;padding:14px 18px;text-decoration:none;font-weight:800}
        .btn:hover{filter:brightness(1.05)}
        .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
        @media(max-width:980px){.grid{grid-template-columns:1fr}}
        .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px;backdrop-filter:blur(6px)}
        .card h3{margin:0 0 6px}
        .card p{margin:0 0 12px;color:#dbe9ff}
        .card a{display:inline-flex;align-items:center;gap:8px}
      </style>
    </head>
    <body>
      <div class="wrap">
        <header>
          <div class="brand">
            <div class="badge">AS</div>
            <div>
              <h1 class="title">عربي سايكو</h1>
              <p class="subtitle">مركز عربي سايكو يرحّب بكم — نخدمك أينما كنت</p>
            </div>
          </div>
          <nav class="actions">
            <a href="{{ url_for('contact_whatsapp') }}">💬 واتساب</a>
            <a href="{{ url_for('contact_telegram') }}">📨 تلجرام</a>
            <a href="{{ url_for('contact_email') }}">✉️ إيميل</a>
          </nav>
        </header>

        <section class="hero">
          <p style="margin:0 0 12px">ابدأ من هنا:</p>
          <div style="display:flex;flex-wrap:wrap;gap:12px">
            <a class="btn" href="{{ url_for('dsm') }}">🗂️ دراسة الحالة + التشخيص (DSM)</a>
            <a class="btn" href="{{ url_for('cbt') }}">💡 العلاج السلوكي المعرفي + الاختبارات</a>
            <a class="btn" href="{{ url_for('addiction') }}">🚭 علاج الإدمان</a>
          </div>
        </section>

        <section class="grid">
          <div class="card">
            <h3>📖 DSM-5</h3>
            <p>قائمة اضطرابات موسّعة + مطابقة كلمات لنتيجة تقديرية فورية.</p>
            <a class="btn" href="{{ url_for('dsm') }}">ابدأ الآن</a>
          </div>
          <div class="card">
            <h3>🧪 الاختبارات</h3>
            <p>PHQ-9 | GAD-7 | PCL-5 | Big Five وغيرها — تُربط بـ CBT.</p>
            <a class="btn" href="{{ url_for('cbt') }}">افتح لوحة الاختبارات</a>
          </div>
          <div class="card">
            <h3>🚭 الإدمان</h3>
            <p>تقييم أولي، خطة علاجية، وإحالة عند الحاجة.</p>
            <a class="btn" href="{{ url_for('addiction') }}">ابدأ التقييم</a>
          </div>
        </section>
      </div>
    </body>
    </html>
    """
    return render_template_string(html)
