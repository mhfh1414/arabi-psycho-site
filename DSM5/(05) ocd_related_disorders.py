"""
DSM-5 OCD & Related Disorders (Arabic)
ملف: ocd_related_disorders.py
"""
# بقية الاستيرادات…
""" DSM-5 OCD & Related Disorders (Arabic, structured for app/bot use) File: DSM5/ocd_related_disorders.py

Usage: from DSM5.ocd_related_disorders import list_disorders, get_disorder, search, to_markdown, checklist, export_json

Notes:

نص عربي مُبسّط ومكثّف اعتماداً على صياغات DSM‑5 (تلخيص لأغراض سريرية وتعليمية).

الحقول معدّة لتغذية الموقع/البوت + الطباعة. """ from typing import Dict, List, Any import json


------------------------------

Core dataset

------------------------------

OCD_RELATED: Dict[str, Dict[str, Any]] = { "ocd": { "name_ar": "اضطراب الوسواس القهري", "name_en": "Obsessive-Compulsive Disorder (OCD)", "overview": ( "وساوس (أفكار/اندفاعات/صور متكررة ومُلحّة) و/أو أفعال قهرية (سلوكيات/ذهنيات متكررة) تهدف لتخفيف الضيق، لكنها ليست مرتبطة واقعياً بما تخشاه أو مفرطة. تسبب ضيقاً أو اختلالاً واضحاً." ), "duration": "مزمن عادة بدرجات مختلفة؛ لا شرط مدة محدد لكن استمرار ملحوظ ومؤثر.", "criteria": [ {"code": "A1", "text": "وجود وساوس: أفكار/اندفاعات/صور مُلحّة، يُنظر لها كدخيلة وتسبب قلقاً/ضيقاً."}, {"code": "A2", "text": "يحاول الفرد تجاهل/قمع الوساوس أو تحييدها بفعل قهري."}, {"code": "B1", "text": "أفعال قهرية: سلوكيات متكررة (غسل، ترتيب، تحقق) أو أفعال ذهنية (دعاء، عدّ)."}, {"code": "B2", "text": "يهدف السلوك إلى تقليل القلق أو منع حدث ما؛ لكنه مفرط أو غير مرتبط واقعياً."}, {"code": "C", "text": "الوساوس/الأفعال القهرية تستغرق وقتاً (مثلاً >1 ساعة/يوم) أو تسبب اختلالاً واضحاً."}, {"code": "D", "text": "غير منسوب لمادة/حالة طبية وغير مفسّر باضطراب آخر (مثل قلق، أكل، طيف ذهاني)."} ], "specifiers": [ "درجة البصيرة: جيدة/متوسطة، ضعيفة، غائبة (معتقدات وهامية)", "مرتبط بالتشنجات اللاإرادية (Tic-related)" ], "severity_guidance": "قدّر الوقت المستغرق، درجة الضيق، التهرب/التجنّب، والاختلال الوظيفي.", "differentials": [ "اضطراب قلق معمّم/رُهاب التلوّث بدون طقوس واضحة", "اضطراب وسواس قهري شخصية (سمة مقابل اضطراب سريري)", "ذهانات، اضطرابات أكل، اضطراب طيف التوحد" ] },

"body_dysmorphic": {
    "name_ar": "اضطراب التشوّه الجسدي",
    "name_en": "Body Dysmorphic Disorder",
    "overview": "انشغال بعيب مُدرك في المظهر (غير ملحوظ للآخرين) مع سلوكيات متكررة/أفعال ذهنية استجابة للقلق (تفحّص المرآة، سؤال طمأنة).",
    "duration": "مزمن عادة؛ ليس هناك شرط مدة محدد وإنما تأثير وظيفي واضح.",
    "criteria": [
        {"code": "A", "text": "انشغال بعيب/عيوب مُدرَكة في المظهر غير ملحوظة أو طفيفة."},
        {"code": "B", "text": "سلوكيات متكررة أو أفعال ذهنية استجابة لانشغال المظهر (تفحّص، تمويه، مقارنة)."},
        {"code": "C", "text": "يسبب ضيقاً واختلالاً وظيفياً ملحوظاً."},
        {"code": "D", "text": "غير مفسّر بصورة أفضل باضطراب الأكل (الانشغال بالوزن/الشكل العام)."}
    ],
    "specifiers": [
        "مع انشغال بالعضلات (Muscle dysmorphia)",
        "درجة البصيرة: جيدة/متوسطة، ضعيفة، غائبة"
    ],
    "severity_guidance": "قيّم الزمن المستغرق، درجة التجنّب، وحِدّة السلوكيات المتكررة.",
    "differentials": ["اضطرابات أكل، قلق اجتماعي، ذهان، وسواس قهري"]
},

"hoarding": {
    "name_ar": "اضطراب الاكتناز (Hoarding)",
    "name_en": "Hoarding Disorder",
    "overview": "صعوبة مستمرة في التخلّي عن الممتلكات بغض النظر عن قيمتها، بسبب حاجة مُدرَكة للاحتفاظ وضيق عند التخلّي؛ تراكم يسبب ازدحاماً وفقدان وظائف المساحات.",
    "duration": "مزمن تدريجي؛ لا شرط مدة محدد لكن ينعكس على الاستعمال اليومي للمكان.",
    "criteria": [
        {"code": "A", "text": "صعوبة مستمرة في التخلّي/التصرّف بالممتلكات."},
        {"code": "B", "text": "حاجة مُدركة للاحتفاظ وضيق شديد عند التخلّي."},
        {"code": "C", "text": "تراكم يؤدي لازدحام المناطق المعيشية وفقدان وظيفتها."},
        {"code": "D", "text": "يسبب اختلالاً وظيفياً/خطر أمان (نظافة، حريق)."},
        {"code": "E", "text": "غير مفسّر باضطراب طبي/عقلي آخر (مثال: إصابة دماغية، ذهان)."}
    ],
    "specifiers": [
        "مع الإفراط في الاقتناء (Excessive acquisition)",
        "درجة البصيرة: جيدة/متوسطة، ضعيفة، غائبة"
    ],
    "severity_guidance": "استخدم مقياس ازدحام المنزل، مخاطر السلامة، والإعاقة اليومية.",
    "differentials": ["اكتناز طبيعي/ثقافي، ذهان، خرف/اضطراب إدراكي، وسواس قهري"]
},

"trichotillomania": {
    "name_ar": "اضطراب نتف الشعر",
    "name_en": "Trichotillomania (Hair-Pulling Disorder)",
    "overview": "نتف متكرر للشعر يؤدي إلى فقدان ملحوظ للشعر مع محاولات فاشلة للتقليل/الإيقاف وضيق أو اختلال وظيفي.",
    "duration": "مزمن/ناكس؛ لا شرط مدة محدد.",
    "criteria": [
        {"code": "A", "text": "نتف متكرر للشعر يؤدي لفقدانه."},
        {"code": "B", "text": "محاولات متكررة لتقليل/إيقاف النتف."},
        {"code": "C", "text": "يسبب ضيقاً/اختلالاً وظيفياً."},
        {"code": "D", "text": "غير منسوب لحالة جلدية طبية أو اضطراب عقلي آخر."}
    ],
    "specifiers": [],
    "severity_guidance": "مناطق النتف، الوقت المستغرق، إصابات الجلد، أثره الاجتماعي/المهني.",
    "differentials": ["اضطرابات جلدية، وسواس قهري، اضطرابات طيف التشنجات"]
},

"excoriation": {
    "name_ar": "اضطراب قشط الجلد",
    "name_en": "Excoriation (Skin-Picking) Disorder",
    "overview": "قشط/حكّ متكرر للجلد يؤدي لآفات، مع محاولات فاشلة للتقليل/الإيقاف وضيق أو اختلال." ,
    "duration": "مزمن/ناكس؛ لا شرط مدة محدد.",
    "criteria": [
        {"code": "A", "text": "قشط متكرر للجلد يؤدي لآفات."},
        {"code": "B", "text": "محاولات متكررة لتقليل/إيقاف القشط."},
        {"code": "C", "text": "يسبب ضيقاً/اختلالاً وظيفياً."},
        {"code": "D", "text": "غير منسوب لحالة جلدية أو اضطراب آخر."}
    ],
    "specifiers": [],
    "severity_guidance": "شدة الآفات، الإنتانات، أثره الاجتماعي/المهني.",
    "differentials": ["اضطرابات جلدية أولية، وسواس قهري، تعاطي مواد"]
},

"subst_med_induced_ocd": {
    "name_ar": "اضطراب وسواسي قهري مُحَثّ بمادة/دواء",
    "name_en": "Substance/Medication-Induced Obsessive-Compulsive and Related Disorder",
    "overview": "وساوس/قهور أو سلوكيات ذات صلة ناجمة فيزيولوجياً عن مادة/دواء أو انسحاب.",
    "duration": "مترافقة زمنياً مع التعرض/الانسحاب.",
    "criteria": [
        {"code": "A", "text": "أعراض وسواسية/قهورية تسود الصورة السريرية."},
        {"code": "B", "text": "دليل على البدء أثناء/بعد التعرض لمادة/دواء أو أثناء الانسحاب."},
        {"code": "C", "text": "غير مفسّرة باضطراب أولي مستقل (تسبق التعرض أو تستمر طويلاً بعده)."},
        {"code": "D", "text": "تسبب اختلالاً ملحوظاً."}
    ],
    "specifiers": ["بداية أثناء الانسمام", "بداية أثناء الانسحاب"],
    "severity_guidance": "تحقّق من العلاقة الزمنية واستبعد اضطراباً أولياً.",
    "differentials": ["OCD أولي، ذهان، اضطرابات قلق"]
},

"due_to_medical": {
    "name_ar": "اضطراب وسواسي قهري ناجم عن حالة طبية أخرى",
    "name_en": "Obsessive-Compulsive and Related Disorder Due to Another Medical Condition",
    "overview": "أعراض وسواسية/قهورية ناجمة مباشرة عن حالة طبية (آلية فيزيولوجية).",
    "duration": "وفق سير الحالة الطبية.",
    "criteria": [
        {"code": "A", "text": "أعراض وسواسية/قهورية أو سلوكيات متكررة بارزة."},
        {"code": "B", "text": "دليل على علاقة سببية مباشرة بحالة طبية (قصة/فحص/اختبارات)."},
        {"code": "C", "text": "غير مفسّرة باضطراب عقلي آخر."},
        {"code": "D", "text": "تسبب اختلالاً ملحوظاً."}
    ],
    "specifiers": [],
    "severity_guidance": "تماسك الدليل السببي، واستبعاد أسباب نفسية/دوائية.",
    "differentials": ["OCD أولي، اضطرابات حركية/عصبية"]
},

"other_specified": {
    "name_ar": "اضطراب وسواسي قهري محدد آخر",
    "name_en": "Other Specified Obsessive-Compulsive and Related Disorder",
    "overview": "صورة سريرية مرتبطة بطيف الوسواس القهري تسبب اختلالاً لكنها لا تستوفي معايير تشخيص نوعي؛ مع ذكر السبب (مثال: طقوس قصيرة المدة).",
    "duration": "متغيرة.",
    "criteria": [
        {"code": "A", "text": "أعراض ضمن طيف الوسواس القهري مع اختلال وظيفي، دون بلوغ العتبة الكاملة."}
    ],
    "specifiers": ["مثال: مدة غير كافية، أعراض تحت العتبة"],
    "severity_guidance": "اذكر السبب/السياق، وحدد الأهداف العلاجية.",
    "differentials": []
},

"unspecified": {
    "name_ar": "اضطراب وسواسي قهري غير محدد",
    "name_en": "Unspecified Obsessive-Compulsive and Related Disorder",
    "overview": "يستخدم عندما تكون المعلومات غير كافية لتصنيف أدق (إسعافي/مؤقت).",
    "duration": "—",
    "criteria": [
        {"code": "A", "text": "أعراض على طيف الوسواس القهري مهمة سريرياً مع نقص معلومات/زمن."}
    ],
    "specifiers": [],
    "severity_guidance": "تصنيف مؤقت إلى أن تتضح الصورة.",
    "differentials": []
}

}

