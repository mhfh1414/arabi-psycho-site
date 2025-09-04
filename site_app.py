from flask import Flask, render_template
from tests.tests_psych import score_test, psych_info
from tests.tests_personality import personality_test

app = Flask(__name__)


# الصفحة الرئيسية
@app.route("/")
def index():
    return render_template("main/index.html")


# صفحة الاختبار النفسي (عام)
@app.route("/test/psych")
def test_psych():
    results = score_test(["نعم", "لا", "yes"])  # تجربة افتراضية
    info = psych_info()
    return {"results": results, "info": info}


# صفحة اختبار الشخصية
@app.route("/test/personality")
def test_personality():
    results = personality_test(["A", "B", "C"])  # تجربة افتراضية
    return {"results": results}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
