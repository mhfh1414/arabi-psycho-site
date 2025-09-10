# -*- coding: utf-8 -*-
# home.py — الواجهة الرئيسية (Landing Page) لمنصة عربي سايكو

from flask import Blueprint, render_template_string

home_bp = Blueprint("home", __name__)

HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | منصة نفسية تخدم الجميع</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg1:#0b143a; --bg2:#0a3a75; --bg3:#0a65b0;
      --ink:#0b1020; --w:#fff; --muted:#cfe0ff;
      --gold:#ffd86a; --amber:#f4b400; --mint:#38f6c6; --rose:#ff7aa8;
      --glass: rgba(255,255,255,.10);
      --border: rgba(255,255,255,.14);
      --glow: 0 8px 30px rgba(0,200,255,.25), 0 0 0 1px rgba(255,255,255,.06) inset;
    }
    *{box-sizing:border-box}
    body{
      margin:0; font-family:"Tajawal",system-ui; color:var(--w);
      background:
        radial-gradient(1200px 600px at 80% -10%, #1a4bbd33, transparent),
        radial-gradient(900px 420px at -10% 10%, #00ffd51a, transparent),
        linear-gradient(135deg,var(--bg1),var(--bg2) 45%, var(--bg3));
      min-height:100dvh;
      display:flex; align-items:stretch;
    }
    .wrap{width:100%; max-width:1220px; margin:auto; padding:28px 18px}
    header{display:flex; align-items:center; justify-content:space-between; gap:14px; margin-bottom:18px}
    .brand{display:flex; align-items:center; gap:14px}
    .logo{
      width:64px; height:64px; border-radius:18px;
      display:grid; place-items:center;
      background:linear-gradient(180deg,#0e204f,#173a87); border:1px solid var(--border);
      box-shadow: var(--glow);
      font-weight:800; letter-spacing:.5px;
    }
    .brand h1{margin:0; font-size:30px}
    .tag{margin:.25rem 0 0; color:var(--muted); font-weight:600}
    .badges{display:flex; gap:8px; flex-wrap:wrap; margin-top:6px}
    .badge{
      display:inline-flex; align-items:center; gap:8px; padding:6px 10px; border-radius:999px;
      background:rgba(255,255,255,.08); border:1px solid var(--border); color:#e8f0ff; font-size:.9rem
    }
    .hero{
      display:grid; grid-template-columns: 1.1fr .9fr; gap:16px; margin:18px 0 22px;
    }
    @media(max-width:992px){ .hero{grid-template-columns:1fr} }

    .card{
      background:var(--glass); border:1px solid var(--border); border-radius:18px; padding:18px;
      box-shadow: var(--glow);
    }
    .headline{font-size:22px; margin:0 0 8px}
    .lead{color:#d7e6ff; margin:0}
    .cta-grid{
      display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:14px;
    }
    @media(max-width:992px){ .cta-grid{grid-template-columns:1fr} }

    .tile{
      position:relative; overflow:hidden; border-radius:18px; padding:16px; isolation:isolate;
      background:linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,.06));
      border:1px solid var(--border); min-height:132px; display:flex; flex-direction:column; justify-content:space-between;
      transition: transform .2s ease, box-shadow .2s ease, background .2s ease;
    }
    .tile::after{
      content:""; position:absolute; inset:-20%; background: radial-gradient(600px 160px at 60% -30%, rgba(255,216,106,.3), transparent);
      opacity:.55; pointer-events:none; z-index:0;
    }
    .tile:hover{ transform: translateY(-2px); box-shadow: 0 10px 36px rgba(0,0,0,.25), 0 0 0 1px rgba(255,255,255,.08) inset; }
    .tile h3{margin:0 0 6px; font-size:20px}
    .tile p{margin:0; color:#e9f2ff; opacity:.9}
    .tile .actions{display:flex; gap:10px; margin-top:12px; z-index:1}
    .btn{
      text-decoration:none; font-weight:800; cursor:pointer; border:none; outline:none;
      padding:12px 14px; border-radius:12px; display:inline-flex; align-items:center; gap:8px;
      color:#1a1300; background:linear-gradient(180deg,var(--gold),var(--amber));
      box-shadow:0 10px 26px rgba(244,180,0,.32);
    }
    .btn.glow{
      color:#021a1a; background:linear-gradient(180deg,#8dffe7,#38f6c6);
      box-shadow:0 10px 26px rgba(56,246,198,.36);
    }
    .btn.rose{
      color:#2c0011; background:linear-gradient(180deg,#ffc1d5,#ff7aa8);
      box-shadow:0 10px 26px rgba(255,122,168,.35);
    }
    .nav{
      display:flex; gap:10px; flex-wrap:wrap;
    }
    .icon{
      width:18px; height:18px; display:inline-block;
    }
    .links{
      display:flex; flex-direction:column; gap:10px;
    }
    .contact{
      display:flex; gap:10px; flex-wrap:wrap; justify-content:flex-end;
    }
    footer{display:flex; align-items:center; justify-content:space-between; gap:12px; margin-top:18px}
    .muted{color:#cfe0ff}
    .list{margin:0; padding-left:1rem; opacity:.95}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="brand">
        <div class="logo">AS</div>
        <div>
          <h1>عربي سايكو</h1>
          <div class="tag">منصة نفسية عربية — تشخيص ذكي، اختبارات معيارية، علاج معرفي سلوكي، بسرية تامة</div>
          <div class="badges">
            <span class="badge">🔒 خصوصية و سرّية</span>
            <span class="badge">🔬 إعتماد أدلة DSM-5</span>
            <span class="badge">⚡ نتائج فورية</span>
          </div>
        </div>
      </div>
      <nav class="contact">
        <a class="btn glow" href="/contact/telegram">
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M9.1 16.3 8.9 20c.4 0 .6-.2.9-.4l2.1-2 4.3 3.1c.8.5 1.4.3 1.6-.8l2.9-13.4c.3-1.2-.4-1.7-1.2-1.4L2.8 9.7c-1.1.4-1.1 1.1-.2 1.4l4.3 1.3 10-6.3c.5-.3.9-.1.5.2l-8.1 7Z"/></svg>
          تلجرام
        </a>
        <a class="btn rose" href="/contact/email">
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5v2Z"/></svg>
          إيميل
        </a>
      </nav>
    </header>

    <section class="hero">
      <div class="card">
        <h2 class="headline">ابدأ هنا</h2>
        <p class="lead">اختر خدمتك، كلها تعمل فوريًا داخل الموقع:</p>

        <div class="cta-grid">
          <!-- DSM -->
          <div class="tile">
            <div>
              <h3>التشخيص + دراسة حالة (DSM)</h3>
              <p>قارئ ذكي للأعراض بالعربية مع مرادفات ولهجات، يعطي تشخيصًا مرجّحًا مع المطابقات.</p>
            </div>
            <div class="actions">
              <a class="btn" href="/dsm">اذهب إلى DSM</a>
            </div>
          </div>

          <!-- CBT -->
          <div class="tile">
            <div>
              <h3>العلاج السلوكي المعرفي + اختبارات</h3>
              <p>لوحة تمارين CBT ونماذج واجبات، مع مقاييس PHQ-9 / GAD-7 / OCI وغيرها.</p>
            </div>
            <div class="actions">
              <a class="btn glow" href="/cbt">ابدأ العلاج والاختبارات</a>
            </div>
          </div>

          <!-- ADDICTION -->
          <div class="tile">
            <div>
              <h3>برنامج الإدمان والتعافي</h3>
              <p>تقييم أولي، خطة 12 خطوة، متابعة انتكاسة، وإحالات متخصصة عند الحاجة.</p>
            </div>
            <div class="actions">
              <a class="btn rose" href="/addiction">الدخول إلى برنامج التعافي</a>
            </div>
          </div>
        </div>
      </div>

      <aside class="card">
        <h2 class="headline">لماذا عربي سايكو؟</h2>
        <ul class="list">
          <li>لغة عربية طبيّة + فهم العامية مباشرة.</li>
          <li>نموذج تشخيصي مبني على كلمات DSM ومرادفات دقيقة.</li>
          <li>تمارين CBT عملية قابلة للطباعة والمتابعة.</li>
          <li>سياسة خصوصية صارمة، ولا تُحفظ أي معلومات حساسة بدون موافقة.</li>
        </ul>
        <div class="links" style="margin-top:14px">
          <a class="btn" href="/dsm">ابدأ التشخيص الآن</a>
          <a class="btn glow" href="/cbt">انتقل للتمارين والاختبارات</a>
          <a class="btn rose" href="/addiction">برنامج الإدمان</a>
        </div>
      </aside>
    </section>

    <footer>
      <div class="muted">© {{year}} عربي سايكو — منصة نفسية عربية</div>
      <div class="badges">
        <span class="badge">🔐 تشفير اتصال HTTPS</span>
        <span class="badge">🛡️ لا نشارك بياناتك مع طرف ثالث</span>
      </div>
    </footer>
  </div>
</body>
</html>
"""

@home_bp.route("/")
def hub():
    from datetime import datetime
    return render_template_string(HOME_HTML, year=datetime.utcnow().year)

# روابط تواصل (إعادة توجيه بسيطة — يمكنك تعديلها لاحقًا)
@home_bp.route("/contact/telegram")
def contact_telegram():
    from flask import redirect
    return redirect("https://t.me/USERNAME", code=302)

@home_bp.route("/contact/email")
def contact_email():
    from flask import redirect
    return redirect("mailto:info@arabipsycho.com", code=302)
