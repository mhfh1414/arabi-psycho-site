# --- DSM Routes ---
from DSM5 import dsm
from flask import render_template, request, abort

@app.route("/dsm")
def dsm_list():
    q = (request.args.get("q") or "").strip()
    categories = dsm.CATEGORIES
    results = dsm.search(q) if q else None
    return render_template("dsm.html", categories=categories, q=q, results=results)

@app.route("/dsm/<cat_key>/<item_key>")
def dsm_detail(cat_key, item_key):
    cat = dsm.CATEGORIES.get(cat_key)
    if not cat:
        return abort(404)
    item = None
    for it in cat.get("items", []):
        if str(it.get("id")) == str(item_key) or str(it.get("key")) == str(item_key):
            item = it
            break
    if not item:
        return abort(404)
    return render_template("dsm_detail.html", category=cat, item=item)
