# -*- coding: utf-8 -*-
# site_app.py — ملف التشغيل الرئيسي لموقع عربي سايكو

from flask import Flask
from home import home_bp
from dsm_suite import dsm_bp
from addiction_suite import addiction_bp
from cbt import cbt_bp   # انتبه: هنا لازم اسم المجلد أو الملف صح

app = Flask(__name__)

# ================== تسجيل البلوبرنتات ==================
app.register_blueprint(home_bp)  # الواجهة الرئيسية على /
app.register_blueprint(dsm_bp, url_prefix="/dsm")  # DSM
app.register_blueprint(addiction_bp, url_prefix="/addiction")  # الإدمان
app.register_blueprint(cbt_bp, url_prefix="/cbt")  # CBT (اللي كان يعطيك 404)

# ================== التشغيل ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
