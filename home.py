# -*- coding: utf-8 -*-
# home.py — واجهة رئيسية أنيقة (كلها داخل الملف)

from flask import Blueprint, render_template_string, redirect
from datetime import datetime

home_bp = Blueprint("home_bp", __name__)

HOME_HTML = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>عربي سايكو | المركز العربي للصحة النفسية</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;600;800&display=swap" rel="stylesheet">
<style>
:root{--p1:#0b3a75;--p2:#0a65b0;--gold:#f4b400;--w:#fff;--glass:rgba(255,255,255,.08);--b:rgba(255,255,255,.14)}
*{box-sizing:border-box}body{margin:0;font-family:Tajawal,system-ui;background:
radial-gradient(900px 500px at 85% -10%, #1a4bbd22, transparent),
linear-gradient(135deg,var(--p1),var(--p2));color:var(--w)}
.wrap{max-width:1240px;margin:auto;padding:28px 20px}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;position:sticky;top:0;background:linear-gradient(180deg,rgba(0,0,0,.25),rgba(0,0,0,.0));backdrop-filter:blur(8px)}
.brand{display:flex;align-items:center;gap:12px}
.badge{width:58px;height:58px;border-radius:16px;background:#0d2c54;border:1px solid #ffffff33;display:grid;place-items:center;font-weight:800;color:#ffd86a;box-shadow:0 8px 24px rgba(0,0,0,.25)}
h1{margin:0;font-size:30px;letter-spacing:.2px}
.subtitle{margin:.25rem 0 0;color:#cfe0ff}
.actions{display:flex;gap:10px;flex-wrap:wrap}
.iconbtn{display:inline-flex;align-items:center;gap:8px;text-decoration:none;color:#fff;padding:10px 12px;border-radius:12px;border:1px solid var(--b);background:var(--glass)}
.iconbtn:hover{background:rgba(255,255,255,.16)}
.ico{width:18px;height:18px}
.hero{margin:24px 0;padding:22px;border-radius:18px;background:var(--glass);border:1px solid var(--b)}
.btn{display:inline-flex;align-items:center;gap:10px;text-decoration:none;font-weight:800;
background:linear-gradient(180deg,#ffd86a,#f4b400);color:#2b1b02;padding:14px 18px;border-radius:14px;box-shadow:0 6px 18px rgba(244,180,0,.28)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:980px){.grid{grid-template-columns:1fr}}
.card{background:var(--glass);border:1px solid var(--b);border-radius:16px;padding:18px}
footer{margin-top:28px;color:#cfe0ff;opacity:.9}
</style></head><body><div class="wrap">
<header>
  <div class="brand">
    <div class="badge">AS</div>
    <div><h1>عربي سايكو</h1><div class="subtitle">المركز العربي للصحة النفسية</div></div>
  </div>
  <nav class="actions">
    <a class="iconbtn" href="/contact/whatsapp" title="واتساب">
      <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M20 3.9A10 10 0 0 0 3.5 17.4L3 21l3.7-.9A10 10 0 1 0 20 3.9ZM12 21a8.5 8.5 0 1 1 0-17 8.5 8.5 0 0 1 0 17Zm4.7-6.3-.6-.3c-.3-.1-1.8-.9-2-.9s-.5-.1-.7.3-.8.9-.9 1-.3.2-.6.1a7 7 0 0 1-2-1.2 7.4 7.4 0 0 1-1.4-1.7c-.1-.2 0-.4.2-.5l.5-.6.2-.3v-.3l-.1-.3-1-2c-.2-.6-.5-.5-.7-.5h-.6l-.3.1a1.4 1.4 0 0 0-.4 1.1 4.9 4.9 0 0 0 1 2.4 11.2 11.2 0 0 0 4.3 4 4.8 4.8 0 0 0 2.8.9c.6 0 1.2 0 1.7-.3a3.8 3.8 0 0 0 1.3-1 .9.9 0 0 0 .2-1c-.1-.2-.5-.3-.8-.5Z"/></svg>
      <span>واتساب</span>
    </a>
    <a class="iconbtn" href="/contact/telegram" title="تلجرام">
      <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M9.1 16.3 8.9 20c.4 0 .6-.2.9-.4l2.1-2 4.3 3.1c.8.5 1.4.3 1.6-.8l2.9-13.4c.3-1.2-.4-1.7-1.2-1.4L2.8 9.7c-1.1.4-1.1 1.1-.2 1.4l4.3 1.3 10-6.3c.5-.3.9-.1.5.2l-8.1 7Z"/></svg>
      <span>تلجرام</span>
    </a>
    <a class="iconbtn" href="/contact/email" title="إيميل">
      <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5v2Z"/></svg>
      <span>إيميل</span>
    </a>
  </nav>
</header>

<section class="hero">
  <a class="btn" href="/dsm">🗂️ دراسة الحالة + التشخيص (DSM)</a>
</section>

<section class="grid">
  <div class="card">
    <h3>📖 DSM-5</h3>
    <p>قاعدة اضطرابات موسّعة + مطابقة كلمات صارمة/ناعمة لنتيجة تقديرية.</p>
    <a class="btn" href="/dsm">ابدأ التشخيص</a>
  </div>
  <div class="card">
    <h3>🧠 CBT + اختبارات</h3>
    <p>لوحة اختبارات قياسية (PHQ-9, GAD-7, DASS-21, PCL-5, ASRS, OCI-R, AUDIT وغيرها).</p>
    <a class="btn" href="/cbt">اذهب للاختبارات</a>
  </div>
  <div class="card">
    <h3>🚭 علاج الإدمان</h3>
    <p>تقييم شامل (ASSIST المختصر + فحص معايير DSM-5) وخطط أولية.</p>
    <a class="btn" href="/addiction">ابدأ التقييم</a>
  </div>
</section>

<footer>© {{year}} عربي سايكو — جميع الحقوق محفوظة</footer>
</div></body></html>
"""

@home_bp.route("/")
def home():
    return render_template_string(HOME_HTML, year=datetime.now().year)

# روابط تواصل
@home_bp.route("/contact/<kind>")
def contact(kind):
    if kind == "whatsapp":  return redirect("https://wa.me/9665XXXXXXXX", code=302)
    if kind == "telegram":  return redirect("https://t.me/USERNAME",      code=302)
    if kind == "email":     return redirect("mailto:info@arabipsycho.com", code=302)
    return redirect("/", 302)
