# -*- coding: utf-8 -*-
# واجهة الموقع الرئيسية (هوم) + روابط تواصل
from flask import Blueprint, render_template_string, redirect

home_bp = Blueprint("home", __name__)

HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | المنصّة</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg1:#0b3a75; --bg2:#0a65b0; --ink:#091b33;
      --gold:#f4b400; --card:rgba(255,255,255,.08); --line:rgba(255,255,255,.18);
    }
    *{box-sizing:border-box}
    body{
      margin:0; font-family:"Tajawal", system-ui; color:#fff;
      background:
        radial-gradient(1200px 600px at 90% -10%, #1a4bbd22, transparent),
        linear-gradient(135deg,var(--bg1),var(--bg2)) fixed;
    }
    .wrap{max-width:1200px;margin:auto;padding:28px 16px}
    header{display:flex;align-items:center;justify-content:space-between;gap:16px}
    .brand{display:flex;align-items:center;gap:14px}
    .badge{width:60px;height:60px;border-radius:16px;background:#0d2c54;border:1px solid #ffffff33;display:grid;place-items:center;font-weight:800;box-shadow:0 8px 24px rgba(0,0,0,.25)}
    .title{margin:0;font-size:34px;letter-spacing:.5px}
    .subtitle{margin:.25rem 0 0;color:#cfe0ff}
    .hero{margin:22px 0 26px;padding:22px;border:1px solid var(--line);border-radius:18px;background:var(--card)}
    .cta{display:flex;flex-wrap:wrap;gap:14px}
    a.btn{
      display:inline-flex;align-items:center;gap:10px;text-decoration:none;
      background:linear-gradient(180deg,#ffd86a,#f4b400); color:#2b1b02;
      padding:14px 18px;border-radius:14px;font-weight:800;
      box-shadow:0 6px 18px rgba(244,180,0,.28); border:1px solid #e7b000;
      min-width:240px; justify-content:center;
    }
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
    @media(max-width:980px){.grid{grid-template-columns:1fr}}
    .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px}
    .card h3{margin:0 0 6px}
    footer{margin:28px 0 10px;color:#cfe0ff;opacity:.9;text-align:center}
    .icon{width:18px;height:18px}
    .ghost{background:rgba(255,255,255,.08); color:#fff; border:1px solid #ffffff22}
    .ghost:hover{background:rgba(255,255,255,.14)}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="brand">
        <div class="badge">AS</div>
        <div>
          <h1 class="title">عربي سايكو</h1>
          <p class="subtitle">منصّة نفسية عربية: تشخيص مبدئي، اختبارات، علاج سلوكي معرفي</p>
        </div>
      </div>
      <nav class="cta">
        <a class="ghost btn" href="/contact/telegram" title="تلجرام">
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M9.1 16.3 8.9 20c.4 0 .6-.2.9-.4l2.1-2 4.3 3.1c.8.5 1.4.3 1.6-.8l2.9-13.4c.3-1.2-.4-1.7-1.2-1.4L2.8 9.7c-1.1.4-1.1 1.1-.2 1.4l4.3 1.3 10-6.3c.5-.3.9-.1.5.2l-8.1 7Z"/></svg>
          تلجرام
        </a>
        <a class="ghost btn" href="/contact/email" title="إيميل">
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5v2Z"/></svg>
          إيميل
        </a>
      </nav>
    </header>

    <section class="hero">
      <div class="cta">
        <a class="btn" href="/dsm">📋 التشخيص + دراسة حالة (DSM)</a>
        <a class="btn" href="/cbt">🧠 العلاج السلوكي المعرفي + اختبارات</a>
        <a class="btn" href="/addiction">🚭 برنامج الإدمان والتعافي</a>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h3>📖 DSM-5</h3>
        <p>مطابقة أعراض دقيقة مع مرادفات عاميّة، تشخيص مرجّح واحد، وتوثيق دراسة الحالة.</p>
        <a class="ghost btn" href="/dsm">ابدأ الآن</a>
      </div>
      <div class="card">
        <h3>🧪 الاختبارات + CBT</h3>
        <p>حزم اختبارات (PHQ-9 / GAD-7 / PCL-5 …) مع توصيات علاج سلوكي معرفي.</p>
        <a class="ghost btn" href="/cbt">افتح الحزمة</a>
      </div>
      <div class="card">
        <h3>🚭 الإدمان</h3>
        <p>تقييم أولي، شدة التعاطي، خطة تعافي تدريجية وربط بخدمات الدعم.</p>
        <a class="ghost btn" href="/addiction">ادخل البرنامج</a>
      </div>
    </section>

    <footer>© {{year}} عربي سايكو — أداة مساعدة لا تغني عن التقييم السريري</footer>
  </div>
</body>
</html>
"""

@home_bp.route("/", methods=["GET"])
def home():
    import datetime
    return render_template_string(HOME_HTML, year=datetime.datetime.utcnow().year)

# روابط تواصل بسيطة (تحويل)
@home_bp.route("/contact/telegram")
def contact_telegram():
    return redirect("https://t.me/USERNAME", code=302)

@home_bp.route("/contact/email")
def contact_email():
    return redirect("mailto:info@arabipsycho.com", code=302)
