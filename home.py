# -*- coding: utf-8 -*-
from flask import Blueprint, render_template_string, url_for
from datetime import datetime

home_bp = Blueprint("home", __name__)

PAGE = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>عربي سايكو</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap" rel="stylesheet">
<style>
:root{--b:#0a3a75;--b2:#0a65b0;--gold:#f4b400;--g:rgba(255,255,255,.12)}
*{box-sizing:border-box}body{margin:0;font-family:Tajawal,system-ui;background:linear-gradient(135deg,var(--b),var(--b2));color:#fff}
.wrap{max-width:1100px;margin:40px auto;padding:0 16px}
.head{display:flex;justify-content:space-between;align-items:center}
.logo{display:flex;gap:12px;align-items:center}
.logo span{display:inline-flex;width:54px;height:54px;border-radius:14px;background:rgba(255,255,255,.08);border:1px solid var(--g);align-items:center;justify-content:center;font-weight:800;color:#f4b400}
h1{margin:0;background:linear-gradient(90deg,#ffd86a,#f4b400);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:28px}
.card{background:rgba(255,255,255,.06);border:1px solid var(--g);border-radius:16px;padding:20px}
.btn{display:inline-block;background:linear-gradient(145deg,#ffd86a,#f4b400);color:#2b1b02;padding:12px 18px;border-radius:12px;text-decoration:none;font-weight:800}
.links a{color:#fff;text-decoration:none;margin-inline:8px;padding:8px 12px;border-radius:10px;background:rgba(255,255,255,.08);border:1px solid var(--g)}
</style></head><body>
<div class="wrap">
  <div class="head">
    <div class="logo"><span>AS</span>
      <div><h1>عربي سايكو</h1><small>المركز العربي للصحة النفسية</small></div>
    </div>
    <div class="links">
      <a href="https://wa.me/966000000000">واتساب</a>
      <a href="https://t.me/your_channel">تلجرام</a>
      <a href="mailto:info@arabipsycho.com">إيميل</a>
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <h3>📖 التشخيص وفق DSM-5</h3>
      <p>نظام موحّد: دراسة حالة + تشخيص تلقائي.</p>
      <a class="btn" href="{{ url_for('dsm.dsm_unified') }}">ابدأ الآن</a>
    </div>
    <div class="card">
      <h3>🧠 CBT + الاختبارات</h3>
      <p>حزمة CBT مع اختبارات قياسية (PHQ-9 / GAD-7 / PCL-5 ...).</p>
      <a class="btn" href="{{ url_for('cbt.cbt_home') }}">الدخول</a>
    </div>
    <div class="card">
      <h3>🚭 علاج الإدمان</h3>
      <p>تقييم وخطط علاجية وتأهيل ومتابعة.</p>
      <a class="btn" href="{{ url_for('addiction.addiction_home') }}">ابدأ التقييم</a>
    </div>
  </div>

  <p style="opacity:.8;margin-top:26px">© {{year}} عربي سايكو — جميع الحقوق محفوظة</p>
</div>
</body></html>
"""

@home_bp.route("/")
def home():
    return render_template_string(PAGE, year=datetime.now().year)
