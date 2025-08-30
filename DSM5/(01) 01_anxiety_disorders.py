"""
DSM-5 Anxiety Disorders (Arabic)
ملف: 01_anxiety_disorders.py
"""

from typing import Dict, List, Any
import json

CATEGORY: str = "anxiety"
LABEL_AR: str = "اضطرابات القلق"

DATA: Dict[str, Any] = {
    "meta": {
        "version": "v1.0",
        "source": "DSM-5 (مبسّط للاستخدام البرمجي)",
        "label_ar": LABEL_AR,
        "category": CATEGORY,
    },
    "items": [
        {
            "id": "GAD",
            "name_ar": "اضطراب القلق العام",
            "name_en": "Generalized Anxiety Disorder",
            "overview": "قلق وتوتر مفرط صعب التحكم فيه مع أعراض جسدية وتأثر وظيفي.",
            "duration": "معظم الأيام لمدة ≥ 6 أشهر",
            "criteria": [
                "قلق وتوتر مفرط بشأن عدد من الأحداث أو الأنشطة.",
                "صعوبة في التحكم بالقلق.",
                "ثلاثة أو أكثر: توتر/إجهاد عضلي، تهيّج، صعوبة تركيز، اضطراب نوم، تعب سهل، توتر داخلي.",
                "يسبّب ضيقًا معتبرًا أو اختلالًا وظيفيًا.",
                "غير مفسَّر بشكل أفضل بمادة/حالة طبية أو اضطراب آخر."
            ],
            "specifiers": ["خفيف", "متوسط", "شديد"],
            "differentials": ["فرط نشاط الغدة الدرقية", "الاكتئاب", "اضطراب الهلع"],
            "notes": "العلاج المعرفي السلوكي وSSRIs خيارات خط أول."
        }
    ]
}


# دوال مساعدة
def list_ids() -> List[str]:
    return [it["id"] for it in DATA.get("items", [])]

def to_json(indent: int = 2) -> str:
    return json.dumps(DATA, ensure_ascii=False, indent=indent)

# alias للتماشي مع dsm_index
ANXIETY_DISORDERS = DATA
