from flask import Flask, render_template, request, abort
from jinja2 import TemplateNotFound, TemplateSyntaxError
from pathlib import Path
import logging

# دوال DSM
from data.dsm5 import list_disorders, get_disorder

app = Flask(__name__, static_folder="static", template_folder="templates")

# -----------------------------
# إعدادات اللوقّات
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = app.logger

# -----------------------------
# الصفحات الأساسية
# -----------------------------
@app.route("/", endpoint="home")
def home():
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

# صفحات ثابتة اختيارية
@app.route("/cbt", endpoint="cbt")
def cbt():
    return render_template("cbt/cbt.html")

@app.route("/tests", endpoint="tests")
def tests():
    return render_template("tests/tests.html")

# تشغيل اختبار بسيط (نعم/لا) + عرض نتيجة وتوصية
from services.tests import score_test
from services.recommend import recommend_by_score

@app.route("/test_run", methods=["GET", "POST"], endpoint="test_run")
def test_run():
    if request.method == "POST":
        answers = [request.form.get("q1"), request.form.get("q2")]
        result = score_test(answers)
        recommendation = recommend_by_score(result["score"])
        return render_template("tests/test_result.html", result=result, recommendation=recommendation)
    return render_template("tests/test_run.html")

@app.route("/test_result", endpoint="test_result")
def test_result():
    return render_template("tests/test_result.html", result=None, recommendation=None)

# دراسة حالة
@app.route("/case_study", endpoint="case_study")
def case_study():
    return render_template("case/case_study.html")

# -----------------------------
# مسار عام لعرض أي قالب موجود
# مثال: /view/dsm/dsm  يفتح templates/dsm/dsm.html
# -----------------------------
@app.route("/view/<path:name>", endpoint="view_generic")
def view_generic(name: str):
    file_path = Path(app.template_folder) / f"{name}.html"
    if file_path.exists():
        try:
            return render_template(f"{name}.html")
        except TemplateSyntaxError as e:
            logger.error(f"Jinja error in {name}.html: {e.message} @ line {e.lineno}")
            return render_template("_shared/500.html", msg=f"{name}.html:{e.lineno} {e.message}"), 500
        except Exception as e:
            logger.error(f"Render error in {name}.html: {e}")
            return render_template("_shared/500.html", msg=str(e)), 500
    abort(404)

# -----------------------------
# معالجات الأخطاء
# -----------------------------
@app.errorhandler(404)
def not_found(e):
    try:
        return render_template("_shared/404.html"), 404
    except Exception:
        return "404 Not Found", 404

@app.errorhandler(500)
def server_error(e):
    # ملاحظة: يُستدعى هذا إذا رفعت أنت 500 يدويًا، أما الاستثناءات غير المتوقعة فسيعالجها المعالج العام بالأسفل.
    try:
        return render_template("_shared/500.html"), 500
    except Exception:
        return "500 Internal Server Error", 500

# معالج عام لأي استثناء غير متوقع
@app.errorhandler(Exception)
def handle_unexpected_error(e):
    # لو كان الاستثناء من Jinja نعرض السطر والرسالة
    if isinstance(e, TemplateSyntaxError):
        logger.exception("Unhandled Jinja TemplateSyntaxError")
        try:
            return render_template(
                "_shared/500.html",
                msg=f"{getattr(e, 'filename', 'template')}:{e.lineno} {e.message}"
            ), 500
        except Exception:
            return f"TemplateSyntaxError: {e}", 500
    # أي استثناء آخر
    logger.exception("Unhandled Exception")
    try:
        return render_template("_shared/500.html", msg=str(e)), 500
    except Exception:
        return f"Internal Server Error: {e}", 500

# -----------------------------
# صحّة الخدمة
# -----------------------------
@app.route("/healthz", endpoint="healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    # للتجربة محلياً
    app.run(host="0.0.0.0", port=5000, debug=True)
