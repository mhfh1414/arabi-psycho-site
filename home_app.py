# -*- coding: utf-8 -*-
# home_app.py — ملف التشغيل الرئيسي

from __future__ import annotations
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)

# سجّل البلوبربنتس (DSM / CBT) إن وجدت
# DSM
try:
    from dsm_suite import dsm_bp  # مساره /dsm
    app.register_blueprint(dsm_bp)
except Exception as e:
    print("DSM not registered:", e)

# CBT
try:
    from cbt_suite import cbt_bp  # مساره /cbt
    app.register_blueprint(cbt_bp)
except Exception as e:
    print("CBT not registered:", e)

# (اختياري) الإدمان إن كان عندك Blueprint داخل addiction_suite.py
try:
    from addiction_suite import addiction_bp  # إن لم يوجد تجاهل
    app.register_blueprint(addiction_bp)
except Exception as e:
    print("Addiction not registered:", e)

# صفحة رئيسية بسيطة ومنسقة
HOME_HTML = """
<!doctype html><html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>عربي سايكو | المنصة</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400;--ink:#0b1220}
*{box-sizing:border-box} body{margin:0;font-family:"Tajawal",system-ui;background:linear-gradient(135deg,var(--bg1),var(--bg2));color:#fff}
.wrap{max-width:1100px;margin:28px auto;padding:14px}
.hero{display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px}
.logo{width:42px;height:42px;border-radius:10px;background:linear-gradient(180deg,#ffd86a,#f4b400);display:flex;align-items:center;justify-content:center;color:var(--ink);font-weight:900}
.tag{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.18);padding:6px 10px;border-radius:999px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:980px){.grid{grid-template-columns:1fr}}
.card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:18px;padding:18px}
.btn{display:inline-block;background:linear-gradient(180deg,#ffd86a,#f4b400);color:#1d1502;text-decoration:none;padding:12px 16px;border-radius:14px;font-weight:800}
.btn.alt{background:#9bd5ff;color:#04223d}
ul{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:10px}
h1{margin:.2rem 0 0;font-size:2rem}
h3{margin:.2rem 0 10px}
small{opacity:.85}
.footer{opacity:.75;margin-top:18px}
.kv{display:flex;flex-direction:column;gap:10px}
.kv .row{display:flex;gap:10px;flex-wrap:wrap}
.kv .pill{flex:1;min-width:180px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:10px}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <div class="brand">
      <div class="logo">AS</div>
      <div>
        <h1>عربي سايكو</h1>
        <small>منصة نفسية عربية — تشخيص مبدئي، اختبارات قياس، وأدوات CBT عملية.</small>
      </div>
    </div>
    <div class="tag">الخصوصية والسرية محفوظة</div>
  </div>

  <div class="grid">
    <section class="card">
      <h3>🗂️ التشخيص ودراسة الحالة (DSM)</h3>
      <p>محرك مطابقات ذكي للأعراض بالعربية مع مراعاة المدة والأثر الوظيفي لإعطاء تشخيص مرجّح واحد.</p>
      <a class="btn" href="/dsm">ابدأ دراسة الحالة</a>
    </section>

    <section class="card">
      <h3>🧪 العلاج السلوكي المعرفي + اختبارات</h3>
      <p>لوحة CBT متكاملة: PHQ-9، GAD-7، PCL-5، DASS-21 + سجل أفكار، تنشيط سلوكي، سُلّم التعرض وخطة جلسات.</p>
      <a class="btn" href="/cbt">افتح لوحة CBT</a>
    </section>
  </div>

  <div class="card" style="margin-top:12px">
    <h3>لمحة سريعة</h3>
    <div class="kv">
      <div class="row">
        <div class="pill">تشخيص مرجّح واحد بدل قائمة طويلة من الاحتمالات</div>
        <div class="pill">لغة عربية طبيعية ومراعاة المرادفات العامية</div>
        <div class="pill">نتائج القياس تُعين على خطة علاج قابلة للمتابعة</div>
      </div>
    </div>
  </div>

  <p class="footer">© {{y}} عربي سايكو</p>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    from datetime import datetime
    return render_template_string(HOME_HTML, y=datetime.now().year)

@app.get("/healthz")
def healthz():
    return "ok", 200

# للتشغيل المحلي فقط
if __name__ == "__main__":
    app.run(debug=True, port=5000)
