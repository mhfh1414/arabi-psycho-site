# -*- coding: utf-8 -*-
# home_app.py — ملف التشغيل والواجهة الرئيسية + ربط CBT و DSM (إن وُجد)

from flask import Flask, render_template_string, redirect
app = Flask(__name__)

# ========= تسجيل البلوبرنتات =========
# CBT (مطلوب)
from cbt import cbt_bp
app.register_blueprint(cbt_bp)

# DSM (اختياري: يسجل فقط إذا عندك dsm.py فيه dsm_bp)
try:
    from dsm import dsm_bp
    app.register_blueprint(dsm_bp)
except Exception:
    pass  # تجاهل لو ما عندك dsm الآن

# ========= واجهة HOME بسيطة وفخمة =========
HOME = """
<!doctype html><html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>عربي سايكو | المنصة</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400;--w:#fff;--glass:rgba(255,255,255,.08);--gb:rgba(255,255,255,.18)}
*{box-sizing:border-box}
body{margin:0;font-family:"Tajawal",system-ui;background:
  radial-gradient(900px 500px at 85% -10%, #1a4bbd22, transparent),
  linear-gradient(135deg,var(--bg1),var(--bg2)) fixed;color:var(--w)}
.wrap{max-width:1180px;margin:28px auto;padding:16px}
header{display:flex;justify-content:space-between;align-items:center;gap:12px}
.brand{display:flex;align-items:center;gap:12px}
.badge{width:56px;height:56px;border-radius:16px;background:#0d2c54;border:1px solid #ffffff33;display:grid;place-items:center;font-weight:800;box-shadow:0 8px 24px rgba(0,0,0,.25)}
h1{margin:0;font-size:32px}
.sub{margin:2px 0 0;color:#cfe0ff}
.actions{display:flex;gap:8px}
.btn{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-weight:800;border:none;cursor:pointer;border-radius:14px;padding:10px 14px}
.btn.primary{background:linear-gradient(180deg,#ffd86a,#f4b400);color:#2b1b02}
.btn.secondary{background:linear-gradient(180deg,#9cc5ff,#63a4ff);color:#04122c}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px}
@media(max-width:980px){.grid{grid-template-columns:1fr}}
.card{background:var(--glass);border:1px solid var(--gb);border-radius:16px;padding:18px}
.card h3{margin-top:0}
.tile{display:flex;justify-content:space-between;align-items:center;gap:10px;background:var(--glass);border:1px solid var(--gb);border-radius:14px;padding:12px;margin:8px 0}
.t{font-weight:700}
footer{margin-top:22px;opacity:.75}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="brand">
      <div class="badge">AS</div>
      <div>
        <h1>عربي سايكو</h1>
        <p class="sub">منصة نفسية عربية — تشخيص وعلاج مبني على الدليل</p>
      </div>
    </div>
    <nav class="actions">
      <a class="btn secondary" href="/cbt/">لوحة CBT</a>
      <a class="btn primary" href="/dsm">دراسة الحالة + DSM</a>
    </nav>
  </header>

  <section class="grid">
    <div class="card">
      <h3>🧪 الاختبارات القياسية</h3>
      <div class="tile"><span class="t">PHQ-9 — الاكتئاب</span><a class="btn primary" href="/cbt/phq9">ابدأ</a></div>
      <div class="tile"><span class="t">GAD-7 — القلق العام</span><a class="btn primary" href="/cbt/gad7">ابدأ</a></div>
      <div class="tile"><span class="t">PCL-5 — ما بعد الصدمة</span><a class="btn primary" href="/cbt/pcl5">ابدأ</a></div>
      <div class="tile"><span class="t">DASS-21 — DEA</span><a class="btn primary" href="/cbt/dass21">ابدأ</a></div>
    </div>
    <div class="card">
      <h3>💡 أدوات CBT</h3>
      <div class="tile"><span class="t">سجل الأفكار</span><a class="btn primary" href="/cbt/thought-record">افتح</a></div>
      <div class="tile"><span class="t">التنشيط السلوكي (BA)</span><a class="btn primary" href="/cbt/ba">افتح</a></div>
      <div class="tile"><span class="t">سُلّم التعرض (ERP)</span><a class="btn primary" href="/cbt/exposures">افتح</a></div>
      <div class="tile"><span class="t">خطة جلسات</span><a class="btn primary" href="/cbt/plan">افتح</a></div>
    </div>
    <div class="card">
      <h3>🗂️ التشخيص (DSM)</h3>
      <p>أدخل دراسة الحالة بكلمات واضحة (عامية/فصحى) وسيقترح النظام تشخيصًا مرجّحًا.</p>
      <a class="btn secondary" href="/dsm">الانتقال إلى DSM</a>
    </div>
  </section>

  <footer>© {{year}} عربي سايكو — سرية وخصوصية عالية</footer>
</div>
</body></html>
"""

@app.route("/")
def home():
    from datetime import datetime
    return render_template_string(HOME, year=datetime.now().year)

# روابط تواصل (لو حبيت تضيفها لاحقًا)
@app.route("/contact/whatsapp")
def wa(): return redirect("https://wa.me/9665XXXXXXXX", code=302)
@app.route("/contact/telegram")
def tg(): return redirect("https://t.me/USERNAME", code=302)
@app.route("/contact/email")
def em(): return redirect("mailto:info@arabipsycho.com", code=302)

if __name__ == "__main__":
    # شغّل على نفس المنفذ اللي تستخدمه دائمًا
    app.run(host="0.0.0.0", port=10000, debug=True)
