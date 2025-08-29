# -*- coding: utf-8 -*-
"""
DSM-5 Somatic Symptom and Related Disorders (Arabic)
ملف: DSM5/somatic_symptom_disorders.py
"""

from typing import Dict, List, Any
import json

SOMATIC: Dict[str, Dict[str, Any]] = {
    "somatic_symptom": {
        "name_ar": "اضطراب الأعراض الجسدية",
        "name_en": "Somatic Symptom Disorder",
        "overview": "عرض/أعراض جسدية مزعجة مع أفكار/مشاعر/سلوكيات مفرطة مرتبطة بها.",
        "duration": "عادة مزمن لأشهر عديدة.",
        "criteria": [
            {"code": "A", "text": "عرض/أعراض جسدية تسبب ضيقًا."},
            {"code": "B", "text": "استغراق ذهني/قلق/سلوكيات صحية مفرطة حول الأعراض."}
        ]
    },
    "illness_anxiety": {
        "name_ar": "اضطراب قلق المرض",
        "name_en": "Illness Anxiety Disorder",
        "overview": "انشغال بفكرة الإصابة بمرض خطير مع أعراض جسدية غائبة أو خفيفة جدًا.",
        "duration": "≥ 6 أشهر.",
        "criteria": [
            {"code": "A", "text": "انشغال مرضي رغم طمأنة طبية."},
            {"code": "B", "text": "سلوكيات تفقد/طمأنة أو تجنب مفرطة."}
        ]
    },
    "conversion_disorder": {
        "name_ar": "اضطراب التحويل (الأعراض العصبية الوظيفية)",
        "name_en": "Conversion Disorder (Functional Neurological Symptom)",
        "overview": "أعراض عصبية (حركية/حسية) غير متناسقة مع أمراض عصبية معروفة.",
        "duration": "متفاوت.",
        "criteria": [
            {"code": "A", "text": "عرض واحد أو أكثر من الأعراض العصبية."},
            {"code": "B", "text": "عدم التوافق مع أمراض عصبية معروفة بعد التقييم."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in SOMATIC.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return SOMATIC[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(SOMATIC, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
