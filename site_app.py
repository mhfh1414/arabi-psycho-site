# -*- coding: utf-8 -*-
from flask import Flask
from home import home_bp
from dsm_suite import dsm_bp
from cbt_suite import cbt_bp
from addiction_suite import addiction_bp

def create_app():
    app = Flask(__name__)

    # تسجيل البلوبرنت لكل ملف
    app.register_blueprint(home_bp)
    app.register_blueprint(dsm_bp, url_prefix="/dsm")
    app.register_blueprint(cbt_bp, url_prefix="/cbt")
    app.register_blueprint(addiction_bp, url_prefix="/addiction")

    return app

# المتغير app لازم يكون موجود عشان Render أو Gunicorn يشغل الموقع
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
