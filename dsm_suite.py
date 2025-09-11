# -*- coding: utf-8 -*-
# dsm.py — DSM مستقل: دراسة حالة + قاعدة اضطرابات موسّعة + تشخيص واحد مرجّح

from __future__ import annotations
from flask import Blueprint, request, render_template_string
import re
from datetime import datetime

# ============================ إعدادات عامة ============================
dsm_bp = Blueprint("dsm", __name__)

MIN_SCORE        = 2.20     # أقل درجة لقبول التشخيص كـ "مرجّح"
CRITICAL_BOOST   = 1.20     # تعزيز عند وجود أعراض حرجة
FUNCTIONAL_BOOST = 1.10     # تعزيز عند وجود أثر وظيفي (عمل/دراسة/زواج...)
DURATION_BOOSTS  = [(365*2, 1.25),(180,1.18),(90,1.12),(30,1.06)]  # حسب مدة الأعراض (أيام)

# ============================ أدوات لغوية عربية ============================
_AR_DIAC  = r"[ًٌٍَُِّْـ]"
_AR_PUNCT = r"[.,،;؛!?؟()\[\]{}\"\'<>:…]"

def normalize(s: str) -> str:
    if not s: return ""
    s = re.sub(_AR_DIAC, "", s.strip())
    s = re.sub(_AR_PUNCT, " ", s)
    s = (s.replace("أ","ا").replace("إ","ا").replace("آ","ا")
           .replace("ة","ه").replace("ى","ي").replace("ؤ","و").replace("ئ","ي")
           .replace("ـ","").replace("ﻻ","لا").replace("ﻷ","لا"))
    s = re.sub(r"\s+"," ", s)
    return s.lower()

def sim_contains(text_norm: str, phrase: str, hard: bool=False) -> bool:
    """مطابقة ناعمة: كل كلمات العبارة موجودة بالنص (أو تطابق حرفي عند hard)."""
    p = normalize(phrase)
    if not p: return False
    if hard: return p in text_norm
    ptoks = set(p.split())
    ttoks = set(text_norm.split())
    return ptoks.issubset(ttoks)

# ============================ مرادفات لتعزيز المطابقة ============================
SYNONYMS = {
    # مزاج
    "حزن": ["كابه","تعاسه","زعل","ضيقه","غم","طفش"],
    "انعدام المتعة": ["فقدان المتعه","لا استمتع","عدم استمتاع","فقدان الاهتمام","ما عاد يفرحني شي"],
    "طاقة منخفضة": ["خمول","كسل","ارهاق","تعب","وهن","هبوط طاقه"],
    "اضطراب نوم": ["ارق","قلة نوم","نوم متقطع","استيقاظ مبكر","كثرة نوم","كوابيس","نعاس نهاري"],
    "شهية منخفضة": ["قلة اكل","سدت نفسي","فقدان شهيه","ما ليا نفس"],
    "شهية زائدة": ["نهم","شراهه","اكل كثير","اكل عاطفي"],
    "انسحاب اجتماعي": ["انعزال","انطواء","تجنب اجتماعي","ما اطلع"],
    "تفكير انتحاري": ["افكار انتحار","تمني الموت","رغبه بالموت"],

    # قلق/هلع/رهاب
    "قلق": ["توتر","توجس","على اعصابي","قلق مفرط","ترقب"],
    "نوبة هلع": ["خفقان","اختناق","ضيق نفس","ذعر","رجفه","تعرق","دوخه","خوف الموت"],
    "خوف اجتماعي": ["رهبه مواجهه","خجل شديد","قلق اداء"],
    "خوف شديد": ["فوبيا","خوف طيران","خوف المرتفعات","خوف الظلام","خوف حقن","خوف حشرات","خوف دم"],
    "قلق انفصال": ["صعوبه ابتعاد","خوف الفراق","كابوس فقد"],

    # وسواس/قهري
    "وسواس": ["افكار متسلطه","اقتحاميه","هواجس","خوف تلوث","تدنيس"],
    "سلوك قهري": ["طقوس","تفقد متكرر","عد قهري","غسل متكرر","تنظيم مفرط"],

    # صدمة
    "حدث صادم": ["تعرضت لحادث","اعتداء","كارثه","حرب","فقد عزيز","تنمر قاس"],
    "استرجاع الحدث": ["فلاش باك","ذكريات مؤلمه","كوابيس","فرط تيقظ"],

    # ذهان
    "هلوسة": ["هلاوس سمعيه","هلاوس بصريه","اسمع اصوات","اشوف اشياء"],
    "اوهام": ["ضلالات","اعتقادات وهميه","اضطهاد","عظمه","غيره وهاميه"],

    # ADHD
    "تشتت": ["عدم تركيز","سهو","شرود","نسيان","ضعف تنظيم"],
    "فرط حركة": ["نشاط زائد","اندفاع","مقاطعه","ملل سريع"],

    # توحد
    "تواصل اجتماعي ضعيف": ["صعوبه تواصل","تواصل بصري ضعيف","تواصل غير لفظي ضعيف"],
    "اهتمامات مقيدة": ["روتين صارم","حساسيات صوت","حساسيات ضوء","سلوك نمطي"],

    # أكل/نوم/جسد
    "نهم": ["نوبات اكل","اكل سرا","شراهه"],
    "تطهير": ["استفراغ متعمد","ملينات","صيام تعويضي"],
    "الم غير مفسر": ["اوجاع متنقله","وجع بلا سبب","شكاوى جسديه"],
    "قلق صحي": ["وسواس مرض","توهم المرض","تفقد جسد"],

    # شخصية
    "تقلب عاطفي": ["مزاج متقلب","سريع الانفعال","مشاعر متطرفة"],
    "انشغال بالتفاصيل": ["كماليه","صرامه","جمود","قواعد صارمه"],
}

