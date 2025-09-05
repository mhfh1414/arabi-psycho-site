from flask import Flask, render_template, request

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def index():
    return render_template("index.html")

# دراسة حالة
@app.route("/case_study", methods=["GET", "POST"])
def case_study():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        symptoms = request.form.get("symptoms")
        return f"<h2>تم استلام الحالة ✅</h2><p>الاسم: {name}</p><p>العمر: {age}</p><p>الأعراض: {symptoms}</p>"
    return render_template("case_study.html")

# الأمراض النفسية DSM-5
@app.route("/dsm")
def dsm():
    return render_template("dsm.html")

# الاختبارات النفسية والشخصية
@app.route("/tests")
def tests():
    return render_template("tests.html")

# العلاج السلوكي المعرفي CBT
@app.route("/cbt")
def cbt():
    return render_template("cbt.html")

# علاج الإدمان
@app.route("/addiction")
def addiction():
    return render_template("addiction.html")

# طلب الطبيب
@app.route("/request_doctor", methods=["GET", "POST"])
def request_doctor():
    if request.method == "POST":
        name = request.form.get("name")
        case = request.form.get("case")
        return f"<h2>تم إرسال طلب الطبيب ✅</h2><p>الاسم: {name}</p><p>الحالة: {case}</p>"
    return render_template("request_doctor.html")

# طلب الأخصائي النفسي
@app.route("/request_specialist", methods=["GET", "POST"])
def request_specialist():
    if request.method == "POST":
        name = request.form.get("name")
        notes = request.form.get("notes")
        return f"<h2>تم إرسال طلب الأخصائي النفسي ✅</h2><p>الاسم: {name}</p><p>ملاحظات: {notes}</p>"
    return render_template("request_specialist.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
