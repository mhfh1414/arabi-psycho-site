"""
DSM-5 Disorders — مجموعة A (02–05)
ملف: DSM_A.py
يشمل:
  02) اضطرابات الوسواس القهري وما يرتبط بها (ocd_related_disorders)
  03) الاضطرابات المزاجية (mood_disorders)
  04) طيف الفصام والذهانات (schizophrenia_spectrum)
  05) الاضطرابات النمائية العصبية (neurodevelopmental_disorders)
"""

from typing import List, Dict, Any

# ========= 02) OCD & Related =========
CATEGORY_OCD: Dict[str, Any] = {
    "id": "02",
    "key": "ocd_related_disorders",
    "name_ar": "اضطرابات الوسواس القهري وما يرتبط بها",
}
DISORDERS_OCD: List[Dict[str, Any]] = [
    {
        "code": "OCD",
        "name_ar": "اضطراب الوسواس القهري",
        "desc": "أفكار قهرية و/أو أفعال قسرية متكررة تستنزف الوقت وتؤثر على الأداء.",
        "criteria": [
            "وجود وساوس أو أفعال قهرية أو كليهما",
            "تسبّب ضيقًا ملحوظًا/تأثيرًا وظيفيًا أو تستغرق وقتًا طويلًا",
            "غير مفسّرة بشكل أفضل بمادة/حالة طبية أو اضطراب آخر",
        ],
    },
    {
        "code": "BDD",
        "name_ar": "اضطراب تشوّه صورة الجسد",
        "desc": "انشغال بعيوب متصوّرة بالمظهر مع سلوكيات متكررة للتحقق/الإخفاء.",
    },
    {
        "code": "HOARD",
        "name_ar": "اضطراب الاكتناز",
        "desc": "صعوبة التخلص من الممتلكات → تراكم يعيق المساحات ويؤثر على الأداء.",
    },
]

# ========= 03) Mood =========
CATEGORY_MOOD: Dict[str, Any] = {
    "id": "03",
    "key": "mood_disorders",
    "name_ar": "الاضطرابات المزاجية",
}
DISORDERS_MOOD: List[Dict[str, Any]] = [
    {
        "code": "MDD",
        "name_ar": "اضطراب اكتئابي جسيم",
        "desc": "نوبة اكتئابية كبرى (≥ أسبوعين) مع تأثير وظيفي.",
        "criteria": [
            "مزاج مكتئب أو فقدان المتعة",
            "مجموع ≥5 أعراض (نوم/شهية/طاقة/تركيز/ذنب/بطء/انتحار...)",
        ],
    },
    {
        "code": "BP1",
        "name_ar": "اضطراب ثنائي القطب النوع الأول",
        "desc": "حدوث نوبة هوس واحدة على الأقل (± اكتئاب).",
    },
    {
        "code": "BP2",
        "name_ar": "اضطراب ثنائي القطب النوع الثاني",
        "desc": "نوبة هوس خفيف + نوبة اكتئاب كبرى، دون هوس تام.",
    },
]

# ========= 04) Schizophrenia Spectrum =========
CATEGORY_SCZ: Dict[str, Any] = {
    "id": "04",
    "key": "schizophrenia_spectrum",
    "name_ar": "طيف الفصام والاضطرابات الذهانية",
}
DISORDERS_SCZ: List[Dict[str, Any]] = [
    {
        "code": "SCZ",
        "name_ar": "الفصام",
        "desc": "وهام/هلوسات/تفكك كلامي أو سلوكي/أعراض سلبية لمدة ممتدة (≥ 6 أشهر).",
    },
    {
        "code": "BRFPSY",
        "name_ar": "اضطراب ذهاني وجيز",
        "desc": "أعراض ذهانية مفاجئة تستمر من يوم إلى أقل من شهر مع عودة للخط الأساس.",
    },
]

# ========= 05) Neurodevelopmental =========
CATEGORY_NDEV: Dict[str, Any] = {
    "id": "05",
    "key": "neurodevelopmental_disorders",
    "name_ar": "الاضطرابات النمائية العصبية",
}
DISORDERS_NDEV: List[Dict[str, Any]] = [
    {
        "code": "ASD",
        "name_ar": "اضطراب طيف التوحّد",
        "desc": "عجز تواصلي/تفاعلي وأنماط سلوك مقيدة/متكررة منذ الطفولة المبكرة.",
    },
    {
        "code": "ADHD",
        "name_ar": "اضطراب فرط الحركة وتشتت الانتباه",
        "desc": "نمط مستمر من عدم الانتباه و/أو فرط الحركة-اندفاعية قبل سن 12 سنة.",
    },
]

# حزمة التصدير الموحّدة ليستفيد منها الدالّة في dsm_index
PACK = [
    (CATEGORY_OCD, DISORDERS_OCD),
    (CATEGORY_MOOD, DISORDERS_MOOD),
    (CATEGORY_SCZ, DISORDERS_SCZ),
    (CATEGORY_NDEV, DISORDERS_NDEV),
]
