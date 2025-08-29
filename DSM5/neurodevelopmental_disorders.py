# -*- coding: utf-8 -*-
"""
DSM-5 Neurodevelopmental Disorders (Arabic)
ملف: DSM5/neurodevelopmental_disorders.py
"""

from typing import Dict, List, Any
import json

NEURODEV: Dict[str, Dict[str, Any]] = {
    "asd": {
        "name_ar": "اضطراب طيف التوحّد",
        "name_en": "Autism Spectrum Disorder",
        "overview": "قصور في التواصل/التفاعل الاجتماعي مع سلوكيات وأنماط متكررة ومقيدة.",
        "duration": "بداية مبكرة في مرحلة النمو.",
        "criteria": [
            {"code": "A", "text": "قصور تواصلي/تفاعلي عبر سياقات متعددة."},
            {"code": "B", "text": "أنماط سلوك واهتمامات متكررة أو مقيدة."},
            {"code": "C", "text": "يسبب خللاً وظيفياً سريرياً."}
        ]
    },
    "adhd": {
        "name_ar": "اضطراب فرط الحركة وتشتت الانتباه",
        "name_en": "Attention-Deficit/Hyperactivity Disorder",
        "overview": "نمط دائم من نقص الانتباه و/أو فرط الحركة-الاندفاعية يؤثر على الأداء أو التطور.",
        "duration": "≥ 6 أشهر وبداية قبل عمر 12 سنة في بيئتين أو أكثر.",
        "criteria": [
            {"code": "A", "text": "≥6 أعراض من نقص الانتباه و/أو فرط الحركة-اندفاعية."},
            {"code": "B", "text": "ظهور الأعراض في أكثر من بيئة (مدرسة، منزل، عمل)."}
        ]
    },
    "intellectual_disability": {
        "name_ar": "الإعاقة الذهنية",
        "name_en": "Intellectual Disability",
        "overview": "قصور في الوظائف الذهنية والتكيفية يبدأ في فترة النمو.",
        "duration": "مستمر منذ الطفولة.",
        "criteria": [
            {"code": "A", "text": "قصور في الوظائف الذهنية (الاستدلال، التخطيط، الحكم...)."},
            {"code": "B", "text": "قصور في السلوك التكيفي يؤثر على الاستقلالية."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in NEURODEV.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return NEURODEV[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(NEURODEV, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
