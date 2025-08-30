"""
DSM-5 Elimination Disorders (Arabic)
ملف: 10_elimination_disorders.py
"""

from typing import Dict, Any

CATEGORY = "elimination"
LABEL_AR = "اضطرابات الإطراح"

DATA: Dict[str, Any] = {
    "enuresis": {
        "name_ar": "سلس البول الليلي/النهاري",
        "name_en": "Enuresis",
        "overview": "تبليل لا إرادي متكرر لدى طفل بعمر نمائي مناسب، مع ضيق/أثر وظيفي.",
        "duration": "≥ مرتين أسبوعيًا لمدة 3 أشهر أو ضيق شديد",
        "criteria": [
            {"code": "A", "text": "تبليل متكرر للفراش/الملابس مكانيًا أو زمانيًا."},
            {"code": "B", "text": "العمر النمائي ≥ 5 سنوات تقريبًا."}
        ],
        "specifiers": ["ليلي فقط", "نهاري فقط", "مختلط"],
        "severity_guidance": "حسب التواتر والأثر الأسري/المدرسي.",
        "differentials": ["أسباب طبية بولية", "اضطرابات نوم"]
    },
    "encopresis": {
        "name_ar": "تغوّط لا إرادي",
        "name_en": "Encopresis",
        "overview": "خروج براز في أماكن غير مناسبة بشكل متكرر لدى طفل بعمر نمائي مناسب.",
        "duration": "≥ مرة شهريًا لمدة 3 أشهر",
        "criteria": [
            {"code": "A", "text": "تغوّط في أماكن غير مناسبة (ملابس/أرض)."},
            {"code": "B", "text": "العمر النمائي ≥ 4 سنوات تقريبًا."}
        ],
        "specifiers": ["مع إمساك وسلس فائض", "بدون إمساك"],
        "severity_guidance": "حسب العوامل الطبية والسلوكية المصاحبة.",
        "differentials": ["حالات طبية معدية/قولونية", "اضطرابات سلوكية"]
    }
}
