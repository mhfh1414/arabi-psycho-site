# -*- coding: utf-8 -*-
# dsm_suite.py — بلوبرنت DSM موسّع (تشخيص واحد أدق)

from flask import Blueprint, render_template_string, request
import re
from difflib import SequenceMatcher

dsm_bp = Blueprint("dsm", __name__, url_prefix="/dsm")

# ------------------ أدوات نص عربية ------------------
_AR_DIAC = r"[ًٌٍَُِّْـ]"
_AR_PUNCT = r"[.,،;؛!?؟()\[\]{}\"'<>:/\\|*_+=-]"

def normalize(text: str) -> str:
    if not text: return ""
    t = text.strip().lower()
    t = re.sub(_AR_DIAC, "", t)
    t = re.sub(_AR_PUNCT, " ", t)
    t = (t.replace("أ","ا").replace("إ","ا").replace("آ","ا")
           .replace("ة","ه").replace("ى","ي").replace("ؤ","و").replace("ئ","ي"))
    t = re.sub(r"\s+", " ", t)
    return t

def sim(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

# ------------------ مرادفات بسيطة لتعزيز المطابقة ------------------
SYN = {
    "حزن": ["كابه","ضيقه","تعاسه","زعل"],
    "انعدام المتعه": ["فقدان المتعه","فقدان الاهتمام","ما عاد يفرحني شي"],
    "قلق": ["توتر","توجس","على اعصابي"],
    "نوبه هلع": ["هلع","ذعر","فجعه"],
    "هلوسه": ["هلاوس","اسمع اصوات","اشوف اشياء"],
    "اوهام": ["ضلالات","افكار وهاميه","بارانويا","اضطهاد"],
    "رهاب اجتماعي": ["خوف اجتماعي","خجل شديد","قلق اداء"],
    "وسواس": ["افكار متسلطه","اقتحاميه","هواجس"],
    "سلوك قهري": ["طقوس","غسل متكرر","تفقد متكرر","عد قهري"],
    "تشتت": ["عدم تركيز","نسيان","سهو"],
    "فرط حركه": ["نشاط زائد","اندفاع","مقاطعه"],
    "شهية منخفضه": ["سدت نفسي","قلة اكل"],
    "نهم": ["شراهه","اكل كثير","نوبات اكل"],
    "تطهير": ["استفراغ متعمد","ملينات","صيام تعويضي"],
}

def expand_with_syn(text: str) -> str:
    base = normalize(text)
    bag = [base]
    for k, vs in SYN.items():
        k_n = normalize(k)
        if k_n in base or any(normalize(v) in base for v in vs):
            bag += [k_n] + [normalize(v) for v in vs]
    return " ".join(bag)

# ------------------ قاعدة DSM موسعة (مختارة) ------------------
# لكل اضطراب: required (يجب توفرها)، keywords (تحسب نقاط)، weight (ترجيح)
DSM = {
    "اضطراب اكتئابي جسيم": {
        "required": ["حزن", "انعدام المتعه"],
        "keywords": ["قلة نوم","كثرة نوم","تعب","بطء نفسي حركي","شعور بالذنب","ياس","تفكير انتحاري","شهية منخفضه"],
        "weight": 1.7
    },
    "اكتئاب مستمر (عسر المزاج)": {
        "required": ["حزن"],
        "keywords": ["مزمن","سنتين","قلة طاقه","قله تركيز","نوم سيء","ثقه منخفضه"],
        "weight": 1.3
    },
    "اضطراب ثنائي القطب (نوبة هوس)": {
        "required": ["طاقة عاليه","قليل نوم"],
        "keywords": ["اندفاع","افكار سباق","طلاقة الكلام","عظمه","تهور","مشاكل قانونيه"],
        "weight": 1.8
    },
    "اضطراب القلق العام": {
        "required": ["قلق"],
        "keywords": ["شد عضلي","صعوبه تركيز","ارق","تعب","قابليه استفزاز","قلق مفرط"],
        "weight": 1.4
    },
    "اضطراب الهلع": {
        "required": ["نوبه هلع"],
        "keywords": ["خفقان","ضيق نفس","اختناق","رجفه","تعرق","خوف الموت"],
        "weight": 1.6
    },
    "رهاب اجتماعي": {
        "required": ["رهاب اجتماعي"],
        "keywords": ["تجنب اجتماعي","احمرار","رجفه","خوف تقييم"],
        "weight": 1.35
    },
    "رهاب محدد": {
        "required": ["خوف شديد"],
        "keywords": ["فوبيا","حشرات","طيران","مرتفعات","حقن","دم","ظلام"],
        "weight": 1.2
    },
    "رهاب الساحه": {
        "required": ["خوف من الاماكن المفتوحه"],
        "keywords": ["مواصلات","تجمعات","تجنب الخروج وحيدا"],
        "weight": 1.3
    },
    "اضطراب الوسواس القهري": {
        "required": ["وسواس","سلوك قهري"],
        "keywords": ["غسل متكرر","تفقد","عد","تنظيم","تدنيس","خوف تلوث"],
        "weight": 1.7
    },
    "اضطراب ما بعد الصدمة": {
        "required": ["حدث صادم","استرجاع"],
        "keywords": ["كوابيس","يقظه مفرطه","تجنب","خدر عاطفي","ذنب الناجي"],
        "weight": 1.7
    },
    "فصام": {
        "required": ["هلوسه","اوهام"],
        "keywords": ["تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني"],
        "weight": 1.9
    },
    "اضطراب فصامي عاطفي": {
        "required": ["هلوسه"],
        "keywords": ["نوبات اكتئاب","نوبات هوس","تذبذب مزاج"],
        "weight": 1.6
    },
    "نهم عصبي (نهام)": {
        "required": ["نهم","تطهير"],
        "keywords": ["ذنب بعد الاكل","اختلال وزن"],
        "weight": 1.5
    },
    "قهم عصبي": {
        "required": ["نقص وزن شديد","خوف من زياده الوزن"],
        "keywords": ["تقييد طعام","صورة جسد سلبيه"],
        "weight": 1.6
    },
    "اضطراب نهم الطعام": {
        "required": ["نهم"],
        "keywords": ["فقدان تحكم","اكل سرا","زياده وزن"],
        "weight": 1.4
    },
    "اعراض جسديه (Somatic)": {
        "required": ["الم غير مفسر"],
        "keywords": ["زياره اطباء كثيره","انشغال صحي"],
        "weight": 1.3
    },
    "اضطراب نقص الانتباه وفرط الحركه": {
        "required": ["تشتت","فرط حركه"],
        "keywords": ["اندفاع","نسيان","تنظيم ضعيف"],
        "weight": 1.25
    },
    "شخصية حدّيه": {
        "required": ["تقلب عاطفي"],
        "keywords": ["اندفاع","خوف هجر","ايذاء ذاتي","فراغ مزمن"],
        "weight": 1.2
    },
}

# حوّل كل required/keywords إلى نسخ مطبّعة لسرعة المطابقة
DSM_IDX = {}
for name, meta in DSM.items():
    DSM_IDX[name] = {
        "required": [normalize(x) for x in meta["required"]],
        "keywords": [normalize(x) for x in meta["keywords"]],
        "weight": float(meta.get("weight", 1.0)),
    }

# ------------------ محرك التشخيص (يعيد تشخيص واحد) ------------------
def diagnose(symptoms: str, duration_days: int = 0) -> tuple[str, float, list]:
    text = expand_with_syn(symptoms)
    durB = 1.0
    if duration_days >= 365: durB = 1.2
    elif duration_days >= 90: durB = 1.12
    elif duration_days >= 30: durB = 1.06

    best_name, best_score, best_hits = None, 0.0, []

    for name, meta in DSM_IDX.items():
        # تحقّق المطلوبات
        if meta["required"] and not all(r in text or sim(text, r) >= 0.72 for r in meta["required"]):
            continue

        sc = 0.0
        hits = []
        for kw in meta["keywords"] + meta["required"]:
            if kw in text:
                w = 1.0
                if kw in ("هلوسه","اوهام","تفكير انتحاري","نوبه هلع"): w = 1.6
                sc += w; hits.append(kw)
            else:
                s = sim(text, kw)
                if s >= 0.72:
                    sc += 0.7; hits.append(kw+"~")
                elif s >= 0.5:
                    sc += 0.35

        # ترجيحات عامة
        sc *= meta["weight"]
        sc *= durB

        if sc > best_score:
            best_name, best_score, best_hits = name, sc, hits

    return best_name, round(best_score, 2), best_hits

# ------------------ واجهة HTML ------------------
PAGE = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>DSM-5 | دراسة حالة وتشخيص أدق</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap" rel="stylesheet">
  <style>
    body{margin:0;font-family:'Tajawal',system-ui;background:linear-gradient(135deg,#0b3a75,#0a65b0);color:#fff}
    .wrap{max-width:1100px;margin:24px auto;padding:16px}
    .card{background:rgba(255,255,255,.08);border:1px solid #ffffff22;border-radius:16px;padding:18px}
    label{color:#ffd86a;margin:8px 0 6px;display:block}
    input,textarea{width:100%;padding:12px 14px;border-radius:12px;border:1px solid #ffffff33;background:rgba(255,255,255,.12);color:#fff}
    textarea{min-height:130px;resize:vertical}
    button{margin-top:12px;background:#f4b400;color:#2b1b02;border:none;border-radius:12px;padding:12px 16px;font-weight:800;cursor:pointer}
    .result{margin-top:16px;padding:14px;border-radius:14px;background:#fff;color:#111}
    .hits span{display:inline-block;margin:3px 6px 0 0;padding:4px 8px;border-radius:999px;background:#eef}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h2>🗂️ دراسة حالة + تشخيص (DSM)</h2>
      <form method="post">
        <label>الأعراض (اكتب وصفًا حرًا)</label>
        <textarea name="symptoms" placeholder="مثال: هلوسه سمعيه، اوهام اضطهاد، انسحاب عن الناس...">{{ symptoms or "" }}</textarea>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <div>
            <label>مدة الأعراض (بالأيام)</label>
            <input name="duration" value="{{ duration or "" }}" placeholder="90">
          </div>
          <div>
            <label>الاسم (اختياري)</label>
            <input name="name" value="{{ name or "" }}" placeholder="الاسم">
          </div>
        </div>
        <button type="submit">تشخيص أدق</button>
      </form>

      {% if dx %}
        <div class="result">
          <h3>📋 التشخيص الأدق: {{ dx }}</h3>
          <p>الدرجة الكلية: <b>{{ score }}</b></p>
          <div class="hits">
            <small>مطابقات:</small>
            {% for h in hits %}<span>{{ h }}</span>{% endfor %}
          </div>
          <p style="opacity:.75;margin-top:8px">⚠️ هذه نتيجة مساعدة وليست بديلاً عن التقييم الإكلينيكي.</p>
        </div>
      {% elif tried %}
        <div class="result"><b>❌ لا توجد مطابقة كافية.</b> أضف مفردات أدق (مثلاً: هلوسه/اوهام/وسواس/نوبه هلع/رهاب/نهم/تطهير/انعدام المتعه...).</div>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

# ------------------ المسار ------------------
@dsm_bp.route("/", methods=["GET","POST"])
def dsm_hub():
    ctx = {"dx": None, "score": None, "hits": [], "tried": False,
           "symptoms":"", "duration":"", "name":""}
    if request.method == "POST":
        ctx["tried"] = True
        raw_symptoms = request.form.get("symptoms","")
        ctx["symptoms"] = raw_symptoms
        dur_raw = request.form.get("duration","")
        ctx["duration"] = dur_raw
        try: dur = int(dur_raw or 0)
        except: dur = 0
        dx, score, hits = diagnose(raw_symptoms, duration_days=dur)
        ctx.update({"dx": dx, "score": score, "hits": hits})
    return render_template_string(PAGE, **ctx)
