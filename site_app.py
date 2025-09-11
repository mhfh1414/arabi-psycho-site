# site_app.py — ملف التشغيل الرئيسي
from __future__ import annotations
from flask import Flask

app = Flask(__name__)

# سجّل البلوبرنتات المتوفّرة
try:
    from home import home_bp
    app.register_blueprint(home_bp)
except Exception as e:
    print("home_bp not loaded:", e)

try:
    from dsm_suite import dsm_bp
    app.register_blueprint(dsm_bp)          # /dsm
except Exception as e:
    print("dsm_bp not loaded:", e)

try:
    from cbt_suite import cbt_bp
    app.register_blueprint(cbt_bp)          # /cbt و المسارات الفرعية
except Exception as e:
    print("cbt_bp not loaded:", e)

try:
    from addiction_suite import addiction_bp
    app.register_blueprint(addiction_bp)    # /addiction  (اختياري)
except Exception as e:
    print("addiction_bp not loaded:", e)

# هاندلر بسيط لـ 404 يظهر رابط العودة
@app.errorhandler(404)
def not_found(e):
    return (
        '<h2>404 — الصفحة غير موجودة</h2>'
        '<p><a href="/">العودة للواجهة</a></p>'
    ), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
