# -*- coding: utf-8 -*-
# home.py — صفحة ترحيب وروابط

from flask import Blueprint, render_template_string, redirect

home_bp = Blueprint("home", __name__)

HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>عربي سايكو | الصفحة الرئيسية</title>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  :root{--b1:#0e2a47;--b2:#0f5fa4;--w:#fff;--g:#ffd54a}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:"Tajawal",system-ui;background:linear-gradient(135deg,var(--b1),var(--b2));color:var(--w);line-height:1.6}
  .wrap{max-width:860px;margin:48px auto;padding:24px}
  h1{margin:0 0 12px;font-size:2.2rem;text-shadow:1px 1px 3px rgba(0,0,0,0.3)}
  p.sub{opacity:.9;margin-bottom:1.8rem;font-size:1.1rem}
  .grid{display:grid;gap:16px;margin-bottom:24px}
  a.btn{display:block;text-decoration:none;text-align:center;font-weight:800;
        background:linear-gradient(180deg,#ffe27a,var(--g));color:#1f1402;
        padding:18px;border-radius:16px;border:1px solid #fff2;
        font-size:1.1rem;transition:transform 0.2s ease}
  a.btn:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.2)}
  a.btn.secondary{background:#ffffff22;color:#fff;border-color:#ffffff33}
  .links{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}
  .chip{background:#ffffff22;border:1px solid #ffffff33;color:#fff;
        padding:10px 16px;border-radius:999px;text-decoration:none;
        transition:background 0.2s ease;font-size:0.9rem}
  .chip:hover{background:#ffffff44}
  @media (max-width: 600px) {
    .wrap{padding:16px;margin:24px auto}
    h1{font-size:1.8rem}
    .grid{gap:12px}
    a.btn{padding:16px}
  }
</style>
</head>
<body>
  <div class="wrap">
    <h1>مرحبًا بك في <span style="color:var(--g)">عربي سايكو</span></h1>
    <p class="sub">خدمات نفسية متكاملة باللغة العربية: تشخيص مبدئي، اختبارات نفسية، علاج سلوكي معرفي، وأدوات التعافي من الإدمان</p>

    <div class="grid">
      <a class="btn" href="/dsm">📋 التشخيص النفسي ودراسة الحالة (DSM)</a>
      <a class="btn secondary" href="/cbt">🧠 العلاج السلوكي المعرفي والاختبارات النفسية</a>
      <a class="btn secondary" href="/addiction">🚭 برنامج التعافي من الإدمان</a>
    </div>

    <div class="links">
      <a class="chip" href="/contact/telegram">📧 تواصل عبر التلجرام</a>
      <a class="chip" href="/contact/email">✉️ التواصل عبر الإيميل</a>
    </div>
  </div>
</body>
</html>
"""

@home_bp.route("/")
def root():
    return render_template_string(HOME_HTML)

@home_bp.route("/contact/telegram")
def contact_telegram():
    return redirect("https://t.me/USERNAME", code=302)

@home_bp.route("/contact/email")
def contact_email():
    return redirect("mailto:info@arabipsycho.com", code=302)
