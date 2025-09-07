# home.py
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template_string, redirect
from datetime import datetime

home_bp = Blueprint("home_bp", __name__)

# ========================= صفحة الواجهة =========================
@home_bp.route("/")
def home():
    year = datetime.now().year
    return render_template_string("""
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | الرئيسية</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{
      --primary:#0a3a75; --secondary:#0a65b0; --dark:#0a1330;
      --gold:#f4b400; --light:#cfe0ff; --glass:rgba(255,255,255,.08); --border:rgba(255,255,255,.15);
      --white:#fff;
    }
    *{box-sizing:border-box}
    body{
      margin:0; font-family:"Tajawal",system-ui;
      background: radial-gradient(900px 420px at 85% -10%, #1a4bbd22, transparent),
                  linear-gradient(135deg,var(--primary),var(--secondary));
      color:var(--white);
      background-attachment: fixed;
    }
    .container{max-width:1280px;margin:auto;padding:18px}
    header{position:sticky;top:0;z-index:10;background:rgba(10,19,48,.6);backdrop-filter:blur(10px);
           border-bottom:1px solid var(--border)}
    .head{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:12px 0}
    .brand{display:flex;align-items:center;gap:12px}
    .logo{width:56px;height:56px;border-radius:16px;background:linear-gradient(145deg,#0b1e3f,#0e2b5d);
          display:grid;place-items:center;font-weight:800;color:var(--gold);border:1px solid var(--border);box-shadow:0 6px 18px #0003}
    .title{margin:0;font-size:28px;background:linear-gradient(90deg,#ffd86a,var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
    .subtitle{margin:0;color:var(--light);font-size:.95rem}
    .nav{display:flex;gap:10px;flex-wrap:wrap}
    .nav a{display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border-radius:12px;text-decoration:none;
           color:#fff;background:var(--glass);border:1px solid var(--border);transition:.2s}
    .nav a:hover{transform:translateY(-2px);background:rgba(255,255,255,.15)}
    .ico{width:18px;height:18px}

    .hero{padding:40px 0;text-align:center}
    .hero h2{margin:0 0 10px;font-size:2.2rem}
    .hero p{margin:0 auto 22px;color:var(--light);max-width:680px}

    .cta{display:flex;justify-content:center;gap:14px;flex-wrap:wrap}
    .btn{display:inline-flex;align-items:center;gap:10px;text-decoration:none;font-weight:800;border-radius:14px;padding:14px 20px;transition:.2s}
    .primary{background:linear-gradient(145deg,#ffd86a,var(--gold));color:#2b1b02;box-shadow:0 8px 22px rgb(244 180 0 / .35)}
    .secondary{background:linear-gradient(145deg,#a8c9ff,#6aa8ff);color:#04122c;box-shadow:0 8px 22px rgb(70 130 255 / .30)}
    .btn:hover{transform:translateY(-3px)}

    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:26px 0}
    @media (max-width:980px){.grid{grid-template-columns:1fr}}
    .card{background:var(--glass);border:1px solid var(--border);border-radius:16px;padding:18px;min-height:170px;display:flex;flex-direction:column}
    .card h3{margin:0 0 8px}
    .card p{color:var(--light);margin:0 0 14px;flex-grow:1}

    footer{border-top:1px solid var(--border);background:rgba(10,19,48,.7);margin-top:26px}
    .foot{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;color:var(--light);padding:14px 0}
  </style>
</head>
<body>
  <header>
    <div class="container head">
      <div class="brand">
        <div class="logo">AS</div>
        <div>
          <h1 class="title">عربي سايكو</h1>
          <p class="subtitle">المركز العربي للصحة النفسية</p>
        </div>
      </div>
      <nav class="nav">
        <a href="/contact/whatsapp" title="واتساب">
          <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M20 3.9A10 10 0 0 0 3.5 17.4L3 21l3.7-.9A10 10 0 1 0 20 3.9ZM12 21a8.4 8.4 0 0 1-4.3-1.2l-.3-.2-2.5.6.5-2.4-.2-.3A8.5 8.5 0 1 1 12 21Zm4.7-6.3-.6-.3c-.3-.1-1.8-.9-2-.9s-.5-.1-.7.3-.8.9-.9 1-.3.2-.6.1a7 7 0 0 1-2-1.2 7.4 7.4 0 0 1-1.4-1.7c-.1-.2 0-.4.2-.5l.5-.6.2-.3v-.3l-.1-.3-1-2c-.2-.6-.5-.5-.7-.5h-.6l-.3.1a1.4 1.4 0 0 0-.4 1.1 4.9 4.9 0 0 0 1 2.4 11.2 11.2 0 0 0 4.3 4 4.8 4.8 0 0 0 2.8.9c.6 0 1.2 0 1.7-.3a3.8 3.8 0 0 0 1.3-1 .9.9 0 0 0 .2-1c-.1-.2-.5-.3-.8-.5Z"/></svg>
          <span>واتساب</span>
        </a>
        <a href="/contact/telegram" title="تلجرام">
          <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M9.1 16.3 8.9 20c.4 0 .6-.2.9-.4l2.1-2 4.3 3.1c.8.5 1.4.3 1.6-.8l2.9-13.4c.3-1.2-.4-1.7-1.2-1.4L2.8 9.7c-1.1.4-1.1 1.1-.2 1.4l4.3 1.3 10-6.3c.5-.3.9-.1.5.2l-8.1 7Z"/></svg>
          <span>تلجرام</span>
        </a>
        <a href="/contact/email" title="إيميل">
          <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5v2Z"/></svg>
          <span>إيميل</span>
        </a>
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <h2>رعاية نفسية متكاملة بمعايير عالمية</h2>
      <p>ابدأ التشخيص وفق DSM، نفّذ اختبارات CBT المعتمدة، أو ابدأ تقييم وعلاج الإدمان — كل ذلك بواجهة عربية واضحة.</p>
      <div class="cta">
        <a class="btn primary" href="/dsm">🗂️ دراسة الحالة + DSM</a>
        <a class="btn secondary" href="/cbt">🧠 اختبارات وCBT</a>
        <a class="btn secondary" href="/addiction">🚭 علاج الإدمان</a>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h3>📖 التشخيص وفق DSM-5</h3>
        <p>مطابقة ذكية للأعراض مع قاموس موسّع، وإظهار أفضل التشخيصات بدرجات واضحة.</p>
        <a class="btn primary" href="/dsm">ابدأ التشخيص</a>
      </div>
      <div class="card">
        <h3>🧪 اختبارات نفسية + CBT</h3>
        <p>مجموعة اختبارات موثوقة (PHQ-9، GAD-7، PCL-5، وغيرها) مع لوحات نتائج فورية.</p>
        <a class="btn secondary" href="/cbt">افتح الاختبارات</a>
      </div>
      <div class="card">
        <h3>🚭 برامج علاج الإدمان</h3>
        <p>تقييم شامل وخطط علاج فردية ومتابعة، بإطار علاجي آمن وسري.</p>
        <a class="btn secondary" href="/addiction">ابدأ التقييم</a>
      </div>
    </section>
  </main>

  <footer>
    <div class="container foot">
      <div>© {{year}} عربي سايكو — جميع الحقوق محفوظة</div>
      <div>خدمة آمنة وسرية — أينما كنت</div>
    </div>
  </footer>
</body>
</html>
    """, year=year)

# ========================= روابط الاتصال (تحويل) =========================
@home_bp.route("/contact/whatsapp")
def contact_whatsapp():
    # ضع رقمك الدولي بصيغة 9665XXXXXXXX
    return redirect("https://wa.me/9665XXXXXXXX", code=302)

@home_bp.route("/contact/telegram")
def contact_telegram():
    # غيّر USERNAME إلى اسم المستخدم الخاص بك
    return redirect("https://t.me/USERNAME", code=302)

@home_bp.route("/contact/email")
def contact_email():
    return redirect("mailto:info@arabipsycho.com", code=302)
