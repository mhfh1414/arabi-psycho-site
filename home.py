# -*- coding: utf-8 -*-
# home.py — واجهة أنيقة وخفيفة

from flask import Blueprint, render_template_string, redirect

home_bp = Blueprint("home", __name__)

HTML = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>عربي سايكو | الرئيسية</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{--b1:#081f3a;--b2:#0a4e8a;--w:#fff;--g:#ffd54a}
*{box-sizing:border-box} body{margin:0;font-family:"Tajawal",system-ui;background:linear-gradient(135deg,var(--b1),var(--b2));color:var(--w)}
.wrap{max-width:860px;margin:48px auto;padding:16px}
h1{margin:0 0 8px}
.sub{opacity:.9;margin:.2rem 0 1.2rem}
.grid{display:grid;gap:12px}
a.btn{display:block;text-decoration:none;text-align:center;font-weight:800;
      background:linear-gradient(180deg,#ffe27a,var(--g));color:#1f1402;
      padding:16px;border-radius:14px;border:1px solid #fff2}
a.sec{background:#ffffff22;color:#fff;border-color:#ffffff33}
.links{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.chip{background:#ffffff22;border:1px solid #ffffff33;color:#fff;padding:8px 10px;border-radius:999px;text-decoration:none}
</style></head><body><div class="wrap">
  <h1>مرحبًا في <b>عربي سايكو</b></h1>
  <p class="sub">تشخيص مبدئي دقيق (DSM) + اختبارات موثوقة + أدوات الإدمان</p>

  <div class="grid">
    <a class="btn" href="/dsm">📋 التشخيص + دراسة حالة (DSM)</a>
    <a class="btn sec" href="/cbt">🧠 العلاج السلوكي المعرفي + الاختبارات</a>
    <a class="btn sec" href="/addiction">🚭 الإدمان والتعافي</a>
  </div>

  <div class="links">
    <a class="chip" href="/contact/telegram">تلجرام</a>
    <a class="chip" href="/contact/email">إيميل</a>
  </div>
</div></body></html>
"""

@home_bp.route("/")
def home():
    return render_template_string(HTML)

@home_bp.route("/contact/telegram")
def tg():
    return redirect("https://t.me/USERNAME", code=302)

@home_bp.route("/contact/email")
def em():
    return redirect("mailto:info@arabipsycho.com", code=302)
