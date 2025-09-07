# -*- coding: utf-8 -*-
# site_app.py — ملف التشغيل الرئيسي الصحيح

from flask import Flask
from home import home_bp            # ← انتبه للاسم
from dsm_suite import dsm_bp
from cbt_suite import cbt_bp
from addiction_suite import addiction_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp)        # كان home.bp ← يصلّح الخطأ
    app.register_blueprint(dsm_bp)
    app.register_blueprint(cbt_bp)
    app.register_blueprint(addiction_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
