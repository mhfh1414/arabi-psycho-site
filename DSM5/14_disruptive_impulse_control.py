# -*- coding: utf-8 -*-
"""
DSM-5 Disruptive, Impulse-Control, and Conduct Disorders (Arabic)
ملف: 14_disruptive_impulse_control.py
"""

from typing import Dict, List, Any
import json

DISRUPTIVE: Dict[str, Dict[str, Any]] = {
    "conduct_disorder": {
        "name_ar": "اضطراب المسلك",
        "name_en": "Conduct Disorder",
        "overview": "نمط متكرر من خرق حقوق الآخرين أو القواعد الأساسية (عدوان، تدمير ممتلكات، خداع، انتهاكات).",
        "duration": "≥12 شهراً مع معيار خلال 6 أشهر.",
        "criteria": [
            {"code": "A", "text": "≥3 سلوكيات خلال 12 شهراً (عدوان، تدمير، خداع/سرقة، انتهاك قواعد)."}
        ]
    },
    "ied": {
        "name_ar": "الاضطراب الانفجاري المتقطع",
        "name_en": "Intermittent Explosive Disorder",
        "overview": "نوبات اندفاعية عدوانية غير متناسبة مع المثير.",
        "duration": "≥3 أشهر (نوبات لفظية/سلوك تخريبي) أو 3 نوبات تسببت بأذى خلال سنة.",
        "criteria": [
            {"code": "A", "text": "نوبات عدوانية متكررة وغير متناسبة."}
        ]
    },
    "odd": {
        "name_ar": "اضطراب المعارضة المتحدي",
        "name_en": "Oppositional Defiant Disorder",
        "overview": "نمط من الجدال/العناد/المزاج الغاضب ≥6 أشهر.",
        "duration": "≥6 أشهر.",
        "criteria": [
            {"code": "A", "text": "≥4 أعراض (مزاج غاضب، جدال، عناد، ضغينة)."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in DISRUPTIVE.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return DISRUPTIVE[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(DISRUPTIVE, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
