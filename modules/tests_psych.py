# -*- coding: utf-8 -*-
"""
اختبارات نفسية (أعراض): قلق، اكتئاب، أرق، هلع... إلخ
صيغة موحّدة: dict اسمه PSYCH_TESTS يحتوي على اختبارات.
كل اختبار: { key, name, about, scale, items: [{id, text}], interpret(total)->str }
تقويم الدرجات: score_test(test_key, answers)
"""

from __future__ import annotations
from typing import Dict, Any, List

# مقياس ليكرت موحد 0..3
LIKERT_0_3 = {
    0: "أبدًا/لا",
    1: "أحيانًا",
    2: "غالبًا",
    3: "دائمًا/شديد"
}

def _items_from_text(block: str) -> List[Dict[str, Any]]:
    """يبني قائمة بنود من نص سطر-سطر (يفيد سهولة القراءة/الترجمة)."""
    out: List[Dict[str, Any]] = []
    i = 1
    for line in block.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        out.append({"id": i, "text": line})
        i += 1
    return out

PSYCH_TESTS: Dict[str, Dict[str, Any]] = {
    "gad7": {
        "key": "gad7",
        "name": "مقياس القلق العام (GAD-7)",
        "about": "أداة سريعة لقياس شدة القلق خلال آخر أسبوعين.",
        "scale": LIKERT_0_3,
        "items": _items_from_text("""
الشعور بالعصبية أو القلق أو التوتر
عدم القدرة على التوقف عن القلق أو التحكم فيه
القلق الزائد حول أشياء مختلفة
صعوبة في الاسترخاء
التململ بحيث يصعب الجلوس ساكنًا
الانزعاج بسهولة أو التهيّج
الشعور بالخوف مثل أن شيئًا سيئًا قد يحدث
        """),
        "interpret": lambda total: (
            "خفيف (0-4)" if total <= 4 else
            "متوسط (5-9)" if total <= 9 else
            "متوسط-شديد (10-14)" if total <= 14 else
            "شديد (15-21)"
        )
    },
    "phq9": {
        "key": "phq9",
        "name": "مقياس الاكتئاب (PHQ-9)",
        "about": "يقدّر شدة أعراض الاكتئاب خلال أسبوعين.",
        "scale": LIKERT_0_3,
        "items": _items_from_text("""
قلة الاهتمام أو المتعة في فعل الأشياء
الشعور بالاكتئاب أو الإحباط أو اليأس
صعوبة في النوم أو فرط النوم
التعب أو قلة الطاقة
ضعف الشهية أو فرط الأكل
الشعور بسوء حول الذات أو بالفشل
صعوبة التركيز على الأمور
بطء في الحركة/الكلام أو توتر زائد
أفكار بأنك سيكون من الأفضل لو مت أو بإيذاء النفس
        """),
        "interpret": lambda total: (
            "خفيف (0-4)" if total <= 4 else
            "خفيف-متوسط (5-9)" if total <= 9 else
            "متوسط (10-14)" if total <= 14 else
            "متوسط-شديد (15-19)" if total <= 19 else
            "شديد (20-27)"
        )
    },
    "insomnia": {
        "key": "insomnia",
        "name": "مؤشر الأرق المختصر",
        "about": "مؤشر تقريبي لصعوبات البدء/الاستمرار وجودة النوم.",
        "scale": LIKERT_0_3,
        "items": _items_from_text("""
صعوبة في بدء النوم
الاستيقاظ المتكرر ليلاً
الاستيقاظ مبكرًا دون القدرة على العودة للنوم
عدم الرضا عن جودة النوم
تأثير الأرق على النشاط النهاري
قلق/انشغال بسبب مشاكل النوم
        """),
        "interpret": lambda total: (
            "لا يُحتمل أرق سريري (0-7)" if total <= 7 else
            "احتمال أرق متوسّط (8-14)" if total <= 14 else
            "أرق شديد محتمل (15-18)"
        )
    },
    "panic": {
        "key": "panic",
        "name": "فاحص أعراض الهلع",
        "about": "شدة أعراض نوبات الهلع والسلوك التجنبي المرافق.",
        "scale": LIKERT_0_3,
        "items": _items_from_text("""
نوبات مفاجئة من خوف شديد
خفقان/تعرّق/ارتجاف أثناء النوبة
الخوف من فقدان السيطرة أو الموت خلال النوبة
قلق توقعي من حدوث النوبات
تجنب أماكن/مواقف خوفًا من النوبة
طلب طمأنة أو فحوصات متكررة
        """),
        "interpret": lambda total: (
            "خفيف" if total <= 5 else
            "متوسط" if total <= 10 else
            "شديد"
        )
    },
}

def score_test(test_key: str, answers: Dict[int, int]) -> Dict[str, Any]:
    """
    يُعيد: {"total": int, "by_item": {id: value}, "range": (min,max), "level": str}
    """
    test = PSYCH_TESTS.get(test_key)
    if not test:
        raise ValueError("اختبار غير معروف")
    total = 0
    by_item: Dict[int, int] = {}
    for it in test["items"]:
        qid = it["id"]
        val = int(answers.get(qid, 0))
        by_item[qid] = val
        total += val
    # الحد الأعلى = عدد البنود * 3
    mx = len(test["items"]) * 3
    level = test["interpret"](total) if callable(test.get("interpret")) else ""
    return {
        "total": total,
        "by_item": by_item,
        "range": (0, mx),
        "level": level,
        "name": test["name"],
        "key": test_key,
    }

__all__ = ["PSYCH_TESTS", "score_test"]
