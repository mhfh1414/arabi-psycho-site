# -*- coding: utf-8 -*-
# واجهة رئيسية محسّنة لهوية "عربي سايكو"
from flask import Blueprint, render_template_string, redirect

home_bp = Blueprint("home", __name__)

HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | منصّة نفسية عربية</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg1:#0b3a75; --bg2:#0a65b0; --bg3:#091b33;
      --gold:#f4b400; --ink:#071321; --card:rgba(255,255,255,.07); --line:rgba(255,255,255,.16);
      --pill:#0f2f60; --text-2:#cfe0ff;
    }
    *{box-sizing:border-box}
    html,body{margin:0;height:100%;font-family:"Tajawal",system-ui}
    body{
      color:#fff;
      background:
        radial-gradient(1200px 700px at 100% -10%, #2b6fff22, transparent),
        linear-gradient(140deg,var(--bg1),var(--bg2) 55%, var(--bg3));
    }
    .wrap{max-width:1180px;margin:auto;padding:26px 16px}
    header{display:flex;align-items:center;justify-content:space-between;gap:14px}
    .brand{display:flex;align-items:center;gap:14px}
    .logo{
      width:70px;height:70px;border-radius:18px;background:#0d2c54;
      border:1px solid #ffffff2a;display:grid;place-items:center;box-shadow:0 10px 26px rgba(0,0,0,.35)
    }
    .logo svg{width:48px;height:48px}
    .title{margin:0;font-size:34px;letter-spacing:.4px}
    .subtitle{margin:.25rem 0 0;color:var(--text-2)}
    .pill{padding:8px 12px;border-radius:999px;background:var(--pill);border:1px solid #ffffff22;color:#fff;font-weight:700}
    .hero{
      margin:22px 0 20px;padding:22px;border:1px solid var(--line);border-radius:22px;background:var(--card)
    }
    .hero h2{margin:0 0 6px;font-size:28px}
    .hero p{margin:0;color:#d9e6ff}
    .cta{display:flex;flex-wrap:wrap;gap:14px;margin-top:16px}
    a.btn{
      display:inline-flex;align-items:center;justify-content:center;gap:10px;min-width:260px;
      text-decoration:none;font-weight:800;padding:14px 18px;border-radius:16px;border:1px solid #e7b000;
      color:#2b1b02;background:linear-gradient(180deg,#ffe07c,#f4b400);
      box-shadow:0 10px 24px rgba(244,180,0,.28);
      transition:transform .08s ease, box-shadow .2s ease;
    }
    a.btn:hover{transform:translateY(-2px);box-shadow:0 14px 28px rgba(244,180,0,.35)}
    .btn.outline{
      color:#fff;background:rgba(255,255,255,.08);border-color:#ffffff2a;box-shadow:none
    }
    .btn.outline:hover{background:rgba(255,255,255,.14)}
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:14px}
    @media(max-width:980px){.grid{grid-template-columns:1fr}}
    .card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px}
    .card h3{margin:0 0 6px}
    .feats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}
    @media(max-width:980px){.feats{grid-template-columns:1fr}}
    .feat{background:rgba(255,255,255,.06);border:1px solid var(--line);border-radius:14px;padding:12px}
    .feat b{display:block;margin-bottom:4px}
    footer{margin:26px 0 10px;color:#cfe0ff;opacity:.9;text-align:center}
    .icon{width:18px;height:18px}
    .links{display:flex;gap:10px;flex-wrap:wrap}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="brand">
        <div class="logo" aria-label="شعار عربي سايكو">
          <!-- شعار بسيط (SVG أحرف عربية) -->
          <svg viewBox="0 0 64 64" fill="#f4b400" aria-hidden="true">
            <circle cx="32" cy="32" r="28" fill="#0a2a57"/>
            <path d="M18 38q6-10 14-10t14 10q-6 8-14 8t-14-8Z" fill="#f4b400"/>
            <path d="M23 28q0-6 9-6t9 6" stroke="#f4b400" stroke-width="3" fill="none" stroke-linecap="round"/>
          </svg>
        </div>
        <div>
          <h1 class="title">عربي سايكو</h1>
          <p class="subtitle">خدمات نفسية متكاملة بالعربية: تشخيص مبدئي، اختبارات، علاج سلوكي معرفي</p>
        </div>
      </div>
      <div class="links">
        <span class="pill">خصوصية وسريّة</span>
        <a class="btn outline" href="/contact/telegram" title="تلجرام">
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M9.1 16.3 8.9 20c.4 0 .6-.2.9-.4l2.1-2 4.3 3.1c.8.5 1.4.3 1.6-.8l2.9-13.4c.3-1.2-.4-1.7-1.2-1.4L2.8 9.7c-1.1.4-1.1 1.1-.2 1.4l4.3 1.3 10-6.3c.5-.3.9-.1.5.2l-8.1 7Z"/></svg>
          تلجرام
        </a>
        <a class="btn outline" href="/contact/email" title="إيميل">
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5v2Z"/></svg>
          إيميل
        </a>
      </div>
    </header>

    <section class="hero">
      <h2>مرحباً بك 👋</h2>
      <p>ابدأ بالتشخيص المبدئي (DSM) أو اختبارات القلق والاكتئاب وغيرها، ثم احصل على خطة علاج سلوكي معرفي (CBT) مبسطة.</p>
      <div class="cta">
        <a class="btn" href="/dsm">📋 التشخيص + دراسة حالة (DSM)</a>
        <a class="btn" href="/cbt">🧪 الاختبارات + CBT</a>
        <a class="btn" href="/addiction">🚭 برنامج الإدمان والتعافي</a>
      </div>
    </section>

    <section class="feats">
      <div class="feat"><b>دقّة عملية</b>مطابقة كلمات عاميّة ومرادفات + مدة الأعراض + الأثر الوظيفي لإخراج تشخيص مرجّح واحد.</div>
      <div class="feat"><b>اختبارات معيارية</b>PHQ-9 للاكتئاب، GAD-7 للقلق، PCL-5 للصدمة… بنتائج فورية وتفسير مبسّط.</div>
      <div class="feat"><b>CBT خطوة بخطوة</b>تمارين أفكار/سلوك/تعرض، متابعة أسبوعية، وتوصيات عملية قابلة للتطبيق.</div>
    </section>

    <section class="grid">
      <div class="card">
        <h3>📖 DSM-5</h3>
        <p>تحليل الأعراض بالعربية (فصحى/عامية)، رصد “رايات حمراء”، ونتيجة مرجّحة واضحة قابلة للطباعة.</p>
        <a class="btn outline" href="/dsm">ابدأ التشخيص</a>
      </div>
      <div class="card">
        <h3>🧠 العلاج السلوكي المعرفي</h3>
        <p>مخططات سجلات أفكار، التعرض، جدول أنشطة ممتعة، وخطة أهداف أسبوعية.</p>
        <a class="btn outline" href="/cbt">انتقل إلى التمارين</a>
      </div>
      <div class="card">
        <h3>🚭 الإدمان</h3>
        <p>تقييم شدة التعاطي، محفّزات الانتكاس، وبناء خطة تعافٍ تدريجية مع روابط دعم.</p>
        <a class="btn outline" href="/addiction">ابدأ برنامج التعافي</a>
      </div>
    </section>

    <footer>© {{year}} عربي سايكو — أداة مساعدة لا تُغني عن التقييم السريري المباشر</footer>
  </div>
</body>
</html>
"""

@home_bp.route("/", methods=["GET"])
def home():
    import datetime
    return render_template_string(HOME_HTML, year=datetime.datetime.utcnow().year)

# تحويلات تواصل
@home_bp.route("/contact/telegram")
def contact_telegram():
    return redirect("https://t.me/USERNAME", code=302)

@home_bp.route("/contact/email")
def contact_email():
    return redirect("mailto:info@arabipsycho.com", code=302)
