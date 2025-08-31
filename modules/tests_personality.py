# -*- coding: utf-8 -*-
"""
اختبارات الشخصية (نماذج أساسية)
- TIPI: اختبار قصير جداً لسمات الخمسة الكبرى (10 بنود)
- BFI-20: نسخة مختصرة (20 بند) للخمسة الكبار
يحسب الدرجات لكل بُعد، ويُرجعها كنسبة مئوية 0-100 لتسهيل القراءة.
"""

from typing import Dict, List, Any

# ======================================================================
# تعريف الاختبارات
# ======================================================================

PERS_TESTS: Dict[str, Dict[str, Any]] = {
    "tipi": {
        "title": "TIPI — الخمسة الكبار (10 بنود)",
        "instruction": "اختر درجة موافقتك من 1 (أعارض بشدة) إلى 7 (أوافق بشدة).",
        "scale": {
            1: "أعارض بشدة",
            2: "أعارض",
            3: "أعارض قليلاً",
            4: "محايد",
            5: "أوافق قليلاً",
            6: "أوافق",
            7: "أوافق بشدة",
        },
        # كل بُعد يحسب من بندين (أحدهما معكوس)
        # reverse: البنود التي تُعكس (x -> 8 - x)
        "items": [
            {"id": 1, "text": "منفتح/اجتماعي", "trait": "الانبساط", "reverse": False},
            {"id": 2, "text": "ناقد/متعارض غالباً", "trait": "التوافقية", "reverse": True},
            {"id": 3, "text": "واعٍ ومنظم", "trait": "الضمير الحي", "reverse": False},
            {"id": 4, "text": "قلِق/يتوتر بسهولة", "trait": "العُصابية", "reverse": False},
            {"id": 5, "text": "مبتكر/واسع الخيال", "trait": "الانفتاح", "reverse": False},
            {"id": 6, "text": "محفوظ/خجول", "trait": "الانبساط", "reverse": True},
            {"id": 7, "text": "طيّب/دافئ ومتعاون", "trait": "التوافقية", "reverse": False},
            {"id": 8, "text": "مهمل/يفتقد الانضباط", "trait": "الضمير الحي", "reverse": True},
            {"id": 9, "text": "هادئ/ثابت انفعالياً", "trait": "العُصابية", "reverse": True},
            {"id": 10, "text": "تقليدي/غير خلاق", "trait": "الانفتاح", "reverse": True},
        ],
        "traits": ["الانبساط", "التوافقية", "الضمير الحي", "العُصابية", "الانفتاح"],
        "max_per_item": 7,
    },

    "bfi20": {
        "title": "BFI-20 — الخمسة الكبار (20 بند)",
        "instruction": "اختر درجة موافقتك من 1 (أعارض بشدة) إلى 5 (أوافق بشدة).",
        "scale": {
            1: "أعارض بشدة",
            2: "أعارض",
            3: "محايد",
            4: "أوافق",
            5: "أوافق بشدة",
        },
        # 4 بنود لكل بُعد، اثنان منها معكوسة عادةً
        "items": [
            # الانبساط
            {"id": 101, "text": "أرى نفسي شخصاً منفتحاً وحيوياً", "trait": "الانبساط", "reverse": False},
            {"id": 102, "text": "أرى نفسي قليل الكلام", "trait": "الانبساط", "reverse": True},
            {"id": 103, "text": "أشعر بالراحة وسط المجموعات", "trait": "الانبساط", "reverse": False},
            {"id": 104, "text": "أفضل البقاء وحيداً", "trait": "الانبساط", "reverse": True},

            # التوافقية
            {"id": 105, "text": "متعاطف ويهتم بالآخرين", "trait": "التوافقية", "reverse": False},
            {"id": 106, "text": "يميل للنقد والجدال", "trait": "التوافقية", "reverse": True},
            {"id": 107, "text": "متعاون ويثق بالناس", "trait": "التوافقية", "reverse": False},
            {"id": 108, "text": "بارد/غير مهتم بالناس", "trait": "التوافقية", "reverse": True},

            # الضمير الحي
            {"id": 109, "text": "منظم ويُتم أعماله", "trait": "الضمير الحي", "reverse": False},
            {"id": 110, "text": "يميل للفوضى وترك المهام", "trait": "الضمير الحي", "reverse": True},
            {"id": 111, "text": "يعتمد عليه ويمكن الوثوق به", "trait": "الضمير الحي", "reverse": False},
            {"id": 112, "text": "غير منضبط ويفوّت المواعيد", "trait": "الضمير الحي", "reverse": True},

            # العصابية (الاستقرار الانفعالي عكسها)
            {"id": 113, "text": "يتوتر ويقلق بسهولة", "trait": "العُصابية", "reverse": False},
            {"id": 114, "text": "يبقى هادئاً تحت الضغط", "trait": "العُصابية", "reverse": True},
            {"id": 115, "text": "يتقلب مزاجه كثيراً", "trait": "العُصابية", "reverse": False},
            {"id": 116, "text": "نادراً ما يشعر بالغضب أو الانزعاج", "trait": "العُصابية", "reverse": True},

            # الانفتاح
            {"id": 117, "text": "خياله واسع ويقدّر الفن والأفكار الجديدة", "trait": "الانفتاح", "reverse": False},
            {"id": 118, "text": "يفضل المألوف ويرفض التغيير", "trait": "الانفتاح", "reverse": True},
            {"id": 119, "text": "فضولي ويحب التعلّم", "trait": "الانفتاح", "reverse": False},
            {"id": 120, "text": "غير مهتم بالتجارب الجديدة", "trait": "الانفتاح", "reverse": True},
        ],
        "traits": ["الانبساط", "التوافقية", "الضمير الحي", "العُصابية", "الانفتاح"],
        "max_per_item": 5,
    },
}

