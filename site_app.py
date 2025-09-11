# -*- coding: utf-8 -*-
# site_app.py — نقطة تشغيل موحّدة للموقع (WSGI)

from __future__ import annotations
from flask import Flask

# استيراد الصفحات/السوتس
from home import home_bp               # واجهة الموقع
from dsm_suite import dsm_bp           # دراسة الحالة + DSM (يقرأ من dsm_criteria)
from cbt_suite import cbt_bp           # CBT (اختبارات + أدوات)
from addiction_suite import addiction_bp  # برنامج الإدمان

def create_app() -> Flask:
    app = Flask(__name__)

    # تسجيل الـ Blueprints
    app.register_blueprint(home_bp)        # /
    app.register_blueprint(dsm_bp)         # /dsm
    app.register_blueprint(cbt_bp, url_prefix="/cbt")          # /cbt/...
    app.register_blueprint(addiction_bp, url_prefix="/addiction")  # /addiction/...

    # صحّة بسيطة
    @app.get("/healthz")
    def _health():
        return {"ok": True}

    return app

# كائن التطبيق المطلوب لـ gunicorn:  site_app:app
app = create_app()
