"""
DSM-5 Somatic Symptom & Related Disorders (Arabic)
ملف: 08_somatic_symptom_disorders.py
"""

from typing import Dict, Any

CATEGORY = "somatic"
LABEL_AR = "أعراض جسدية واضطرابات مرتبطة"

DATA: Dict[str, Any] = {
    "somatic_symptom": {
        "name_ar": "اضطراب الأعراض الجسدية",
        "name_en": "Somatic Symptom Disorder",
        "overview": "عرض/أعراض جسدية مُقلِقة مع أفكار/مشاعر/سلوكيات مفرطة مرتبطة بها.",
        "duration": "غالبًا > 6 أشهر مع تواتر متغير",
        "criteria": [
            {"code": "A", "text": "عرض جسدي واحد أو أكثر مُقلِق."},
            {"code": "B", "text": "أفكار/سلوكيات/مشاعر مفرطة (انشغال عالي، قلق صحي مفرط، وقت وطاقة مكرّسان)."},
            {"code": "C", "text": "استمرارية الأعراض أو الانشغال رغم تغير شدتها."}
        ],
        "specifiers": ["مع ألم غالب"],
        "severity_guidance": "خفيف/متوسط/شديد حسب المعايير B.",
        "differentials": ["اضطراب قلق المرض", "حالة طبية عامة"]
    },
    "illness_anxiety": {
        "name_ar": "اضطراب قلق المرض",
        "name_en": "Illness Anxiety Disorder",
        "overview": "انشغال قوي بوجود/اكتساب مرض خطير مع أعراض جسدية قليلة أو معدومة.",
        "duration": "≥ 6 أشهر غالبًا",
        "criteria": [
            {"code": "A", "text": "انشغال بالمرض دون أعراض جسدية كبيرة."},
            {"code": "B", "text": "قلق صحي مرتفع وسلوكيات فحص/تجنّب."}
        ],
        "specifiers": ["ساعي للرعاية / متجنب للرعاية"],
        "severity_guidance": "حسب شدة القلق والسلوكيات.",
        "differentials": ["SSD", "وسواس قهري", "اضطرابات قلق"]
    }
}
