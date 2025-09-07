# -*- coding: utf-8 -*-
# dsm_suite.py — ملف واحد ضخم: دراسة حالة + DSM موسّع + واجهة HTML داخلية
# يعمل عبر Blueprint: from dsm_suite import dsm_bp  ← ثم register في site_app.py

from flask import Blueprint, request, render_template_string, redirect
import re

dsm_bp = Blueprint("dsm_bp", __name__, url_prefix="/dsm")

# ===================== أدوات لغوية عربية =====================
_AR_DIAC  = r"[ًٌٍَُِّْـ]"
_AR_PUNCT = r"[.,،;؛!?؟()\[\]{}\"\'<>:/\\]"

def normalize(s: str) -> str:
    if not s: return ""
    s = s.strip()
    s = re.sub(_AR_DIAC, "", s)
    s = re.sub(_AR_PUNCT, " ", s)
    s = (s.replace("أ","ا").replace("إ","ا").replace("آ","ا")
           .replace("ة","ه").replace("ى","ي").replace("ؤ","و").replace("ئ","ي")
           .replace("ـ","").replace("ﻻ","لا").replace("ﻷ","لا"))
    s = re.sub(r"\s+", " ", s)
    return s.lower()

def tokenize(s: str): return normalize(s).split()

def similarity(text: str, phrase: str) -> float:
    """تشابه بسيط Jaccard على مستوى الكلمات بعد التطبيع."""
    T = set(tokenize(text)); P = set(tokenize(phrase))
    if not P: return 0.0
    return len(T & P) / len(P)

# ===================== مرادفات واسعة (عامي + فصيح) =====================
SYNONYMS = {
    # مزاج
    "حزن": ["زعل","كابه","تعاسه","ضيقه","طفش","غم","نكده"],
    "انعدام المتعة": ["فقدان المتعه","مافي متعه","لا استمتع","فقدان الاهتمام","ما عاد يفرحني شي"],
    "طاقة منخفضة": ["خمول","كسل","ارهاق","تعب","وهن","هبوط طاقه","تثاقل"],
    "اضطراب نوم": ["قلة نوم","كثرة نوم","ارق","نوم متقطع","استيقاظ مبكر","كوابيس","نعاس نهاري"],
    "شهية منخفضة": ["قلة اكل","سدت نفسي","فقدان شهية","ما لي نفس","شهية مسدوده"],
    "شهية زائدة": ["نهم","اكل بكثره","اكل عاطفي"],
    "انسحاب اجتماعي": ["انعزال","انطواء","تجنب اجتماعي","ما اطلع","ابتعاد عن الناس"],
    "تفكير انتحاري": ["افكار انتحار","تمني الموت","رغبه بالموت","افكر انهي حياتي"],
    # قلق/هلع
    "قلق": ["توتر","توجس","على اعصابي","ترقب","خوف مستمر","قلقان"],
    "نوبة هلع": ["خفقان","اختناق","ضيق نفس","ذعر","رجفه","تعرق","دوخه","خوف الموت"],
    "خوف اجتماعي": ["رهبه مواجهه","خجل مفرط","قلق اداء","اخاف اتكلم"],
    "خوف محدد": ["فوبيا","خوف طيران","خوف المرتفعات","خوف الظلام","خوف حقن","خوف حشرات","خوف دم"],
    # وسواس
    "وسواس": ["افكار متسلطه","اقتحاميه","هواجس","تدنيس"],
    "سلوك قهري": ["طقوس","تفقد متكرر","عد قهري","غسل متكرر","تنظيم مفرط"],
    # صدمة
    "حدث صادم": ["حادث شديد","اعتداء","كارثه","حرب","فقد عزيز","تنمر قاس"],
    "استرجاع الحدث": ["فلاش باك","ذكريات مؤلمه","كوابيس","فرط تيقظ"],
    # ذهان
    "هلوسة": ["هلاوس سمعيه","هلاوس بصريه","اسمع اصوات","اشوف اشياء","تهيؤات"],
    "اوهام": ["ضلالات","اعتقادات وهميه","اضطهاد","عظمه","غيره وهاميه","بارانويا"],
    # ADHD
    "تشتت": ["عدم تركيز","سهو","شرود","نسيان","ما اركز"],
    "فرط حركة": ["نشاط زائد","اندفاع","مقاطعه","ملل سريع","حركه زياده"],
    # توحد
    "تواصل اجتماعي ضعيف": ["صعوبه تواصل","تواصل غير لفظي ضعيف","قله تواصل بصري"],
    "اهتمامات مقيدة": ["روتين صارم","حساسيات صوت/ضوء","سلوك نمطي","اهتمامات محدوده"],
    # أكل/نوم
    "نهم": ["شراهه","نوبات اكل","اكل سرا","اكل عاطفي"],
    "تطهير": ["استفراغ متعمد","ملينات","صيام تعويضي"],
    # جسدية
    "الم غير مفسر": ["اوجاع متنقله","وجع بلا سبب"],
    "قلق صحي": ["وسواس مرض","توهم المرض","تفقد جسد"],
    # شخصية
    "تقلب عاطفي": ["مزاج متقلب","سريع الانفعال","مشاعر متطرفه"],
    "انشغال بالتفاصيل": ["كماليه","صرامه","جمود","قواعد صارمه"],
}

