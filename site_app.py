# -*- coding: utf-8 -*-
# site_app.py — ملف التشغيل الرئيسي

from flask import Flask
from home import home_bp
from dsm_suite import dsm_bp
from cbt_suite import cbt_bp
from addiction_suite import addiction_bp

def create_app():
    app = Flask(__name__)
    # تسجيل البلوبريـنتس
    app.register_blueprint(home_bp)        # /
    app.register_blueprint(dsm_bp)         # /dsm
    app.register_blueprint(cbt_bp)         # /cbt
    app.register_blueprint(addiction_bp)   # /addiction
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
