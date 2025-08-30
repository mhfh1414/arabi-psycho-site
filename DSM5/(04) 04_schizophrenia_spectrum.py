"""
DSM-5 Schizophrenia Spectrum & Other Psychotic Disorders (Arabic)
ملف: 04_schizophrenia_spectrum.py
"""

from typing import Dict, Any

CATEGORY = "schizo_spectrum"
LABEL_AR = "طيف الفصام والذهانات الأخرى"

DATA: Dict[str, Any] = {
    "schizophrenia": {
        "name_ar": "الفصام",
        "name_en": "Schizophrenia",
        "overview": "أعراض ذهانية أساسية (وهام، هلوسة، كلام/سلوك مفكك، أعراض سلبية) لمدة ممتدة.",
        "duration": "≥ 6 أشهر (شهر نشط على الأقل)",
        "criteria": [
            {"code": "A", "text": "عرضان أو أكثر من الذهانية (أحدها من: وهام، هلوسة، كلام مفكك)."},
            {"code": "B", "text": "اختلال واضح في الوظيفة."},
            {"code": "C", "text": "استمرار الاضطراب ≥ 6 أشهر."}
        ],
        "specifiers": ["مع كاتاتونيا", "بعُمق جزئي/تام", "نمط أولي مبكر"],
        "severity_guidance": "حسب الشدة الوظيفية والتواتر.",
        "differentials": ["اضطراب schizoaffective", "اضطرابات مزاج مع سمات ذهانية", "مواد/حالات طبية"]
    },
    "brief_psychotic": {
        "name_ar": "اضطراب ذهاني وجيز",
        "name_en": "Brief Psychotic Disorder",
        "overview": "أعراض ذهانية مفاجئة قصيرة المدى مع عودة كاملة للخط الأساس.",
        "duration": "من يوم إلى أقل من شهر",
        "criteria": [
            {"code": "A", "text": "أحد: وهام، هلوسة، كلام مفكك؛ وقد يُضاف سلوك مفكك/كاتاتونيا."},
            {"code": "B", "text": "المدة قصيرة مع عودة للأداء السابق."}
        ],
        "specifiers": ["مع عامل ضغطي واضح", "بدون عامل ضغطي", "مع بداية محيطية"],
        "severity_guidance": "شدّة البداية، المخاطر، الحاجة لدعم حاد.",
        "differentials": ["ذهان محرض بمادة", "نوبة ذهانية في اضطراب مزاج"]
    }
}