# ===================== قاعدة DSM موسَّعة (مختارة وكبيرة) =====================
# ملاحظة: كل تشخيص يحوي: keywords, required, weight, onset (اختياري)
DSM_DB = {
    # عصبي نمائي
    "اضطراب طيف التوحد": {
        "keywords": ["تواصل اجتماعي ضعيف","سلوك نمطي","روتين","حساسيات حسيه","اهتمامات مقيده","لغة متأخره","حركات نمطيه"],
        "required": ["تواصل اجتماعي ضعيف","سلوك نمطي"], "weight": 1.2, "onset": "طفوله"
    },
    "اضطراب نقص الانتباه وفرط الحركة": {
        "keywords": ["تشتت","عدم تركيز","فرط حركة","اندفاع","نسيان","تنظيم ضعيف","مقاطعه","ملل سريع"],
        "required": ["تشتت","فرط حركة"], "weight": 1.1, "onset": "طفوله"
    },

    # ذهان
    "فصام": {
        "keywords": ["هلوسة","اوهام","ضلالات","تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني","انعدام اراده"],
        "required": ["هلوسة","اوهام"], "weight": 1.85, "onset": "بلوغ مبكر"
    },
    "اضطراب فصامي عاطفي": {
        "keywords": ["اعراض ذهانيه","اكتئاب شديد","هوس","تذبذب مزاج"], "required": ["اعراض ذهانيه"], "weight": 1.6
    },
    "اضطراب وهامي": {
        "keywords": ["ضلالات ثابته","غيرة وهاميه","اضطهاد","عظمة","شك مرضي"],
        "required": ["ضلالات ثابته"], "weight": 1.5
    },

    # مزاج
    "اضطراب اكتئابي جسيم": {
        "keywords": ["حزن","مزاج منخفض","انعدام المتعة","فقدان المتعة","بكاء","انسحاب اجتماعي",
                     "طاقة منخفضة","ارهاق","تعب","بطء نفسي حركي",
                     "اضطراب نوم","ارق","نوم متقطع","استيقاظ مبكر","كثرة نوم",
                     "شهية منخفضة","قلة اكل","فقدان شهية","فقدان وزن","زيادة وزن",
                     "تركيز ضعيف","شعور بالذنب","يأس","تفكير انتحاري"],
        "required": ["حزن","انعدام المتعة"], "weight": 1.9
    },
    "اكتئاب مستمر (عسر المزاج)": {
        "keywords": ["مزاج مكتئب مزمن","تشاؤم مزمن","طاقة قليلة","نوم ضعيف","شهية قليلة","ثقه منخفضه","انتاجية ضعيفه"],
        "required": ["مزاج مكتئب مزمن"], "weight": 1.5
    },
    "اضطراب ثنائي القطب": {
        "keywords": ["نوبة هوس","طاقة عالية","قليل نوم","اندفاع","تهور","افكار سباق","طلاقة الكلام","عظمة","نوبات اكتئاب"],
        "required": ["نوبة هوس"], "weight": 1.75
    },
    "اضطراب ما قبل الطمث المزعج": {
        "keywords": ["تقلب مزاج قبل الدوره","تهيج","حساسيه","انتفاخ","شهية","غضب","حزن قبل الحيض"],
        "required": ["تقلب مزاج قبل الدوره"], "weight": 1.3
    },
    "اكتئاب ما حول الولادة": {
        "keywords": ["بعد الولاده","حزن ما بعد الولاده","بكاء","قلق طفل","نوم مضطرب"],
        "required": ["بعد الولاده","حزن ما بعد الولاده"], "weight": 1.4
    },

    # قلق/رهاب/هلع
    "اضطراب القلق العام": {
        "keywords": ["قلق","قلق مفرط","توتر","توجس","افكار سلبية","شد عضلي","صعوبة تركيز","قابلية استفزاز","ارق","تعب"],
        "required": ["قلق مفرط"], "weight": 1.45
    },
    "اضطراب الهلع": {
        "keywords": ["نوبة هلع","خفقان","اختناق","ضيق نفس","تعرق","رجفه","دوار","خوف الموت","خوف فقدان السيطره","غثيان","خدر"],
        "required": ["نوبة هلع"], "weight": 1.6
    },
    "رهاب اجتماعي": {
        "keywords": ["خوف اجتماعي","خوف التقييم","خجل شديد","تجنب اجتماعي","قلق اداء","احمرار","رجفه"],
        "required": ["خوف اجتماعي"], "weight": 1.4
    },
    "رهاب الساحة": {
        "keywords": ["خوف من الاماكن المفتوحه","خوف من الازدحام","تجنب مواصلات","صعوبه الخروج وحيدا"],
        "required": ["خوف من الاماكن المفتوحه"], "weight": 1.4
    },
    "رهاب محدد": {
        "keywords": ["خوف شديد","فوبيا","تجنب مواقف","خوف طيران","خوف حشرات","خوف المرتفعات","خوف الظلام","خوف حقن","خوف دم"],
        "required": ["خوف شديد"], "weight": 1.3
    },
    "قلق انفصالي (بالغ)": {
        "keywords": ["قلق انفصال","صعوبة ابتعاد","كابوس فقد","اعراض جسدية عند الفراق"],
        "required": ["قلق انفصال"], "weight": 1.3
    },

    # وسواس وما يرتبط به
    "اضطراب الوسواس القهري": {
        "keywords": ["وسواس","افكار اقتحاميه","سلوك قهري","طقوس","تفقد متكرر","غسل متكرر","تنظيم مفرط","عد قهري","خوف تلوث"],
        "required": ["وسواس","سلوك قهري"], "weight": 1.7
    },
    "تشوه صورة الجسد": {
        "keywords": ["انشغال بالمظهر","عيوب متخيله","تفقد المرآه","تعديل مظهر مفرط"],
        "required": ["انشغال بالمظهر"], "weight": 1.5
    },
    "اكتناز": {
        "keywords": ["اكتناز","صعوبة رمي","تكديس","فوضى منزل"],
        "required": ["اكتناز"], "weight": 1.4
    },
    "نتف الشعر": {
        "keywords": ["شد شعر","سحب شعر","فراغات شعر","توتر ثم ارتياح"],
        "required": ["شد شعر"], "weight": 1.4
    },

    # صدمة/ضغوط
    "اضطراب ما بعد الصدمة": {
        "keywords": ["حدث صادم","استرجاع الحدث","فلاش باك","كابوس","تجنب","خدر عاطفي","يقظه مفرطه","حساسيه صوت","ذنب الناجي"],
        "required": ["حدث صادم","استرجاع الحدث"], "weight": 1.85
    },
    "اضطراب كرب حاد": {
        "keywords": ["اعراض صدمة قصيره","خلال اسابيع","يقظه مفرطه","تجنب"],
        "required": ["اعراض صدمة قصيره"], "weight": 1.45
    },
    "اضطراب تكيف": {
        "keywords": ["توتر موقف","حزن بعد حدث","قلق ظرفي","تراجع اداء بعد ضغط","مشاكل عمل/دراسة"],
        "required": ["توتر موقف"], "weight": 1.3
    },

    # جسدية/تحولي
    "اعراض جسدية": {
        "keywords": ["الم غير مفسر","اعراض جسدية متعدده","انشغال صحي","زياره اطباء كثيره"],
        "required": ["الم غير مفسر"], "weight": 1.5
    },
    "قلق المرض": {
        "keywords": ["خوف مرض خطير","تفقد جسد","طمأنه متكرره","بحث طبي مستمر","توهم المرض"],
        "required": ["خوف مرض خطير"], "weight": 1.5
    },
    "اضطراب تحولي": {
        "keywords": ["اعراض عصبية بدون سبب عضوي","شلل وظيفي","نوبات غير صرعية","فقدان احساس"],
        "required": ["اعراض عصبية بدون سبب عضوي"], "weight": 1.5
    },

    # أكل
    "قهم عصبي": {
        "keywords": ["نقص وزن شديد","خوف من زياده الوزن","صورة جسد سلبيه","تقييد طعام"],
        "required": ["نقص وزن شديد","خوف من زياده الوزن"], "weight": 1.7
    },
    "نهام عصبي": {
        "keywords": ["نهم متكرر","تطهير","استفراغ","ملينات","ذنب بعد الاكل"],
        "required": ["نهم متكرر","تطهير"], "weight": 1.6
    },
    "اضطراب نهم الطعام": {
        "keywords": ["نهم","اكل بشراهه","فقدان تحكم","اكل سرا","زيادة وزن"],
        "required": ["نهم","فقدان تحكم"], "weight": 1.5
    },

    # نوم/يقظة
    "أرق مزمن": {
        "keywords": ["صعوبه نوم","استيقاظ مبكر","نوم متقطع","عدم راحه","اجهاد نهاري","تفكير ليلي"],
        "required": ["صعوبه نوم"], "weight": 1.4
    },
    "فرط نعاس/ناركوليبسي": {
        "keywords": ["نعاس نهاري","غفوات مفاجئة","شلل نوم","هلوسات نعاس"],
        "required": ["نعاس نهاري"], "weight": 1.35
    },
    "انقطاع نفس اثناء النوم": {
        "keywords": ["شخير","توقف تنفس","اختناق ليلي","نعاس نهاري"],
        "required": ["شخير","توقف تنفس"], "weight": 1.3
    },

    # مادة/إدمان
    "اضطراب تعاطي الكحول": {
        "keywords": ["كحول","سكر متكرر","تحمل","اعراض انسحاب","فقدان سيطرة","مشاكل عمل"],
        "required": ["كحول"], "weight": 1.6
    },
    "اضطراب تعاطي القنب": {
        "keywords": ["حشيش","قنب","استخدام يومي","تسامح","انسحاب","قلق بعد الايقاف"],
        "required": ["حشيش","قنب"], "weight": 1.4
    },
    "اضطراب تعاطي المنبهات": {
        "keywords": ["منشطات","امفيتامين","كوكايين","سهر","فقدان شهيه","بارانويا"],
        "required": ["منشطات"], "weight": 1.6
    },
    "اضطراب تعاطي الأفيونات": {
        "keywords": ["هيروين","مورفين","اوكسيدودون","انسحاب افيوتي","رغبه ملحه","تحمل"],
        "required": ["هيروين","مورفين","اوكسيدودون"], "weight": 1.7
    },

    # شخصية
    "شخصية حدّية": {
        "keywords": ["اندفاع","تقلب عاطفي","خوف هجر","ايذاء ذاتي","فراغ مزمن","علاقات غير مستقرة","غضب شديد"],
        "required": ["تقلب عاطفي"], "weight": 1.4
    },
    "شخصية نرجسية": {
        "keywords": ["عظمه","حاجه اعجاب","تعاطف قليل","استغلالي","حساس للنقد"],
        "required": ["عظمه"], "weight": 1.2
    },
    "شخصية وسواسية قهرية": {
        "keywords": ["انشغال بالتفاصيل","كماليه","صرامه","قواعد","عناد","عمل بلا تفويض"],
        "required": ["انشغال بالتفاصيل"], "weight": 1.2
    },
}

