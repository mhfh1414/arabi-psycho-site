# -*- coding: utf-8 -*-
"""
ترشيح الاختبارات المناسبة بناءً على دراسة الحالة (الشكوى + الأعراض).
يعيد قائمة مفاتيح اختبارات مع سبب مختصر.
"""

from __future__ import annotations
from typing import List, Dict

_RULES: List[Dict] = [
    # قلق
    {"keywords": ["قلق", "توتر", "خوف", "انشغال"], "tests": ["gad7"], "why": "مؤشرات قلق عامة"},
    # اكتئاب
    {"keywords": ["حزن", "اكتئاب", "فقدان متعة", "ذنب", "يأس"], "tests": ["phq9"], "why": "مؤشرات اكتئاب"},
    # أرق
    {"keywords": ["نوم", "أرق", "استيقاظ", "أحلام"], "tests": ["insomnia"], "why": "مشكلات نوم"},
    # هلع
    {"keywords": ["نوبة", "هلع", "خفقان", "دوخة", "مفاجئة"], "tests": ["panic"], "why": "نوبات هلع محتملة"},
    # شخصية عامة
    {"keywords": ["شخصية", "سمات", "خجول", "انطوائي", "اجتماعي"], "tests": ["bfi10"], "why": "فحص سمات عامة"},
    # تقدير ذات
    {"keywords": ["ثقة", "ذاتي", "أحتقر", "احتقار", "قلة قيمة"], "tests": ["self_esteem"], "why": "تقدير ذات"},
    # مثابرة
    {"keywords": ["تسويف", "ملل", "ثبات", "صمود", "أهداف"], "tests": ["grit"], "why": "مثابرة وانضباط"},
]

_DEFAULT = [
    {"key": "gad7", "reason": "فحص قلق عام"},
    {"key": "phq9", "reason": "فحص اكتئاب"},
]

def _hit(text: str, words: List[str]) -> bool:
    t = (text or "").lower()
    return any(w.lower() in t for w in words)

def recommend_tests_from_case(presenting_problem: str, symptoms_text: str) -> List[Dict[str, str]]:
    blob = f"{presenting_problem} {symptoms_text}".strip()
    if not blob:
        return _DEFAULT.copy()

    picked: List[Dict[str, str]] = []
    used = set()
    for rule in _RULES:
        if _hit(blob, rule["keywords"]):
            for k in rule["tests"]:
                if k not in used:
                    picked.append({"key": k, "reason": rule["why"]})
                    used.add(k)

    # ضمان وجود حزمة أساسية
    for base in _DEFAULT:
        if base["key"] not in used:
            picked.append(base)
            used.add(base["key"])

    return picked[:6]  # حد أقصى عرض 6 توصيات

__all__ = ["recommend_tests_from_case"]