------------------------------

Public helpers

------------------------------

def list_disorders() -> List[Dict[str, Any]]: """Return a list of all OCD-related disorders with keys and Arabic/English names.""" return [{"key": k, "name_ar": v["name_ar"], "name_en": v["name_en"]} for k, v in OCD_RELATED.items()]

def get_disorder(key: str) -> Dict[str, Any]: """Fetch a disorder dict by its key (e.g., 'ocd'). Raises KeyError if not found.""" return OCD_RELATED[key]

def search(query: str) -> List[str]: """Simple case-insensitive search in Arabic/English names and overview. Returns matching keys.""" q = (query or "").strip().lower() if not q: return [] hits: List[str] = [] for k, v in OCD_RELATED.items(): hay = f"{v['name_ar']} {v['name_en']} {v['overview']}".lower() if q in hay: hits.append(k) return hits

def to_markdown(key: str) -> str: """Render a disorder as Markdown (Arabic).""" d = get_disorder(key) lines = [ f"# {d['name_ar']}", f"{d['name_en']}\n", f"نظرة عامة: {d['overview']}", f"المدة الشائعة/الشرط الزمني: {d['duration']}\n", "المعايير التشخيصية (ملخص):", ] for c in d["criteria"]: lines.append(f"- ({c['code']}) {c['text']}") if d.get("specifiers"): lines.append("\nمحدِّدات/أنماط فرعية: " + ", ".join(d["specifiers"])) if d.get("severity_guidance"): lines.append(f"\nتوجيه تقدير الشدة: {d['severity_guidance']}") if d.get("differentials"): lines.append("\nتشاخيص تفريقية مختصرة: " + ", ".join(d["differentials"])) return "\n".join(lines)

def checklist(key: str) -> List[Dict[str, str]]: """Return a flat checklist of criteria suitable لرُدود (نعم/لا) في الواجهة.""" d = get_disorder(key) return [{"id": c["code"], "label": c["text"]} for c in d["criteria"]]

def export_json(indent: int = 2) -> str: """Export the whole dataset as JSON string (UTF-8).""" return json.dumps(OCD_RELATED, ensure_ascii=False, indent=indent)

Quick manual run (for debugging):

if name == "main": print("Available OCD-related disorders:\n", list_disorders()) print("\nMarkdown sample (OCD):\n") print(to_markdown("ocd"))
