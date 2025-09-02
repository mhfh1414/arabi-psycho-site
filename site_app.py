# site_app.py
from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound, TemplateSyntaxError
from pathlib import Path

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/", endpoint="home")
def home():
    return render_template("index.html")

# طابق الأسماء الموجودة عندك بالصورة
PAGES = {
    "dsm": "dsm.html",
    "cbt": "cbt.html",
    "tests": "tests.html",
    "test_run": "test_run.html",
    "test_result": "test_result.html",
    "case_study": "case_study.html",
}

def register_page(endpoint_name: str, template_name: str):
    def _view():
        try:
            return render_template(template_name)
        except TemplateNotFound:
            # يظهر 404 جميلة لو الملف ناقص
            abort(404)
        except TemplateSyntaxError as e:
            # يساعدنا في اللوق لمعرفة السطر الخاطئ
            app.logger.error(f"Jinja syntax error in {template_name}: {e.message} at line {e.lineno}")
            return render_template("500.html", msg=f"خطأ في القالب {template_name} بالسطر {e.lineno}"), 500
        except Exception as e:
            app.logger.error(f"Render error in {template_name}: {e}")
            return render_template("500.html", msg=str(e)), 500
    _view.__name__ = f"view__{endpoint_name}"
    app.add_url_rule(f"/{endpoint_name}", endpoint=endpoint_name, view_func=_view)

for ep, tpl in PAGES.items():
    register_page(ep, tpl)

@app.route("/view/<name>", endpoint="view_generic")
def view_generic(name: str):
    file_path = Path(app.template_folder) / f"{name}.html"
    if file_path.exists():
        return render_template(f"{name}.html")
    abort(404)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

@app.route("/healthz", endpoint="healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
