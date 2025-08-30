"""
DSM-5 Trauma- and Stressor-Related Disorders (Arabic)
ملف: 06_trauma_stressor_disorders.py
"""

from typing import Dict, Any

CATEGORY = "trauma_stressor"
LABEL_AR = "الاضطرابات المرتبطة بالصدمة والشدّة"

DATA: Dict[str, Any] = {
    "ptsd": {
        "name_ar": "اضطراب الكرب التالي للصدمة",
        "name_en": "Posttraumatic Stress Disorder",
        "overview": "يتلو حدثًا صادمًا مع إعادة معايشة وتجنب وتبدلات سلبية وفرط يقظة لأكثر من شهر.",
        "duration": "أكثر من شهر",
        "criteria": [
            {"code": "A", "text": "التعرّض لحدث صادم مباشر أو غير مباشر."},
            {"code": "B", "text": "أعراض اقتحامية (ذكريات/كوابيس/فلاش باك)."},
            {"code": "C", "text": "تجنب للمثيرات المرتبطة."},
            {"code": "D", "text": "تبدلات سلبية معرفية/مزاجية."},
            {"code": "E", "text": "فرط تنبه/يقظة."}
        ],
        "specifiers": ["مع تعبير متأخر", "مع أعراض انفصالية"],
        "severity_guidance": "حسب شدّة العجز/الخطر والتواتر.",
        "differentials": ["اضطراب تكيّف", "اكتئاب", "قلق عام"]
    },
    "adjustment": {
        "name_ar": "اضطراب التكيّف",
        "name_en": "Adjustment Disorder",
        "overview": "أعراض عاطفية/سلوكية متناسبة مع ضغوط محددة خلال 3 أشهر من حدوثها مع أثر وظيفي.",
        "duration": "خلال 3 أشهر من الضغوط؛ لا يتجاوز 6 أشهر بعد زوالها عادة",
        "criteria": [
            {"code": "A", "text": "ظهور أعراض مرتبطة بوضوح بضغوط محددة خلال 3 أشهر."},
            {"code": "B", "text": "تجاوز رد الفعل المتوقع و/أو خلل وظيفي."},
            {"code": "C", "text": "لا يستوفي معيار اضطراب آخر ولا تفاقم اضطراب سابق فقط."}
        ],
        "specifiers": ["مع مزاج مكتئب", "مع قلق", "مختلط", "مع سلوك مضطرب"],
        "severity_guidance": "خفيف/متوسط/شديد حسب الأثر والسياق.",
        "differentials": ["حزن طبيعي", "MDD", "PTSD مبكر"]
    }
}
