# -*- coding: utf-8 -*-
# home.py — واجهة عربي سايكو (تصميم عصري + مربعات + أزرار مصفوفة)

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
      --bg1:#0a1b3f; --bg2:#0b3a75; --bg3:#0a65b0;
      --tile:#102b5f; --tile2:#143f88; --w:#fff; --ink:#0b1323;
      --gold:#f4b400; --gold2:#ffd86a; --mint:#34d399; --blue:#60a5fa;
      --glass:rgba(255,255,255,.08); --glass2:rgba(255,255,255,.12); --brd:#ffffff2a
    }
    *{box-sizing:border-box}
    body{
      margin:0; font-family:"Tajawal",system-ui; color:var(--w);
      background:
        radial-gradient(900px 520px at 85% -10%, #1a4bbd22, transparent),
        linear-gradient(120deg,var(--bg1),var(--bg2) 40%, var(--bg3));
    }
    .wrap{max-width:1240px;margin:auto;padding:28px 16px}

    /* Header */
    header{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:18px}
    .brand{display:flex;align-items:center;gap:14px}
    .logo{
      width:70px;height:70px;border-radius:20px;flex:none;
      background:linear-gradient(180deg,#0f2658,#1a4aa0);
      border:1px solid var(--brd); display:grid; place-items:center;
      box-shadow:0 12px 28px rgba(0,0,0,.30)
    }
    .logo svg{width:42px;height:42px;color:var(--gold2)}
    .title{margin:0;font-size:34px;line-height:1;font-weight:800;letter-spacing:.2px}
    .sub{margin:6px 0 0;color:#d7e7ff}
    .badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
    .badge{
      display:inline-flex;align-items:center;gap:8px;padding:6px 10px;border-radius:999px;
      background:#0d2c54;border:1px solid var(--brd);font-size:13.5px
    }
    .dot{width:8px;height:8px;border-radius:50%;background:var(--mint)}

    .contactbar{display:flex;gap:10px;flex-wrap:wrap}
    .contact{
      text-decoration:none;color:var(--w);
      display:inline-flex;align-items:center;gap:8px;padding:10px 12px;border-radius:12px;
      background:var(--glass);border:1px solid var(--brd)
    }

    /* Hero */
    .hero{
      display:grid;grid-template-columns:1.1fr .9fr;gap:18px;
      background:var(--glass);border:1px solid var(--brd);border-radius:20px;padding:18px;margin-bottom:18px
    }
    @media(max-width:1080px){.hero{grid-template-columns:1fr}}

    /* CTA buttons row */
    .cta{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
    @media(max-width:980px){.cta{grid-template-columns:1fr}}
    .btn{
      display:flex;align-items:center;justify-content:center;gap:10px;
      text-decoration:none;font-weight:800;color:#1b1200;
      padding:14px 16px;border-radius:14px;border:0;cursor:pointer;
      background:linear-gradient(180deg,var(--gold2),var(--gold));
      box-shadow:0 8px 18px rgba(244,180,0,.28)
    }

    /* Tiles */
    .tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
    @media(max-width:980px){.tiles{grid-template-columns:repeat(2,1fr)}}
    @media(max-width:620px){.tiles{grid-template-columns:1fr}}

    .tile{
      aspect-ratio:1/1;background:linear-gradient(180deg,var(--tile),var(--tile2));
      border:1px solid var(--brd);border-radius:22px;padding:16px;
      display:flex;flex-direction:column;justify-content:space-between;
      box-shadow:0 12px 24px rgba(0,0,0,.25)
    }
    .tile .head{display:flex;align-items:center;gap:10px}
    .tile .ico{
      width:44px;height:44px;border-radius:14px;display:grid;place-items:center;
      background:var(--glass2);border:1px solid var(--brd);font-size:22px
    }
    .tile h3{margin:6px 0 2px;font-size:20px}
    .tile p{margin:0;color:#cfe0ff;font-size:14px}
    .tile .actions{display:flex;gap:10px;flex-wrap:wrap}
    .ghost{
      text-decoration:none;color:#fff;display:inline-flex;align-items:center;gap:8px;
      padding:10px 12px;border-radius:12px;background:var(--glass2);border:1px solid var(--brd)
    }
    .ghost:hover{background:rgba(255,255,255,.18)}

    /* Footer */
    footer{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:16px;color:#d7e7ff}
    footer a{color:#d7e7ff}
  </style>
</head>
<body>
  <div class="wrap">
    <!-- Header -->
    <header>
      <div class="brand">
        <div class="logo" aria-label="Arabi Psycho logo">
          <!-- قلب + موجة دماغ -->
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4">
            <path d="M12 21s-7-4.6-7-10a4 4 0 0 1 7-2 4 4 0 0 1 7 2c0 5.4-7 10-7 10Z" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M5.8 11c3.2-1.6 9.2-1.6 12.4 0" stroke-linecap="round"/>
          </svg>
        </div>
        <div>
          <h1 class="title">عربي سايكو</h1>
          <p class="sub">خدمات نفسية عربية متكاملة: تشخيص دقيق، اختبارات معيارية، وعلاج سلوكي معرفي، مع برامج تعافٍ من الإدمان</p>
          <div class="badges">
            <span class="badge"><span class="dot"></span> خصوصية وسرّية كاملة</span>
            <span class="badge">استشارات عن بُعد</span>
            <span class="badge">تقارير قابلة للطباعة</span>
          </div>
        </div>
      </div>
      <div class="contactbar">
        <a class="contact" href="/contact/telegram">✈️ تلجرام</a>
        <a class="contact" href="/contact/email">✉️ إيميل</a>
      </div>
    </header>

    <!-- Hero -->
    <section class="hero">
      <div>
        <div class="cta" style="margin-bottom:12px">
          <a class="btn" href="/dsm">📋 التشخيص + دراسة حالة (DSM)</a>
          <a class="btn" href="/cbt">🧪 الاختبارات + CBT</a>
          <a class="btn" href="/addiction">🚭 برنامج الإدمان والتعافي</a>
        </div>
        <div style="display:flex;gap:10px;flex-wrap:wrap">
          <a class="contact" href="/contact/whatsapp">واتساب</a>
          <a class="contact" href="/contact/telegram">تلجرام</a>
          <a class="contact" href="/contact/email">إيميل</a>
        </div>
      </div>
      <div class="tiles">
        <div class="tile">
          <div>
            <div class="head"><div class="ico">📋</div><h3>تشخيص DSM-5</h3></div>
            <p>مطابقة ذكية للأعراض العربية + دراسة حالة منسقة</p>
          </div>
          <div class="actions"><a class="ghost" href="/dsm">ابدأ التشخيص</a></div>
        </div>
        <div class="tile">
          <div>
            <div class="head"><div class="ico">🧪</div><h3>اختبارات + CBT</h3></div>
            <p>PHQ-9 / GAD-7 / BDI / OCI وتمارين علاج سلوكي معرفي</p>
          </div>
          <div class="actions"><a class="ghost" href="/cbt">ابدأ الآن</a></div>
        </div>
        <div class="tile">
          <div>
            <div class="head"><div class="ico">🚭</div><h3>التقييم والإقلاع</h3></div>
            <p>تقييم أولي وخطة تعافٍ مع متابعة سرية ومقاييس تقدم</p>
          </div>
          <div class="actions"><a class="ghost" href="/addiction">للتقييم السريع</a></div>
        </div>
      </div>
    </section>

    <footer>
      <div>© {{year}} عربي سايكو — جميع الحقوق محفوظة</div>
      <div>سياسة الخصوصية • شروط الاستخدام</div>
    </footer>
  </div>
</body>
</html>
"""

@home_bp.route("/")
def home():
    import datetime
    return render_template_string(HOME_HTML, year=datetime.datetime.utcnow().year)
