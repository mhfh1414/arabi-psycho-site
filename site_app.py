from flask import Flask, render_template, request, abort
from jinja2 import TemplateNotFound, TemplateSyntaxError
from pathlib import Path

# دوال DSM
from data.dsm5 import list_disorders, get_disorder

app = Flask(__name__, static_folder="static", template_folder="templates")

# -----------------------------
# الصفحات الأساسية
# -----------------------------
@app.route("/", endpoint="home")
def home():
    # الرئيسية: تأكد أن عندك templates/main/index.html
    return render_template("main/index.html")

# قائمة DSM
@app.route("/dsm", endpoint="dsm")
def dsm():
    disorders = list_disorders()
    return render_template("dsm/dsm.html", disorders=disorders)

# تفاصيل اضطراب DSM
@app.route("/dsm/<int:disorder_id>", endpoint="dsm_detail")
def dsm_detail(disorder_id: int):
    disorder = get_disorder(disorder_id)
    return render_template("dsm/dsm_detail.html", disorder=disorder)

# صفحات ثابتة اختيارية (لو عندك قوالبها)
@app.route("/cbt", endpoint="cbt")
def cbt():
    return render_template("cbt/cbt.html")

@app.route("/tests", endpoint="tests")
def tests():
    return render_template("tests/tests.html")

# -----------------------------
# مسار عام لعرض أي قالب موجود
# مثال: /view/dsm/dsm  يفتح templates/dsm/dsm.html
# -----------------------------
@app.route("/view/<path:name>", endpoint="view_generic")
def view_generic(name: str):
    file_path = Path(app.template_folder) / f"{name}.html"
    if file_path.exists():
        return render_template(f"{name}.html")
    abort(404)

# -----------------------------
# صفحات الأخطاء
# -----------------------------
@app.errorhandler(404)
def not_found(e):
    # تأكد من وجود templates/_shared/404.html
    try:
        return render_template("_shared/404.html"), 404
    except Exception:
        return "404 Not Found", 404

@app.errorhandler(500)
def server_error(e):
    # تأكد من وجود templates/_shared/500.html
    try:
        return render_template("_shared/500.html"), 500
    except Exception:
        return "500 Internal Server Error", 500

# فحص صحة الخدمة
@app.route("/healthz", endpoint="healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    # للتجربة محلياً
    app.run(host="0.0.0.0", port=5000, debug=True)
