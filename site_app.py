from flask import Flask, render_template, request

# استدعاءات من مجلد tests
from tests.tests_psych import score_test, psych_info
from tests.tests_personality import personality_test

# استدعاء من مجلد services
from services.recommend import recommend_plan

# إنشاء التطبيق
app = Flask(__name__)

# -------------------------
# المسارات الرئيسية
# -------------------------

@app.route("/")
def index():
    return render_template("main/index.html")

@app.route("/dsm")
def dsm():
    return render_template("dsm/dsm.html")

@app.route("/cbt")
def cbt():
    return render_template("cbt/cbt.html")

@app.route("/case")
def case():
    return render_template("case/case_study.html")

# -------------------------
# اختبارات
# -------------------------

@app.route("/tests/psych", methods=["GET", "POST"])
def tests_psych():
    if request.method == "POST":
        user_answers = request.form.getlist("answers")
        result = score_test(user_answers)
        return render_template("tests/psych_result.html", result=result)
    return render_template("tests/psych_form.html")

@app.route("/tests/personality", methods=["GET", "POST"])
def tests_personality():
    if request.method == "POST":
        user_answers = request.form.getlist("answers")
        result = personality_test(user_answers)
        return render_template("tests/personality_result.html", result=result)
    return render_template("tests/personality_form.html")

# -------------------------
# توصيات / خطة علاجية
# -------------------------

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    plan = recommend_plan(data)
    return {"status": "ok", "plan": plan}

# -------------------------
# أخطاء مخصصة
# -------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template("_shared/404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("_shared/500.html"), 500

# -------------------------
# تشغيل التطبيق محلياً
# -------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
