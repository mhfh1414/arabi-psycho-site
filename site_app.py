from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from DSM5.dsm import get_categories, get_disorder_by_id, search_disorders

app = Flask(__name__)
app.secret_key = "super-secret"  # لرسائل الفلاش المؤقتة

# ---------------------------
# الصفحات العامة
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dsm")
def dsm():
    q = request.args.get("q", "").strip()
    if q:
        hits = search_disorders(q)  # يرجع [{'category':..., 'item':{...}}]
        return render_template("dsm.html", q=q, hits=hits, categories=None)
    categories = get_categories()
    return render_template("dsm.html", q="", hits=None, categories=categories)

@app.route("/dsm/<cat>/<item_id>")
def dsm_detail(cat, item_id):
    item = get_disorder_by_id(cat, item_id)
    if not item:
        flash("العنصر المطلوب غير موجود")
        return redirect(url_for("dsm"))
    return render_template("dsm_detail.html", item=item, cat=cat)

@app.route("/cbt")
def cbt():
    return render_template("cbt.html")

@app.route("/tests")
def tests():
    return render_template("tests.html")

@app.route("/case-study", methods=["GET", "POST"])
def case_study():
    if request.method == "POST":
        data = request.form.to_dict(flat=True)
        # مؤقتًا نطبعها في اللوجز وتظهر لك في Render
        app.logger.info("CASE_SUBMISSION: %s", data)
        flash("تم حفظ دراسة الحالة بنجاح (مؤقتًا في السجلات).")
        return redirect(url_for("case_study"))
    return render_template("case_study.html")

# API صغيرة لاختبار البحث السريع
@app.route("/api/dsm/search")
def api_dsm_search():
    q = request.args.get("q", "")
    return jsonify(search_disorders(q))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
