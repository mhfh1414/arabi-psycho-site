"""
DSM-5 Dissociative Disorders (Arabic)
ملف: 07_dissociative_disorders.py
"""

from typing import Dict, Any

CATEGORY = "dissociative"
LABEL_AR = "الاضطرابات التفارقية"

DATA: Dict[str, Any] = {
    "dpdr": {
        "name_ar": "اضطراب تبدد الشخصية/الواقع",
        "name_en": "Depersonalization/Derealization Disorder",
        "overview": "خبرات مستمرة أو متكررة من تبدد الشخصية و/أو تبدد الواقع مع إدراك سليم نسبيًا.",
        "duration": "متغير، غالبًا مزمن/ناكس",
        "criteria": [
            {"code": "A", "text": "تبدد شخصية و/أو تبدد واقع مستمر/متكرر."},
            {"code": "B", "text": "إدراك أن الخبرات ذاتية وليس فقدانا للتماس مع الواقع."},
            {"code": "C", "text": "ضيق/خلل وظيفي ملحوظ."}
        ],
        "specifiers": [],
        "severity_guidance": "حسب التواتر وحدّة الضيق والتأثير الوظيفي.",
        "differentials": ["صرع فص صدغي", "تعاطي مواد", "اضطرابات قلق/مزاج"]
    },
    "dissociative_amnesia": {
        "name_ar": "فقدان ذاكرة تفارقي",
        "name_en": "Dissociative Amnesia",
        "overview": "عجز في استذكار معلومات شخصية مهمة عادة بعد صدمة/شدّة بدون سبب عصبي واضح.",
        "duration": "متغير (قد يترافق مع هروب تفارقي)",
        "criteria": [
            {"code": "A", "text": "عجز لا يفسّر بعصبية/مادة في استرجاع معلومات ذاتية مهمة."},
            {"code": "B", "text": "ضيق/خلل وظيفي."}
        ],
        "specifiers": ["مع هروب تفارقي"],
        "severity_guidance": "حسب اتساع الفقد وتأثيره.",
        "differentials": ["خرف", "اضطراب عصبي", "تمارض"]
    }
}
