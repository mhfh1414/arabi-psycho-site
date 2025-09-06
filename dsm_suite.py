# -*- coding: utf-8 -*-
"""
dsm_suite.py
ملف واحد ضخم يجمع:
- قاعدة DSM موسّعة (مرنة وقابلة للتغذية)
- دراسة الحالة (النموذج + النتيجة في نفس الصفحة)
- مطابقة ذكية (تطبيع عربي + مرادفات + أوزان + تعزيز بالمدّة/العمر/الجنس/الأثر)
- اقتراح كلمات مفقودة لتقوية الإدخال
"""

import re
from collections import defaultdict
from flask import render_template_string

# ============================= أدوات مساعدة لغوية =============================
_AR_DIAC = r"[ًٌٍَُِّْـ]"
def normalize(s: str) -> str:
    if not s:
        return ""
    s = s.strip()
    # حذف الحركات
    s = re.sub(_AR_DIAC, "", s)
    # توحيد بعض الحروف
    s = (s.replace("أ","ا").replace("إ","ا").replace("آ","ا")
           .replace("ة","ه").replace("ى","ي").replace("ؤ","و").replace("ئ","ي"))
    # ازالة التكرارات المبالغ فيها (مممم → مم)
    s = re.sub(r"(.)\1{2,}", r"\1\1", s)
    # مسافات
    s = re.sub(r"\s+", " ", s)
    return s

