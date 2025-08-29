# -*- coding: utf-8 -*-
"""
DSM-5 Elimination Disorders (Arabic)
ملف: 10_elimination_disorders.py
"""

from typing import Dict, List, Any
import json

ELIMINATION: Dict[str, Dict[str, Any]] = {
    "enuresis": {
        "name_ar": "التبول اللاإرادي",
        "name_en": "Enuresis",
        "overview": "تبول متكرر في السرير/الملابس بعد العمر المتوقع للتحكم.",
        "duration": "مرتين أسبوعياً ≥3 أشهر أو ضائقة واضحة.",
        "criteria": [
            {"code": "A", "text": "تبول متكرر غير إرادي أو متعمد."},
            {"code": "B", "text": "العمر ≥5 سنوات أو مكافئ نمائي."}
        ]
    },
    "encopresis": {
        "name_ar": "التغوط اللاإرادي",
        "name_en": "Encopresis",
        "overview": "تغوط متكرر في أماكن غير مناسبة.",
        "duration": "مرة واحدة شهرياً لمدة ≥3 أشهر.",
        "criteria": [
            {"code": "A", "text": "تغوط متكرر في أماكن غير مناسبة."},
            {"code": "B", "text": "العمر ≥4 سنوات أو مكافئ نمائي."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in ELIMINATION.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return ELIMINATION[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(ELIMINATION, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