# ======================================================================
# أدوات مساعدة
# ======================================================================

def _reverse_if_needed(score: int, max_per_item: int, reverse: bool) -> int:
    """عكس الدرجة إذا لزم: new = (max+1) - old  (مثلاً في مقياس 1..7 يصبح 8 - x)."""
    if not reverse:
        return score
    return (max_per_item + 1) - score

def _traits_init(traits: List[str]) -> Dict[str, List[int]]:
    return {t: [] for t in traits}

def _normalize_0_100(x: float, max_val: float) -> float:
    if max_val <= 0:
        return 0.0
    return round(100.0 * x / max_val, 1)

# ======================================================================
# حساب النتيجة
# ======================================================================

def score_personality(test_key: str, answers: Dict[int, int]) -> Dict[str, Any]:
    """
    يُرجع:
      {
        "traits": { "الانبساط": 62.5, ... }  # نسب مئوية 0-100
        "raw_means": { "الانبساط": 4.8, ... } # متوسطات قبل التحويل
        "total_answered": n
      }
    """
    test = PERS_TESTS.get(test_key)
    if not test:
        return {"error": "اختبار شخصية غير معروف"}

    max_per_item = test["max_per_item"]
    traits = test["traits"]
    buckets = _traits_init(traits)

    # ضع الدرجات (مع العكس للبنود المعكوسة)
    items = test["items"]
    for it in items:
        qid = it["id"]
        if qid not in answers:
            # تجاهل البنود الفارغة (أو يمكننا فرضها في صفحة النموذج)
            continue
        raw = int(answers[qid])
        adj = _reverse_if_needed(raw, max_per_item, bool(it.get("reverse")))
        buckets[it["trait"]].append(adj)

    # حساب المتوسطات وتحويلها إلى 0..100
    raw_means: Dict[str, float] = {}
    norm: Dict[str, float] = {}
    for trait, vals in buckets.items():
        if not vals:
            raw_means[trait] = 0.0
            norm[trait] = 0.0
            continue
        mean_val = sum(vals) / float(len(vals))   # متوسط 1..max_per_item
        raw_means[trait] = round(mean_val, 2)
        norm[trait] = _normalize_0_100(mean_val - 1, max_per_item - 1)  # حوّله لنسبة

    return {
        "traits": norm,
        "raw_means": raw_means,
        "total_answered": len([k for k in answers if k in {i["id"] for i in items}]),
    }

def get_scale_options(test_key: str) -> Dict[int, str]:
    test = PERS_TESTS.get(test_key)
    return test.get("scale", {}) if test else {}
