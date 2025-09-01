from flask import Flask, render_template, request
from modules import PSYCH_TESTS, score_psych, PERS_TESTS, score_personality, recommend_tests_from_case

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def index():
    return render_template("index.html")

# صفحة DSM
@app.route("/dsm")
def dsm():
    return render_template("dsm.html")

# صفحة الاختبارات
@app.route("/tests")
def tests():
    return render_template("tests.html", psych_tests=PSYCH_TESTS, pers_tests=PERS_TESTS)

# تشغيل اختبار نفسي
@app.route("/tests/psych/<test_id>", methods=["GET", "POST"])
def run_psych_test(test_id):
    test = next((t for t in PSYCH_TESTS if t["id"] == test_id), None)
    if not test:
        return render_template("404.html"), 404

    if request.method == "POST":
        answers = [int(x) for x in request.form.getlist("answer")]
        result = score_psych(test_id, answers)
        return render_template("test_result.html", result=result)

    return render_template("test_run.html", test=test)

# تشغيل اختبار شخصية
@app.route("/tests/personality/<test_id>", methods=["GET", "POST"])
def run_personality_test(test_id):
    test = next((t for t in PERS_TESTS if t["id"] == test_id), None)
    if not test:
        return render_template("404.html"), 404

    if request.method == "POST":
        answers = [int(x) for x in request.form.getlist("answer")]
        result = score_personality(test_id, answers)
        return render_template("test_result.html", result=result)

    return render_template("test_run.html", test=test)

# توصيات بناءً على حالة
@app.route("/recommend", methods=["POST"])
def recommend():
    case = request.form.get("case", "")
    recommendations = recommend_tests_from_case(case)
    return render_template("recommend.html", case=case, recommendations=recommendations)

# خطأ 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# خطأ 500
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
