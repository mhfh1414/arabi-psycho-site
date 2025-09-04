from flask import Flask, render_template
from tests.tests_psych import score_test, psych_info
from tests.tests_personality import personality_info
from services.recommend import get_recommendations

app = Flask(__name__)

# -----------------------------
# الصفحات الرئيسية
# -----------------------------
@app.route("/")
def index():
    return render_template("main/index.html")

@app.route("/dsm")
def dsm():
    return render_template("dsm/index.html")

@app.route("/cbt")
def cbt():
    return render_template("cbt/index.html")

@app.route("/case")
def case():
    return render_template("case/index.html")

@app.route("/tests")
def tests_home():
    return render_template("tests/index.html")

# -----------------------------
# اختبارات نفسية
# -----------------------------
@app.route("/tests/psych")
def tests_psych():
    # مثال تجريبي: نستدعي معلومات من ملف tests_psych
    info = psych_info()
    return render_template("tests/psych.html", info=info)

@app.route("/tests/personality")
def tests_personality():
    info = personality_info()
    return render_template("tests/personality.html", info=info)

# -----------------------------
# التوصيات
# -----------------------------
@app.route("/recommend")
def recommend():
    recs = get_recommendations()
    return render_template("recommend.html", recommendations=recs)

# -----------------------------
# معالجة الأخطاء
# -----------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("_shared/404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("_shared/500.html"), 500

# -----------------------------
# تشغيل التطبيق
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
