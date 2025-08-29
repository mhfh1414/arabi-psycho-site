# -*- coding: utf-8 -*-
"""
DSM-5 Personality Disorders (Arabic)
ملف: 17_personality_disorders.py
"""

from typing import Dict, List, Any
import json

PERSONALITY: Dict[str, Dict[str, Any]] = {
    "bpd": {
        "name_ar": "اضطراب الشخصية الحدّية",
        "name_en": "Borderline Personality Disorder",
        "overview": "عدم استقرار في العلاقات والمزاج وصورة الذات مع اندفاعية.",
        "duration": "بداية مبكرة وثابت عبر السياقات.",
        "criteria": [
            {"code": "A", "text": "≥5 سمات: تجنّب هجر، علاقات شديدة، اضطراب هوية، اندفاعية، إيذاء الذات، تقلب وجداني، فراغ، غضب، ارتيابية عابرة."}
        ]
    },
    "npd": {
        "name_ar": "اضطراب الشخصية النرجسية",
        "name_en": "Narcissistic Personality Disorder",
        "overview": "نمط من العظمة، الحاجة للإعجاب، نقص التعاطف.",
        "duration": "بداية باكرة وثابت.",
        "criteria": [
            {"code": "A", "text": "نمط عظمة (خيال/سلوك) مع استحقاق، استغلال، غيرة، غطرسة."}
        ]
    },
    "aspd": {
        "name_ar": "اضطراب الشخصية المعادية للمجتمع",
        "name_en": "Antisocial Personality Disorder",
        "overview": "تجاهل وانتهاك حقوق الآخرين منذ عمر 15 سنة على الأقل.",
        "duration": "منذ المراهقة المبكرة.",
        "criteria": [
            {"code": "A", "text": "سلوكيات خرق القانون، خداع، اندفاع، عدوانية، استهتار، عدم مسؤولية، انعدام ندم."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in PERSONALITY.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return PERSONALITY[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(PERSONALITY, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
