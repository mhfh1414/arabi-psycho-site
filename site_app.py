# -*- coding: utf-8 -*-
# site_app.py — نقطة تشغيل التطبيق (Flask + Blueprints)

from flask import Flask

# استيراد الـ Blueprints من الملفات الموجودة عندك
# تأكد أن كل ملف يعرّف Blueprint بهذه الأسماء:
# home.py            -> home_bp
# cbt_suite.py       -> cbt_bp
# addiction_suite.py -> addiction_bp
# dsm_suite.py       -> dsm_bp
from home import home_bp
from cbt_suite import cbt_bp
from addiction_suite import addiction_bp
from dsm_suite import dsm_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # تسجيل الـ Blueprints
    # ملاحظة: اترك home بدون prefix ليكون على "/"
    app.register_blueprint(home_bp)                           # "/"
    app.register_blueprint(dsm_bp,       url_prefix="/dsm")   # "/dsm"
    app.register_blueprint(cbt_bp,       url_prefix="/cbt")   # "/cbt"
    app.register_blueprint(addiction_bp, url_prefix="/addiction")  # "/addiction"

    # مسار صحي للفحص السريع
    @app.get("/_health")
    def _health():
        return "ok", 200

    # صفحة 404 أبسط مع تلميح بالمسارات المتاحة
    @app.errorhandler(404)
    def not_found(e):
        return (
            "404 Not Found — المسار غير صحيح. جرّب: /  /dsm  /cbt  /addiction",
            404,
        )

    return app


# مهم: متغير app موجود لِـ gunicorn حسب Procfile (web: gunicorn site_app:app)
app = create_app()

if __name__ == "__main__":
    # تشغيل محلي
    app.run(host="0.0.0.0", port=10000, debug=True)
