# -*- coding: utf-8 -*-
from flask import Blueprint, render_template_string
home_bp = Blueprint("home", __name__)

HOME_HTML = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>عربي سايكو | الرئيسية</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{
  --bg1:#0b1437; --bg2:#112e6b; --accent:#f4b400; --accent2:#ffd86a; --ink:#0a0f1f; --w:#fff;
  --glass:rgba(255,255,255,.08); --brd:#ffffff26; --muted:#cfe0ff; --ok:#22c55e;
}
*{box-sizing:border-box} body{margin:0;font-family:"Tajawal",system-ui;color:var(--w);
  background:radial-gradient(1000px 600px at 90% -10%, #1a4bbd22, transparent),
             linear-gradient(120deg,var(--bg1),var(--bg2))}
.wrap{max-width:1200px;margin:auto;padding:28px 16px}
header{display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{display:flex;align-items:center;gap:14px}
.logo{width:76px;height:76px;border-radius:22px;background:linear-gradient(180deg,#0f2658,#1a4aa0);
  border:1px solid var(--brd);display:grid;place-items:center;box-shadow:0 12px 28px rgba(0,0,0,.28)}
.logo svg{width:46px;height:46px;color:var(--accent2)}
.title{margin:0;font-size:36px;font-weight:800}
.meta{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}
.badge{display:inline-flex;align-items:center;gap:8px;padding:6px 12px;border-radius:999px;
  background:#0e2554;border:1px solid var(--brd);font-size:13.5px}
.dot{width:8px;height:8px;border-radius:50%;background:var(--ok)}
.contactbar{display:flex;gap:10px;flex-wrap:wrap}
.link{color:var(--w);text-decoration:none;padding:10px 12px;border-radius:12px;background:var(--glass);border:1px solid var(--brd)}
.hero{margin-top:18px;display:grid;grid-template-columns:1.1fr .9fr;gap:18px}
@media(max-width:1000px){.hero{grid-template-columns:1fr}}
.panel{background:var(--glass);border:1px solid var(--brd);border-radius:22px;padding:18px}
.cta{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:12px}
@media(max-width:980px){.cta{grid-template-columns:1fr}}
.btn{display:flex;align-items:center;justify-content:center;gap:10px;text-decoration:none;border:0;cursor:pointer;
  font-weight:800;color:#1b1200;padding:16px 18px;border-radius:14px;
  background:linear-gradient(180deg,var(--accent2),var(--accent));box-shadow:0 8px 20px rgba(244,180,0,.28)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:980px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:620px){.grid{grid-template-columns:1fr}}
.tile{aspect-ratio:1/1;background:linear-gradient(180deg,#102b5f,#133a82);
  border:1px solid var(--brd);border-radius:22px;padding:16px;display:flex;flex-direction:column;justify-content:space-between;
  box-shadow:0 12px 24px rgba(0,0,0,.22)}
.head{display:flex;align-items:center;gap:10px}
.ico{width:46px;height:46px;border-radius:14px;display:grid;place-items:center;background:rgba(255,255,255,.12);border:1px solid var(--brd)}
.tile h3{margin:6px 0 2px;font-size:20px}
.tile p{margin:0;color:var(--muted);font-size:14px}
.ghost{display:inline-flex;gap:8px;align-items:center;text-decoration:none;color:#fff;
  padding:10px 12px;border-radius:12px;background:rgba(255,255,255,.12);border:1px solid var(--brd)}
footer{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-top:18px;color:var(--muted)}
</style>
</head><body><div class="wrap">

<header>
  <div class="brand">
    <div class="logo" aria-label="Arabi Psycho">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4">
        <path d="M12 21s-7-4.6-7-10a4 4 0 0 1 7-2 4 4 0 0 1 7 2c0 5.4-7 10-7 10Z" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M5.8 11c3.2-1.6 9.2-1.6 12.4 0" stroke-linecap="round"/>
      </svg>
    </div>
    <div>
      <h1 class="title">عربي سايكو</h1>
      <div class="meta">
        <span class="badge"><span class="dot"></span> خصوصية وسرّية كاملة</span>
        <span class="badge">استشارات عن بُعد</span>
        <span class="badge">تقارير مهنية</span>
      </div>
    </div>
  </div>
  <div class="contactbar">
    <a class="link" href="/contact/telegram">✈️ تلجرام</a>
    <a class="link" href="/contact/email">✉️ إيميل</a>
  </div>
</header>

<section class="hero">
  <div class="panel">
    <div class="cta">
      <a class="btn" href="/dsm">📋 التشخيص + دراسة حالة (DSM)</a>
      <a class="btn" href="/cbt">🧪 الاختبارات + CBT</a>
      <a class="btn" href="/addiction">🚭 برنامج الإدمان والتعافي</a>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <a class="link" href="/contact/whatsapp">واتساب</a>
      <a class="link" href="/contact/telegram">تلجرام</a>
      <a class="link" href="/contact/email">إيميل</a>
    </div>
  </div>

  <div class="grid">
    <div class="tile">
      <div>
        <div class="head"><div class="ico">📋</div><h3>تشخيص DSM-5</h3></div>
        <p>مطابقة ذكية للأعراض العربية + دراسة حالة مُحكمة</p>
      </div>
      <a class="ghost" href="/dsm">ابدأ التشخيص</a>
    </div>
    <div class="tile">
      <div>
        <div class="head"><div class="ico">🧪</div><h3>اختبارات + CBT</h3></div>
        <p>PHQ-9 / GAD-7 / BDI / OCI وتمارين علاج سلوكي معرفي</p>
      </div>
      <a class="ghost" href="/cbt">ابدأ الآن</a>
    </div>
    <div class="tile">
      <div>
        <div class="head"><div class="ico">🚭</div><h3>الإدمان والتعافي</h3></div>
        <p>تقييم أولي وخطة إقلاع مع متابعة سرية ومقاييس تقدّم</p>
      </div>
      <a class="ghost" href="/addiction">للتقييم السريع</a>
    </div>
  </div>
</section>

<footer>
  <div>© {{year}} عربي سايكو</div>
  <div>سياسة الخصوصية • شروط الاستخدام</div>
</footer>

</div></body></html>
"""

@home_bp.route("/")
def home():
    import datetime
    return render_template_string(HOME_HTML, year=datetime.datetime.utcnow().year)
