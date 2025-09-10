# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, render_template_string

home_bp = Blueprint("home", __name__)

HOME_HTML = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>عربي سايكو | الرئيسية</title>
<style>body{font-family:Tahoma,Arial;direction:rtl;background:#0a3a75;color:#fff;margin:0}
.wrap{max-width:1000px;margin:auto;padding:24px}
a.btn{display:inline-block;background:#f4b400;color:#2b1b02;padding:12px 16px;border-radius:10px;text-decoration:none;margin:6px}
.card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);padding:16px;border-radius:12px;margin:12px 0}
</style></head><body><div class="wrap">
<h1>عربي سايكو</h1>
<p>مرحبًا! اختر خدمة:</p>
<div class="card">
  <a class="btn" href="/dsm">📋 دراسة حالة + تشخيص (DSM)</a>
  <a class="btn" href="/cbt">🧠 اختبارات + CBT</a>
  <a class="btn" href="/addiction">🚭 تقييم الإدمان</a>
</div>
<div class="card">
  <a class="btn" href="/contact/whatsapp">واتساب</a>
  <a class="btn" href="/contact/telegram">تلجرام</a>
  <a class="btn" href="/contact/email">إيميل</a>
</div>
<p><a class="btn" href="/routes">عرض قائمة المسارات</a></p>
</div></body></html>
"""

@home_bp.route("/")
def home_index():
    return render_template_string(HOME_HTML)

@home_bp.route("/contact/whatsapp")
def contact_whatsapp():
    return redirect("https://wa.me/9665XXXXXXXX", code=302)

@home_bp.route("/contact/telegram")
def contact_telegram():
    return redirect("https://t.me/USERNAME", code=302)

@home_bp.route("/contact/email")
def contact_email():
    return redirect("mailto:info@arabipsycho.com", code=302)
