"""
DSM-5 Disorders — مجموعة B (06–09)
ملف: DSM_B.py
"""

from typing import List, Dict, Any

# ========= 06) Trauma & Stressor =========
CATEGORY_TRAUMA: Dict[str, Any] = {
    "id": "06",
    "key": "trauma_stressor_disorders",
    "name_ar": "اضطرابات الصدمة والضغوط",
}
DISORDERS_TRAUMA: List[Dict[str, Any]] = [
    {"code": "PTSD", "name_ar": "اضطراب ما بعد الصدمة", "desc": "تعرض لحدث صادم مع إعادة خبرات وتجنب وفرط يقظة ≥ شهر."},
    {"code": "ADJ", "name_ar": "اضطراب التكيّف", "desc": "أعراض مرتبطة بضغوط خلال 3 أشهر مع أثر وظيفي."},
]

# ========= 07) Dissociative =========
CATEGORY_DISS: Dict[str, Any] = {
    "id": "07",
    "key": "dissociative_disorders",
    "name_ar": "الاضطرابات التفارقية",
}
DISORDERS_DISS: List[Dict[str, Any]] = [
    {"code": "DID", "name_ar": "اضطراب الهوية التفارقي", "desc": "وجود هويتين/أكثر مع فجوات في التذكر."},
    {"code": "DPDR", "name_ar": "تبدد الشخصية/الواقع", "desc": "خبرات مستمرة من تبدد الشخصية أو تبدد الواقع."},
]

# ========= 08) Somatic Symptom =========
CATEGORY_SOM: Dict[str, Any] = {
    "id": "08",
    "key": "somatic_symptom_disorders",
    "name_ar": "الاضطرابات الجسدية الشكل",
}
DISORDERS_SOM: List[Dict[str, Any]] = [
    {"code": "SSD", "name_ar": "اضطراب الأعراض الجسدية", "desc": "عرض جسدي مقلق مع أفكار/سلوكيات مفرطة."},
    {"code": "IAD", "name_ar": "اضطراب قلق المرض", "desc": "انشغال قوي بوجود مرض خطير مع أعراض قليلة."},
]

# ========= 09) Feeding & Eating =========
CATEGORY_FEED: Dict[str, Any] = {
    "id": "09",
    "key": "feeding_eating_disorders",
    "name_ar": "اضطرابات الأكل",
}
DISORDERS_FEED: List[Dict[str, Any]] = [
    {"code": "AN", "name_ar": "القهم العصبي", "desc": "تقييد الطعام وخوف من زيادة الوزن."},
    {"code": "BN", "name_ar": "الشره العصبي", "desc": "نوبات نهم مع سلوكيات تعويضية."},
    {"code": "BED", "name_ar": "اضطراب نهم الطعام", "desc": "نوبات نهم دون سلوكيات تعويضية مع ضيق."},
]

# حزمة التصدير
PACK = [
    (CATEGORY_TRAUMA, DISORDERS_TRAUMA),
    (CATEGORY_DISS,   DISORDERS_DISS),
    (CATEGORY_SOM,    DISORDERS_SOM),
    (CATEGORY_FEED,   DISORDERS_FEED),
]
