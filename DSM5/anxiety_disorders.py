# -*- coding: utf-8 -*-
"""
DSM-5 Anxiety Disorders (Arabic)
ملف: DSM5/anxiety_disorders.py

هذا الملف يحتوي على جميع اضطرابات القلق من DSM-5
مكتوبة بشكل مبسّط مع المعايير التشخيصية.
يمكن استدعاؤها في الموقع أو البوت.
"""

from typing import Dict, List, Any
import json

# ------------------------------
# قاعدة البيانات
# ------------------------------

ANXIETY_DISORDERS: Dict[str, Dict[str, Any]] = {
    "panic_disorder": {
        "name_ar": "اضطراب الهلع",
        "name_en": "Panic Disorder",
        "overview": "نوبات هلع متكرّرة وغير متوقعة يتبعها قلق مستمر أو تغيّر سلوكي تجنّبي.",
        "duration": "شهر واحد أو أكثر.",
        "criteria": [
            {"code": "A", "text": "نوبات هلع مفاجئة مع ≥4 أعراض (خفقان، ضيق نفس، دوخة...)."},
            {"code": "B", "text": "قلق مستمر حول نوبات جديدة أو عواقبها."},
            {"code": "C", "text": "غير منسوب لمادة أو مرض جسدي."},
            {"code": "D", "text": "غير مفسَّر باضطراب آخر."}
        ]
    },

    "agoraphobia": {
        "name_ar": "رهاب الساحات/الأماكن العامة",
        "name_en": "Agoraphobia",
        "overview": "خوف من ≥2 من: المواصلات العامة، الأماكن المفتوحة، المغلقة، الزحام، الخروج وحيداً.",
        "duration": "≥ 6 أشهر.",
        "criteria": [
            {"code": "A", "text": "الخوف لأن الهرب صعب أو المساعدة غير متاحة."},
            {"code": "B", "text": "المواقف تثير القلق دوماً وتُتجنّب."},
            {"code": "C", "text": "الخوف غير متناسب مع الخطر."},
            {"code": "D", "text": "يسبب اختلال وظيفي."}
        ]
    },

    "specific_phobia": {
        "name_ar": "الرهاب المحدد",
        "name_en": "Specific Phobia",
        "overview": "خوف مفرط من شيء محدد (حيوان، طائرة، دم...).",
        "duration": "≥ 6 أشهر.",
        "criteria": [
            {"code": "A", "text": "خوف/قلق من شيء أو موقف محدد."},
            {"code": "B", "text": "يثير القلق فورياً ويُتجنّب."},
            {"code": "C", "text": "غير متناسب مع الخطر."},
            {"code": "D", "text": "يسبب خللاً وظيفياً."}
        ]
    },

    "social_anxiety": {
        "name_ar": "اضطراب القلق الاجتماعي (الرهاب الاجتماعي)",
        "name_en": "Social Anxiety Disorder",
        "overview": "خوف من المواقف الاجتماعية والتقييم السلبي.",
        "duration": "≥ 6 أشهر.",
        "criteria": [
            {"code": "A", "text": "خوف من المواقف الاجتماعية مع التقييم."},
            {"code": "B", "text": "خشية من إظهار أعراض تُقيَّم سلبياً."},
            {"code": "C", "text": "المواقف تُثير القلق وتُتجنّب."},
            {"code": "D", "text": "يسبب خللاً وظيفياً."}
        ]
    },

    "gad": {
        "name_ar": "اضطراب القلق المعمّم",
        "name_en": "Generalized Anxiety Disorder",
        "overview": "قلق مفرط أغلب الأيام حول موضوعات متعددة مع صعوبة ضبطه.",
        "duration": "≥ 6 أشهر.",
        "criteria": [
            {"code": "A", "text": "قلق/همّ مفرط أغلب الأيام لمدة ≥ 6 أشهر."},
            {"code": "B", "text": "صعوبة السيطرة على القلق."},
            {"code": "C", "text": "3 أعراض أو أكثر (توتر، إرهاق، نوم...)."},
            {"code": "D", "text": "يسبب خللاً وظيفياً."}
        ]
    },

    "separation_anxiety": {
        "name_ar": "اضطراب قلق الانفصال",
        "name_en": "Separation Anxiety Disorder",
        "overview": "قلق مفرط وغير ملائم للعمر يتعلق بالانفصال عن شخص مرتبط عاطفياً.",
        "duration": "≥ 4 أسابيع (الأطفال)، 6 أشهر (البالغين).",
        "criteria": [
            {"code": "A", "text": "≥3 مظاهر (رفض الخروج، كوابيس، شكاوى جسدية...)."},
            {"code": "B", "text": "يسبب خللاً وظيفياً."}
        ]
    },

    "selective_mutism": {
        "name_ar": "الصمت الاختياري",
        "name_en": "Selective Mutism",
        "overview": "فشل ثابت في الكلام في مواقف اجتماعية رغم القدرة في مواقف أخرى.",
        "duration": "≥ شهر واحد.",
        "criteria": [
            {"code": "A", "text": "يعيق التحصيل/التواصل."},
            {"code": "B", "text": "ليس بسبب نقص اللغة."},
            {"code": "C", "text": "غير منسوب لاضطراب آخر."}
        ]
    }
}

# ------------------------------
# دوال مساعدة
# ------------------------------

def list_disorders() -> List[Dict[str, Any]]:
    """عرض جميع اضطرابات القلق"""
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in ANXIETY_DISORDERS.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    """جلب اضطراب واحد حسب المفتاح"""
    return ANXIETY_DISORDERS[key]

def to_json() -> str:
    """تصدير البيانات كـ JSON"""
    return json.dumps(ANXIETY_DISORDERS, ensure_ascii=False, indent=2)

# اختبار سريع
if __name__ == "__main__":
    print("اضطرابات القلق:")
    for d in list_disorders():
        print("-", d["name_ar"])
