# -*- coding: utf-8 -*-
"""
DSM-5 Sleep-Wake Disorders (Arabic)
ملف: 11_sleep_wake_disorders.py
"""

from typing import Dict, List, Any
import json

SLEEP_WAKE: Dict[str, Dict[str, Any]] = {
    "insomnia": {
        "name_ar": "الأرق",
        "name_en": "Insomnia Disorder",
        "overview": "صعوبة بدء/استمرار النوم أو الاستيقاظ المبكر مع ضيق/اختلال نهاري.",
        "duration": "≥3 ليالٍ أسبوعياً لمدة ≥3 أشهر.",
        "criteria": [
            {"code": "A", "text": "صعوبة البدء أو الاستمرار أو الاستيقاظ المبكر."},
            {"code": "B", "text": "يسبب ضائقة أو اختلال وظيفي."}
        ]
    },
    "hypersomnolence": {
        "name_ar": "اضطراب فرط النعاس",
        "name_en": "Hypersomnolence Disorder",
        "overview": "نعاس مفرط يومياً رغم نوم ≥7 ساعات.",
        "duration": "≥3 مرات أسبوعياً لمدة ≥3 أشهر.",
        "criteria": [
            {"code": "A", "text": "نعاس مفرط مع نوبات نوم متكررة أو نوم مطوّل."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in SLEEP_WAKE.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return SLEEP_WAKE[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(SLEEP_WAKE, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