CRITICAL_SYM = {"هلوسة","اوهام","نوبة هلع","تفكير انتحاري"}

def expand_with_synonyms(text: str) -> str:
    t = normalize(text)
    for base, syns in SYNONYMS.items():
        if any(normalize(w) in t for w in [base] + syns):
            t += " " + " ".join(set(normalize(s) for s in ([base] + syns)))
    return t

# ============================ قاعدة DSM موسّعة ============================
# ملاحظة: أضف/وسّع كما تريد عبر نفس البنية: required / keywords / min_days / weight / (max_days اختياري)
DSM_DB = {
    # --------- طيف ذهاني ---------
    "فصام": {
        "required": ["هلوسة","اوهام"],
        "keywords": ["تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني","انعدام اراده"],
        "min_days": 180, "weight": 2.0
    },
    "اضطراب فصامي عاطفي": {
        "required": ["هلوسة"],
        "keywords": ["اوهام","اكتئاب شديد","نوبة هوس","تذبذب مزاج"],
        "min_days": 30, "weight": 1.7
    },
    "اضطراب وهامي": {
        "required": ["اوهام"],
        "keywords": ["غيرة وهاميه","اضطهاد","عظمه"],
        "min_days": 30, "weight": 1.6
    },

    # --------- اضطرابات المزاج ---------
    "اضطراب اكتئابي جسيم": {
        "required": ["حزن","انعدام المتعة"],
        "keywords": ["طاقة منخفضة","اضطراب نوم","انسحاب اجتماعي","تركيز ضعيف","شعور بالذنب","يأس","تفكير انتحاري","شهية منخفضة","شهية زائدة"],
        "min_days": 14, "weight": 1.9
    },
    "اكتئاب مستمر (عسر المزاج)": {
        "required": ["مزاج مكتئب مزمن"],
        "keywords": ["طاقة منخفضة","نوم ضعيف","شهية قليلة","ثقه منخفضه","انتاجية ضعيفه"],
        "min_days": 730, "weight": 1.5
    },
    "اضطراب ثنائي القطب": {
        "required": ["نوبة هوس"],
        "keywords": ["قلة نوم","اندفاع","تهور","افكار سباق","طلاقة الكلام","عظمة","نوبات اكتئاب"],
        "min_days": 4, "weight": 1.85
    },

    # --------- قلق/هلع/رهاب ---------
    "اضطراب القلق العام": {
        "required": ["قلق"],
        "keywords": ["قلق مفرط","توتر","توجس","شد عضلي","صعوبة تركيز","أرق","تعب","قابلية استفزاز"],
        "min_days": 90, "weight": 1.45
    },
    "اضطراب الهلع": {
        "required": ["نوبة هلع"],
        "keywords": ["خفقان","اختناق","ضيق نفس","رجفه","تعرق","دوار","خوف الموت","خوف فقدان السيطرة"],
        "min_days": 0, "weight": 1.6
    },
    "رهاب اجتماعي": {
        "required": ["خوف اجتماعي"],
        "keywords": ["قلق اداء","خجل شديد","تجنب اجتماعي","احمرار","رجفه"],
        "min_days": 30, "weight": 1.4
    },
    "رهاب محدد": {
        "required": ["خوف شديد"],
        "keywords": ["خوف طيران","خوف المرتفعات","خوف الظلام","خوف حقن","خوف حشرات","خوف دم"],
        "min_days": 0, "weight": 1.30
    },
    "قلق انفصالي (بالغ)": {
        "required": ["قلق انفصال"],
        "keywords": ["صعوبه ابتعاد","اعراض جسدية عند الفراق","كابوس فقد"],
        "min_days": 30, "weight": 1.30
    },

    # --------- وسواس قهري وما يرتبط به ---------
    "اضطراب الوسواس القهري": {
        "required": ["وسواس","سلوك قهري"],
        "keywords": ["تفقد متكرر","غسل متكرر","تنظيم مفرط","عد قهري","خوف تلوث"],
        "min_days": 30, "weight": 1.7
    },
    "تشوه صورة الجسد": {
        "required": ["انشغال بالمظهر"],
        "keywords": ["عيوب متخيله","تفقد المرآه","تعديل مظهر مفرط"],
        "min_days": 30, "weight": 1.5
    },
    "اكتناز": {
        "required": ["اكتناز"],
        "keywords": ["صعوبة رمي","تكديس","فوضى منزل"],
        "min_days": 90, "weight": 1.4
    },

    # --------- صدمة وضغوط ---------
    "اضطراب ما بعد الصدمة": {
        "required": ["حدث صادم","استرجاع الحدث"],
        "keywords": ["كابوس","تجنب","خدر عاطفي","يقظه مفرطه","ذنب الناجي"],
        "min_days": 30, "weight": 1.8
    },
    "اضطراب تكيف": {
        "required": ["توتر موقف"],
        "keywords": ["حزن بعد حدث","قلق ظرفي","تراجع اداء بعد ضغط","مشاكل عمل/دراسة"],
        "min_days": 0, "max_days": 180, "weight": 1.25
    },

    # --------- أعراض جسدية ---------
    "أعراض جسدية": {
        "required": ["الم غير مفسر"],
        "keywords": ["اعراض جسدية متعددة","انشغال صحي","زياره اطباء كثيره"],
        "min_days": 30, "weight": 1.5
    },
    "قلق المرض": {
        "required": ["قلق صحي"],
        "keywords": ["خوف مرض خطير","تفقد جسد","طمانه متكرره","بحث طبي مستمر"],
        "min_days": 90, "weight": 1.45
    },
    "اضطراب تحولي": {
        "required": ["اعراض عصبية بدون سبب عضوي"],
        "keywords": ["شلل وظيفي","نوبات غير صرعية","فقدان احساس"],
        "min_days": 7, "weight": 1.5
    },

    # --------- أكل ---------
    "قهم عصبي": {
        "required": ["نقص وزن شديد","خوف من زياده الوزن"],
        "keywords": ["صورة جسد سلبيه","تقييد طعام"],
        "min_days": 30, "weight": 1.7
    },
    "نهام عصبي": {
        "required": ["نهم","تطهير"],
        "keywords": ["استفراغ","ملينات","ذنب بعد الاكل"],
        "min_days": 30, "weight": 1.6
    },
    "اضطراب نهم الطعام": {
        "required": ["نهم","فقدان تحكم"],
        "keywords": ["اكل سرا","زيادة وزن"],
        "min_days": 30, "weight": 1.5
    },

    # --------- نوم ويقظة ---------
    "أرق مزمن": {
        "required": ["صعوبه نوم"],
        "keywords": ["استيقاظ مبكر","نوم متقطع","عدم راحه","اجهاد نهاري","تفكير ليلي"],
        "min_days": 30, "weight": 1.4
    },
    "فرط نعاس/ناركوليبسي": {
        "required": ["نعاس نهاري"],
        "keywords": ["غفوات مفاجئة","شلل نوم","هلوسات نعاس"],
        "min_days": 30, "weight": 1.35
    },

    # --------- إدمان مواد ---------
    "اضطراب تعاطي الكحول": {
        "required": ["كحول"],
        "keywords": ["سكر متكرر","تحمل","اعراض انسحاب","فقدان سيطرة","مشاكل عمل"],
        "min_days": 30, "weight": 1.6
    },
    "اضطراب تعاطي القنب": {
        "required": ["حشيش","قنب"],
        "keywords": ["استخدام يومي","تسامح","انسحاب","قلق بعد الايقاف"],
        "min_days": 30, "weight": 1.4
    },
    "اضطراب تعاطي المنبهات": {
        "required": ["منشطات"],
        "keywords": ["امفيتامين","كوكايين","سهر","فقدان شهيه","بارانويا"],
        "min_days": 0, "weight": 1.6
    },

    # --------- الشخصية ---------
    "شخصية حدّية": {
        "required": ["تقلب عاطفي"],
        "keywords": ["اندفاع","خوف هجر","ايذاء ذاتي","فراغ مزمن","علاقات غير مستقرة","غضب شديد"],
        "min_days": 180, "weight": 1.4
    },
    "شخصية وسواسية قهرية": {
        "required": ["انشغال بالتفاصيل"],
        "keywords": ["كماليه","صرامه","قواعد","عناد","عمل بلا تفويض"],
        "min_days": 180, "weight": 1.25
    },
    "شخصية اجتنابية": {
        "required": ["خوف اجتماعي"],
        "keywords": ["تجنب نقد","خجل شديد","نقص كفاءه","حساسيه رفض"],
        "min_days": 180, "weight": 1.25
    },
}

