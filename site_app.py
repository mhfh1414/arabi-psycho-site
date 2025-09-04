from flask import Flask, render_template

app = Flask(__name__)

# --------------------
# الصفحة الرئيسية (تحويل مباشر لقسم الاختبارات)
# --------------------
@app.route("/")
def home():
    # بدل index.html نرسل المستخدم مباشرة إلى صفحة الاختبارات
    return render_template("tests/index.html")


# --------------------
# قسم الاختبارات
# --------------------
@app.route("/tests")
def tests_home():
    return render_template("tests/index.html")


# اختبار نفسي
@app.route("/tests/psych")
def psych_test_page():
    return render_template("tests/psych_form.html")


@app.route("/tests/psych/result")
def psych_result_page():
    return render_template("tests/psych_result.html")


# اختبار الشخصية
@app.route("/tests/personality")
def personality_test_page():
    return render_template("tests/personality_form.html")


@app.route("/tests/personality/result")
def personality_result_page():
    return render_template("tests/personality_result.html")


# --------------------
# صفحة تشغيل اختبار عام
# --------------------
@app.route("/tests/run")
def test_run_page():
    return render_template("tests/test_run.html")


@app.route("/tests/result")
def test_result_page():
    return render_template("tests/test_result.html")


# --------------------
# تشغيل التطبيق
# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
