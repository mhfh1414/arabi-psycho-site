# -*- coding: utf-8 -*-
"""
DSM-5 Trauma- and Stressor-Related Disorders (Arabic)
ملف: DSM5/trauma_stressor_disorders.py
"""

from typing import Dict, List, Any
import json

TRAUMA_STRESSOR: Dict[str, Dict[str, Any]] = {
    "ptsd": {
        "name_ar": "اضطراب الكرب ما بعد الصدمة (PTSD)",
        "name_en": "Posttraumatic Stress Disorder",
        "overview": "تعرض لحدث صادمي مع أعراض اقتحامية وتجنب وتبدلات سلبية وفرط تنبه.",
        "duration": "أكثر من شهر بعد الحدث.",
        "criteria": [
            {"code": "A", "text": "التعرّض لصدمة: مباشرة/مشاهدة/علم بوقوعها لقريب/تعرّض متكرر لتفاصيلها."},
            {"code": "B", "text": "أعراض اقتحامية (ذكريات/كوابيس/استرجاع/ضيق عند التذكير)."},
            {"code": "C", "text": "تجنب للمنبّهات المرتبطة بالحدث (داخلي/خارجي)."},
            {"code": "D", "text": "تبدلات سلبية في الأفكار/المزاج (ذنب، خدر، أفكار سلبية دائمة)."},
            {"code": "E", "text": "فرط تنبه (تهيّج، فرط يقظة، صعوبة نوم/تركيز، فزعات)."}
        ]
    },
    "acute_stress_disorder": {
        "name_ar": "اضطراب الكرب الحاد",
        "name_en": "Acute Stress Disorder",
        "overview": "أعراض مشابهة لـ PTSD لكنها خلال الأيام/الأسابيع الأولى بعد الصدمة.",
        "duration": "من 3 أيام إلى أقل من شهر بعد الحدث.",
        "criteria": [
            {"code": "A", "text": "التعرض لحدث صادمي."},
            {"code": "B", "text": "≥9 أعراض من فئات الاقتحام/المزاج/التجنب/التفارق/الاستثارة."}
        ]
    },
    "adjustment_disorder": {
        "name_ar": "اضطراب التكيف",
        "name_en": "Adjustment Disorder",
        "overview": "أعراض انفعالية/سلوكية مستجيبة لضغط محدد مع اختلال وظيفي واضح.",
        "duration": "خلال 3 أشهر من الضاغط، وتنتهي عادة خلال 6 أشهر بعد زواله.",
        "criteria": [
            {"code": "A", "text": "تطور أعراض بشكل متناسب مع الضاغط خلال 3 أشهر."},
            {"code": "B", "text": "ضائقة مفرطة و/أو اختلال وظيفي واضح."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in TRAUMA_STRESSOR.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return TRAUMA_STRESSOR[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(TRAUMA_STRESSOR, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