# ============================ محرك الدرجات ============================
def score_case(symptoms: str, duration_days: int, history: str="") -> list[dict]:
    text = expand_with_synonyms(symptoms or "")
    hist = normalize(history or "")

    # تعزيز المدة
    dur_boost = 1.0
    for d, b in DURATION_BOOSTS:
        if duration_days >= d:
            dur_boost = b
            break

    # أثر وظيفي؟
    functional_terms = ["مشاكل عمل","تعثر دراسي","غياب","طلاق","تراجع اداء","مشاكل زواج","مشاكل ماليه"]
    func_boost = FUNCTIONAL_BOOST if any(normalize(k) in hist for k in functional_terms) else 1.0

    out = []
    for dx, meta in DSM_DB.items():
        req = meta.get("required", [])
        # تحقّق المطلوبات (ناعمة)
        if req and not all(sim_contains(text, r) for r in req):
            continue

        # شرط المدة
        min_days = meta.get("min_days", 0)
        if duration_days < min_days:
            continue
        max_days = meta.get("max_days", None)
        if max_days is not None and duration_days > max_days:
            continue

        sc = 0.0; hits = []

        # نقاط أقوى للأعراض المطلوبة
        for r in req:
            if sim_contains(text, r):
                sc += 1.10; hits.append(r)

        # نقاط للكلمات المفتاحية
        for k in meta.get("keywords", []):
            if sim_contains(text, k):
                sc += 0.70; hits.append(k)

        if sc == 0:
            continue

        # رايات حرجة
        if any(sim_contains(text, c) for c in CRITICAL_SYM):
            sc *= CRITICAL_BOOST

        # أوزان عامة
        sc *= meta.get("weight", 1.0)
        sc *= dur_boost
        sc *= func_boost

        out.append({"name": dx, "score": round(sc, 2), "hits": list(dict.fromkeys(hits))[:14]})

    out.sort(key=lambda x: x["score"], reverse=True)
    return out

