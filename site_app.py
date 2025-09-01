from flask import Flask, render_template, request
from modules import PSYCH_TESTS, PERS_TESTS, score_psych, score_personality, recommend_tests

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def index():
    return render_template("index.html")

# صفحة DSM
@app.route("/dsm")
def dsm():
    return render_template("dsm.html")

# تفاصيل DSM
@app.route("/dsm/<string:disorder>")
def dsm_detail(disorder):
    return render_template("dsm_detail.html", disorder=disorder)

# صفحة الاختبارات
@app.route("/tests")
def tests():
    return render_template("tests.html")

# تشغيل اختبار نفسي
@app.route("/tests/psych/<string:test_id>", methods=["GET", "POST"])
def run_psych_test(test_id):
    if request.method == "POST":
        answers = request.form.to_dict()
        score = score_psych(test_id, answers)
        return render_template("test_result.html", score=score, test_id=test_id)
    return render_template("test_run.html", test_id=test_id, questions=PSYCH_TESTS.get(test_id, []))

# تشغيل اختبار شخصية
@app.route("/tests/personality/<string:test_id>", methods=["GET", "POST"])
def run_personality_test(test_id):
    if request.method == "POST":
        answers = request.form.to_dict()
        score = score_personality(test_id, answers)
        return render_template("test_result.html", score=score, test_id=test_id)
    return render_template("test_run.html", test_id=test_id, questions=PERS_TESTS.get(test_id, []))

# صفحة التوصيات
@app.route("/recommend")
def recommend():
    tests = recommend_tests()
    return render_template("tests.html", tests=tests)

# ✅ صفحة دراسة الحالة (case_study)
@app.route("/case_study")
def case_study():
    return render_template("case_study.html")

# صفحة 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# صفحة 500
@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
