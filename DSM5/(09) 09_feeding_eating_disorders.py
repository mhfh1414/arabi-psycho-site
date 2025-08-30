"""
DSM-5 Feeding & Eating Disorders (Arabic)
ملف: 09_feeding_eating_disorders.py
"""

from typing import Dict, Any

CATEGORY = "feeding_eating"
LABEL_AR = "اضطرابات الأكل"

DATA: Dict[str, Any] = {
    "anorexia": {
        "name_ar": "القهم العصبي",
        "name_en": "Anorexia Nervosa",
        "overview": "تقييد مدخول الطاقة يؤدي إلى وزن منخفض بشكل ملحوظ مع خوف من الزيادة واضطراب صورة الجسد.",
        "duration": "مزمن/ناكس غالبًا",
        "criteria": [
            {"code": "A", "text": "وزن منخفض بشكل ملحوظ نتيجة تقييد مستمر."},
            {"code": "B", "text": "خوف شديد من زيادة الوزن أو سلوكيات مستمرة تمنعها."},
            {"code": "C", "text": "اضطراب في تجربة وزن/شكل الجسم أو إنكار خطورة الانخفاض."}
        ],
        "specifiers": ["نمط مقيّد", "نمط نهم/تطهير"],
        "severity_guidance": "حسب BMI وعوامل إكلينيكية أخرى.",
        "differentials": ["فرط نشاط الدرق", "MDD", "جسدية أخرى"]
    },
    "bulimia": {
        "name_ar": "الشره العصبي",
        "name_en": "Bulimia Nervosa",
        "overview": "نوبات نهم يعقبها سلوكيات تعويضية غير صحية مع تقييم ذاتي يرتبط بشكل الجسم.",
        "duration": "≥ مرة أسبوعيًا لمدة 3 أشهر",
        "criteria": [
            {"code": "A", "text": "نوبات نهم (كميات كبيرة مع فقد السيطرة)."},
            {"code": "B", "text": "سلوكيات تعويضية متكررة (قيء، مسهلات، صيام، تمرين مفرط)."},
            {"code": "C", "text": "التقييم الذاتي يتأثر بشدة بشكل/وزن الجسم."}
        ],
        "specifiers": [],
        "severity_guidance": "حسب تواتر السلوكيات التعويضية.",
        "differentials": ["اضطراب نهم الطعام", "القهم العصبي (نوع النهم/التطهير)"]
    }
}
