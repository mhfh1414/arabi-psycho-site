"""
DSM-5 Schizophrenia Spectrum Disorders (Arabic)
ملف: DSM5/schizophrenia_spectrum.py
"""

from typing import Dict, List, Any
import json

SCHIZO_SPECTRUM: Dict[str, Dict[str, Any]] = {
    "schizophrenia": {
        "name_ar": "الفصام",
        "name_en": "Schizophrenia",
        "overview": "أعراض ذهانية مستمرة تشمل أوهام، هلوسات، كلام/سلوك غير منظّم، وأعراض سلبية.",
        "duration": "≥ 6 أشهر مع شهر نشط على الأقل.",
        "criteria": [
            {"code": "A", "text": "≥2 أعراض (أوهام، هلوسات، كلام غير منظم، سلوك غير منظّم/جامودي، أعراض سلبية)."},
            {"code": "B", "text": "اختلال كبير في الأداء الاجتماعي/المهني."},
            {"code": "C", "text": "استمرار ≥6 أشهر."}
        ]
    },
    "schizoaffective": {
        "name_ar": "الاضطراب الفصامي العاطفي",
        "name_en": "Schizoaffective Disorder",
        "overview": "نوبة مزاجية كبرى مترافقة مع أعراض فصامية، مع وجود فترة ذهانية دون أعراض مزاجية.",
        "duration": "≥ شهر واحد لأعراض الفصام، مع نوبات مزاجية مرافقة.",
        "criteria": [
            {"code": "A", "text": "نوبة مزاجية كبرى (اكتئاب/هوس) مع أعراض فصامية."},
            {"code": "B", "text": "≥2 أسبوع من الذهان بدون أعراض مزاجية."}
        ]
    }
}

def list_disorders() -> List[Dict[str, Any]]:
    return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in SCHIZO_SPECTRUM.items()]

def get_disorder(key: str) -> Dict[str, Any]:
    return SCHIZO_SPECTRUM[key]

def export_json(indent: int = 2) -> str:
    return json.dumps(SCHIZO_SPECTRUM, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    print(list_disorders())
  
