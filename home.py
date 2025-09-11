# -*- coding: utf-8 -*-
# home.py — واجهة "عربي سايكو" فخمة (Blueprint مستقل)

from __future__ import annotations
from flask import Blueprint, render_template_string
from datetime import datetime

home_bp = Blueprint("home", __name__)

def _year():
    try:
        return datetime.now().year
    except:
        return 2025

HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | منصة نفسية تخدم الجميع</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="description" content="عربي سايكو — منصة عربية للصحة النفسية: دراسة الحالة + التشخيص DSM، العلاج السلوكي المعرفي CBT، وعلاج الإدمان.">
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{
      --blue1:#081b3f; --blue2:#0b3a75; --blue3:#0a65b0;
      --gold:#f4b400;  --gold2:#ffd86a; --ink:#0d1326;
      --glass:rgba(255,255,255,.10); --glass2:rgba(255,255,255,.16); --w:#fff;
    }
    *{box-sizing:border-box}
    body{
      margin:0; font-family:"Tajawal",system-ui,sans-serif; color:var(--w);
      background:
        radial-gradient(1100px 600px at 90% -10%, #1a4bbd22, transparent),
        linear-gradient(135deg,var(--blue2),var(--blue3));
      background-attachment: fixed;
    }
    .wrap{max-width:1280px;margin:0 auto;padding:18px 18px 36px}
    /* ——— هيدر ——— */
    header{
      position:sticky; top:0; z-index:50; backdrop-filter: blur(10px);
      background: linear-gradient(0deg, rgba(0,0,0,.0), rgba(0,0,0,.18));
      border-bottom:1px solid #ffffff22;
    }
    .bar{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:14px 0}
    .brand{display:flex;align-items:center;gap:14px}
    .logo{
      width:64px;height:64px;border-radius:18px;display:grid;place-items:center;
      background:linear-gradient(145deg,var(--blue1),var(--blue2));
      border:1px solid #ffffff22; box-shadow:0 10px 28px rgba(0,0,0,.28)
    }
    .logo svg{width:34px;height:34px;fill:var(--gold)}
    .title{margin:0; font-size:28px; background:linear-gradient(90deg,var(--gold2),var(--gold));
      -webkit-background-clip:text; -webkit-text-fill-color:transparent}
    .subtitle{margin:2px 0 0; color:#cfe0ff; font-size:14px}
    .privacy{
      display:flex; gap:8px; flex-wrap:wrap; align-items:center; margin-top:6px
    }
    .chip{
      display:inline-flex; align-items:center; gap:8px; padding:6px 10px; border-radius:999px;
      background:var(--glass); border:1px solid var(--glass2); font-size:12px
    }
    .chip svg{width:16px;height:16px}
    /* ——— هيرو ——— */
    .hero{
      display:grid; grid-template-columns: 1.2fr .8fr; gap:22px; margin-top:18px
    }
    @media(max-width:980px){ .hero{grid-template-columns:1fr} }
    .panel{
      background:var(--glass); border:1px solid var(--glass2); border-radius:22px; padding:22px;
      backdrop-filter: blur(6px); box-shadow:0 18px 42px rgba(0,0,0,.22)
    }
    .hero h1{margin:0 0 10px; font-size:40px}
    .hero p{margin:0 0 18px; color:#e6efff; line-height:1.7}
    .cta{display:flex; flex-wrap:wrap; gap:12px}
    .btn{
      text-decoration:none; display:inline-flex; align-items:center; gap:10px;
      padding:14px 18px; border-radius:14px; font-weight:800; transition: .2s transform
    }
    .btn:hover{transform: translateY(-2px)}
    .btn-gold{background: linear-gradient(180deg,var(--gold2),var(--gold)); color:#2b1b02; box-shadow:0 8px 24px rgba(244,180,0,.28)}
    .btn-blue{background: linear-gradient(145deg,#a8cbff,#6aa8ff); color:#081b3f; box-shadow:0 8px 24px rgba(80,140,255,.28)}
    /* ——— بطاقات الخدمات ——— */
    .grid{display:grid; grid-template-columns: repeat(3,1fr); gap:18px; margin-top:22px}
    @media(max-width:1200px){ .grid{grid-template-columns:repeat(2,1fr)} }
    @media(max-width:820px){ .grid{grid-template-columns:1fr} }
    .card{
      background:var(--glass); border:1px solid var(--glass2); border-radius:20px; padding:20px; height:100%;
      display:flex; flex-direction:column; gap:10px; transition:.25s transform,.25s box-shadow
    }
    .card:hover{ transform: translateY(-6px); box-shadow:0 16px 40px rgba(0,0,0,.24) }
    .icon{
      width:56px; height:56px; border-radius:14px; display:grid; place-items:center;
      background:linear-gradient(145deg,var(--blue1),var(--blue2)); border:1px solid #ffffff22
    }
    .icon span{font-size:26px}
    .card h3{margin:6px 0 0; font-size:20px}
    .card p{margin:0 0 8px; color:#dfeaff}
    .card .line{height:1px; background:#ffffff1e; margin:6px 0}
    /* ——— فوتر ——— */
    footer{margin-top:26px; padding-top:18px; border-top:1px solid #ffffff22; color:#cfe0ff; font-size:14px}
    .links{display:flex; gap:10px; flex-wrap:wrap}
    .sm{
      text-decoration:none; display:inline-flex; align-items:center; gap:8px; padding:10px 12px;
      background:var(--glass); border:1px solid var(--glass2); border-radius:12px; color:#fff
    }
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <div class="bar">
        <div class="brand">
          <div class="logo" aria-label="شعار عربي سايكو">
            <!-- حرفَي AS بشكل نخلة/تداخل بسيط -->
            <svg viewBox="0 0 24 24"><path d="M7 19h4v-7.5c0-.8-.3-1.6-.9-2.1L7.6 7.9c-.5-.4-.6-1.1-.2-1.6.4-.5 1.1-.6 1.6-.2l2 1.5c.6.4 1.4.4 2-.1l2.1-1.7c.5-.4 1.2-.3 1.6.2.4.5.3 1.2-.2 1.6l-1.6 1.3c-.6.5-.9 1.3-.9 2.1V19h4c.6 0 1 .4 1 1s-.4 1-1 1H7c-.6 0-1-.4-1-1s.4-1 1-1Z"/></svg>
          </div>
          <div>
            <h1 class="title">عربي سايكو</h1>
            <p class="subtitle">منصة نفسية تخدم الجميع — نخدمك أينما كنت</p>
            <div class="privacy">
              <span class="chip" title="سرّية وخصوصية">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 1a5 5 0 0 0-5 5v3H5a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2h-2V6a5 5 0 0 0-5-5Zm-3 8V6a3 3 0 1 1 6 0v3H9Z"/></svg>
                سرّية وخصوصية
              </span>
              <span class="chip" title="معلوماتك مشفّرة">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 17a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm8-7h-1V7a7 7 0 1 0-14 0v3H4a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2ZM8 7a4 4 0 1 1 8 0v3H8V7Z"/></svg>
                تشفير متقدّم
              </span>
              <span class="chip" title="خبرة علمية">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 1 7l11 5 9-4.09V17h2V7L12 2Zm0 7L3.74 6.04 12 2l8.26 4.04L12 9ZM1 10v4l11 5 7-3.18V12l-7 3-11-5Z"/></svg>
                معايير مهنية
              </span>
            </div>
          </div>
        </div>
        <div class="links">
          <a class="sm" href="/contact/whatsapp" aria-label="واتساب">واتساب</a>
          <a class="sm" href="/contact/telegram" aria-label="تلجرام">تلجرام</a>
          <a class="sm" href="/contact/email" aria-label="إيميل">إيميل</a>
        </div>
      </div>
    </div>
  </header>

  <main class="wrap">
    <section class="hero">
      <div class="panel">
        <h1>رعاية نفسية عربية بمعايير عالمية</h1>
        <p>
          أنشأنا عربي سايكو ليقدّم لك <strong>تشخيصًا مبدئيًا دقيقًا</strong> وفق DSM،
          مع <strong>اختبارات قياسية</strong> (PHQ-9, GAD-7, PCL-5, DASS-21) وأدوات
          <strong>CBT</strong> عملية، إضافة لبرامج <strong>علاج الإدمان</strong> والتأهيل.
        </p>
        <div class="cta">
          <a class="btn btn-gold" href="/dsm">🗂️ دراسة الحالة + التشخيص (DSM)</a>
          <a class="btn btn-blue" href="/cbt">🧠 العلاج السلوكي المعرفي (CBT)</a>
          <a class="btn btn-blue" href="/addiction">🚭 علاج الإدمان</a>
        </div>
      </div>
      <div class="panel" style="display:grid;gap:12px">
        <div class="card" style="margin:0">
          <div class="icon"><span>📊</span></div>
          <h3 style="margin:8px 0 4px">تشخيص DSM مُحسَّن</h3>
          <p>مطابقة ذكية للأعراض مع تعزيزات للمدة والأثر الوظيفي لإعطاء تشخيص مُرجّح واحد.</p>
          <div class="line"></div>
          <a class="btn btn-gold" href="/dsm">ابدأ التشخيص الآن</a>
        </div>
        <div class="card" style="margin:0">
          <div class="icon"><span>🧪</span></div>
          <h3 style="margin:8px 0 4px">اختبارات + أدوات CBT</h3>
          <p>PHQ-9, GAD-7, PCL-5, DASS-21 وسجل الأفكار/BA/التعرض وخطة جلسات تلقائية.</p>
          <div class="line"></div>
          <a class="btn btn-blue" href="/cbt">افتح لوحة CBT</a>
        </div>
      </div>
    </section>

    <section class="grid">
      <article class="card">
        <div class="icon"><span>🔒</span></div>
        <h3>سرّية تامّة</h3>
        <p>نلتزم بأعلى درجات الخصوصية والتشفير لحماية بياناتك ومراسلاتك.</p>
        <a class="btn btn-gold" href="/contact/whatsapp">تواصل الآمن</a>
      </article>
      <article class="card">
        <div class="icon"><span>🎓</span></div>
        <h3>محتوى مُعتمد</h3>
        <p>أدوات مبنية على دلائل علاجية واختبارات قياسية مستخدمة عالميًا.</p>
        <a class="btn btn-blue" href="/cbt">جرّب الاختبارات</a>
      </article>
      <article class="card">
        <div class="icon"><span>🌍</span></div>
        <h3>نخدمك أينما كنت</h3>
        <p>خدمات عن بُعد عبر واتساب وتلجرام وإيميل مع مرونة عالية في المواعيد.</p>
        <a class="btn btn-blue" href="/contact/email">راسلنا الآن</a>
      </article>
    </section>

    <footer>
      <div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap">
        <div>© {{year}} عربي سايكو — منصة نفسية تخدم الجميع</div>
        <div>واجهة مصممة بالأزرق الذهبي | تجربة عصرية بثبات وأناقة</div>
      </div>
    </footer>
  </main>
</body>
</html>
"""

@home_bp.route("/")
@home_bp.route("/home")
def landing():
    return render_template_string(HOME_HTML, year=_year())
"""

# 👉 تعليمات الدمج:
# 1) ضع هذا الملف باسم: home.py في نفس مسار ملف التشغيل الرئيسي (site_app.py).
# 2) في site_app.py أضف السطرين:
#       from home import home_bp
#       app.register_blueprint(home_bp)
# 3) الروابط الجاهزة تعمل مع المسارات:
#       /dsm   | /cbt   | /addiction
#    وروابط التواصل:
#       /contact/whatsapp  /contact/telegram  /contact/email
#    (تأكد أن هذه المسارات موجودة في ملف التشغيل عندك كما اتفقنا).
