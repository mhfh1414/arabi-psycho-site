from flask import Flask, render_template, request, abort
from jinja2 import TemplateNotFound, TemplateSyntaxError
from pathlib import Path

# استيراد الدوال من DSM
from data.dsm5 import list_disorders, get_disorder

# استيراد الاختبارات والتوصيات
from services.tests import score_test, psych_info, score_big5
from services.recommend import recommend_by_score

app = Flask(__name__, static_folder="static", template_folder="templates")

# الصفحة الرئيسية
@app.route("/", endpoint="home")
def home():
    return render_template("main/index.html")

# صفحة DSM تعرض قائمة الاضطرابات
@app.route("/dsm", endpoint="dsm")
def dsm():
    disorders = list_disorders()
    return render_template("dsm/dsm.html", disorders=disorders)

# صفحة CBT
@app.route("/cbt", endpoint="cbt")
def cbt():
    return render_template("cbt/cbt.html")

# صفحة الاختبارات
@app.route("/tests", endpoint="tests")
def tests():
    return render_template("tests/tests.html")

# تشغيل اختبار نفسي بسيط
@app.route("/test_run", methods=["GET", "POST"], endpoint="test_run")
def test_run():
    if request.method == "POST":
        # اجمع الإجابات
        answers = [request.form.get("q1"), request.form.get("q2")]
        result = score_test(answers)
        # استخرج التوصية
        recommendation = recommend_by_score(result["score"])
        return render_template(
            "tests/test_result.html",
            result=result,
            recommendation=recommendation
        )
    return render_template("tests/test_run.html")

# صفحة نتيجة اختبار (لو فتحتها مباشرة بدون POST)
@app.route("/test_result", endpoint="test_result")
def test_result():
    return render_template("tests/test_result.html", result=None, recommendation=None)

# صفحة دراسة حالة
@app.route("/case_study", endpoint="case_study")
def case_study():
    return render_template("case/case_study.html")

# مسار عام لعرض أي قالب بالاسم
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

# مسار صحي للتأكد أن السيرفر شغال
@app.route("/healthz", endpoint="healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
