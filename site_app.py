# site_app.py
from flask import Flask, render_template, request
import re
from services.dsm_data import DSM_DB   # ← كل الأمراض هنا

app = Flask(__name__)

def normalize(s: str) -> str:
    s = s.strip()
    s = re.sub(r"[ًٌٍَُِّْـ]", "", s)
    s = s.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ة","ه").replace("ى","ي")
    return s

def score_diagnoses(symptoms_text: str):
    text = normalize(symptoms_text or "")
    scores = {}
    for disorder, keywords in DSM_DB.items():
        sc = sum(1 for kw in keywords if normalize(kw) in text)
        if sc:
            scores[disorder] = sc
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dsm", methods=["GET","POST"])
def dsm():
    diagnosis = None
    name = age = gender = duration = history = symptoms = ""
    if request.method == "POST":
        name     = request.form.get("name","")
        age      = request.form.get("age","")
        gender   = request.form.get("gender","")
        duration = request.form.get("duration","")
        symptoms = request.form.get("symptoms","")
        history  = request.form.get("history","")

        ranked = score_diagnoses(symptoms)
        if ranked:
            top = [f"{d} <span class='badge ok'>مطابقة تقريبية ({pts})</span>" for d, pts in ranked[:3]]
            diagnosis = f"<strong>أقرب التشخيصات:</strong><br>" + "<br>".join(top)
        else:
            diagnosis = "<span class='badge warn'>لا توجد أعراض كافية للتشخيص وفق القاموس المبسّط.</span>"

    return render_template("dsm.html",
                           name=name, age=age, gender=gender, duration=duration,
                           symptoms=symptoms, history=history, diagnosis=diagnosis)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
