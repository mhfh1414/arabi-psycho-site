# -*- coding: utf-8 -*-
# site_app.py — ملف التشغيل الرئيسي لموقع عربي سايكو

from flask import Flask
from home import home_bp
from dsm_suite import dsm_bp
from cbt_suite import cbt_bp
from addiction_suite import addiction_bp

def create_app():
    app = Flask(__name__)

    # تسجيل جميع البلوبرنتس
    app.register_blueprint(home_bp, url_prefix="/")          # الصفحة الرئيسية
    app.register_blueprint(dsm_bp, url_prefix="/dsm")        # DSM
    app.register_blueprint(cbt_bp, url_prefix="/cbt")        # CBT
    app.register_blueprint(addiction_bp, url_prefix="/addiction")  # الإدمان

    return app

# هذا هو التطبيق الأساسي
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
