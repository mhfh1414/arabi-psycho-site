# -*- coding: utf-8 -*-
"""
DSM-5 Arabic Index / Loader
ملف: dsm_index.py

✅ الفكرة:
- يجمع كل ملفات DSM5 تلقائياً (سواءً كانت مرقّمة مثل 01_*.py أو بدون أرقام).
- يحمّل الداتا من كل ملف ويضعها في سجل REGISTRY جاهز للاستدعاء.
- يوفر دوال موحّدة: categories / list_all / get / search_all / to_markdown / export_all_json

📌 ضع هذا الملف داخل مجلد المشروع (جذر الريبو) أو بجانب site_app.py
   مع وجود مجلد DSM5/ بداخله الملفات.
"""

import os, glob, json, re, importlib.util
from typing import Dict, Any, List, Tuple

# مجلد ملفات DSM5
DSM_DIR = os.path.join(os.path.dirname(__file__), "DSM5")

# تعريف كل فئة: نمط اسم الملف -> اسم المتغيّر الداخلي في الملف -> مفتاح الفئة في الريجيستري
CATEGORIES: List[Tuple[str, str, str]] = [
    ("*anxiety_disorders.py",              "ANXIETY_DISORDERS",   "anxiety"),
    ("*ocd_related_disorders.py",          "OCD_RELATED",         "ocd_related"),
    ("*mood_disorders.py",                 "MOOD_DISORDERS",      "mood"),
    ("*schizophrenia_spectrum.py",         "SCHIZO_SPECTRUM",     "schizo_spectrum"),
    ("*neurodevelopmental_disorders.py",   "NEURODEV",            "neurodevelopmental"),
    ("*trauma_stressor_disorders.py",      "TRAUMA_STRESSOR",     "trauma_stressor"),
    ("*dissociative_disorders.py",         "DISSOCIATIVE",        "dissociative"),
    ("*somatic_symptom_disorders.py",      "SOMATIC",             "somatic"),
    ("*feeding_eating_disorders.py",       "EATING",              "feeding_eating"),
    ("*elimination_disorders.py",          "ELIMINATION",         "elimination"),
    ("*sleep_wake_disorders.py",           "SLEEP_WAKE",          "sleep_wake"),
    ("*sexual_dysfunctions.py",            "SEXUAL_DYS",          "sexual_dys"),
    ("*gender_dysphoria.py",               "GENDER_DYSPHORIA",    "gender_dysphoria"),
    ("*disruptive_impulse_control.py",     "DISRUPTIVE",          "disruptive_impulse"),
    ("*substance_disorders.py",            "SUBSTANCE",           "substance"),
    ("*neurocognitive_disorders.py",       "NEUROCOG",            "neurocognitive"),
    ("*personality_disorders.py",          "PERSONALITY",         "personality"),
    ("*paraphilic_disorders.py",           "PARAPHILIC",          "paraphilic"),
    ("*other_disorders.py",                "OTHER",               "other"),
]

# السجل النهائي: {category_key: dataset_dict}
REGISTRY: Dict[str, Dict[str, Any]] = {}

def _safe_mod_name(path: str) -> str:
    """حَوّل اسم الملف لاسم صالح لبايثون لتحميله ديناميكياً."""
    stem = os.path.splitext(os.path.basename(path))[0]
    return re.sub(r"[^0-9a-zA-Z_]", "_", stem)

def _load_module_from_path(path: str):
    name = _safe_mod_name(path)
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot load module: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod

def load_all() -> Dict[str, Dict[str, Any]]:
    """حمّل كل الفئات حسب الأنماط أعلاه وضعها في REGISTRY."""
    REGISTRY.clear()
    if not os.path.isdir(DSM_DIR):
        raise FileNotFoundError(f"DSM5 folder not found at: {DSM_DIR}")

    for pattern, varname, cat_key in CATEGORIES:
        matches = sorted(glob.glob(os.path.join(DSM_DIR, pattern)))
        if not matches:
            continue
        # لو وُجد أكثر من ملف لنفس الفئة، نأخذ الأحدث تعديلًا
        path = max(matches, key=os.path.getmtime)
        mod = _load_module_from_path(path)
        if not hasattr(mod, varname):
            raise AttributeError(f"{os.path.basename(path)} لا يحتوي المتغير {varname}")
        data = getattr(mod, varname)
        if not isinstance(data, dict):
            raise TypeError(f"{varname} في {path} يجب أن يكون dict")
        REGISTRY[cat_key] = data
    return REGISTRY

# حمّل مباشرة عند الاستيراد
load_all()

# -----------------------
# واجهة استخدام موحّدة
# -----------------------
def categories() -> List[str]:
    """أرجع قائمة مفاتيح الفئات المحمّلة."""
    return list(REGISTRY.keys())

def list_all() -> Dict[str, List[Dict[str, Any]]]:
    """أرجع قائمة مختصرة لكل الفئات (key + name_ar + name_en)."""
    out: Dict[str, List[Dict[str, Any]]] = {}
    for cat, ds in REGISTRY.items():
        items = []
        for k, v in ds.items():
            items.append({"key": k, "name_ar": v.get("name_ar"), "name_en": v.get("name_en")})
        out[cat] = items
    return out

def get(category: str, key: str) -> Dict[str, Any]:
    """جِب اضطراباً محدداً بالتصنيف والمفتاح."""
    return REGISTRY[category][key]

def search_all(query: str) -> List[Dict[str, str]]:
    """بحث بسيط عبر جميع الفئات (بالاسم العربي/الإنجليزي ونبذة overview)."""
    q = (query or "").strip().lower()
    if not q:
        return []
    hits: List[Dict[str, str]] = []
    for cat, ds in REGISTRY.items():
        for k, v in ds.items():
            hay = f"{v.get('name_ar','')} {v.get('name_en','')} {v.get('overview','')}".lower()
            if q in hay:
                hits.append({"category": cat, "key": k, "name_ar": v.get("name_ar","")})
    return hits

def to_markdown(category: str, key: str) -> str:
    """صياغة Markdown جاهزة للعرض/الطباعة."""
    d = get(category, key)
    lines = [
        f"# {d.get('name_ar','')}",
        f"**{d.get('name_en','')}**\n",
        f"**نظرة عامة:** {d.get('overview','')}",
        f"**المدة الشائعة/الشرط الزمني:** {d.get('duration','—')}\n",
        "**المعايير التشخيصية (ملخص):**",
    ]
    for c in d.get("criteria", []):
        lines.append(f"- ({c.get('code','?')}) {c.get('text','')}")
    specs = d.get("specifiers")
    if specs:
        lines.append("\n**محددات/أنماط فرعية:** " + ", ".join(specs))
    sev = d.get("severity_guidance")
    if sev:
        lines.append(f"\n**توجيه تقدير الشدة:** {sev}")
    diffs = d.get("differentials")
    if diffs:
        lines.append("\n**تشاخيص تفريقية مختصرة:** " + ", ".join(diffs))
    return "\n".join(lines)

def export_all_json(indent: int = 2) -> str:
    """تصدير كل السجل كـ JSON واحد."""
    return json.dumps(REGISTRY, ensure_ascii=False, indent=indent)

# مثال تشغيل يدوي
if __name__ == "__main__":
    print("الفئات المحمّلة:", categories())
    print("أمثلة نتائج البحث عن 'قلق':", search_all("قلق"))
    # مثال Markdown
    # print(to_markdown("anxiety", "gad"))
