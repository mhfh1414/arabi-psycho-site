# site_app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import os

# ✅ استيرادات الحزمة الداخلية بشكل صحيح (من modules/__init__.py)
# تأكد أن __init__.py فيه:
# from .tests_psych import PSYCH_TESTS, score_test as score_psych
# from .tests_personality import PERS_TESTS, score_personality
# from .recommend import recommend_tests_from_case
from modules import (
    PSYCH_TESTS,
    PERS_TESTS,
    score_psych,
    score_personality,
    recommend_tests_from_case,
)

# مبدئيًا، سنُعرّف قائمة وهمية لـ DSM حتى لا يتعطل الموقع إن لم تكن الداتا جاهزة
DSM_LIST = [
    {"code": "F32", "name": "اضطراب اكتئابي"},
    {"code": "F41", "name": "اضطرابات القلق"},
    {"code": "F90", "name": "اضطراب فرط الحركة وتشتت الانتباه"},
]

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

    # -------------------- صفحات عامة --------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    # -------------------- DSM --------------------
    @app.route("/dsm")
    def dsm():
        return render_template("dsm.html", items=DSM_LIST)

    @app.route("/dsm/<code>")
    def dsm_detail(code):
        item = next((i for i in DSM_LIST if i["code"] == code), None)
        if not item:
            return render_template("404.html"), 404
        return render_template("dsm_detail.html", item=item)

    # -------------------- الاختبارات --------------------
    @app.route("/tests")
    def tests():
        """صفحة قائمة الاختبارات (نفسي + شخصية)"""
        return render_template(
            "tests.html",
            psych_tests=PSYCH_TESTS,
            pers_tests=PERS_TESTS
        )

    @app.route("/tests/run/<test_code>", methods=["GET", "POST"])
    def test_run(test_code):
        """
        تشغيل اختبار محدد.
        نفترض أن test_code موجود في أحد القائمتين: PSYCH_TESTS أو PERS_TESTS
        """
        test_info = None
        test_info = next((t for t in PSYCH_TESTS if t["code"] == test_code), test_info)
        test_info = next((t for t in PERS_TESTS if t["code"] == test_code), test_info)

        if not test_info:
            flash("الاختبار غير موجود.", "danger")
            return redirect(url_for("tests"))

        if request.method == "POST":
            # نجمع الإجابات كنِسَب/قيم
            # نفترض أن كل سؤال اسمه q1, q2, ...
            answers = {k: v for k, v in request.form.items() if k.startswith("q")}
            # نقرر الدالة المناسبة للتقييم
            if test_code in [t["code"] for t in PSYCH_TESTS]:
                result = score_psych(test_code, answers)
            else:
                result = score_personality(test_code, answers)

            return render_template("test_result.html", test=test_info, result=result)

        # GET: عرض النموذج
        return render_template("test_run.html", test=test_info)

    # -------------------- دراسة حالة --------------------
    @app.route("/case-study", methods=["GET", "POST"])
    def case_study():
        """
        صفحة دراسة الحالة + توصيات بالاختبارات
        endpoint name = 'case_study'  (طابقناه مع url_for في القالب)
        """
        recommended = None
        if request.method == "POST":
            patient_name = request.form.get("patient_name", "").strip()
            notes = request.form.get("session_notes", "").strip()
            rec = request.form.get("recommendations", "").strip()

            # توصية آلية بناءً على نص الحالة (إن أردت)
            recommended = recommend_tests_from_case(notes)

            flash("تم حفظ الحالة (مبدئيًا).", "success")
            return render_template(
                "case_study.html",
                patient_name=patient_name,
                session_notes=notes,
                recommendations=rec,
                recommended=recommended,
            )

        return render_template("case_study.html", recommended=recommended)

    # -------------------- CBT (اختياري) --------------------
    @app.route("/cbt")
    def cbt():
        return render_template("cbt.html")

    # -------------------- أخطاء --------------------
    @app.errorhandler(404)
    def _404(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def _500(e):
        return render_template("500.html", error=e), 500

    return app

# كائن التطبيق لـ gunicorn
app = create_app()

if __name__ == "__main__":
    # للتجربة محليًا فقط
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
