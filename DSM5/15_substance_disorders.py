# -*- coding: utf-8 -*-
"""
DSM-5 Substance-Related and Addictive Disorders (Arabic)
ملف: 15_substance_disorders.py
"""

from typing import Dict, List, Any
import json

SUBSTANCE: Dict[str, Dict[str, Any]] = {
    "alcohol_use": {
        "name_ar": "اضطراب استعمال الكحول",
        "name_en": "Alcohol Use Disorder",
        "overview": "نمط مشكّل من استعمال الكحول يؤدي لخلل/ضائقة مع ≥2 معايير خلال 12 شهر.",
        "duration": "12 شهراً.",
        "criteria": [
            {"code": "A", "text": "≥2 معايير: فقد السيطرة، رغبة ملحّة، مشاكل اجتماعية، تحمل/انسحاب."}
        ]
    },
    "cannabis_use": {
        "name_ar": "اضطراب استعمال الحشيش",
        "name_en": "Cannabis Use Disorder",
        "overview": "نمط مستمر من استعمال الحشيش مع ≥2 معايير خلال 12 شهر.",
        "duration": "12 شهراً.",
        "criteria": [
            {"code": "A", "text": "≥2 معايير مشابهة (سيطرة، مشاكل، تحمل، انسحاب)."}
        ]
    },
    "gambling_disorder": {
        "name_ar": "اضطراب القمار",
        "name_en": "Gambling Disorder",
        "overview": "سلوك قهري متكرر في المقامرة رغم العواقب السلبية.",
        "duration": "≥12 شهر.",
        "criteria": [
            {"code": "A", "text": "≥4 معايير (انشغال، زيادة المبالغ، فشل الإقلاع، المخاطرة بالعلاقات...)."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in SUBSTANCE.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return SUBSTANCE[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(SUBSTANCE, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
