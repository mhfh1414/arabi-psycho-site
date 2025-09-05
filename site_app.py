from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret-key-change-me"   # غيرها لمفتاح سري خاص بك
app.permanent_session_lifetime = timedelta(hours=6)

# الصفحة الرئيسية
@app.route("/")
def index():
    return render_template("index.html")

# دراسة حالة
@app.route("/case_study", methods=["GET", "POST"])
def case_study():
    if request.method == "POST":
        # نحفظ بيانات الحالة في السيشن
        session["case_data"] = {
            "name": request.form.get("name"),
            "age": request.form.get("age"),
            "gender": request.form.get("gender"),
            "symptoms": request.form.get("symptoms"),
            "history": request.form.get("history"),
        }
        return redirect(url_for("dsm"))
    return render_template("case_study.html")

# DSM
@app.route("/dsm")
def dsm():
    case_data = session.get("case_data", {})
    return render_template("dsm.html", case_data=case_data)

# باقي الأقسام
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
