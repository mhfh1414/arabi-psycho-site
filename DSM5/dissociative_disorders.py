# -*- coding: utf-8 -*-
"""
DSM-5 Dissociative Disorders (Arabic)
ملف: DSM5/dissociative_disorders.py
"""

from typing import Dict, List, Any
import json

DISSOCIATIVE: Dict[str, Dict[str, Any]] = {
    "did": {
        "name_ar": "اضطراب الهوية التفارقي",
        "name_en": "Dissociative Identity Disorder",
        "overview": "وجود هويتين أو أكثر مع فجوات في استذكار الأحداث اليومية والمعلومات الشخصية.",
        "duration": "مزمن غالبًا.",
        "criteria": [
            {"code": "A", "text": "اضطراب هوية بهويات متعددة أو تبدلات ملحوظة في الإحساس بالذات."},
            {"code": "B", "text": "فجوات ذاكرة متكررة للحياة اليومية/المعلومات الشخصية/الأحداث الصادمة."}
        ]
    },
    "dissociative_amnesia": {
        "name_ar": "فقدان الذاكرة التفارقي",
        "name_en": "Dissociative Amnesia",
        "overview": "عجز عن استذكار معلومات شخصية مهمة عادةً مرتبطة بصدمة/ضغط، غير مفسر عضويًا.",
        "duration": "متفاوت؛ قد يكون محددًا بموقف/زمن.",
        "criteria": [
            {"code": "A", "text": "فقدان ذاكرة لا يُفسر باعتلال عصبي/دواء."},
            {"code": "B", "text": "يسبب ضائقة/اختلال وظيفي."}
        ]
    },
    "depersonalization_derealization": {
        "name_ar": "تبدد الشخصية/تبدد الواقع",
        "name_en": "Depersonalization/Derealization Disorder",
        "overview": "خبرات مستمرة من الانفصال عن الذات أو الإحساس بالواقع كأنه غير حقيقي مع حفظ الاستبصار.",
        "duration": "مزمن/ناكس.",
        "criteria": [
            {"code": "A", "text": "نوبات متكررة من تبدد الشخصية و/أو تبدد الواقع."},
            {"code": "B", "text": "استبصار بأن التجربة ذاتية وليست حقيقة خارجية."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in DISSOCIATIVE.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return DISSOCIATIVE[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(DISSOCIATIVE, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
