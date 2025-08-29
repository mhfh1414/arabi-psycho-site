# -*- coding: utf-8 -*-
"""
DSM-5 Neurocognitive Disorders (Arabic)
ملف: 16_neurocognitive_disorders.py
"""

from typing import Dict, List, Any
import json

NEUROCOG: Dict[str, Dict[str, Any]] = {
    "major_neurocognitive": {
        "name_ar": "اضطراب إدراكي عصبي جسيم",
        "name_en": "Major Neurocognitive Disorder",
        "overview": "تراجع كبير في واحد أو أكثر من مجالات الإدراك مع اختلال الاستقلالية.",
        "duration": "مستمر وتدريجي عادة.",
        "criteria": [
            {"code": "A", "text": "دليل على تراجع كبير موثق أو ملاحظ."},
            {"code": "B", "text": "يتداخل مع الاستقلال في الأنشطة اليومية."}
        ]
    },
    "mild_neurocognitive": {
        "name_ar": "اضطراب إدراكي عصبي خفيف",
        "name_en": "Mild Neurocognitive Disorder",
        "overview": "تراجع معتدل في الإدراك لكن دون فقدان الاستقلال التام.",
        "duration": "مزمن/تدريجي.",
        "criteria": [
            {"code": "A", "text": "دليل على تراجع معتدل موثق أو ملاحظ."},
            {"code": "B", "text": "لا يتداخل بشكل كبير مع الاستقلالية اليومية."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in NEUROCOG.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return NEUROCOG[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(NEUROCOG, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