# ===================== تجهيز القاعدة =====================
def _prep_db(db):
    out = {}
    for dx, meta in db.items():
        out[dx] = {
            "req": [normalize(x) for x in meta.get("required", [])],
            "kwn": [normalize(x) for x in meta["keywords"]],
            "kw_raw": meta["keywords"],
            "w": float(meta.get("weight", 1.0)),
            "onset": meta.get("onset", "")
        }
    return out

DSM = _prep_db(DSM_DB)

# ===================== محرك الدرجات =====================
SUICIDE_TERMS = {normalize("تفكير انتحاري")}
CRITICAL_TERMS = SUICIDE_TERMS | {normalize("نوبة هلع"), normalize("هلوسة"), normalize("اوهام")}

def score_case(symptoms: str, age: str="", gender: str="", duration_days: str="", history: str=""):
    text = normalize(symptoms or "")

    # تعزيز بالمرادفات
    for base, syns in SYNONYMS.items():
        if any(normalize(w) in text for w in [base] + syns):
            text += " " + " ".join(set(normalize(s) for s in ([base] + syns)))

    # عوامل مدة/تاريخ
    try: dur = float(duration_days)
    except: dur = 0.0
    durB = 1.25 if dur>=365 else 1.15 if dur>=90 else 1.08 if dur>=30 else 1.0

    histB = 1.0
    h = normalize(history or "")
    if any(k in h for k in ["مشاكل عمل","مشاكل زواج","طلاق","تعثر دراسي","غياب متكرر","قضيه"]):
        histB = 1.1

    out = []
    for dx, meta in DSM.items():
        # تحقق المطلوبات
        req = meta["req"]
        if req and not all((r in text) or (similarity(text, r)>=0.65) for r in req):
            continue

        sc = 0.0; hits=[]
        for raw_kw, kw in zip(meta["kw_raw"], meta["kwn"]):
            if kw in text:
                w = 1.0
                if kw in CRITICAL_TERMS: w = 1.9
                sc += w; hits.append(raw_kw)
            else:
                sim = similarity(text, kw)
                if sim >= 0.66:
                    sc += 0.8; hits.append(raw_kw+"~")
                elif sim >= 0.4:
                    sc += 0.4

        if sc == 0: 
            continue

        sc *= meta["w"]; sc *= durB; sc *= histB
        out.append({"name": dx, "score": round(sc,2), "hits": hits[:12]})

    out.sort(key=lambda x: x["score"], reverse=True)
    return out[:5]

