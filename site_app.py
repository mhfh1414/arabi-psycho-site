from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "change-me"
app.permanent_session_lifetime = timedelta(hours=6)

@app.route("/")
def index():
    # لو عندك صفحة رئيسية مخصّصة، استبدلها بـ index.html
    return redirect(url_for("case_study"))

@app.route("/case_study", methods=["GET", "POST"])
def case_study():
    if request.method == "POST":
        session["case_data"] = {
            "name": request.form.get("name","").strip(),
            "age": request.form.get("age","").strip(),
            "gender": request.form.get("gender",""),
            "duration": request.form.get("duration_days","").strip(),
            "symptoms": request.form.get("symptoms","").strip(),
            "history": request.form.get("history","").strip(),
        }
        return redirect(url_for("dsm"))
    return render_template("case_study.html")

@app.route("/dsm")
def dsm():
    # نمرّر بيانات دراسة الحالة للصفحة لتهيئتها تلقائيًا
    return render_template("dsm.html", case_data=session.get("case_data", {}))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
