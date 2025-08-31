# -*- coding: utf-8 -*-
"""
توصية بالاختبارات بناءً على دراسة الحالة
يربط بين الأعراض/المشكلات المذكورة وبين الاختبارات النفسية أو الشخصية
"""

from typing import List

# قائمة كلمات مفتاحية → اختبارات مقترحة
# يمكن توسعتها بسهولة
RULES = {
    "قلق": ["gad7", "tipi", "bfi20"],
    "توتر": ["gad7", "phq9"],
    "اكتئاب": ["phq9", "bdi", "bfi20"],
    "حزن": ["phq9"],
    "وسواس": ["y_bocs", "tipi"],
    "نوم": ["insomnia", "psqi"],
    "إدمان": ["assist", "audit"],
    "شخصية": ["tipi", "bfi20"],
    "صدمة": ["pcl5", "tipi"],
    "رهاب": ["spinh", "lsas"],
    "ثقة": ["rosenberg", "tipi"],
}

def recommend_tests_from_case(problem: str, symptoms: str) -> List[str]:
    """
    يستقبل وصف المشكلة والأعراض (نصوص)
    يعيد قائمة مفاتيح الاختبارات المقترحة
    """
    text = f"{problem} {symptoms}".lower()
    recommended: List[str] = []

    for keyword, tests in RULES.items():
        if keyword in text:
            for t in tests:
                if t not in recommended:
                    recommended.append(t)

    # fallback: لو ما انطبق شيء
    if not recommended:
        recommended = ["tipi", "bfi20"]  # اختبارات شخصية عامة

    return recommended

# تجربة سريعة
if __name__ == "__main__":
    case = "المريض يشتكي من القلق والأرق"
    rec = recommend_tests_from_case(case, "")
    print("توصية:", rec)
