# -*- coding: utf-8 -*-
"""
DSM-5 Feeding and Eating Disorders (Arabic)
ملف: DSM5/feeding_eating_disorders.py
"""

from typing import Dict, List, Any
import json

EATING: Dict[str, Dict[str, Any]] = {
    "anorexia": {
        "name_ar": "القهم العصبي",
        "name_en": "Anorexia Nervosa",
        "overview": "تقييد للطعام يؤدي لوزن منخفض بشكل ملحوظ مع خوف شديد من زيادة الوزن وتشوه صورة الجسد.",
        "duration": "مستمر.",
        "criteria": [
            {"code": "A", "text": "انخفاض ملحوظ بالوزن بسبب تقييد المدخول."},
            {"code": "B", "text": "خوف شديد من زيادة الوزن/البدانة."},
            {"code": "C", "text": "اضطراب في صورة الجسد/إنكار خطورة النحافة."}
        ]
    },
    "bulimia": {
        "name_ar": "الشره العصبي",
        "name_en": "Bulimia Nervosa",
        "overview": "نوبات أكل شَرِه مع سلوك تعويضي غير مناسب (استفراغ/ملينات/صوم/تمارين مفرطة).",
        "duration": "مرة أسبوعيًا لمدة 3 أشهر على الأقل.",
        "criteria": [
            {"code": "A", "text": "نوبات شَرَه مع فقد السيطرة."},
            {"code": "B", "text": "سلوك تعويضي متكرر وغير مناسب."}
        ]
    },
    "bingeeating": {
        "name_ar": "اضطراب نهم الطعام",
        "name_en": "Binge-Eating Disorder",
        "overview": "نوبات أكل مفرط بدون سلوك تعويضي، مع ضيق ملحوظ.",
        "duration": "مرة واحدة أسبوعيًا لمدة 3 أشهر على الأقل.",
        "criteria": [
            {"code": "A", "text": "نوبات نهم مع ≥3 ملامح (أكل سريع/حتى الامتلاء المؤلم/وأنت غير جائع/أكل منفردًا/اشمئزاز/ذنب)."},
            {"code": "B", "text": "ضائقة ملحوظة بشأن النهم."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in EATING.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return EATING[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(EATING, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
