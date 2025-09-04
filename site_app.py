from flask import Flask, render_template, request
from tests.tests_psych import score_test, psych_info
from tests.tests_personality import personality_test
from tests.recommend import recommend

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("main/index.html")

# صفحة اختبارات نفسية عامة
@app.route("/tests/psych", methods=["GET", "POST"])
def psych_tests():
    if request.method == "POST":
        user_answers = request.form.getlist("answers")
        result = score_test(user_answers)
        return render_template("tests/result.html", result=result)
    return render_template("tests/psych.html")

# صفحة معلومات نفسية
@app.route("/tests/psych/info")
def psych_info_page():
    info = psych_info()
    return render_template("tests/info.html", info=info)

# صفحة اختبارات شخصية
@app.route("/tests/personality", methods=["GET", "POST"])
def personality_tests():
    if request.method == "POST":
        user_answers = request.form.getlist("answers")
        result = personality_test(user_answers)
        return render_template("tests/result.html", result=result)
    return render_template("tests/personality.html")

# صفحة التوصيات
@app.route("/recommend")
def recommend_page():
    recs = recommend()
    return render_template("tests/recommend.html", recs=recs)

# صفحة DSM
@app.route("/dsm")
def dsm_page():
    return render_template("dsm/dsm.html")

@app.route("/dsm/<int:disorder_id>")
def dsm_detail(disorder_id):
    # هنا تربطها مع data/dsm5 لاحقًا
    return render_template("dsm/dsm_detail.html", disorder_id=disorder_id)

# صفحة CBT
@app.route("/cbt")
def cbt_page():
    return render_template("cbt/cbt.html")

# صفحة دراسة حالة
@app.route("/case")
def case_page():
    return render_template("case/case_study.html")

# تشغيل التطبيق
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
