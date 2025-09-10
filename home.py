# -*- coding: utf-8 -*-
# home.py — الواجهة الرئيسية للموقع

from flask import Blueprint, render_template_string, redirect

home_bp = Blueprint("home", __name__)

HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو</title>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400;--ink:#04122c}
    *{box-sizing:border-box}
    body{margin:0;font-family:"Tajawal",system-ui;background:
      radial-gradient(900px 480px at 85% -10%, #1a4bbd22, transparent),
      linear-gradient(135deg,var(--bg1),var(--bg2)); color:#fff;}
    .wrap{max-width:980px;margin:auto;padding:28px 16px}
    header{display:flex;justify-content:space-between;align-items:center}
    .brand{display:flex;gap:12px;align-items:center}
    .badge{width:54px;height:54px;border-radius:16px;background:#0d2c54;border:1px solid #ffffff2a;display:grid;place-items:center;font-weight:800}
    h1{margin:.2rem 0 .1rem}
    .subtitle{margin:0;color:#cfe0ff}
    .grid{display:grid;grid-template-columns:1fr;gap:12px;margin-top:22px}
    .card{background:rgba(255,255,255,.08);border:1px solid #ffffff22;border-radius:16px;padding:16px}
    .btn{display:block;width:100%;text-decoration:none;text-align:center;
         background:var(--gold);color:var(--ink);padding:14px;border-radius:12px;
         font-weight:800;box-shadow:0 6px 18px rgba(244,180,0,.28)}
    .btn.ghost{background:rgba(255,255,255,.1);color:#fff;border:1px solid #ffffff2a;box-shadow:none}
    footer{opacity:.8;margin-top:18px;font-size:.9rem}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="brand">
        <div class="badge">AS</div>
        <div>
          <h1>عربي سايكو</h1>
          <p class="subtitle">خدمة تشخيص مبدئي + CBT + برامج التعافي</p>
        </div>
      </div>
    </header>

    <div class="grid">
      <a class="btn" href="/dsm">🗂️ التشخيص + دراسة حالة (DSM)</a>
      <a class="btn ghost" href="/cbt">🧠 العلاج السلوكي المعرفي (CBT)</a>
      <a class="btn ghost" href="/addiction">🚭 الإدمان والتعافي</a>
      <a class="btn ghost" href="/contact/telegram">✉️ تواصل عبر التلجرام</a>
    </div>

    <footer>⚠️ التنبيه: النتائج تقديرية للمساعدة ولا تُعد تشخيصًا نهائيًا.</footer>
  </div>
</body>
</html>
"""

@home_bp.route("/")
def index():
    return render_template_string(HOME_HTML)

# روابط تواصل
@home_bp.route("/contact/telegram")
def contact_telegram():
    return redirect("https://t.me/USERNAME", code=302)
