"""
DSM-5 Disorders — مجموعة D (15–19)
ملف: DSM_D.py
"""

from typing import List, Dict, Any

# ========= 15) Substance-Related =========
CATEGORY_SUB: Dict[str, Any] = {
    "id": "15",
    "key": "substance_disorders",
    "name_ar": "اضطرابات تعاطي المواد",
}
DISORDERS_SUB: List[Dict[str, Any]] = [
    {"code": "AUD", "name_ar": "اضطراب تعاطي الكحول", "desc": "نمط مشكل من التعاطي يسبب ضيق/ضعف."},
    {"code": "OUD", "name_ar": "اضطراب استخدام الأفيونات", "desc": "استخدام مشكل للأفيونات مع معايير DSM-5."},
    {"code": "GAM", "name_ar": "اضطراب المقامرة", "desc": "سلوك مقامرة متكرر يسبب ضيقًا/اختلالًا."},
]

# ========= 16) Neurocognitive =========
CATEGORY_NC: Dict[str, Any] = {
    "id": "16",
    "key": "neurocognitive_disorders",
    "name_ar": "الاضطرابات العصبية الإدراكية",
}
DISORDERS_NC: List[Dict[str, Any]] = [
    {"code": "MAJ-NCD", "name_ar": "اضطراب معرفي كبير", "desc": "تدهور ملحوظ يعيق الاستقلالية."},
    {"code": "MILD-NCD", "name_ar": "اضطراب معرفي طفيف", "desc": "تدهور معتدل دون فقدان كامل للاستقلالية."},
]

# ========= 17) Personality =========
CATEGORY_PD: Dict[str, Any] = {
    "id": "17",
    "key": "personality_disorders",
    "name_ar": "اضطرابات الشخصية",
}
DISORDERS_PD: List[Dict[str, Any]] = [
    {"code": "BPD", "name_ar": "شخصية حدّية", "desc": "عدم استقرار عاطفي وعلاقات متقلبة."},
    {"code": "ASPD", "name_ar": "شخصية معادية للمجتمع", "desc": "انتهاك حقوق الآخرين متكرر."},
    {"code": "OCPD", "name_ar": "شخصية قهرية الوسواس", "desc": "انشغال بالكمال والنظامية."},
]

# ========= 18) Paraphilic =========
CATEGORY_PARA: Dict[str, Any] = {
    "id": "18",
    "key": "paraphilic_disorders",
    "name_ar": "الانحرافات الجنسية",
}
DISORDERS_PARA: List[Dict[str, Any]] = [
    {"code": "VOY", "name_ar": "التلصص", "desc": "إثارة من مراقبة غير واعين."},
    {"code": "EXH", "name_ar": "الاستعراء", "desc": "إثارة من كشف الأعضاء لشخص غريب."},
    {"code": "PED", "name_ar": "اشتهاء الأطفال", "desc": "خيالات/دوافع نحو أطفال قبل البلوغ."},
]

# ========= 19) Other / Residual =========
CATEGORY_OTHER: Dict[str, Any] = {
    "id": "19",
    "key": "other_disorders",
    "name_ar": "اضطرابات أخرى/متبقي",
}
DISORDERS_OTHER: List[Dict[str, Any]] = [
    {"code": "OSD", "name_ar": "اضطراب محدد آخر", "desc": "يوضح سبب عدم استيفاء المعايير."},
    {"code": "USD", "name_ar": "اضطراب غير محدد", "desc": "عند عدم اكتمال المعطيات مع ضيق."},
]

# حزمة التصدير
PACK = [
    (CATEGORY_SUB,   DISORDERS_SUB),
    (CATEGORY_NC,    DISORDERS_NC),
    (CATEGORY_PD,    DISORDERS_PD),
    (CATEGORY_PARA,  DISORDERS_PARA),
    (CATEGORY_OTHER, DISORDERS_OTHER),
]
