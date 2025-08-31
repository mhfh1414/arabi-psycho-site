from flask import Flask, render_template, request, abort
from DSM5 import dsm   # ملف DSM5/dsm.py اللي فيه البيانات

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def index():
    return render_template("index.html")

# قائمة DSM-5 (مع علاج)
@app.route("/dsm")
def dsm_list():
    q = (request.args.get("q") or "").strip()
    categories = dsm.CATEGORIES
    results = dsm.search(q) if q else None
    return render_template("dsm.html", categories=categories, q=q, results=results)

# تفاصيل الاضطراب (علاج)
@app.route("/dsm/<cat_key>/<item_key>")
def dsm_detail(cat_key, item_key):
    cat = dsm.CATEGORIES.get(cat_key)
    if not cat:
        abort(404)
    item = next(
        (it for it in cat.get("items", [])
         if str(it.get("id")) == str(item_key) or str(it.get("key")) == str(item_key)),
        None
    )
    if not item:
        abort(404)
    return render_template("dsm_detail.html", category=cat, item=item)

# صفحة العلاج المعرفي السلوكي CBT
@app.route("/cbt")
def cbt():
    return render_template("cbt.html")

# صفحة دراسة حالة
@app.route("/case")
def case_study():
    return render_template("case_study.html")

# صفحة الاختبارات
@app.route("/tests")
def tests():
    return render_template("tests.html")

# تشغيل محلي
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
