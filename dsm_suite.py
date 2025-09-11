# -*- coding: utf-8 -*-
# dsm_suite.py — تشخيص واحد مرجّح + عرض أقرب 3 احتمالات عند الحاجة
from __future__ import annotations
from flask import Blueprint, request, render_template_string
import re

dsm_bp = Blueprint("dsm", __name__)

# إعدادات تسجيل
MIN_SCORE = 1.6           # تم تخفيض العتبة
CRITICAL_BOOST = 1.25
FUNCTIONAL_BOOST = 1.12
DURATION_BOOSTS = [(365*2,1.25),(180,1.18),(90,1.12),(30,1.06)]

# أدوات عربية
_AR_DIAC  = r"[ًٌٍَُِّْـ]"
_AR_PUNCT = r"[.,،;؛!?؟()\[\]{}\"\'<>:]"

def normalize(s: str) -> str:
    if not s: return ""
    s = re.sub(_AR_DIAC, "", s.strip())
    s = re.sub(_AR_PUNCT, " ", s)
    s = (s.replace("أ","ا").replace("إ","ا").replace("آ","ا")
           .replace("ة","ه").replace("ى","ي").replace("ؤ","و").replace("ئ","ي")
           .replace("ـ","").replace("ﻻ","لا").replace("ﻷ","لا"))
    s = re.sub(r"\s+", " ", s)
    return s.lower()

def sim_contains(text_norm: str, phrase: str, hard: bool=False) -> bool:
    p = normalize(phrase)
    if hard:
        return p in text_norm
    ptoks = set(p.split())
    return ptoks.issubset(set(text_norm.split()))

# مرادفات موسعة
SYNONYMS = {
    # اكتئاب
    "حزن": ["كابه","ضيقه","غم","زعل","انكسار نفس"],
    "انعدام المتعة": ["فقدان المتعه","ما عاد يفرحني شي","فقدان الاهتمام","برود تجاه الهوايات"],
    "طاقة منخفضة": ["خمول","كسل","ارهاق","وهن","هبوط الطاقه","مالي خلق"],
    "اضطراب نوم": ["ارق","قلة نوم","نوم متقطع","استيقاظ مبكر","كثرة نوم","كوابيس"],
    "انسحاب اجتماعي": ["انعزال","انطواء","ترك اصحاب","تجنب اجتماعي"],
    "تفكير انتحاري": ["افكار انتحار","تمني الموت","افكر اذيني","ما لي رغبه بالحياه"],
    "شهية منخفضة": ["قلة اكل","سدت نفسي","فقدان شهيه"],
    "شهية زائدة": ["نهم","اكل كثير","شراهه"],

    # قلق/هلع/رهاب
    "قلق": ["توتر","توجس","قلق مفرط","على اعصابي"],
    "نوبة هلع": ["خفقان","اختناق","ضيق نفس","ذعر","رجفه","تعرق","دوار","خوف الموت","خوف فقدان السيطره"],
    "خوف اجتماعي": ["رهبه مواجهه","خجل شديد","قلق اداء"],
    "خوف شديد": ["فوبيا","خوف طيران","خوف المرتفعات","خوف الظلام","خوف حقن","خوف حشرات","خوف دم"],

    # وسواس قهري
    "وسواس": ["افكار متسلطه","اقتحاميه","هواجس","خوف تلوث","شك متكرر"],
    "سلوك قهري": ["طقوس","تفقد متكرر","عد قهري","غسل متكرر","تنظيم مفرط","طمأنه"],

    # صدمة
    "حدث صادم": ["حادث قوي","اعتداء","كارثه","فقد عزيز","تنمر قاس","تعذيب","تحرش"],
    "استرجاع الحدث": ["فلاش باك","ذكريات مؤلمه","كوابيس","فرط تيقظ","تجنب التذكيرات"],

    # ذهاني
    "هلوسة": ["هلاوس سمعيه","اسمع اصوات","اشوف اشياء","اسمع ينادوني"],
    "اوهام": ["ضلالات","افكار اضطهاد","افكار عظمه","غيره وهاميه","افكار مرقبه"],

    # تشتت/حركة (للدعم)
    "تشتت": ["سهو","شرود","نسيان","ضعف تنظيم"],
    "فرط حركة": ["نشاط زائد","اندفاع","مقاطعه","ملل سريع"],

    # اضطرابات الأكل
    "نهم": ["شراهه","نوبات اكل","اكل سرا"],
    "تطهير": ["استفراغ متعمد","ملينات","صيام تعويضي"],

    # صحية/جسدية
    "الم غير مفسر": ["اوجاع متنقله","وجع بلا سبب","شكاوى جسديه"],
    "قلق صحي": ["وسواس مرض","توهم المرض","تفقد جسد"],

    # ثنائي القطب
    "نوبة هوس": ["نشوه غير طبيعيه","طاقه عاليه","قلة نوم","اندفاع","تهور","افكار سباق","طلاقة الكلام","عظمه"],
    "مزاج مكتئب مزمن": ["حزن مزمن","تشاؤم مزمن","تعاسه مزمنه"],
}