# ===================== HTML (مضمن) =====================
PAGE_SHELL = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400}
    *{box-sizing:border-box}
    body{font-family:"Tajawal",system-ui;background:linear-gradient(135deg,var(--bg1),var(--bg2)) fixed;color:#fff;margin:0}
    .wrap{max-width:1180px;margin:28px auto;padding:16px}
    .bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
    .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px}
    a.btn,button.btn{display:inline-block;background:var(--gold);color:#2b1b02;border-radius:14px;padding:12px 16px;text-decoration:none;font-weight:800;border:none;cursor:pointer}
    label{display:block;color:#ffe28a;margin:8px 2px 6px}
    input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:12px 14px}
    textarea{min-height:130px;resize:vertical}
    .grid{display:grid;grid-template-columns:1.1fr .9fr;gap:16px}
    @media(max-width:1000px){.grid{grid-template-columns:1fr}}
    .result{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px}
    .badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:4px 0}
    .ok{background:#16a34a;color:#fff}
    .warn{background:#ef4444;color:#fff}
    table{width:100%;border-collapse:collapse;margin-top:8px}
    th,td{border-bottom:1px solid rgba(255,255,255,.15);padding:8px 6px;text-align:right}
    th{color:#ffe28a}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="bar">
      <h2 style="margin:0">{{ heading }}</h2>
      <a class="btn" href="/">الواجهة</a>
    </div>
    {{ body|safe }}
  </div>
</body>
</html>
"""

def _form_html():
    return """
    <div class="grid">
      <section class="card">
        <form method="post">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label>الاسم الكامل</label><input name="name" placeholder="مثال: مشرف العنزي"></div>
            <div><label>العمر</label><input name="age" placeholder="30"></div>
            <div><label>الجنس</label>
              <select name="gender"><option value="">— اختر —</option><option>ذكر</option><option>أنثى</option></select>
            </div>
            <div><label>مدة الأعراض (بالأيام)</label><input name="duration" placeholder="90"></div>
          </div>
          <label>الأعراض (كلمات دقيقة + عامية)</label>
          <textarea name="symptoms" placeholder="أمثلة: حزن شديد، خمول، قلة نوم، فقدان شهية، انسحاب عن الناس..."></textarea>
          <label>التاريخ الطبي/الأثر الوظيفي (اختياري)</label>
          <textarea name="history" placeholder="أدوية، جلسات، مشاكل عمل/دراسة أو علاقات..."></textarea>
          <div style="margin-top:10px"><button class="btn" type="submit">تشخيص مبدئي</button></div>
        </form>
      </section>
      <aside class="result"><span class="badge warn">لا توجد نتيجة بعد</span><p>املأ الأعراض بدقة. سنعرض أفضل 5 دائمًا.</p></aside>
    </div>
    """

def _result_html(form):
    name     = (form.get("name","") or "").strip()
    age      = (form.get("age","") or "").strip()
    gender   = (form.get("gender","") or "").strip()
    duration = (form.get("duration","") or "").strip()
    symptoms = (form.get("symptoms","") or "").strip()
    history  = (form.get("history","") or "").strip()

    details = score_case(symptoms, age=age, gender=gender, duration_days=duration, history=history)

    if not details:
        res_html = """
        <div class="result">
          <h3>📋 النتيجة</h3>
          <p><span class="badge warn">لا تطابقات مباشرة كافية</span> — زد مفردات مثل: وسواس/نهم/نوبة هلع/هلوسة/رهاب/أرق…</p>
          <p>اذكر <strong>المدة</strong> بدقّة، ووجود <strong>أثر وظيفي</strong> (عمل/دراسة/علاقات) وأي <strong>أدوية</strong>.</p>
        </div>
        """
    else:
        rows = [f"<tr><td>{d['name']}</td><td>{d['score']}</td><td>{', '.join(d['hits'])}</td></tr>" for d in details]
        table = "<table><thead><tr><th>التشخيص المقترح</th><th>الدرجة</th><th>مطابقات</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
        res_html = f"""
        <div class="result">
          <h3>📋 أقرب التشخيصات (أفضل 5)</h3>
          {table}
          <p style="opacity:.85;margin-top:8px">⚠️ نتيجة تقديرية للمساعدة وليست تشخيصًا نهائيًا.</p>
        </div>
        """

    body = f"""
    <div class="grid">
      <section class="card">
        <form method="post">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label>الاسم الكامل</label><input name="name" value="{name}"></div>
            <div><label>العمر</label><input name="age" value="{age}"></div>
            <div><label>الجنس</label>
              <select name="gender">
                <option value="" {"selected" if not gender else ""}>— اختر —</option>
                <option {"selected" if gender=="ذكر" else ""}>ذكر</option>
                <option {"selected" if gender=="أنثى" else ""}>أنثى</option>
              </select>
            </div>
            <div><label>مدة الأعراض (بالأيام)</label><input name="duration" value="{duration}"></div>
          </div>
          <label>الأعراض</label>
          <textarea name="symptoms">{symptoms}</textarea>
          <label>التاريخ الطبي/الأثر الوظيفي</label>
          <textarea name="history">{history}</textarea>
          <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap">
            <button class="btn" type="submit">إعادة التشخيص</button>
            <a class="btn" href="/">الواجهة</a>
          </div>
        </form>
      </section>
      {res_html}
    </div>
    """
    return render_template_string(PAGE_SHELL, title="DSM-5 | دراسة حالة وتشخيص", heading="🗂️ دراسة حالة + تشخيص (DSM-5)", body=body)

# ===================== المسارات =====================
@dsm_bp.route("/", methods=["GET", "POST"])
def entry():
    if request.method == "POST":
        return _result_html(request.form)
    return render_template_string(PAGE_SHELL, title="DSM-5 | دراسة حالة", heading="🗂️ دراسة حالة + تشخيص (DSM-5)", body=_form_html())

# روابط تواصل احتياطية لو احتجتها في الواجهة داخل هذا الملف (غير ضرورية هنا)
@dsm_bp.route("/contact/<kind>")
def _contact(kind):
    if kind == "whatsapp":  return redirect("https://wa.me/9665XXXXXXXX", code=302)
    if kind == "telegram":  return redirect("https://t.me/USERNAME",      code=302)
    if kind == "email":     return redirect("mailto:info@arabipsycho.com", code=302)
    return redirect("/", code=302)
