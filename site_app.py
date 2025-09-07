# -*- coding: utf-8 -*-
# site_app.py — ملف التشغيل الرئيسي لمشروع عربي سايكو

from flask import Flask, redirect

# استيراد الصفحات الأساسية
import dsm       # دراسة الحالة + التشخيص
import cbt       # العلاج السلوكي المعرفي + الاختبارات
import home      # الواجهة الرئيسية
import addiction # علاج الإدمان

app = Flask(__name__)

# ربط البلوبرنتس من الملفات المستقلة
app.register_blueprint(home.bp)
app.register_blueprint(dsm.bp)
app.register_blueprint(cbt.bp)
app.register_blueprint(addiction.bp)

# روابط التواصل (ثابتة)
@app.route("/contact/whatsapp")
def contact_whatsapp():
    return redirect("https://wa.me/9665XXXXXXXX", code=302)

@app.route("/contact/telegram")
def contact_telegram():
    return redirect("https://t.me/USERNAME", code=302)

@app.route("/contact/email")
def contact_email():
    return redirect("mailto:info@arabipsycho.com", code=302)

# تشغيل
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
