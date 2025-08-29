# -*- coding: utf-8 -*-
"""
DSM-5 Sexual Dysfunctions (Arabic)
ملف: 12_sexual_dysfunctions.py
"""

from typing import Dict, List, Any
import json

SEXUAL_DYS: Dict[str, Dict[str, Any]] = {
    "ed": {
        "name_ar": "ضعف الانتصاب",
        "name_en": "Erectile Disorder",
        "overview": "صعوبة مستمرة في تحقيق أو الحفاظ على الانتصاب.",
        "duration": "≥6 أشهر في معظم المناسبات.",
        "criteria": [
            {"code": "A", "text": "صعوبة في تحقيق أو الحفاظ على الانتصاب."},
            {"code": "B", "text": "يسبب ضائقة ملحوظة."}
        ]
    },
    "female_orgasmic": {
        "name_ar": "اضطراب النشوة الأنثوي",
        "name_en": "Female Orgasmic Disorder",
        "overview": "تأخر أو غياب دائم أو متكرر للنشوة الجنسية عند المرأة.",
        "duration": "≥6 أشهر.",
        "criteria": [
            {"code": "A", "text": "تأخر أو غياب أو انخفاض شدة النشوة."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in SEXUAL_DYS.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return SEXUAL_DYS[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(SEXUAL_DYS, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
