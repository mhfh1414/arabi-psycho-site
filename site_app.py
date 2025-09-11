# -*- coding: utf-8 -*-
# site_app.py — التطبيق الرئيسي

from __future__ import annotations
from flask import Flask, redirect

app = Flask(__name__)

# استيراد الـ Blueprints بالأسماء الصحيحة (حسب ملفاتك الحالية)
from home import home_bp               # home.py  -> home_bp
from cbt_suite import cbt_bp           # cbt_suite.py -> cbt_bp
from dsm_suite import dsm_bp           # dsm_suite.py -> dsm_bp
from addiction_suite import addiction_bp  # addiction_suite.py -> addiction_bp

# تسجيل الـ Blueprints (لا تضيف url_prefix هنا لأن بعضها مضمّن داخل الملف)
app.register_blueprint(home_bp)          # "/" و "/home"
app.register_blueprint(cbt_bp)           # يحتوي url_prefix="/cbt" داخل الملف
app.register_blueprint(dsm_bp)           # يعرّف المسار "/dsm" داخل الملف
app.register_blueprint(addiction_bp)     # يعرّف "/addiction" داخل الملف

# إعادة توجيه الجذر دائماً للواجهة
@app.route("/")
def _root():
    return redirect("/home")

# مسارات التواصل البسيطة (إن لم تكن مضافة)
@app.route("/contact/whatsapp")
def contact_whatsapp():
    return redirect("https://wa.me/")  # ضع رقمك

@app.route("/contact/telegram")
def contact_telegram():
    return redirect("https://t.me/")   # ضع معرفك

@app.route("/contact/email")
def contact_email():
    return "راسلنا على البريد: support@arabipsycho.example"  # عدّلها

# معرّف التشغيل لـ gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
