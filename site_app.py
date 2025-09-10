# -*- coding: utf-8 -*-
# site_app.py — ملف التشغيل الرئيسي للموقع

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# استيراد البلوبرنتس حسب الملفات الموجودة عندك
from home import home_bp            # "/" الواجهة
from dsm_suite import dsm_bp        # "/dsm"
from cbt_suite import cbt_bp        # "/cbt"
from addiction_suite import addiction_bp  # "/addiction"

def create_app():
    app = Flask(__name__)
    # دعم خلف عكس وكيل (Render/Heroku)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

    # تسجيل البلوبرنتس من غير url_prefix عشان المسارات تبقى نفسها
    app.register_blueprint(home_bp)
    app.register_blueprint(dsm_bp)
    app.register_blueprint(cbt_bp)
    app.register_blueprint(addiction_bp)

    # صحّة الخدمة
    @app.route("/health")
    def _health(): return "ok", 200

    return app

app = create_app()

if __name__ == "__main__":
    # للتشغيل المحلي فقط
    app.run(host="0.0.0.0", port=10000, debug=True)
