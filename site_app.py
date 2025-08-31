from flask import Flask, render_template

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")

# صفحة DSM (الأمراض)
@app.route("/dsm")
def dsm():
    return render_template("dsm.html")

# صفحة العلاج السلوكي المعرفي CBT
@app.route("/cbt")
def cbt():
    return render_template("cbt.html")

# صفحة الاختبارات النفسية
@app.route("/tests")
def tests():
    return render_template("tests.html")

# صفحة دراسة الحالة
@app.route("/case-study")
def case_study():
    return render_template("case_study.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