def tokenize(s: str):
    s = normalize(s)
    # فصل علامات
    s = re.sub(r"[^\w\s\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    # كلمات مع الحفاظ على العبارات القصيرة
    return s.split()

def contains_phrase(text_norm: str, phrase: str) -> bool:
    return normalize(phrase) in text_norm

# ============================= مرادفات عامة (تعزيز) =============================
# مرادفات شائعة تُستخدم لتوسيع المطابقة (بدون مكتبات خارجية)
SYNONYMS = {
    # مزاج/اكتئاب
    "حزن": ["زعل","اكتئاب","كدر","طفش","غم","ضيقه","هم"],
    "انعدام المتعة": ["فقدان المتعه","مافي متعه","عدم استمتاع","لا استمتع"],
    "طاقة منخفضة": ["خمول","كسل","ارهاق","تعب","مافي طاقه"],
    "اضطراب نوم": ["قلة نوم","كثرة نوم","ارق","نوم متقطع","استيقاظ مبكر"],
    "شهية منخفضة": ["قلة اكل","ما اقدر اكل","فقدان شهية"],
    "زيادة وزن": ["سمنت","سمنه","وزني زاد"],
    "انسحاب اجتماعي": ["انعزال","ما اطلع","ابتعاد عن الناس"],

    # قلق/هلع
    "قلق": ["توتر","توجس","خوف مستمر","على اعصابي"],
    "نوبة هلع": ["هجوم هلع","تسارع قلب","خفقان","ضيقه تنفس","اختناق"],
    "خوف الموت": ["حاس بموت","بموت","خايف اموت"],

    # وسواس قهري
    "وسواس": ["افكار مزعجه","افكار ملحاحه","افكار قسريه","افكار اقتحاميه"],
    "سلوك قهري": ["طقوس","تكرار غسيل","تفقد مكرر","عد قهري","تنظيف شديد"],
    "خوف تلوث": ["قذاره","وساوس نظافه"],

    # صدمة
    "حدث صادم": ["حادث شديد","تعرضت لحادث","اعتداء","حرب","كارثه"],
    "استرجاع الحدث": ["فلاش باك","ذكريات مؤلمه","كوابيس"],

    # ذهان
    "هلوسة": ["اسمع اصوات","اشوف اشياء","هلاوس سمعيه","هلاوس بصريه"],
    "اوهام": ["ضلالات","افكار غير واقعيه","شكوكيه مبالغ بها"],

    # ADHD
    "تشتت": ["عدم تركيز","سهو","نسيان","ما اركز"],
    "فرط حركة": ["كثرة حركه","اندفاع","مقاطعه","ملل سريع"],

    # توحد
    "تواصل اجتماعي ضعيف": ["صعوبه تواصل","نظره عيون ضعيفه","علاقات محدوده"],
    "اهتمامات مقيدة": ["روتين صارم","تكرار حركات","تمتمه","حساسيات صوت/ضوء"],

    # نوم/أكل
    "نهم": ["شراهه","اكل بكثره","ما اقدر اوقف اكل"],
    "تطهير": ["ترجيع متعمد","استفراغ بعد الاكل","ملينات"],

    # ادمان
    "تعاطي": ["استخدام","ادمان","اعتماد","شراهه استخدام"],
    "انسحاب": ["اعراض انسحاب","رجفه","تعرق","ارق","قلق"],
}

def expand_with_synonyms(text: str) -> str:
    """يضيف مرادفات أساسية للنص لزيادة فرص المطابقة."""
    text_norm = normalize(text)
    extra = []
    for base, syns in SYNONYMS.items():
        if any(normalize(s) in text_norm for s in [base] + syns):
            extra.extend([base] + syns)
    if extra:
        text_norm += " " + " ".join(set(normalize(w) for w in extra))
    return text_norm

# ============================= قاعدة DSM موسّعة =============================
# ملاحظة: القاعدة قابلة للتوسيع بإضافة مفردات عاميّة/طبية.
# أضفت مفردات كثيرة لتقليل رجوع "غير كافية".
DSM_DB = {
    # --------- اضطرابات المزاج ---------
    "اضطراب اكتئابي جسيم": [
        "حزن","مزاج منخفض","انعدام المتعة","فقدان المتعة","تشاؤم","تفكير سلبي","بكاء","انسحاب اجتماعي",
        "طاقة منخفضة","ارهاق","تعب","خمول","كسل","بطء نفسي حركي",
        "اضطراب نوم","قلة نوم","كثرة نوم","ارق","نوم متقطع","استيقاظ مبكر",
        "شهية منخفضة","قلة اكل","فقدان شهية","فقدان وزن","زيادة وزن",
        "تركيز ضعيف","احتقار الذات","شعور بالذنب","يأس","افكار انتحارية","انتحار"
    ],
    "اكتئاب مستمر (عسر المزاج)": [
        "مزاج مكتئب مزمن","تشاؤم مزمن","طاقة قليلة","نوم ضعيف","شهية قليلة",
        "ثقة بالنفس منخفضة","تركيز ضعيف","انتاجية ضعيفه","احباط مزمن"
    ],
    "اضطراب ثنائي القطب": [
        "نوبة هوس","هوس","نشاط زائد","طاقة عالية","قليل نوم","اندفاع","تهور","افكار سباق","طلاقة الكلام","عظمة",
        "نوبات اكتئاب","تذبذب المزاج","تقلب شديد"
    ],

    # --------- القلق والطيف ---------
    "اضطراب القلق العام": [
        "قلق","قلق مفرط","توتر","توجس","افكار سلبية","شد عضلي","صعوبة تركيز","قابلية استفزاز","ارق","تعب"
    ],
    "اضطراب الهلع": [
        "نوبة هلع","خفقان","اختناق","ضيق نفس","تعرق","رجفة","دوار","خوف الموت","خوف فقدان السيطرة","غثيان","خدر"
    ],
    "رهاب اجتماعي": [
        "خوف اجتماعي","خوف التقييم","خجل شديد","تجنب اجتماعي","احمرار","رجفه","قلق اداء","رهبه مواجهه"
    ],
    "رهاب محدد": [
        "رهاب","خوف شديد","تجنب مواقف","خوف من طيران","خوف من حشرات","خوف من المرتفعات","خوف من الظلام"
    ],
    "رهاب الساحة (الاماكن)": [
        "خوف من الاماكن المفتوحه","خوف من الازدحام","تجنب مواصلات","صعوبه الخروج وحيدا"
    ],

    # --------- الوسواس والصدمة ---------
    "اضطراب الوسواس القهري": [
        "وسواس","افكار اقتحاميه","سلوك قهري","طقوس","تفقد متكرر","غسل متكرر","تنظيم مفرط","عد قهري","خوف تلوث"
    ],
    "اضطراب ما بعد الصدمة": [
        "حدث صادم","استرجاع الحدث","فلاش باك","كابوس","تجنب","خدر عاطفي","يقظه مفرطه","حساسيه صوت","فرط يقظه"
    ],

    # --------- الطيف الذهاني ---------
    "فصام": [
        "هلوسة","هلاوس سمعيه","اوهام","ضلالات","تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني","انعدام اراده"
    ],
    "اضطراب فصامي عاطفي": [
        "اعراض ذهانيه","اكتئاب شديد","هوس","تذبذب مزاج","هلوسه","اوهام"
    ],
    "اضطراب وهامي": [
        "ضلالات ثابته","غيره وهاميه","اضطهاد","عظمه","شك مرضي"
    ],

    # --------- نمائي/عصبي ---------
    "اضطراب فرط الحركة وتشتت الانتباه": [
        "تشتت","عدم تركيز","فرط حركة","اندفاعيه","نسيان","تاجيل","تنظيم ضعيف","كثرة حركة","مقاطعه","ملل سريع"
    ],
    "اضطراب طيف التوحد": [
        "تواصل اجتماعي ضعيف","تواصل غير لفظي ضعيف","صعوبات علاقات","اهتمامات مقيده","روتين صارم",
        "حساسيات حسيه","حركات نمطيه","لغة متأخره","قله تواصل بصري"
    ],

    # --------- نوم/أكل/جسد ---------
    "ارَق مزمن": ["صعوبه نوم","استيقاظ مبكر","نوم متقطع","عدم راحه","اجهاد نهاري"],
    "اضطراب نهم الطعام": ["نهم","اكل بشراهه","فقدان تحكم","اكل سرا","ندم بعد الاكل","زياده وزن"],
    "نهام عصبي": ["نهم متكرر","تطهير","استفراغ","ملينات","صورة جسد مشوهه"],
    "قهم عصبي": ["نقص وزن شديد","خوف من زياده الوزن","صورة جسد سلبيه","تقييد طعام"],
    "اعراض جسديه (سوماتيزيشن)": ["الم غير مفسر","اعراض جسديه متعدده","انشغال صحي","زياره اطباء كثيره"],
    "قلق المرض (هيبوكوندريا)": ["خوف مرض خطير","تفقد جسد","طمأنه متكرره","بحث طبي مستمر"],

    # --------- ادمان مواد ---------
    "اضطراب تعاطي الكحول": [
        "كحول","سكر متكرر","تحمل","اعراض انسحاب","فقدان سيطرة","مشاكل عمل","مشاكل علاقات"
    ],
    "اضطراب تعاطي القنب": [
        "حشيش","قنب","استخدام يومي","تسامح","انسحاب","قلق بعد الايقاف"
    ],
    "اضطراب تعاطي المنبهات": [
        "منشطات","امفيتامين","كوكايين","سهر","فقدان شهيه","بارانويا","استخدام قهري"
    ],
    "اضطراب تعاطي الافيونات": [
        "هيروين","مورفين","اوكسيدودون","انسحاب افيوتي","رغبه ملحه","تحمل"
    ],

    # --------- الشخصية ---------
    "شخصية حدّية": ["اندفاع","تقلب عاطفي","خوف هجر","ايذاء ذاتي","فراغ مزمن","علاقات غير مستقرة"],
    "شخصية نرجسية": ["عظمه","حاجه اعجاب","تعاطف قليل","استغلالي","حساس للنقد"],
    "شخصية معادية للمجتمع": ["خرق قواعد","عدوانيه","خداع","اندفاع","لامسؤوليه","ندم قليل"],
    "شخصية اجتنابية": ["تجنب نقد","خجل شديد","نقص كفاءه","حساسيه رفض"],
    "شخصية اتكاليه": ["اتكاليه","صعوبه قرار","خوف فراق","احتياج دعم مستمر"],
    "شخصية وسواسية قهرية": ["انشغال بالتفاصيل","كماليه","صرامه","عناد","انشغال بالقواعد"],
    "شخصية انسحابية": ["برود اجتماعي","قلة متعه","انعزال","قلة علاقات وثيقه"],

    # --------- معرفي/هرموني/تكيّفي ---------
    "اضطراب تكيف": ["توتر موقف","حزن بعد حدث","قلق ظرفي","تراجع اداء بعد ضغط"],
    "اكتئاب ما حول الولادة": ["بعد الولاده","حزن ما بعد الولاده","بكاء","قلق طفل","نوم مضطرب"],
    "اضطراب ما قبل الطمث المزعج": ["تقلب مزاج قبل الدوره","تهيج","حساسيه","انتفاخ","شهيه"],
    "اضطراب معرفي خفيف/خرف مبكر": ["نسيان جديد","ضياع","بطء معالجه","تراجع تنفيذي"]
}

# ============================= تعزيزات الترجيح (سن/جنس/مدة/أثر) =============================
def duration_boost(duration_days: str) -> float:
    try:
        d = float(duration_days)
    except:
        return 0.0
    if d >= 365: return 2.0
    if d >= 90:  return 1.0
    if d >= 30:  return 0.5
    return 0.0

def gender_bias(gender: str, disorder: str) -> float:
    g = normalize(gender)
    if "انثى" in g:
        if "ما قبل الطمث" in disorder or "ما حول الولادة" in disorder:
            return 1.0
    return 0.0

def age_bias(age: str, disorder: str) -> float:
    try:
        a = int(age)
    except:
        return 0.0
    if a < 16 and "فرط الحركة" in disorder:
        return 1.0
    if a >= 50 and ("معرفي" in disorder or "خرف" in disorder):
        return 1.0
    return 0.0

def impairment_boost(history_text: str) -> float:
    """تعزيز عند وجود أثر وظيفي واضح."""
    if not history_text: return 0.0
    t = normalize(history_text)
    keys = ["مشاكل عمل","فصل","انذار","مشاكل زواج","طلاق","خلافات","مخالفه","قضيه","مشاكل ماليه","تعثر دراسي"]
    if any(normalize(k) in t for k in keys):
        return 0.5
    return 0.0

# ============================= خوارزمية المطابقة =============================
def score_diagnoses(symptoms_text: str, age: str="", gender: str="", duration: str="", history: str=""):
    """تعطي ترتيبًا للتشخيصات بأوزان محسّنة + اقتراح كلمات مفقودة."""
    text_raw = symptoms_text or ""
    # توسعة بالنص والمرادفات
    text_norm = expand_with_synonyms(text_raw)

    scores = defaultdict(float)
    hits_by_disorder = {}

    for disorder, keywords in DSM_DB.items():
        local_hits = []
        sc = 0.0
        for kw in keywords:
            kw_n = normalize(kw)
            # وزن أعلى للعبارات الكاملة، وأقل للكلمة المفردة داخل النص
            if contains_phrase(text_norm, kw):
                w = 1.0
                # بعض الكلمات المفتاحية القوية
                if kw_n in ("انتحار","افكار انتحارية","نوبة هلع","هلوسة","اوهام","ضلالات"):
                    w = 1.8
                sc += w
                local_hits.append(kw)
            else:
                # مطابقة جزئية على مستوى التوكنات
                toks = set(tokenize(text_norm))
                if kw_n in toks:
                    sc += 0.6
                    local_hits.append(kw)

        # تعزيزات: سن/جنس/مدّة/أثر
        sc += duration_boost(duration)
        sc += gender_bias(gender, disorder)
        sc += age_bias(age, disorder)
        sc += impairment_boost(history)

        if sc > 0:
            scores[disorder] = sc
            hits_by_disorder[disorder] = local_hits

    # لو ما فيه أي نتيجة، اقترح أقرب فئة عامة بدل "غير كافية"
    if not scores:
        # اقتراح عام حسب كلمات بارزة
        buckets = {
            "مزاج/اكتئاب": ["حزن","مزاج","متعه","يأس","نوم","طاقه","ذنب"],
            "قلق/هلع": ["قلق","توتر","نوبه","خفقان","اختناق","خوف"],
            "وسواس قهري": ["وسواس","طقوس","غسل","تفقد","تلوث"],
            "صدمة": ["حدث","فلاش","كوابيس","تجنب"],
            "ذهان": ["هلوسه","اوهام","ضلالات"],
            "انتباه/حركه": ["تشتت","تركيز","فرط","اندفاع"],
            "توحد": ["تواصل","روتين","حساسيات"],
            "نوم/أكل": ["نوم","شهية","نهم","تطهير"],
            "ادمان": ["تعاطي","انسحاب","تحمل"]
        }
        txt = normalize(text_raw)
        hints = []
        for label, kws in buckets.items():
            if any(normalize(k) in txt for k in kws):
                hints.append(label)
        return [], {"suggestion": "جرّب إضافة وصف أدق للأعراض (المدة/الشدة/السياق).",
                    "buckets": hints[:3]}

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    # بناء تفاصيل غنية للعرض
    details = []
    for d, sc in ranked[:5]:
        hits = hits_by_disorder.get(d, [])
        details.append({
            "name": d,
            "score": round(sc, 2),
            "hits": ", ".join(hits[:7]) + ("..." if len(hits) > 7 else "")
        })
    return details, None

# ============================= القالب وتجميع الصفحة =============================
_BASE = """
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
    .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px;backdrop-filter:blur(6px)}
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

def _render(title, heading, body):
    return render_template_string(_BASE, title=title, heading=heading, body=body)

# ============================= العرض (GET/POST) =============================
def render_dsm_get():
    form_html = """
    <div class="grid">
      <section class="card">
        <form method="post">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label>الاسم الكامل</label><input name="name" placeholder="مثال: مشرف العنزي"></div>
            <div><label>العمر</label><input name="age" placeholder="30"></div>
            <div><label>الجنس</label>
              <select name="gender"><option value="">— اختر —</option><option>ذكر</option><option>أنثى</option></select>
            </div>
            <div><label>مدة الأعراض (بالأيام)</label><input name="duration" placeholder="مثال: 60"></div>
          </div>
          <label>الأعراض (اذكر كلمات دقيقة ومفردات عامية إن وجدت)</label>
          <textarea name="symptoms" placeholder="مثال: حزن شديد، خمول، قلة نوم، فقدان شهية، انسحاب عن الناس..."></textarea>
          <label>التاريخ الطبي/النفسي والأثر الوظيفي (اختياري)</label>
          <textarea name="history" placeholder="أدوية حالية، جلسات سابقة، مشاكل عمل/دراسة، خلافات أسرية..."></textarea>
          <div style="margin-top:10px"><button class="btn" type="submit">تشخيص مبدئي</button></div>
        </form>
      </section>
      <aside class="result"><span class="badge warn">لا توجد نتيجة بعد</span><p>املأ الأعراض بدقة ثم اضغط تشخيص. سنعرض لك أفضل 5 ترشيحات دائمًا.</p></aside>
    </div>
    """
    return _render("DSM-5 | دراسة حالة وتشخيص", "🗂️ دراسة حالة + تشخيص (DSM-5)", form_html)

def render_dsm_post(form):
    name = form.get("name","").strip()
    age = form.get("age","").strip()
    gender = form.get("gender","").strip()
    duration = form.get("duration","").strip()
    symptoms = form.get("symptoms","").strip()
    history = form.get("history","").strip()

    details, fallback = score_diagnoses(symptoms, age=age, gender=gender, duration=duration, history=history)

    if fallback is not None:
        result_html = f"""
        <div class="result">
          <h3>📋 النتيجة</h3>
          <p><span class="badge warn">لا تطابقات مباشرة كافية</span> — جرّب إضافة مفردات أوضح للأعراض (مثال: <em>حزن، قلق، أرق، نهم، وسواس...</em>)</p>
          {"<p><strong>أقرب فئات:</strong> " + ", ".join(fallback.get("buckets", [])) + "</p>" if fallback.get("buckets") else ""}
          <p>نقترح ذكر <strong>المدة</strong> بدقة، ووجود <strong>أثر وظيفي</strong> (مشاكل عمل/دراسة)، وأي <strong>علاجات/أدوية</strong> حالية.</p>
        </div>
        """
    else:
        # بناء جدول لأفضل 5 ترشيحات
        rows = []
        for item in details:
            rows.append(f"<tr><td>{item['name']}</td><td>{item['score']}</td><td>{item['hits']}</td></tr>")
        table = "<table><thead><tr><th>التشخيص المقترح</th><th>الدرجة</th><th>كلمات مطابقة</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
        result_html = f"""
        <div class="result">
          <h3>📋 أقرب التشخيصات (أفضل 5)</h3>
          {table}
          <p style="opacity:.85;margin-top:8px">⚠️ نتيجة تقديرية للمساعدة وليست تشخيصًا نهائيًا. يُنصح بالتقييم السريري.</p>
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
          <label>التاريخ الطبي/النفسي والأثر الوظيفي</label>
          <textarea name="history">{history}</textarea>
          <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap">
            <button class="btn" type="submit">إعادة التشخيص</button>
            <a class="btn" href="/">الواجهة</a>
          </div>
        </form>
      </section>
      {result_html}
    </div>
    """
    return _render("DSM-5 | دراسة حالة وتشخيص", "🗂️ دراسة حالة + تشخيص (DSM-5)", body)

# ملاحظة: ملف site_app.py يستورد:
# from dsm_suite import render_dsm_get, render_dsm_post
# ثم يربط المسار /dsm بـ GET/POST لهذه الدوال.
