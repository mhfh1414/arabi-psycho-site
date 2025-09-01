# -*- coding: utf-8 -*-
import os, sys
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session

# =========[ تأمين مسار المشروع ]=========
# نضيف مجلد المشروع (الذي يحتوي modules و DSM5) إلى sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# =========[ الاستيرادات الداخلية ]=========
from models import db, PatientCase, TestResult

# اختبارات نفسية + شخصية
from modules.tests_psych import PSYCH_TESTS, score_test as score_psych
from modules.tests_personality import PERS_TESTS, score_personality
from modules.recommend import recommend_tests_from_case

# DSM (اختياري: إن تعطل الاستيراد نرجّع قائمة فاضية حتى يعمل الموقع)
try:
    from DSM5.dsm import get_all_disorders as dsm_all
except Exception:
    dsm_all = lambda: []

# =========[ تهيئة التطبيق ]=========
app = Flask(__name__)
app.config["SECRET_KEY"] = "arabi-psycho-secret"

# قاعدة البيانات (SQLite داخل مجلد data)
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "data", "psycho.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# =========[ صفحات عامة ]=========
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

# =========[ الاختبارات ]=========
@app.route("/tests")
def tests():
    case_id = request.args.get("case_id", type=int)
    recommended = []
    if case_id:
        case = PatientCase.query.get(case_id)
        if case:
            recommended = recommend_tests_from_case(case.presenting_problem or "", case.symptoms_text or "")
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
                return render_template("test_run.html", test=test, case_id=case_id)
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
            score_total=result["total"],
            score_json=result,
            created_at=datetime.utcnow()
        )
        db.session.add(tr)
        db.session.commit()
        return redirect(url_for("test_result", result_id=tr.id))

    return render_template("test_run.html", test=test, case_id=case_id)

@app.route("/tests/result/<int:result_id>")
def test_result(result_id):
    tr = TestResult.query.get_or_404(result_id)
    test = PSYCH_TESTS.get(tr.test_key) or PERS_TESTS.get(tr.test_key)
    return render_template("test_result.html", result=tr, test=test)

# =========[ دراسة الحالة ]=========
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

# =========[ هاندلر أخطاء بسيطة ]=========
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_err(e):
    return render_template("500.html"), 500

# =========[ تشغيل محلي ]=========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
