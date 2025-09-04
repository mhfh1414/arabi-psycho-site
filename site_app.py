# site_app.py
from flask import Flask, render_template
from tests.tests_psych import score_test, psych_info
from tests.tests_personality import personality_test

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("main/index.html")

# صفحة DSM
@app.route("/dsm")
def dsm_page():
    return render_template("dsm/dsm.html")

# صفحة CBT
@app.route("/cbt")
def cbt_page():
    return render_template("cbt/cbt.html")

# صفحة دراسة حالة
@app.route("/case")
def case_page():
    return render_template("case/case_study.html")

# صفحة اختبارات عامة (نفسي)
@app.route("/tests/psych")
def psych_test_page():
    result = score_test(["نعم", "لا", "yes"])
    return render_template("tests/psych_test.html", result=result)

# صفحة اختبارات شخصية
@app.route("/tests/personality")
def personality_test_page():
    result = personality_test(["A", "B", "C"])
    return render_template("tests/personality_test.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
