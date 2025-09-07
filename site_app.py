# -*- coding: utf-8 -*-
# site_app.py — ملف التشغيل الرئيسي لمشروع عربي سايكو

from flask import Flask, redirect

# استيراد الوحدات (كل وحدة لها ملف خاص)
import home                   # الواجهة الرئيسية
import dsm_suite as dsm       # DSM (دراسة الحالة والتشخيص)
import cbt_suite as cbt       # CBT (الاختبارات والعلاج السلوكي المعرفي)
import addiction_suite as addiction  # الإدمان

def create_app():
    app = Flask(__name__)

    # ربط البلوبرنتس
    app.register_blueprint(home.bp)        # /
    app.register_blueprint(dsm.bp)         # /dsm
    app.register_blueprint(cbt.bp)         # /cbt
    app.register_blueprint(addiction.bp)   # /addiction

    # روابط التواصل
    @app.route("/contact/whatsapp")
    def contact_whatsapp():
        return redirect("https://wa.me/9665XXXXXXXX", code=302)

    @app.route("/contact/telegram")
    def contact_telegram():
        return redirect("https://t.me/USERNAME", code=302)

    @app.route("/contact/email")
    def contact_email():
        return redirect("mailto:info@arabipsycho.com", code=302)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
