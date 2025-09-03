from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound, TemplateSyntaxError
from pathlib import Path

app = Flask(__name__, static_folder="static", template_folder="templates")

# الرئيسية
@app.route("/", endpoint="home")
def home():
    return render_template("main/index.html")

# خرائط الأقسام ↔ ملفات القوالب
PAGES = {
    "dsm": "dsm/dsm.html",
    "cbt": "cbt/cbt.html",
    "tests": "tests/tests.html",
    "test_run": "tests/test_run.html",
    "test_result": "tests/test_result.html",
    "case_study": "case/case_study.html",
}

def register_page(endpoint_name, template_name):
    def _view():
        try:
            return render_template(template_name)
        except TemplateNotFound:
            abort(404)
        except TemplateSyntaxError as e:
            app.logger.error(f"Jinja error in {template_name}: {e.message} @ line {e.lineno}")
            return render_template("_shared/500.html", msg=f"{template_name}:{e.lineno} {e.message}"), 500
        except Exception as e:
            app.logger.error(f"Render error in {template_name}: {e}")
            return render_template("_shared/500.html", msg=str(e)), 500
    _view.__name__ = f"view__{endpoint_name}"
    app.add_url_rule(f"/{endpoint_name}", endpoint=endpoint_name, view_func=_view)

for ep, tpl in PAGES.items():
    register_page(ep, tpl)

# فتح أي تمبلت موجود بالمسار النسبي داخل templates
@app.route("/view/<path:name>", endpoint="view_generic")
def view_generic(name: str):
    file_path = Path(app.template_folder) / f"{name}.html"
    if file_path.exists():
        return render_template(f"{name}.html")
    abort(404)

# صفحات الأخطاء
@app.errorhandler(404)
def not_found(e):
    return render_template("_shared/404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("_shared/500.html"), 500

# مثال استيراد من الخدمات بعد النقل
try:
    from services.tests.tests_psych import score_test
    @app.route("/try_psych", endpoint="try_psych")
    def try_psych():
        return score_test(["نعم","لا","نعم"])
except Exception as e:
    app.logger.warning(f"tests services not ready: {e}")

@app.route("/healthz", endpoint="healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
