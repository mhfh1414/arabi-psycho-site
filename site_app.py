from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def index():
    return render_template("index.html")

# صفحة الاختبارات
@app.route("/tests")
def tests():
    return render_template("tests.html")

# صفحة DSM
@app.route("/dsm")
def dsm():
    return render_template("dsm.html")

# صفحة CBT
@app.route("/cbt")
def cbt():
    return render_template("cbt.html")

# صفحة دراسة الحالة
@app.route("/case_study", methods=["GET", "POST"])
def case_study():
    if request.method == "POST":
        patient_name = request.form.get("patient_name")
        session_notes = request.form.get("session_notes")
        recommendations = request.form.get("recommendations")

        # هنا تقدر تحفظ البيانات في قاعدة بيانات أو ملف
        print("📝 دراسة حالة جديدة:")
        print("اسم العميل:", patient_name)
        print("ملاحظات الجلسة:", session_notes)
        print("التوصيات:", recommendations)

        return redirect(url_for("index"))

    return render_template("case_study.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
