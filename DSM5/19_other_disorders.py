# -*- coding: utf-8 -*-
"""
DSM-5 Other/Unspecified Disorders (Arabic)
ملف: 19_other_disorders.py
"""

from typing import Dict, List, Any
import json

OTHER: Dict[str, Dict[str, Any]] = {
    "unspecified": {
        "name_ar": "اضطراب غير محدد",
        "name_en": "Unspecified Mental Disorder",
        "overview": "تشخيص يستخدم عند وجود أعراض مهمة سريريًا دون توافق كامل مع فئة محددة.",
        "duration": "غير محدد.",
        "criteria": [
            {"code": "A", "text": "أعراض تسبب ضائقة أو خلل وظيفي لكن لا تنطبق معايير فئة محددة."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in OTHER.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return OTHER[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(OTHER, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
