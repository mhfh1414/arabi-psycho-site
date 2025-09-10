# -*- coding: utf-8 -*-
# site_app.py — نقطة التشغيل الوحيدة للتطبيق

from flask import Flask, jsonify

# استيراد البلوبريـنتس (تأكّد أن هذه الملفات موجودة بنفس الأسماء)
from home import home_bp         # الواجهة
from dsm_suite import dsm_bp     # DSM
from cbt_suite import cbt_bp     # CBT
from addiction_suite import addiction_bp  # الإدمان

def create_app():
    app = Flask(__name__)

    # تسجيل البلوبريـنتس بمسارات ثابتة وواضحة
    app.register_blueprint(home_bp,       url_prefix="/")          # /
    app.register_blueprint(dsm_bp,        url_prefix="/")          # /dsm
    app.register_blueprint(cbt_bp,        url_prefix="/")          # /cbt
    app.register_blueprint(addiction_bp,  url_prefix="/")          # /addiction

    # فحص سريع للمسارات (اختياري): /routes يُظهر المسارات المتاحة
    @app.get("/routes")
    def routes():
        return jsonify(sorted([f"{r.rule} → {','.join(r.methods)}" 
                               for r in app.url_map.iter_rules()]))

    return app

# كائن التطبيق الذي يحتاجه gunicorn
app = create_app()

if __name__ == "__main__":
    # تشغيل محلي فقط
    app.run(host="0.0.0.0", port=5000, debug=True)
