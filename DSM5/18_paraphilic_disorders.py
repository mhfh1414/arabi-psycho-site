# -*- coding: utf-8 -*-
"""
DSM-5 Paraphilic Disorders (Arabic)
ملف: 18_paraphilic_disorders.py
"""

from typing import Dict, List, Any
import json

PARAPHILIC: Dict[str, Dict[str, Any]] = {
    "pedophilic": {
        "name_ar": "اضطراب الولع الجنسي بالأطفال",
        "name_en": "Pedophilic Disorder",
        "overview": "إثارة جنسية متكررة تجاه أطفال قبل البلوغ.",
        "duration": "≥6 أشهر.",
        "criteria": [
            {"code": "A", "text": "خيالات/اندفاعات/سلوكيات لمدة ≥6 أشهر."},
            {"code": "B", "text": "تصرف وفقها أو سببت ضائقة/اختلال."}
        ]
    },
    "voyeuristic": {
        "name_ar": "اضطراب التلصص",
        "name_en": "Voyeuristic Disorder",
        "overview": "إثارة جنسية متكررة من مراقبة أشخاص عراة/عند نشاط جنسي.",
        "duration": "≥6 أشهر.",
        "criteria": [
            {"code": "A", "text": "خيالات/اندفاعات/سلوكيات ≥6 أشهر."}
        ]
    },
    "exhibitionistic": {
        "name_ar": "اضطراب الاستعراض الجنسي",
        "name_en": "Exhibitionistic Disorder",
        "overview": "إثارة جنسية من كشف الأعضاء التناسلية لشخص غير متوقع.",
        "duration": "≥6 أشهر.",
        "criteria": [
            {"code": "A", "text": "خيالات/اندفاعات/سلوكيات ≥6 أشهر."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in PARAPHILIC.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return PARAPHILIC[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(PARAPHILIC, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
