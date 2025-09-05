from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "change-me"      # غيّرها لقيمة سرّية
app.permanent_session_lifetime = timedelta(hours=6)

@app.route("/")
def home():
    return render_template("main/index.html")

# صفحة دراسة الحالة
@app.route("/case", methods=["GET", "POST"])
def case():
    if request.method == "POST":
        data = {
            "name":  request.form.get("name",""),
            "age":   request.form.get("age",""),
            "gender":request.form.get("gender",""),
            "cc":    request.form.get("cc",""),
            "hx":    request.form.get("hx",""),
            "rx":    request.form.get("rx",""),
            "risk":  request.form.get("risk",""),
        }
        session["case_info"] = data
        return redirect(url_for("dsm"))
    # GET
    return render_template("case_study.html")

# صفحة DSM-5 (تقرأ بيانات دراسة الحالة إن وُجدت)
@app.route("/dsm")
def dsm():
    case_info = session.get("case_info", {})
    return render_template("dsm.html", case_info=case_info)

# صفحات أخرى (اختياري)
@app.route("/cbt")
def cbt():
    return render_template("cbt.html")

@app.route("/tests")
def tests():
    return render_template("tests.html")

@app.route("/addiction")
def addiction():
    return render_template("addiction.html")

@app.route("/request/specialist")
def request_specialist():
    return render_template("request_specialist.html")

@app.route("/request/doctor")
def request_doctor():
    return render_template("request_doctor.html")

if __name__ == "__main__":
    app.run(debug=True)
