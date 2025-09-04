from flask import Flask, render_template, request, jsonify
from tests import (
    score_test,
    psych_info,
    personality_test,
    recommend_based_on_psych,
    recommend_based_on_personality,
)

app = Flask(__name__)


# -------------------------
# الصفحة الرئيسية
# -------------------------
@app.route("/")
def index():
    return render_template("main/index.html")


# -------------------------
# صفحات رئيسية أخرى
# -------------------------
@app.route("/dsm")
def dsm_page():
    return render_template("dsm/dsm.html")

@app.route("/cbt")
def cbt_page():
    return render_template("cbt/cbt.html")

@app.route("/case")
def case_page():
    return render_template("case/case_study.html")


# -------------------------
# اختبارات نفسية
# -------------------------
@app.route("/tests/psych", methods=["GET", "POST"])
def psych_test_page():
    if request.method == "POST":
        # استلام الإجابات من الفورم
        answers = request.form.getlist("answers")
        score = score_test([int(x) for x in answers if x.isdigit()])
        info = psych_info(score)
        recommendation = recommend_based_on_psych(score)
        return render_template(
            "tests/psych_result.html",
            score=score,
            info=info,
            recommendation=recommendation,
        )
    return render_template("tests/psych_form.html")


# -------------------------
# اختبارات الشخصية
# -------------------------
@app.route("/tests/personality", methods=["GET", "POST"])
def personality_test_page():
    if request.method == "POST":
        answers = request.form.getlist("answers")
        result = personality_test(answers)
        recommendation = recommend_based_on_personality(result)
        return render_template(
            "tests/personality_result.html",
            result=result,
            recommendation=recommendation,
        )
    return render_template("tests/personality_form.html")


# -------------------------
# API Endpoint (اختياري)
# -------------------------
@app.route("/api/psych", methods=["POST"])
def api_psych_test():
    data = request.json
    answers = data.get("answers", [])
    score = score_test([int(x) for x in answers if str(x).isdigit()])
    info = psych_info(score)
    return jsonify({"score": score, "info": info})


# -------------------------
# معالجة الأخطاء
# -------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("_shared/404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("_shared/500.html"), 500


# -------------------------
# تشغيل التطبيق
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
