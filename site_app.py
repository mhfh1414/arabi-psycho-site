# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, session

# -------------------------------------------------
# استيراد موحّد وقوي من حزمة modules (يشترط وجود modules/__init__.py)
# -------------------------------------------------
try:
    from modules import (
        PSYCH_TESTS,
        score_psych,
        PERS_TESTS,
        score_personality,
        recommend_tests_from_case,
    )
except Exception as e:
    raise RuntimeError(f"[ImportError] مشكلة في استيراد حزمة modules: {e}")

# DSM (مباشر من الحزمة DSM5)
try:
    from DSM5.dsm import get_all_disorders as dsm_all
except Exception:
    # إن حدث خطأ، نوفّر دالة بديلة ترجع قائمة فاضية ونتابع تشغيل الموقع
    def dsm_all():
        return []

# قاعدة البيانات
try:
    from models import db, PatientCase, TestResult
except Exception as e:
    raise RuntimeError(f"[ImportError] مشكلة في استيراد models.py: {e}")

# -------------------------------------------------
# تهيئة التطبيق
# -------------------------------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = "arabi-psycho-secret"

# مسار آمن لقاعدة البيانات حتى على Render/حاويات
DATA_DIR = os.path.join(app.root_path, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "psycho.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ربط قاعدة البيانات وتهيئتها
db.init_app(app)
with app.app_context():
    db.create_all()

# -------------------------------------------------
# الصفحات العامة
# -------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cbt")
def cbt():
    return render_template("cbt.html")

@app.route("/dsm")
def dsm():
    disorders = dsm_all()  # لو فشل الاستيراد ترجع قائمة فاضية
    return render_template("dsm.html", disorders=disorders)

# -------------------------------------------------
# الاختبارات
# -------------------------------------------------
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
        case_id=case_id,
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

        # حفظ النتيجة
        tr = TestResult(
            case_id=case_id,
            test_key=test_key,
            score_total=result.get("total", 0),
            score_json=result,
            created_at=datetime.utcnow(),
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

# -------------------------------------------------
# دراسة الحالة
# -------------------------------------------------
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
            created_at=datetime.utcnow(),
        )
        db.session.add(pc)
        db.session.commit()

        # توصيات اختبارات
        rec = recommend_tests_from_case(pc.presenting_problem or "", pc.symptoms_text or "")
        session["recommended_tests"] = rec
        flash("تم حفظ دراسة الحالة. جهزنا لك اختبارات مناسبة.")
        return redirect(url_for("tests", case_id=pc.id))

    return render_template("case_study.html")

# -------------------------------------------------
# معالجات الأخطاء
# -------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    # مهم: في الإنتاج لا تعرض تفاصيل الاستثناء، فقط صفحة 500
    return render_template("500.html"), 500

# -------------------------------------------------
# تشغيل محلي
# -------------------------------------------------
if __name__ == "__main__":
    # عند التشغيل المحلي فقط
    app.run(host="0.0.0.0", port=5000, debug=True)
