# -*- coding: utf-8 -*-
# ملف التشغيل الرئيسي: يحمّل كل الـ Blueprints ويشغل التطبيق
from flask import Flask

# استيراد الـ Blueprints من ملفاتك الحالية
from home import home_bp
from dsm_suite import dsm_bp
from cbt_suite import cbt_bp
from addiction_suite import addiction_bp

def create_app():
    app = Flask(__name__)
    # تسجيل كل المسارات
    app.register_blueprint(home_bp)        # "/" + /contact/*
    app.register_blueprint(dsm_bp)         # "/dsm"
    app.register_blueprint(cbt_bp)         # "/cbt" وباقي مسارات cbt
    app.register_blueprint(addiction_bp)   # "/addiction" وباقي مسارات الإدمان
    return app

# متغيّر app ليتعرّف عليه Gunicorn من Procfile
app = create_app()

if __name__ == "__main__":
    # للتشغيل المحلي
    app.run(host="0.0.0.0", port=10000, debug=True)
