from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "change-me"  # غيّرها لقيمة سرية
app.permanent_session_lifetime = timedelta(hours=6)

# الصفحة الرئيسية
@app.route("/")
def index():
    return render_template("index.html")

# صفحة دراسة الحالة
@app.route("/case_study", methods=["GET", "POST"])
def case_study():
    if request.method == "POST":
        # نخزن بيانات النموذج في السيشن
        session["case_data"] = {
            "name": request.form.get("name"),
            "age": request.form.get("age"),
            "gender": request.form.get("gender"),
            "symptoms": request.form.get("symptoms"),
            "history": request.form.get("history"),
        }
        # بعد الإرسال نوجّه مباشرة إلى DSM
        return redirect(url_for("dsm"))

    return render_template("case_study.html")

# صفحة DSM
@app.route("/dsm")
def dsm():
    case_data = session.get("case_data")
    diagnosis = None

    # تشخيص مبدئي بسيط (تقدر تطوّره لاحقاً)
    if case_data and case_data.get("symptoms"):
        text = case_data["symptoms"]
        if "قلق" in text:
            diagnosis = "احتمال اضطراب قلق"
        elif "حزن" in text or "اكتئاب" in text:
            diagnosis = "احتمال اضطراب اكتئابي"
        elif "وسواس" in text:
            diagnosis = "احتمال وسواس قهري"
        else:
            diagnosis = "لا توجد مؤشرات كافية للتشخيص"

    return render_template("dsm.html", case_data=case_data, diagnosis=diagnosis)

# بقية الأقسام
@app.route("/tests")
def tests():
    return render_template("tests.html")

@app.route("/cbt")
def cbt():
    return render_template("cbt.html")

@app.route("/addiction")
def addiction():
    return render_template("addiction.html")

@app.route("/request_doctor")
def request_doctor():
    return render_template("request_doctor.html")

@app.route("/request_specialist")
def request_specialist():
    return render_template("request_specialist.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
