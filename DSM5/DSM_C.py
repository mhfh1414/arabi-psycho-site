"""
DSM-5 Disorders — مجموعة C (11–14)
ملف: DSM_C.py
"""

from typing import List, Dict, Any

# ========= 11) Sleep–Wake =========
CATEGORY_SLEEP: Dict[str, Any] = {
    "id": "11",
    "key": "sleep_wake_disorders",
    "name_ar": "اضطرابات النوم واليقظة",
}
DISORDERS_SLEEP: List[Dict[str, Any]] = [
    {"code": "INS", "name_ar": "الأرق", "desc": "صعوبة بدء/استمرار النوم ≥ 3 ليالٍ أسبوعيًا لمدة ≥ 3 أشهر."},
    {"code": "HYP", "name_ar": "فرط النعاس", "desc": "نعاس مفرط رغم نوم كافٍ مع أثر وظيفي."},
    {"code": "NAR", "name_ar": "النوم القهري", "desc": "هجمات نوم لا تُقاوم مع ± كاتابلكسي."},
]

# ========= 12) Sexual Dysfunctions =========
CATEGORY_SEX: Dict[str, Any] = {
    "id": "12",
    "key": "sexual_dysfunctions",
    "name_ar": "الاختلالات الجنسية",
}
DISORDERS_SEX: List[Dict[str, Any]] = [
    {"code": "ED", "name_ar": "اضطراب الانتصاب", "desc": "صعوبة بدء/الحفاظ على الانتصاب."},
    {"code": "DE", "name_ar": "القذف المتأخر", "desc": "تأخر/غياب القذف رغم الإثارة الكافية."},
    {"code": "FOD", "name_ar": "اضطراب هزّة الجماع عند الإناث", "desc": "غياب/تأخر الهزّة أو انخفاض شدتها."},
]

# ========= 13) Gender Dysphoria =========
CATEGORY_GD: Dict[str, Any] = {
    "id": "13",
    "key": "gender_dysphoria",
    "name_ar": "اضطراب الهوية الجندرية",
}
DISORDERS_GD: List[Dict[str, Any]] = [
    {"code": "GD", "name_ar": "ضيق الهوية الجندرية", "desc": "عدم تطابق بين الهوية الجندرية والخصائص الجنسية."},
]

# ========= 14) Disruptive, Impulse-Control =========
CATEGORY_IMP: Dict[str, Any] = {
    "id": "14",
    "key": "disruptive_impulse_control",
    "name_ar": "الاضطرابات التخريبية وضبط الاندفاع",
}
DISORDERS_IMP: List[Dict[str, Any]] = [
    {"code": "ODD", "name_ar": "اضطراب العناد الشارد", "desc": "نمط غاضب/جدلي/حاقد مع تحدٍّ."},
    {"code": "IED", "name_ar": "اضطراب الانفجار المتقطع", "desc": "نوبات غضب غير متناسبة."},
    {"code": "CD", "name_ar": "اضطراب السلوك", "desc": "انتهاك حقوق الآخرين أو القوانين."},
]

# حزمة التصدير
PACK = [
    (CATEGORY_SLEEP, DISORDERS_SLEEP),
    (CATEGORY_SEX,   DISORDERS_SEX),
    (CATEGORY_GD,    DISORDERS_GD),
    (CATEGORY_IMP,   DISORDERS_IMP),
]
