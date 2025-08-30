"""
DSM-5 Neurodevelopmental Disorders (Arabic)
ملف: 05_neurodevelopmental_disorders.py
"""

from typing import Dict, Any

CATEGORY = "neurodevelopmental"
LABEL_AR = "اضطرابات النمو العصبي"

DATA: Dict[str, Any] = {
    "asd": {
        "name_ar": "اضطراب طيف التوحد",
        "name_en": "Autism Spectrum Disorder",
        "overview": "عجز دائم في التواصل/التفاعل الاجتماعي وأنماط سلوك مقيدة ومتكررة تبدأ مبكرًا.",
        "duration": "ظهور مبكر في الطفولة",
        "criteria": [
            {"code": "A", "text": "عجز في التواصل/التفاعل الاجتماعي عبر سياقات متعددة."},
            {"code": "B", "text": "أنماط سلوك/اهتمامات مقيدة ومتكررة."},
            {"code": "C", "text": "ظهور في فترة النمو المبكرة مع أثر وظيفي."}
        ],
        "specifiers": ["مع/بدون عجز فكري", "مع/بدون عجز لغوي", "مرتبط بحالة طبية/جينية"],
        "severity_guidance": "مستويات 1–3 حسب الدعم المطلوب.",
        "differentials": ["إعاقة ذهنية", "اضطرابات تواصل", "ADHD"]
    },
    "adhd": {
        "name_ar": "اضطراب فرط الحركة وتشتت الانتباه",
        "name_en": "Attention-Deficit/Hyperactivity Disorder",
        "overview": "نمط مستمر من تشتت الانتباه و/أو فرط حركة-اندفاعية يؤثر على الأداء.",
        "duration": "≥ 6 أشهر، بعض الأعراض قبل 12 سنة",
        "criteria": [
            {"code": "A", "text": "ستة أعراض أو أكثر من عدم الانتباه و/أو فرط الحركة-اندفاعية."},
            {"code": "B", "text": "حضور الأعراض في مجالين أو أكثر (بيت/مدرسة/عمل)."},
            {"code": "C", "text": "أثر وظيفي واضح وغير مفسّر باضطرابات أخرى."}
        ],
        "specifiers": ["غالب عدم انتباه", "غالب فرط حركة/اندفاعية", "مشترَك"],
        "severity_guidance": "خفيف/متوسط/شديد بحسب التواتر والأثر.",
        "differentials": ["قلق", "اضطرابات تعلم", "اضطرابات طيف التوحد"]
    }
}