def pick_best(candidates: list[dict]) -> dict | None:
    if not candidates: return None
    best = candidates[0]
    return best if best["score"] >= MIN_SCORE else None

# ============================ واجهة HTML ============================
PAGE = """
<!doctype html><html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>DSM | دراسة حالة وتشخيص</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400;--w:#fff}
*{box-sizing:border-box}
body{font-family:"Tajawal",system-ui;background:linear-gradient(135deg,var(--bg1),var(--bg2)) fixed;color:var(--w);margin:0}
.wrap{max-width:1100px;margin:26px auto;padding:14px}
.card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px}
label{display:block;color:#ffe28a;margin:6px 2px}
input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:11px}
textarea{min-height:120px;resize:vertical}
.btn{background:linear-gradient(180deg,#ffd86a,#f4b400);color:#2b1b02;border:none;padding:12px 16px;border-radius:12px;font-weight:800;cursor:pointer;text-decoration:none;display:inline-block}
.grid{display:grid;grid-template-columns:1.1fr .9fr;gap:14px}
@media(max-width:1000px){.grid{grid-template-columns:1fr}}
.badge{display:inline-block;background:#16a34a;color:#fff;padding:4px 10px;border-radius:999px}
.warn{background:#ef4444}
table{width:100%;border-collapse:collapse;margin-top:8px}
th,td{border-bottom:1px solid rgba(255,255,255,.15);padding:8px;text-align:right}
th{color:#ffe28a}
</style>
</head>
<body>
  <div class="wrap">
    <h2 style="margin-top:0">🗂️ دراسة حالة + تشخيص (DSM-5)</h2>
    <div class="grid">
      <section class="card">
        <form method="post">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
            <div><label>الاسم (اختياري)</label><input name="name" value="{{name}}"></div>
            <div><label>العمر</label><input name="age" value="{{age}}" placeholder="مثال 30"></div>
            <div><label>الجنس</label>
              <select name="gender">
                <option value="" {{'selected' if not gender else ''}}>— اختر —</option>
                <option {{'selected' if gender=='ذكر' else ''}}>ذكر</option>
                <option {{'selected' if gender=='أنثى' else ''}}>أنثى</option>
              </select>
            </div>
            <div><label>مدة الأعراض (أيام)</label><input name="duration" value="{{duration}}" placeholder="90"></div>
          </div>
          <label>الأعراض (اكتب بعامية/فصحى واضحة)</label>
          <textarea name="symptoms" placeholder="مثال: حزن شديد، فقدان المتعة، قلة نوم، أفكار انتحار...">{{symptoms}}</textarea>
          <label>التاريخ/الأثر الوظيفي (عمل/دراسة/علاقات/قضايا…)</label>
          <textarea name="history">{{history}}</textarea>
          <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap">
            <button class="btn" type="submit">إصدار تشخيص</button>
            <a class="btn" href="/" style="background:#9bd5ff;color:#04122c">الواجهة</a>
          </div>
        </form>
      </section>
      <aside class="card">
        {% if result %}
          <div><span class="badge">التشخيص المرجّح</span></div>
          <h3 style="margin:.4rem 0 0">{{result.name}}</h3>
          <div style="opacity:.8">الدرجة: {{result.score}}</div>
          <table>
            <thead><tr><th>مطابقات</th></tr></thead>
            <tbody>
              {% for h in result.hits %}
              <tr><td>{{h}}</td></tr>
              {% endfor %}
            </tbody>
          </table>
          <p style="opacity:.8;margin-top:8px">⚠️ أداة مساعدة ولا تغني عن التقييم السريري.</p>
        {% else %}
          <div><span class="badge warn">لا تشخيص مؤكد بعد</span></div>
          <p>اكتب مفردات أدق (مثال: <b>هلوسة/أوهام/نوبة هلع/وسواس+طقوس/نهم+تطهير/انقطاع نفس</b>) واذكر المدة والأثر الوظيفي.</p>
        {% endif %}
      </aside>
    </div>
  </div>
</body>
</html>
"""

# ============================ المسار ============================
@dsm_bp.route("/dsm", methods=["GET","POST"])
def dsm_hub():
    form = request.form if request.method == "POST" else {}
    name     = (form.get("name") or "").strip()
    age      = (form.get("age") or "").strip()
    gender   = (form.get("gender") or "").strip()
    duration = (form.get("duration") or "").strip()
    symptoms = (form.get("symptoms") or "").strip()
    history  = (form.get("history") or "").strip()

    # تحويل المدة إلى أيام رقمية
    try:
        d = int(float(duration)) if duration else 0
    except Exception:
        d = 0

    result = None
    if request.method == "POST":
        candidates = score_case(symptoms, d, history)
        best = pick_best(candidates)
        result = type("R",(object,),best)() if best else None

    return render_template_string(
        PAGE, name=name, age=age, gender=gender,
        duration=duration, symptoms=symptoms, history=history,
        result=result
    )
