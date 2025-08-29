from flask import Flask, render_template, jsonify, request
import json, os

app = Flask(__name__, template_folder="templates", static_folder="static")

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "data")
TESTS_DIR = os.path.join(DATA_DIR, "tests")

@app.route("/")
def index():
    return render_template("index.html", title="عربي سايكو")

# ----------------- Tests UI -----------------
@app.route("/tests")
def tests():
    return render_template("tests.html", title="الاختبارات")

@app.route("/api/tests/index")
def api_tests_index():
    items=[]
    if not os.path.exists(TESTS_DIR):
        return jsonify(items)
    for fname in os.listdir(TESTS_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(TESTS_DIR,fname),"r",encoding="utf-8") as f:
                d=json.load(f)
                items.append({"id":d["id"], "title":d["title"]})
    return jsonify(sorted(items, key=lambda x: x["title"]))

@app.route("/api/tests/<test_id>")
def api_test_def(test_id):
    path = os.path.join(TESTS_DIR, f"{test_id}.json")
    if not os.path.exists(path): return jsonify({"error":"not found"}), 404
    return app.response_class(open(path,"rb"), mimetype="application/json")

@app.route("/api/submit", methods=["POST"])
def api_submit_results():
    data = request.get_json(force=True)
    test_id = data.get("test_id")
    answers = data.get("answers", [])
    path = os.path.join(TESTS_DIR, f"{test_id}.json")
    if not os.path.exists(path): return jsonify({"text":"اختبار غير موجود"}), 400
    test = json.load(open(path,encoding="utf-8"))

    # helper: qid -> int value
    amap = {}
    for a in answers:
        try:
            amap[a["qid"]] = int(a.get("value") if a.get("value") not in [None,""] else 0)
        except:
            amap[a["qid"]] = 0

    scoring = test.get("scoring","sum")
    out = {}
    text = ""

    if scoring == "sum":
        score = sum(amap.get(q["id"],0) for q in test["questions"])
        label = "غير محدد"
        for band in test.get("cutoffs", []):
            if band["min"] <= score <= band["max"]:
                label = band["label"]; break
        text = f"مجموعك = {score} → {label}"
        out = {"total": score, "severity": label}

    elif scoring == "count_yes":
        score = sum(1 for a in answers if str(a.get("value")).strip()=="نعم")
        label = "غير محدد"
        for band in test.get("cutoffs", []):
            if band["min"] <= score <= band["max"]:
                label = band["label"]; break
        text = f"عدد (نعم) = {score} → {label}"
        out = {"count_yes": score, "severity": label}

    elif scoring == "dass21":
        # كل مقياس 7 بنود؛ نضرب ×2 كما هو شائع لملاءمة معايير الشدة
        multiply = test.get("multiply",2)
        results = {}
        for scale in test["scales"]:
            s = sum(amap.get(qid,0) for qid in scale["items"]) * multiply
            # حدد الشدة من cutoffs
            label="غير محدد"
            for band in test["cutoffs"][scale["id"]]:
                if band["min"] <= s <= band["max"]:
                    label = band["label"]; break
            results[scale["name"]] = {"score": s, "severity": label}
        out = results
        text = " | ".join([f'{k}: {v["score"]} → {v["severity"]}' for k,v in results.items()])

    elif scoring == "tipi":
        # 5 سمات، عنصران لكل سمة، بعض العناصر عكسية (1..7)
        traits = {}
        for tr in test["traits"]:
            vals=[]
            for it in tr["items"]:
                v = amap.get(it["id"],0)
                vals.append(8 - v if it.get("reverse") else v)
            mean = round(sum(vals)/len(vals),2)
            traits[tr["name"]] = mean
        out = traits
        text = " | ".join([f"{k}: {v}/7" for k,v in traits.items()])

    else:
        text = "تم استلام الإجابات."

    return jsonify({"text": text, "details": out})

# ----------------- DSM -----------------
@app.route("/dsm")
def dsm():
    return render_template("dsm.html", title="DSM-5")

@app.route("/api/dsm/index")
def api_dsm_index():
    path = os.path.join(DATA_DIR, "dsm_index.json")
    return app.response_class(open(path,"rb"), mimetype="application/json")

# ----------------- CBT -----------------
@app.route("/cbt")
def cbt():
    return render_template("cbt.html", title="CBT")

@app.route("/cbt/submit", methods=["POST"])
def cbt_submit():
    # هنا تقدر تخزن الخطط لاحقًا في قاعدة/ملف/Google Sheets
    return render_template("cbt.html", title="CBT")

# ----------------- Health -----------------
@app.route("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)
