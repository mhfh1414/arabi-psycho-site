# -*- coding: utf-8 -*-
"""
DSM-5 Arabic helper (بدون فهرس عام)
قاعدة أمراض وخطط علاج معرفي-سلوكي مفصلة للاستخدام داخل الموقع.
"""

from __future__ import annotations
from typing import Dict, List, Any
import json

# =========================================================
# قاعدة الأمراض (موسّعة)
# الحقول:
# id, key, name_ar, summary, criteria[], cbt_plan{goals[], techniques[{name,steps[]}], homework[], sessions, measures[]}
# =========================================================

DISORDERS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "key": "gad",
        "name_ar": "اضطراب القلق العام",
        "summary": "قلق مفرط صعب التحكم فيه أغلب الأيام ≥ 6 أشهر مع أعراض جسدية ومعرفية.",
        "criteria": [
            "قلق/انشغال مفرط حول مجالات متعددة ≥ 6 أشهر",
            "صعوبة في السيطرة على القلق",
            "٣ أعراض أو أكثر: توتر، إرهاق، صعوبة تركيز، تهيج، توتر عضلي، اضطراب نوم",
            "ضائقة أو تضرر وظيفي واضح"
        ],
        "cbt_plan": {
            "goals": ["خفض شدة القلق", "زيادة التسامح مع عدم اليقين", "تحسين النوم والوظيفة اليومية"],
            "techniques": [
                {"name": "التثقيف النفسي", "steps": ["نموذج القلق (مثير-فكرة-انفعال-سلوك)", "تمييز القلق المفيد مقابل المضر"]},
                {"name": "مراقبة القلق", "steps": ["سجل يومي: الموقف/الفكرة/الانفعال/السلوك/الشدة (0-10)"]},
                {"name": "إعادة البناء المعرفي", "steps": ["تحديد التشوهات", "أسئلة سقراطية", "بدائل متوازنة"]},
                {"name": "التعرّض للهمّ المؤجل", "steps": ["وقت قلق محدد", "منع الطمأنة", "تجارب سلوكية"]},
                {"name": "استرخاء قصير", "steps": ["تنفس بطني 4-6", "إرخاء عضلي تدريجي مختصر"]},
            ],
            "homework": ["سجل القلق اليومي", "تمارين تنفس مرتين يومياً", "تحدي فكرة واحدة يومياً"],
            "sessions": 10,
            "measures": ["GAD-7", "PSQI للنوم"]
        }
    },
    {
        "id": 2,
        "key": "panic",
        "name_ar": "اضطراب الهلع",
        "summary": "نوبات هلع متكررة مع قلقٍ توقّعي أو تجنب منذ ≥ شهر.",
        "criteria": [
            "نوبات هلع مفاجئة ومتكررة",
            "شهر أو أكثر من القلق التوقعي أو تغيرات سلوكية تجنبية",
            "الاعراض ليست بسبب مادة/حالة طبية"
        ],
        "cbt_plan": {
            "goals": ["إطفاء الخوف من الإحساسات الجسدية", "خفض التجنب والطمأنة"],
            "techniques": [
                {"name": "التثقيف", "steps": ["منحنى القلق", "الأمان الجسدي لأعراض الهلع"]},
                {"name": "التعرّض الداخلي", "steps": ["استثارة الإحساسات (دوران، الجري مكانك، تنفس من قشة)", "المراقبة حتى يهبط القلق دون سلوك أمان"]},
                {"name": "التعرّض للمواقف", "steps": ["سلم مواقف (السوق، السيارة، المصعد)", "منع الهروب/الطمأنة"]},
                {"name": "إعادة التفسير", "steps": ["الخفقان ≠ نوبة قلب", "دوخة ≠ إغماء"]},
            ],
            "homework": ["تكرار تعرّض داخلي يومي", "زيارتان لموقف متجنب أسبوعياً"],
            "sessions": 8,
            "measures": ["PDSS", "MIA"]
        }
    },
    {
        "id": 3,
        "key": "mdd",
        "name_ar": "الاكتئاب الجسيم",
        "summary": "مزاج مكتئب أو فقدان متعة مع 5 أعراض لأسبوعين على الأقل.",
        "criteria": [
            "مزاج مكتئب/فقدان الاهتمام معظم اليوم",
            "تغير نوم/شهية/طاقة/تركيز/تباطؤ أو هياج/ذنب/أفكار إيذاء",
            "ضائقة أو تعطل وظيفي"
        ],
        "cbt_plan": {
            "goals": ["زيادة التفعيل السلوكي", "تعديل المعتقدات السلبية الجوهرية"],
            "techniques": [
                {"name": "التفعيل السلوكي", "steps": ["قائمة أنشطة ممتعة وذات قيمة", "جدولة أسبوعية", "تتبع المزاج مقابل النشاط"]},
                {"name": "رصد الأفكار التلقائية", "steps": ["سجل أفكار", "بدائل واقعية", "تجارب سلوكية"]},
                {"name": "مهارات حل المشكلات", "steps": ["تعريف المشكلة", "عصف بدائل", "خطة وتجربة"]},
                {"name": "وقاية الانتكاس", "steps": ["علامات مبكرة", "خطة عمل 30-60-90 يوم"]},
            ],
            "homework": ["٣ أنشطة/أسبوع على الأقل", "نموذج تفكير واحد يومياً"],
            "sessions": 12,
            "measures": ["PHQ-9", "WSAS"]
        }
    },
    {
        "id": 4,
        "key": "ocd",
        "name_ar": "الوسواس القهري",
        "summary": "وساوس/قهر تستغرق وقتًا وتسبب ضيقًا أو تعطيلاً.",
        "criteria": ["وساوس أو أفعال قهرية متكررة", "استغراق > ساعة يومياً أو تضرر وظيفي"],
        "cbt_plan": {
            "goals": ["زيادة التسامح مع عدم اليقين", "خفض الطقوس القهرية"],
            "techniques": [
                {"name": "ERP (تعرّض ومنع استجابة)", "steps": ["سلم تدرج", "تعرّض حي/تخيلي", "منع كل الطقوس والطمأنة"]},
                {"name": "تجارب سلوكية", "steps": ["اختبار التنبؤات (لو لم أغسل...)", "قياس القلق حتى يهبط"]},
            ],
            "homework": ["ERP منزلي 20-40 دقيقة يومياً"],
            "sessions": 14,
            "measures": ["Y-BOCS"]
        }
    },
    # ... بقية الاضطرابات 5 → 12 كما في نسختك السابقة ...
]