CRITICAL_SYM = {"هلوسة","اوهام","نوبة هلع","تفكير انتحاري"}

def expand_with_synonyms(text: str) -> str:
    t = normalize(text)
    for base, syns in SYNONYMS.items():
        if any(normalize(w) in t for w in [base] + syns):
            t += " " + " ".join(set(normalize(s) for s in ([base] + syns)))
    return t

# قاعدة DSM مبسطة مع أوزان
DSM_DB = {
    "فصام": {
        "required": ["هلوسة","اوهام"],
        "keywords": ["تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني","انعدام اراده"],
        "min_days": 180, "weight": 2.0
    },
    "اضطراب فصامي عاطفي": {
        "required": ["هلوسة"],
        "keywords": ["اوهام","اكتئاب شديد","نوبة هوس","تذبذب مزاج"],
        "min_days": 30, "weight": 1.75
    },
    "اضطراب اكتئابي جسيم": {
        "required": ["حزن","انعدام المتعة"],
        "keywords": ["طاقة منخفضة","اضطراب نوم","انسحاب اجتماعي","شعور بالذنب","يأس","تفكير انتحاري","شهية منخفضة","شهية زائدة"],
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
    "اضطراب القلق العام": {
        "required": ["قلق"],
        "keywords": ["قلق مفرط","توتر","شد عضلي","صعوبة تركيز","أرق","تعب","قابلية استفزاز"],
        "min_days": 90, "weight": 1.45
    },
    "اضطراب الهلع": {
        "required": ["نوبة هلع"],
        "keywords": ["خفقان","اختناق","ضيق نفس","رجفه","تعرق","دوار","خوف الموت","خوف فقدان السيطرة"],
        "min_days": 0, "weight": 1.65
    },
    "رهاب اجتماعي": {
        "required": ["خوف اجتماعي"],
        "keywords": ["قلق اداء","خجل شديد","تجنب اجتماعي","احمرار","رجفه"],
        "min_days": 30, "weight": 1.4
    },
    "رهاب محدد": {
        "required": ["خوف شديد"],
        "keywords": ["خوف طيران","خوف المرتفعات","خوف الظلام","خوف حقن","خوف حشرات","خوف دم"],
        "min_days": 0, "weight": 1.3
    },
    "اضطراب الوسواس القهري": {
        "required": ["وسواس","سلوك قهري"],
        "keywords": ["تفقد متكرر","غسل متكرر","تنظيم مفرط","عد قهري","خوف تلوث","طمأنه"],
        "min_days": 30, "weight": 1.75
    },
    "اضطراب ما بعد الصدمة": {
        "required": ["حدث صادم","استرجاع الحدث"],
        "keywords": ["تجنب","يقظه مفرطه","ذنب الناجي","كوابيس"],
        "min_days": 30, "weight": 1.85
    },
    "اضطراب تكيف": {
        "required": ["توتر موقف"],
        "keywords": ["حزن بعد حدث","قلق ظرفي","تراجع اداء بعد ضغط","مشاكل عمل/دراسة"],
        "min_days": 0, "max_days": 180, "weight": 1.25
    },
    "أعراض جسدية": {
        "required": ["الم غير مفسر"],
        "keywords": ["اعراض جسدية متعددة","انشغال صحي","زياره اطباء كثيره"],
        "min_days": 30, "weight": 1.5
    },
    "قلق المرض": {
        "required": ["قلق صحي"],
        "keywords": ["خوف مرض خطير","تفقد جسد","طمأنه متكرره","بحث طبي مستمر"],
        "min_days": 90, "weight": 1.45
    },
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
}

def score_case(symptoms: str, duration_days: int, history: str="") -> list[dict]:
    text = expand_with_synonyms(symptoms or "")
    hist = normalize(history or "")

    dur_boost = 1.0
    for days, boost in DURATION_BOOSTS:
        if duration_days >= days:
            dur_boost = boost
            break

    func_boost = FUNCTIONAL_BOOST if any(
        k in hist for k in ["مشاكل عمل","تعثر دراسي","غياب","طلاق","تراجع اداء","مشاكل زواج","فصل من العمل"]
    ) else 1.0

    out = []
    for dx, meta in DSM_DB.items():
        req = meta.get("required", [])
        if req and not all(sim_contains(text, r) for r in req):
            continue

        min_days = meta.get("min_days", 0)
        if duration_days < min_days: continue
        max_days = meta.get("max_days")
        if max_days is not None and duration_days > max_days: continue

        sc = 0.0; hits = []
        for r in req:
            if sim_contains(text, r): sc += 1.2; hits.append(r)
        for k in meta.get("keywords", []):
            if sim_contains(text, k): sc += 0.75; hits.append(k)

        if sc == 0: continue
        if any(sim_contains(text, c) for c in CRITICAL_SYM):
            sc *= CRITICAL_BOOST

        sc *= meta.get("weight", 1.0)
        sc *= dur_boost
        sc *= func_boost

        out.append({"name": dx, "score": round(sc, 2), "hits": list(dict.fromkeys(hits))[:12]})

    out.sort(key=lambda x: x["score"], reverse=True)
    return out

def pick_best(candidates: list[dict]) -> dict | None:
    if not candidates: return None
    best = candidates[0]
    return best if best["score"] >= MIN_SCORE else None

PAGE = """
<!doctype html><html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>DSM | دراسة حالة وتشخيص</title>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400}
    *{box-sizing:border-box}
    body{font-family:"Tajawal",system-ui;background:linear-gradient(135deg,var(--bg1),var(--bg2));color:#fff;margin:0}
    .wrap{max-width:1100px;margin:26px auto;padding:14px}
    .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px}
    label{display:block;color:#ffe28a;margin:6px 2px}
    input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:11px}
    textarea{min-height:120px;resize:vertical}
    .btn{background:var(--gold);color:#2b1b02;border:none;padding:12px 16px;border-radius:12px;font-weight:800;cursor:pointer}
    .grid{display:grid;grid-template-columns:1.1fr .9fr;gap:14px}
    @media(max-width:1000px){.grid{grid-template-columns:1fr}}
    .badge{display:inline-block;background:#16a34a;color:#fff;padding:4px 10px;border-radius:999px}
    .warn{background:#ef4444}.mid{background:#f59e0b}.muted{opacity:.8}
    table{width:100%;border-collapse:collapse;margin-top:8px}
    th,td{border-bottom:1px solid rgba(255,255,255,.15);padding:8px;text-align:right}
    th{color:#ffe28a}
  </style>
</head>
<body>
  <div class="wrap">
    <h2>🗂️ دراسة حالة + تشخيص (DSM)</h2>
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
          <label>الأعراض (حرّر بعامية واضحة)</label>
          <textarea name="symptoms" placeholder="مثال: حزن شديد، فقدان المتعة، قلة نوم، أفكار انتحار...">{{symptoms}}</textarea>
          <label>التاريخ/الأثر الوظيفي (عمل/دراسة/علاقات/قضايا…)</label>
          <textarea name="history">{{history}}</textarea>
          <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap">
            <button class="btn" type="submit">إصدار تشخيص</button>
            <a class="btn" href="/" style="text-decoration:none;background:#9bd5ff;color:#04122c">الواجهة</a>
          </div>
        </form>
      </section>
      <aside class="card">
        {% if result %}
          <div><span class="badge">التشخيص المرجّح</span></div>
          <h3 style="margin:.4rem 0 0">{{result.name}}</h3>
          <div class="muted">الدرجة: {{result.score}}</div>
          <table><thead><tr><th>مطابقات</th></tr></thead>
            <tbody>{% for h in result.hits %}<tr><td>{{h}}</td></tr>{% endfor %}</tbody>
          </table>
          <p class="muted">⚠️ أداة مساعدة ولا تغني عن التقييم السريري.</p>
        {% else %}
          {% if top3 %}
            <div class="muted">لا يوجد تشخيص فوق العتبة بعد — أقرب احتمالات:</div>
            <table>
              <thead><tr><th>الاضطراب</th><th>الدرجة</th><th>مطابقات مختصرة</th></tr></thead>
              <tbody>
                {% for r in top3 %}
                  <tr><td>{{r.name}}</td><td>{{r.score}}</td><td>{{", ".join(r.hits[:5])}}</td></tr>
                {% endfor %}
              </tbody>
            </table>
            <p class="muted">زد وضوح الأعراض (هلوسة/أوهام/نوبة هلع/وسواس+طقوس/نهم+تطهير ...) واذكر المدة والأثر الوظيفي.</p>
          {% else %}
            <div class="badge warn">لا مطابقات كافية</div>
            <p class="muted">اكتب الأعراض بمفردات أدق واذكر المدة والتأثير على العمل/الدراسة/العلاقات.</p>
          {% endif %}
        {% endif %}
      </aside>
    </div>
  </div>
</body>
</html>
"""

@dsm_bp.route("/dsm", methods=["GET","POST"])
def dsm_hub():
    form = request.form if request.method == "POST" else {}
    name     = (form.get("name") or "").strip()
    age      = (form.get("age") or "").strip()
    gender   = (form.get("gender") or "").strip()
    duration = (form.get("duration") or "").strip()
    symptoms = (form.get("symptoms") or "").strip()
    history  = (form.get("history") or "").strip()

    try:
        d = int(float(duration)) if duration else 0
    except Exception:
        d = 0

    cand = score_case(symptoms, d, history) if request.method=="POST" else []
    best = pick_best(cand) if cand else None
    result = type("R",(object,),best)() if best else None
    top3 = [type("R",(object,),r)() for r in cand[:3]] if (not result and cand) else []

    return render_template_string(
        PAGE, name=name, age=age, gender=gender,
        duration=duration, symptoms=symptoms, history=history,
        result=result, top3=top3
    )
