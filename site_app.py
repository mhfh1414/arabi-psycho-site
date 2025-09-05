from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)
app.secret_key = "change-me"  # غيّرها

@app.route("/")
def index():
    return render_template("index.html")  # صفحتك الرئيسية الحالية

@app.route("/case_study", methods=["GET", "POST"])
def case_study():
    if request.method == "POST":
        session["case"] = {
            "name": request.form.get("name", "").strip(),
            "age": request.form.get("age", "").strip(),
            "gender": request.form.get("gender", ""),
            "duration": request.form.get("duration", "").strip(),
            "symptoms": request.form.get("symptoms", "").strip(),
            "history": request.form.get("history", "").strip(),
        }
        return redirect(url_for("dsm"))
    return render_template("case_study.html")

@app.route("/dsm")
def dsm():
    case = session.get("case", {})
    # منطق بسيط مؤقّت (بدون محرّك): مجرّد أمثلة على النتيجة
    results, flags = [], []
    text = (case.get("symptoms","") + " " + case.get("history","")).lower()

    if any(k in text for k in ["انتحار","أؤذي نفسي","قتل نفسي"]):
        flags.append("⚠️ وجود مؤشرات خطورة على النفس — يلزم تدخل عاجل")

    if text:
        if any(k in text for k in ["قلق","توتر","أرق","خفقان"]):
            results.append({
                "name":"قلق معمّم","group":"القلق","score":0.78,
                "met":4,"min_required":3,"duration_required":180,
                "matched_keys":["توتر","أرق","تعب","قلق مفرط"],
                "red_flags":[],"tips":["CBT وتمارين الاسترخاء"]
            })
        if any(k in text for k in ["حزن","كآبة","فقدان المتعة"]):
            results.append({
                "name":"نوبة اكتئابية كبرى","group":"المزاج","score":0.72,
                "met":5,"min_required":5,"duration_required":14,
                "matched_keys":["حزن","فقدان المتعة","أرق","ذنب","تشتت"],
                "red_flags":["أفكار انتحار"] if "انتحار" in text else [],
                "tips":["مراجعة مختص، وCBT"]
            })

    return render_template("dsm.html", case=case, results=results, flags=flags)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
