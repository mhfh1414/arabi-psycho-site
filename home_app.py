# -*- coding: utf-8 -*-
# home_app.py — ملف التشغيل/الهوم: يشغل الموقع ويربط DSM
from flask import Flask, render_template_string, redirect
from datetime import datetime

# استيراد DSM (ملف مستقل)
from dsm import dsm_bp

app = Flask(__name__)
app.register_blueprint(dsm_bp)  # المسار: /dsm

HOME_HTML = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>عربي سايكو | الرئيسية</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400;--w:#fff}
*{box-sizing:border-box} body{margin:0;font-family:"Tajawal",system-ui;background:
radial-gradient(900px 480px at 85% -10%, #1a4bbd22, transparent),
linear-gradient(135deg,var(--bg1),var(--bg2));color:var(--w)}
.wrap{max-width:1240px;margin:auto;padding:28px 20px}
header{display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{display:flex;align-items:center;gap:14px}
.badge{width:56px;height:56px;border-radius:16px;background:#0d2c54;border:1px solid #ffffff33;display:grid;place-items:center;font-weight:800;box-shadow:0 8px 24px rgba(0,0,0,.25);color:#ffd86a}
.title{margin:0;font-size:32px} .subtitle{margin:.25rem 0 0;color:#cfe0ff}
.actions{display:flex;gap:10px;flex-wrap:wrap}
.btn,a.btn{display:inline-flex;align-items:center;gap:10px;text-decoration:none;font-weight:800;background:linear-gradient(180deg,#ffd86a,#f4b400);color:#2b1b02;padding:12px 16px;border-radius:14px;box-shadow:0 6px 18px rgba(244,180,0,.28)}
.card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:18px;margin:12px 0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px} @media(max-width:980px){.grid{grid-template-columns:1fr}}
.sec h3{margin:0 0 8px}
</style></head><body>
<div class="wrap">
  <header>
    <div class="brand" style="text-align:right">
      <div class="badge">AS</div>
      <div>
        <h1 class="title">عربي سايكو</h1>
        <p class="subtitle">منصّة نفسية تخدم الجميع — {{year}}</p>
      </div>
    </div>
    <nav class="actions">
      <a class="btn" href="/dsm">🗂️ دراسة الحالة + التشخيص DSM</a>
      <a class="btn" href="https://wa.me/9665XXXXXXXX" target="_blank">واتساب</a>
      <a class="btn" href="https://t.me/USERNAME" target="_blank">تلجرام</a>
      <a class="btn" href="mailto:info@arabipsycho.com">إيميل</a>
    </nav>
  </header>

  <section class="card sec">
    <h3>مرحبًا بك في مركز عربي سايكو</h3>
    <p>واجهة سريعة، ألوان أزرق/ذهبي، وروابط تواصل مباشرة. ابدأ التشخيص عبر DSM ثم أضف لاحقًا CBT والإدمان كملفات مستقلة بنفس الأسلوب.</p>
  </section>

  <section class="grid">
    <div class="card"><h3>📖 DSM-5</h3><p>قاموس أعراض موسّع + دراسة حالة + تشخيص مرجّح.</p><a class="btn" href="/dsm">ابدأ الآن</a></div>
    <div class="card"><h3>🧠 CBT</h3><p>(لاحقًا) لوحة اختبارات وأدوات علاجية.</p><a class="btn" href="/dsm">مؤقتًا ادخل DSM</a></div>
    <div class="card"><h3>🚭 الإدمان</h3><p>(لاحقًا) تقييم وخطط علاج والتأهيل.</p><a class="btn" href="/dsm">مؤقتًا ادخل DSM</a></div>
  </section>
</div>
</body></html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML, year=datetime.now().year)

# مسارات مختصرة للاتصال (اختياري)
@app.route("/contact/whatsapp")
def contact_whatsapp(): return redirect("https://wa.me/9665XXXXXXXX", code=302)
@app.route("/contact/telegram")
def contact_telegram(): return redirect("https://t.me/USERNAME", code=302)
@app.route("/contact/email")
def contact_email(): return redirect("mailto:info@arabipsycho.com", code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
