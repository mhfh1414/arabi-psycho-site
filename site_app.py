from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/case_study", methods=["GET", "POST"])
def case_study():
    if request.method == "POST":
        # نجمع البيانات ونمررها لصفحة DSM (العرض والتحليل)
        payload = {
            "full_name": request.form.get("full_name",""),
            "age": request.form.get("age",""),
            "gender": request.form.get("gender",""),
            "duration_days": request.form.get("duration_days",""),
            "symptoms": request.form.get("symptoms","").strip(),
            "history": request.form.get("history","").strip(),
        }
        # نرسلها إلى dsm.html لعرض التشخيص (DSM الكبير الحالي)
        return render_template("dsm.html", **payload)
    return render_template("case_study.html")

@app.route("/dsm")
def dsm():
    # إبقاء كتالوج DSM كما هو (لا نحذف شيء)
    return render_template("dsm.html")

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
    app.run(host="0.0.0.0", port=10000)
