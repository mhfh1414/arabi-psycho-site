# -*- coding: utf-8 -*-
"""
اختبارات شخصية مختصرة: Big5 (قصير)، مهارة الصمود، تقدير الذات.
صياغة مشابهة للاختبارات النفسية لكن مفتاح مختلف: PERS_TESTS
وتابع التصحيح: score_personality(test_key, answers)
"""

from __future__ import annotations
from typing import Dict, Any, List

LIKERT_1_5 = {
    1: "لا أوافق إطلاقًا",
    2: "لا أوافق",
    3: "محايد",
    4: "أوافق",
    5: "أوافق بشدة",
}

def _items(lines: List[str]) -> List[Dict[str, Any]]:
    return [{"id": i + 1, "text": s.strip()} for i, s in enumerate(lines) if s.strip()]

PERS_TESTS: Dict[str, Dict[str, Any]] = {
    "bfi10": {
        "key": "bfi10",
        "name": "العوامل الخمسة الكبرى (قصير)",
        "about": "نسخة قصيرة جدًا للفحص الأولي للعوامل الخمسة (انفتاح، يقظة، انبساط، توافق، عصابية).",
        "scale": LIKERT_1_5,
        "items": _items([
            "أرى نفسي شخصًا منظمًا ومنضبطًا",
            "أرى نفسي متعاونًا ويهتم بالآخرين",
            "أرى نفسي قلقًا يميل للتوتر",
            "أرى نفسي منفتحًا على التجارب والأفكار الجديدة",
            "أرى نفسي اجتماعيًا ومتحمسًا",
            "أرى نفسي يميل للفوضى أو التسويف (عكسي)",
            "أرى نفسي ينتقد الآخرين أو يتشاجر بسهولة (عكسي)",
            "أرى نفسي هادئًا متزنًا (عكسي للعصابية)",
            "أرى نفسي تقليديًا غير محب للتجديد (عكسي للانفتاح)",
            "أرى نفسي منعزلاً أو خجولاً (عكسي للانبساط)",
        ]),
        # خرائط البنود لكل بعد (مع إشارة -1 للعكسي)
        "keys": {
            "يقظة":  {1: +1, 6: -1},
            "توافق": {2: +1, 7: -1},
            "عصابية":{3: +1, 8: -1},
            "انفتاح":{4: +1, 9: -1},
            "انبساط":{5: +1,10: -1},
        },
        "interpret_dim": lambda x: "مرتفع" if x >= 7 else ("متوسط" if x >= 5 else "منخفض"),
    },
    "grit": {
        "key": "grit",
        "name": "مقياس الصمود/المثابرة (قصير)",
        "about": "يقيس المثابرة والشغف نحو الأهداف طويلة الأمد.",
        "scale": LIKERT_1_5,
        "items": _items([
            "أُكمل ما أبدأه غالبًا",
            "لا أتخلى بسهولة عن الأهداف الصعبة",
            "أتشتت سريعًا عن مشاريعي (عكسي)",
            "أعمل بانتظام لتحقيق أهداف طويلة الأمد",
            "أحافظ على جهدي رغم العراقيل",
            "أغيّر أهدافي كثيرًا (عكسي)",
        ]),
        "reverse": [3, 6],
        "interpret": lambda total: "عالي" if total >= 22 else ("متوسط" if total >= 17 else "منخفض"),
    },
    "self_esteem": {
        "key": "self_esteem",
        "name": "تقدير الذات (قصير)",
        "about": "مؤشر عام لتقدير الذات.",
        "scale": LIKERT_1_5,
        "items": _items([
            "أنا راضٍ عن نفسي عمومًا",
            "أشعر أن لي صفات جيدة",
            "أميل للاعتقاد أنني فاشل (عكسي)",
            "أملك موقفًا إيجابيًا نحو نفسي",
            "أتمنى لو احترمت نفسي أكثر (عكسي)",
        ]),
        "reverse": [3, 5],
        "interpret": lambda total: "مرتفع" if total >= 18 else ("متوسط" if total >= 13 else "منخفض"),
    },
}

def _score_sum(test: Dict[str, Any], answers: Dict[int, int]) -> int:
    total = 0
    rev = set(test.get("reverse", []))
    for it in test["items"]:
        qid = it["id"]
        v = int(answers.get(qid, 1))
        if qid in rev:
            v = 6 - v  # قلب (1..5)
        total += v
    return total

def score_personality(test_key: str, answers: Dict[int, int]) -> Dict[str, Any]:
    test = PERS_TESTS.get(test_key)
    if not test:
        raise ValueError("اختبار شخصية غير معروف")
    result: Dict[str, Any] = {"key": test_key, "name": test["name"]}

    if test_key == "bfi10":
        dims = {}
        for dim, mapping in test["keys"].items():
            s = 0
            for q, w in mapping.items():
                v = int(answers.get(q, 3))
                # قلب العكسي في هذا المقياس: إذا الوزن -1 نعكس
                if w < 0:
                    v = 6 - v
                s += v
            dims[dim] = s
        result["dimensions"] = dims
        result["total"] = sum(dims.values())
        result["levels"] = {k: test["interpret_dim"](v) for k, v in dims.items()}
    else:
        total = _score_sum(test, answers)
        result["total"] = total
        result["level"] = test["interpret"](total) if callable(test.get("interpret")) else ""

    return result

__all__ = ["PERS_TESTS", "score_personality"]