# =========================================================
# دوال مساعدة
# =========================================================

def get_all_disorders() -> List[Dict[str, Any]]:
    return DISORDERS

def get_disorder_by_id(disorder_id: int) -> Dict[str, Any]:
    for it in DISORDERS:
        if it["id"] == disorder_id:
            return it
    return {}

def get_disorder_by_key(key: str) -> Dict[str, Any]:
    key = (key or "").strip().lower()
    for it in DISORDERS:
        if it["key"] == key:
            return it
    return {}

def search_disorders(q: str) -> List[Dict[str, Any]]:
    """بحث بسيط بالاسم/الملخص/المعايير."""
    q = (q or "").strip().lower()
    if not q:
        return []
    hits: List[Dict[str, Any]] = []
    for it in DISORDERS:
        blob = " ".join([
            it.get("name_ar",""),
            it.get("summary",""),
            " ".join(it.get("criteria", [])),
            " ".join([t["name"] for t in it.get("cbt_plan",{}).get("techniques", [])])
        ]).lower()
        if q in blob:
            hits.append({
                "id": it["id"],
                "key": it["key"],
                "name_ar": it["name_ar"],
                "snippet": it["summary"]
            })
    return hits

def get_treatment_plan(key_or_id: Any) -> Dict[str, Any]:
    item: Dict[str, Any] = {}
    if isinstance(key_or_id, int):
        item = get_disorder_by_id(key_or_id)
    else:
        item = get_disorder_by_key(str(key_or_id))
    return item.get("cbt_plan", {})

def to_json(indent: int = 2) -> str:
    return json.dumps(DISORDERS, ensure_ascii=False, indent=indent)

# اختبار سريع محلي
if __name__ == "__main__":
    print("عدد الاضطرابات:", len(get_all_disorders()))
    print("بحث 'تعرّض':", [x["name_ar"] for x in search_disorders("تعرّض")])
    print("خطة الأرق:", get_treatment_plan("insomnia")["techniques"])
