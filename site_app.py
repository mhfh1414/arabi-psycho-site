from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# المسار الموحد لدراسة الحالة + DSM
@app.route("/case_dsm", methods=["GET","POST"])
def case_dsm():
    if request.method == "POST":
        payload = {
            "full_name": request.form.get("full_name",""),
            "age": request.form.get("age",""),
            "gender": request.form.get("gender",""),
            "duration_days": request.form.get("duration_days",""),
            "symptoms": request.form.get("symptoms",""),
            "history": request.form.get("history",""),
        }
        return render_template("case_dsm.html", **payload)
    return render_template("case_dsm.html")

# تحويل قديم لو حاول أحد يدخل /case_study
@app.route("/case_study", methods=["GET","POST"])
def case_study_legacy():
    return redirect(url_for("case_dsm"), code=301)

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
    app.run(host="0.0.0.0", port=5000)
