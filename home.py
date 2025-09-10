# -*- coding: utf-8 -*-
# home.py — واجهة عربية سايكو (هيدر + مربعات كبيرة + خصوصية)

from flask import Blueprint, render_template_string

home_bp = Blueprint("home", __name__)

HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | الرئيسية</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg1:#0b3a75; --bg2:#0a65b0; --ink:#0c1426;
      --tile:#0f2d6b; --tile2:#13408a; --gold:#f4b400; --sky:#9bd5ff; --w:#fff
    }
    *{box-sizing:border-box}
    body{
      margin:0; font-family:"Tajawal",system-ui;
      background:
        radial-gradient(1100px 520px at 85% -10%, #1a4bbd22, transparent),
        linear-gradient(135deg,var(--bg1),var(--bg2));
      color:var(--w)
    }
    .wrap{max-width:1180px; margin:auto; padding:28px 16px}
    header{
      display:flex; align-items:center; justify-content:space-between; gap:16px; margin-bottom:18px
    }
    .brand{display:flex; align-items:center; gap:14px}
    .logo{
      width:64px; height:64px; border-radius:18px;
      background:linear-gradient(180deg,#10285a,#143e8a);
      border:1px solid #ffffff40; display:grid; place-items:center;
      box-shadow:0 10px 28px rgba(0,0,0,.25)
    }
    .logo svg{width:38px; height:38px; color:#ffd86a}
    .title{margin:0; font-size:32px; font-weight:800}
    .sub{margin:4px 0 0; color:#cfe0ff}
    .badges{display:flex; gap:8px; flex-wrap:wrap}
    .badge{
      display:inline-flex; align-items:center; gap:8px; font-size:14px;
      padding:6px 10px; border-radius:999px; background:#0d2c54; border:1px solid #ffffff33
    }
    .badge .dot{width:8px; height:8px; border-radius:50%; background:#22c55e}

    /* Hero */
    .hero{
      display:grid; grid-template-columns:1.1fr .9fr; gap:16px;
      background:rgba(255,255,255,.06); border:1px solid #ffffff22; border-radius:18px;
      padding:18px; margin-bottom:18px
    }
    @media(max-width:1000px){.hero{grid-template-columns:1fr}}

    /* CTA column (vertical buttons) */
    .cta{display:flex; flex-direction:column; gap:12px}
    .cta .btn{
      display:flex; align-items:center; justify-content:center; gap:10px;
      padding:14px 16px; border-radius:14px; text-decoration:none; font-weight:800;
      background:linear-gradient(180deg,#ffd86a,#f4b400); color:#2b1b02;
      box-shadow:0 6px 18px rgba(244,180,0,.28)
    }

    /* Square tiles grid */
    .tiles{
      display:grid; grid-template-columns:repeat(3, 1fr); gap:14px
    }
    @media(max-width:980px){.tiles{grid-template-columns:repeat(2,1fr)}}
    @media(max-width:620px){.tiles{grid-template-columns:1fr}}

    .tile{
      aspect-ratio:1 / 1; /* مربع حقيقي */
      background:linear-gradient(180deg,var(--tile),var(--tile2));
      border:1px solid #ffffff22; border-radius:20px;
      padding:16px; display:flex; flex-direction:column; justify-content:space-between;
      box-shadow:0 10px 22px rgba(0,0,0,.22)
    }
    .tile .ico{
      width:40px; height:40px; display:grid; place-items:center;
      border-radius:12px; background:rgba(255,255,255,.10); border:1px solid #ffffff33
    }
    .tile h3{margin:10px 0 6px; font-size:20px}
    .tile p{margin:0; color:#cfe0ff; font-size:14px}
    .tile a{
      margin-top:10px; display:inline-flex; align-items:center; justify-content:center;
      gap:8px; padding:10px 12px; border-radius:12px; text-decoration:none;
      font-weight:800; background:rgba(255,255,255,.12); color:#fff; border:1px solid #ffffff33
    }
    .tile a:hover{background:rgba(255,255,255,.18)}
    .tile .cta{flex-direction:row}

    /* Footer contacts */
    .contacts{display:flex; gap:10px; flex-wrap:wrap; margin-top:10px}
    .contact{
      text-decoration:none; color:var(--w);
      display:inline-flex; align-items:center; gap:8px;
      border:1px solid #ffffff22; background:rgba(255,255,255,.08);
      padding:10px 12px; border-radius:12px
    }
  </style>
</head>
<body>
  <div class="wrap">

    <!-- Header -->
    <header>
      <div class="brand">
        <div class="logo" aria-label="Arabi Psycho logo">
          <!-- قلب + موجة دماغ -->
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 21s-7-4.5-7-10a4 4 0 0 1 7-2 4 4 0 0 1 7 2c0 5.5-7 10-7 10Z" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M6 11c3-1.5 9-1.5 12 0" stroke-linecap="round"/>
          </svg>
        </div>
        <div>
          <h1 class="title">عربي سايكو</h1>
          <p class="sub">خدمات نفسية عربية متكاملة: تشخيص دقيق، اختبارات، علاج سلوكي معرفي، وتعافٍ من الإدمان</p>
          <div class="badges">
            <span class="badge"><span class="dot"></span> خصوصية وسرّية كاملة</span>
            <span class="badge">استشارات عن بُعد</span>
            <span class="badge">تقارير جاهزة للطباعة</span>
          </div>
        </div>
      </div>

      <div class="badges">
        <a class="contact" href="/contact/telegram" title="تلجرام">✈️ تلجرام</a>
        <a class="contact" href="/contact/email" title="إيميل">✉️ إيميل</a>
      </div>
    </header>

    <!-- Hero: left column vertical CTA + right tiles -->
    <section class="hero">
      <div class="cta">
        <a class="btn" href="/dsm">📋 التشخيص + دراسة حالة (DSM)</a>
        <a class="btn" href="/cbt">🧪 الاختبارات + CBT</a>
        <a class="btn" href="/addiction">🚭 برنامج الإدمان والتعافي</a>
      </div>

      <div class="tiles">
        <div class="tile">
          <div class="ico">📋</div>
          <div>
            <h3>تشخيص DSM-5</h3>
            <p>مطابقة ذكية للأعراض العربية + دراسة حالة منسقة</p>
          </div>
          <a href="/dsm">ابدأ التشخيص</a>
        </div>
        <div class="tile">
          <div class="ico">🧪</div>
          <div>
            <h3>اختبارات + CBT</h3>
            <p>PHQ-9 / GAD-7 / OCI / BDI ودفتر تمارين علاجي</p>
          </div>
          <a href="/cbt">ابدأ الآن</a>
        </div>
        <div class="tile">
          <div class="ico">🚭</div>
          <div>
            <h3>برنامج الإدمان</h3>
            <p>تقييم أولي وخطة تعافٍ مع متابعة سرية</p>
          </div>
          <a href="/addiction">للتقييم السريع</a>
        </div>
      </div>
    </section>

    <!-- Extra contacts (optional) -->
    <div class="contacts">
      <a class="contact" href="/contact/whatsapp">واتساب</a>
      <a class="contact" href="/contact/telegram">تلجرام</a>
      <a class="contact" href="/contact/email">إيميل</a>
    </div>

  </div>
</body>
</html>
"""

@home_bp.route("/")
def home():
    return render_template_string(HOME_HTML)
