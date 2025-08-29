# -*- coding: utf-8 -*-
"""
DSM-5 Mood Disorders (Arabic)
ملف: DSM5/mood_disorders.py
"""

from typing import Dict, List, Any
import json

MOOD_DISORDERS: Dict[str, Dict[str, Any]] = {
    "bipolar_i": {
        "name_ar": "اضطراب ثنائي القطب النوع الأول",
        "name_en": "Bipolar I Disorder",
        "overview": "حدوث نوبة هوس واحدة على الأقل.",
        "duration": "≥ أسبوع أو أي مدة مع دخول مستشفى.",
        "criteria": [
            {"code": "A", "text": "مزاج مرتفع/متهيج مع زيادة طاقة."},
            {"code": "B", "text": "≥3 أعراض: تضخم تقدير الذات، قلة النوم..."}
        ]
    },
    "major_depression": {
        "name_ar": "اضطراب اكتئابي جسيم",
        "name_en": "Major Depressive Disorder",
        "overview": "نوبة اكتئاب مع ≥5 أعراض خلال أسبوعين.",
        "duration": "≥ أسبوعين.",
        "criteria": [
            {"code": "A", "text": "مزاج مكتئب أو فقد متعة + ≥5 أعراض."},
            {"code": "B", "text": "يسبب اختلال وظيفي."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in MOOD_DISORDERS.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return MOOD_DISORDERS[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(MOOD_DISORDERS, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
