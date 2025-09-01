# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات لموقع عربي سايكو
يتضمن: PatientCase, TestResult
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# أنشئ كائن قاعدة البيانات (تُفعّل في site_app.py عبر db.init_app(app))
db = SQLAlchemy()


class PatientCase(db.Model):
    """دراسة حالة المريض الأساسية"""
    __tablename__ = "patient_cases"

    id = db.Column(db.Integer, primary_key=True)

    # بيانات تعريفية
    name = db.Column(db.String(120), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.String(20), nullable=True)        # ذكر/أنثى/آخر
    marital = db.Column(db.String(40), nullable=True)    # أعزب/متزوج/..

    # نصوص حرة
    presenting_problem = db.Column(db.Text, nullable=True)   # المشكلة الحالية
    symptoms_text = db.Column(db.Text, nullable=True)        # الأعراض بوصف حر
    contact = db.Column(db.String(120), nullable=True)       # هاتف/بريد اختياري

    # طوابع وقت
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # علاقات (اختياري: backref للنتائج)
    results = db.relationship("TestResult", backref="case", lazy=True, cascade="all, delete-orphan")

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "sex": self.sex,
            "marital": self.marital,
            "presenting_problem": self.presenting_problem,
            "symptoms_text": self.symptoms_text,
            "contact": self.contact,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:  # للديباغ
        return f"<PatientCase id={self.id} name={self.name!r}>"


class TestResult(db.Model):
    """نتيجة اختبار (نفسي أو شخصية) مرتبطة بدراسة حالة"""
    __tablename__ = "test_results"

    id = db.Column(db.Integer, primary_key=True)

    # ربط بدراسة الحالة (قد تكون None لو اختبار عام)
    case_id = db.Column(db.Integer, db.ForeignKey("patient_cases.id"), nullable=True, index=True)

    # هوية الاختبار
    test_key = db.Column(db.String(64), nullable=False, index=True)  # مثال: phq9, gad7, big5

    # الدرجات
    score_total = db.Column(db.Integer, nullable=False, default=0)

    # تفاصيل إضافية (قاموس: نطاق/ملف شخصي..)
    # Flask-SQLAlchemy يوفّر نوع JSON متوافق مع SQLite/Postgres
    score_json = db.Column(db.JSON, nullable=True)

    # طابع وقت
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "case_id": self.case_id,
            "test_key": self.test_key,
            "score_total": self.score_total,
            "score_json": self.score_json,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<TestResult id={self.id} test={self.test_key!r} total={self.score_total}>"
