from flask import Flask, render_template

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")

# دراسة الحالة
@app.route("/case_study")
def case_study():
    return render_template("case_study.html")

# الأمراض النفسية (DSM-5)
@app.route("/dsm")
def dsm():
    return render_template("dsm.html")

# العلاج السلوكي المعرفي (CBT)
@app.route("/cbt")
def cbt():
    return render_template("cbt.html")

# الاختبارات النفسية والشخصية
@app.route("/tests")
def tests():
    return render_template("tests.html")

# علاج الإدمان
@app.route("/addiction")
def addiction():
    return render_template("addiction.html")

# طلب الطبيب
@app.route("/request_doctor")
def request_doctor():
    return render_template("request_doctor.html")

# طلب الأخصائي النفسي
@app.route("/request_specialist")
def request_specialist():
    return render_template("request_specialist.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
