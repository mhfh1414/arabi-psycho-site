from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os

# قاعدة البيانات والنماذج
from models import db, PatientCase, TestResult

# الاختبارات
from modules.tests_psych import PSYCH_TESTS, score_test as score_psych, get_scale_options
from modules.tests_personality import PERS_TESTS, score_personality

# التوصية بالاختبارات بعد دراسة الحالة
from modules.recommend import recommend_tests_from_case

# DSM (اختياري للعرض/التكامل لاحقاً)
try:
    from DSM5.dsm import get_all_disorders as dsm_all
except Exception:
    dsm_all = lambda: []

def create_app():
    app = Flask(__name__)

    # مفاتيح وبيئة
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "arabi-psycho-secret")
    os.makedirs("data", exist_ok=True)

    # قاعدة البيانات: استخدم DATABASE_URL إن وُجد، وإلا SQLite محلي
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        # تصحيح صيغة postgres:// -> postgresql://
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/psycho.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ------------------ صفحات عامة ------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/cbt")
    def cbt():
        return render_template("cbt.html")

    @app.route("/dsm")
    def dsm():
        disorders = dsm_all()  # إن لم تكن متاحة تعود قائمة فاضية
        return render_template("dsm.html", disorders=disorders)

    # ------------------ الاختبارات ------------------
    @app.route("/tests")
    def tests():
        case_id = request.args.get("case_id", type=int)
        recommended = []
        if case_id:
            case = PatientCase.query.get(case_id)
            if case:
                recommended = recommend_tests_from_case(
                    case.presenting_problem or "", case.symptoms_text or ""
                )
        return render_template(
            "tests.html",
            psych_tests=PSYCH_TESTS,
            pers_tests=PERS_TESTS,
            recommended=recommended,
            case_id=case_id
        )

    @app.route("/tests/start/<test_key>", methods=["GET", "POST"])
    def test_start(test_key):
        case_id = request.args.get("case_id", type=int)
        test = PSYCH_TESTS.get(test_key) or PERS_TESTS.get(test_key)
        if not test:
            flash("الاختبار غير موجود")
            return redirect(url_for("tests"))

        if request.method == "POST":
            # جمع الإجابات
            answers = {}
            for item in test["items"]:
                field = f"q{item['id']}"
                if field not in request.form:
                    flash("الرجاء الإجابة على جميع البنود.")
                    return render_template("test_run.html", test=test, case_id=case_id, scale_options=get_scale_options)
                answers[item["id"]] = int(request.form[field])

            # التصحيح
            if test_key in PSYCH_TESTS:
                result = score_psych(test_key, answers)
            else:
                result = score_personality(test_key, answers)

            # حفظ
            tr = TestResult(
                case_id=case_id,
                test_key=test_key,
                score_total=result.get("total", 0),
                score_json=result,
                created_at=datetime.utcnow()
            )
            db.session.add(tr)
            db.session.commit()
            return redirect(url_for("test_result", result_id=tr.id))

        # تمرير scale_options إلى القالب
        return render_template("test_run.html", test=test, case_id=case_id, scale_options=get_scale_options)

    @app.route("/tests/result/<int:result_id>")
    def test_result(result_id):
        tr = TestResult.query.get_or_404(result_id)
        test = PSYCH_TESTS.get(tr.test_key) or PERS_TESTS.get(tr.test_key)
        return render_template("test_result.html", result=tr, test=test)

    # ------------------ دراسة الحالة ------------------
    @app.route("/case-study", methods=["GET", "POST"])
    def case_study():
        if request.method == "POST":
            data = request.form
            pc = PatientCase(
                name=data.get("name"),
                age=data.get("age", type=int),
                sex=data.get("sex"),
                marital=data.get("marital"),
                presenting_problem=data.get("presenting_problem"),
                symptoms_text=data.get("symptoms"),
                contact=data.get("contact"),
                created_at=datetime.utcnow()
            )
            db.session.add(pc)
            db.session.commit()

            # توصية بالاختبارات
            rec = recommend_tests_from_case(pc.presenting_problem or "", pc.symptoms_text or "")
            session["recommended_tests"] = rec
            flash("تم حفظ دراسة الحالة. جهّزنا لك اختبارات مناسبة.")
            return redirect(url_for("tests", case_id=pc.id))

        return render_template("case_study.html")

    # ------------------ صحّة/أخطاء ------------------
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        # تقدر تضيف logging هنا
        return render_template("500.html"), 500

    return app


app = create_app()

if __name__ == "__main__":
    # للتشغيل المحلي
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
