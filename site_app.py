# site_app.py
from flask import Flask, render_template, abort
from pathlib import Path

app = Flask(__name__, static_folder="static", template_folder="templates")

# ✅ صفحتك الرئيسية
@app.route("/", endpoint="home")
def home():
    return render_template("index.html")

# ✅ هنا تعرّف الصفحات الأساسية مرة واحدة فقط
PAGES = {
    "dsm": "dsm_list.html",
    "cbt": "cbt_list.html",
    "tests": "tests_list.html",
    "addiction": "addiction_list.html",
    # تقدر تضيف أي قسم جديد بهالسطر:
    # "wechsler": "wechsler.html",
}

def register_page(endpoint_name: str, template_name: str):
    """يسجل Route لصفحة معينة باسم endpoint ثابت لتفادي BuildError."""
    def _view():
        return render_template(template_name)
    _view.__name__ = f"view__{endpoint_name}"
    app.add_url_rule(f"/{endpoint_name}", endpoint=endpoint_name, view_func=_view)

# ✅ توليد جميع الروتات من القاموس
for ep, tpl in PAGES.items():
    register_page(ep, tpl)

# ✅ مسار عام لفتح أي تمبليت موجود بدون ما تعمل روت خاص
# مثال: /view/wechsler يفتح templates/wechsler.html إذا موجود
@app.route("/view/<name>", endpoint="view_generic")
def view_generic(name: str):
    expected = Path(app.template_folder) / f"{name}.html"
    if expected.exists():
        return render_template(f"{name}.html")
    abort(404)

# ✅ صفحة صحّة للخدمة (مفيدة لـ Render)
@app.route("/healthz", endpoint="healthz")
def healthz():
    return {"status": "ok"}

# ✅ تعامل أنيق مع 404
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    # للتجربة محلياً
    app.run(host="0.0.0.0", port=5000, debug=True)
