# -*- coding: utf-8 -*-
# dsm_suite.py — DSM تشخيصي مُحسَّن مع إنذارات مخاطر ورسائل أوضح

from flask import Blueprint, request, render_template_string, redirect, url_for
import re

dsm_bp = Blueprint("dsm_bp", __name__)

# ======================= أدوات لغوية (تطبيع عربي) =======================
_AR_DIAC  = r"[ًٌٍَُِّْـ]"
_AR_PUNCT = r"[.,،;؛!?؟()\[\]{}\"\'<>:/\\\-_=+*]"

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

def jaccard_sim(a: str, b: str) -> float:
    A, B = set(tokenize(a)), set(tokenize(b))
    return 0.0 if not A or not B else len(A & B) / len(A | B)

# ======================= مرادفات (تعزيز المطابقة) =======================
SYNONYMS = {
    # ذهان
    "هلوسه": ["هلاوس سمعيه","هلاوس بصريه","اسمع اصوات","اشوف اشياء","اسمع حد يناديني"],
    "اوهام": ["ضلالات","اضطهاد","عظمه","غيره وهاميه","افكار غير واقعيه","افكار مراقبه"],
    "تفكير غير منظم": ["كلام متشتت","افكار مشتته","افكار متسارعه","كلام غير مفهوم"],

    # اكتئاب
    "حزن": ["كآبه","تعاسه","ضيقه","زعل"],
    "انعدام المتعه": ["فقدان المتعه","لا استمتع","ما عاد يفرحني شي","فقدان الاهتمام"],
    "طاقة منخفضه": ["ارهاق","تعب","خمول","كسل","وهن"],
    "اضطراب نوم": ["ارق","قلة نوم","نوم متقطع","استيقاظ مبكر","كثرة نوم"],
    "شهية منخفضه": ["قلة اكل","فقدان شهيه","سدت نفسي"],
    "تفكير انتحاري": ["افكار انتحار","تمني الموت","ارغب انهي حياتي","افكر اذبح نفسي"],

    # قلق/هلع
    "قلق": ["توتر","توجس","على اعصابي"],
    "نوبة هلع": ["خفقان","اختناق","ضيق نفس","رجفه","ذعر","تعرق","دوخه"],

    # وسواس
    "وسواس": ["افكار متسلطه","اقتحاميه","هواجس"],
    "سلوك قهري": ["طقوس","تفقد متكرر","عد قهري","غسل مفرط","تنظيم مفرط"],

    # ADHD
    "تشتت": ["عدم تركيز","نسيان","سهو","شرود"],
    "فرط حركه": ["نشاط زائد","اندفاع","مقاطعه","ملل سريع"],

    # PTSD
    "حدث صادم": ["حادث شديد","اعتداء","كارثه","حرب","فقد عزيز","تعذيب","تنمر قاس"],
    "استرجاع الحدث": ["فلاش باك","ذكريات مؤلمه","كوابيس","فرط تيقظ"],

    # أكل/نوم
    "نهم": ["شراهه","نوبات اكل","اكل سرا"],
    "تطهير": ["ترجيع متعمد","ملينات","صيام تعويضي"],
}

# ======================= قاعدة DSM (أوزان مُعدلة) =======================
DSM_DB = {
    # الذهان أولاً وبأوزان أعلى
    "فصام": {
        "req": ["هلوسه","اوهام"],
        "kw":  ["هلوسه","اوهام","تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني","انعدام اراده","تراجع اداء"],
        "w":   2.4  # رُفعت بشدة
    },
    "اضطراب فصامي عاطفي": {
        "req": ["اعراض ذهانيه"],
        "kw":  ["اعراض ذهانيه","اكتئاب شديد","نوبه هوس","تذبذب مزاج","تفكير غير منظم"],
        "w":   2.0
    },
    "اضطراب وهامي": {
        "req": ["اوهام"],
        "kw":  ["اوهام","غيره وهاميه","اضطهاد","عظمه","شك مرضي"],
        "w":   1.9
    },

    # اكتئابي/ثنائي القطب
    "اضطراب اكتئابي جسيم": {
        "req": ["حزن","انعدام المتعه"],
        "kw":  ["حزن","انعدام المتعه","طاقة منخفضه","اضطراب نوم","شهية منخفضه",
                "تركيز ضعيف","شعور بالذنب","يأس","تفكير انتحاري","انسحاب اجتماعي"],
        "w":   1.8
    },
    "اضطراب ثنائي القطب": {
        "req": ["نوبه هوس"],
        "kw":  ["نوبه هوس","قليل نوم","اندفاع","افكار متسارعه","طلاقة الكلام","عظمه","نوبات اكتئاب"],
        "w":   1.75
    },

    # قلق/هلع/رهاب
    "اضطراب الهلع": {
        "req": ["نوبة هلع"],
        "kw":  ["نوبة هلع","خفقان","اختناق","ضيق نفس","رجفه","خوف الموت"],
        "w":   1.6
    },
    "اضطراب القلق العام": {
        "req": ["قلق"],
        "kw":  ["قلق","قلق مفرط","شد عضلي","ارق","تعب","صعوبة تركيز","استباق سيء"],
        "w":   1.45
    },
    "رهاب اجتماعي": {
        "req": ["خوف اجتماعي"],
        "kw":  ["خوف اجتماعي","خوف التقييم","خجل شديد","تجنب اجتماعي","قلق اداء"],
        "w":   1.4
    },

    # وسواس
    "اضطراب الوسواس القهري": {
        "req": ["وسواس","سلوك قهري"],
        "kw":  ["وسواس","سلوك قهري","تفقد متكرر","غسل متكرر","تنظيم مفرط","عد قهري","خوف تلوث"],
        "w":   1.7
    },

    # PTSD
    "اضطراب ما بعد الصدمة": {
        "req": ["حدث صادم","استرجاع الحدث"],
        "kw":  ["تجنب","خدر عاطفي","فرط تيقظ","كابوس","ذنب الناجي","كوابيس"],
        "w":   1.8
    },

    # ADHD
    "اضطراب نقص الانتباه وفرط الحركة": {
        "req": ["تشتت","فرط حركه"],
        "kw":  ["تشتت","فرط حركه","اندفاع","نسيان","تنظيم ضعيف","تأجيل"],
        "w":   1.2
    },

    # نوم
    "أرق مزمن": {
        "req": ["ارق"],
        "kw":  ["ارق","قلة نوم","نوم متقطع","استيقاظ مبكر","اجهاد نهاري"],
        "w":   1.35
    },
    "ناركوليبسي": {  # خفّضنا وزنه كي لا يتقدّم بالخطأ
        "req": ["نعاس نهاري"],
        "kw":  ["نعاس نهاري","نوم مفاجئ","شلل نوم","هلوسات نعاس"],
        "w":   0.9
    },

    # أكل (مختصر)
    "نهام عصبي": {
        "req": ["نهم","تطهير"],
        "kw":  ["نهم","تطهير","ذنب بعد الاكل"],
        "w":   1.55
    },
}

# ====== تجهيز كلمات + توسيع النص بالمرادفات ======
def expand_text(text: str) -> str:
    t = normalize(text)
    for base, syns in SYNONYMS.items():
        all_terms = [base] + syns
        if any(normalize(s) in t for s in all_terms):
            t += " " + " ".join(normalize(s) for s in all_terms)
    return t

# ====== كاش إنذار مخاطر ======
RISK_TERMS = {
    "suicide": ["انتحار","تفكير انتحاري","افكار انتحار","تمني الموت","انهاء حياتي","اذبح نفسي"],
    "harm":    ["اذي الاخرين","قتل","اعتداء","افجر","احرق"],
    "psychosis_severe": ["هلوسه","اوهام","تفكير غير منظم"]
}

def risk_flags(text_norm: str):
    flags = []
    def has_any(words): return any(normalize(w) in text_norm for w in words)
    if has_any(RISK_TERMS["suicide"]): flags.append(("خطر انتحاري", "red"))
    if has_any(RISK_TERMS["harm"]):    flags.append(("خطر إيذاء الآخرين", "red"))
    if has_any(RISK_TERMS["psychosis_severe"]): flags.append(("أعراض ذهانية واضحة", "amber"))
    return flags

# ====== محرك الدرجات ======
def score(symptoms: str, duration_days: str = "", history: str = ""):
    text = expand_text(symptoms or "")
    try: dur = float(duration_days); 
    except: dur = 0.0

    durB = 1.0
    if dur >= 365: durB = 1.25
    elif dur >= 90: durB = 1.15
    elif dur >= 30: durB = 1.08

    hist = normalize(history or "")
    histB = 1.0 + 0.1*sum(k in hist for k in ["مشاكل عمل","تراجع دراسي","طلاق","مشاكل زواج","قضايا"])

    results = []
    for dx, meta in DSM_DB.items():
        req_ok = all(normalize(r) in text or jaccard_sim(text, r) >= 0.55 for r in meta["req"])
        if not req_ok: 
            continue

        s = 0.0; hits=[]
        for kw in meta["kw"]:
            nk = normalize(kw)
            if nk in text: 
                # أوزان خاصة: ذهان قوي جدًّا
                if dx == "فصام" and nk in (normalize("هلوسه"), normalize("اوهام")):
                    s += 3.0
                elif nk in (normalize("هلوسه"), normalize("اوهام")):
                    s += 2.2
                else:
                    s += 1.0
                hits.append(kw)
            else:
                sim = jaccard_sim(text, kw)
                if sim >= 0.6:
                    s += 0.8; hits.append(kw+"~")
                elif sim >= 0.4:
                    s += 0.4

        if s == 0.0: 
            continue

        s *= float(meta.get("w", 1.0))
        s *= durB
        s *= histB

        # خصم خفيف عن ناركوليبسي إن وُجدت كلمات ذهانية
        if dx == "ناركوليبسي" and (normalize("هلوسه") in text or normalize("اوهام") in text):
            s *= 0.6

        results.append({"dx": dx, "score": round(s,2), "hits": hits[:12]})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5], risk_flags(text)

# ======================= قوالب HTML داخل الملف =======================
BASE = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>DSM | عربي سايكو</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400}
    *{box-sizing:border-box}body{margin:0;font-family:"Tajawal",system-ui;background:linear-gradient(135deg,var(--bg1),var(--bg2)) fixed;color:#fff}
    .wrap{max-width:1180px;margin:28px auto;padding:16px}
    .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:18px}
    .grid{display:grid;grid-template-columns:1.1fr .9fr;gap:16px}
    @media(max-width:1000px){.grid{grid-template-columns:1fr}}
    label{display:block;color:#ffe28a;margin:8px 2px 6px}
    input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:12px 14px}
    textarea{min-height:140px;resize:vertical}
    a.btn,button.btn{display:inline-block;background:var(--gold);color:#2b1b02;border-radius:14px;padding:12px 16px;text-decoration:none;font-weight:800;border:none;cursor:pointer}
    table{width:100%;border-collapse:collapse;margin-top:8px}
    th,td{border-bottom:1px solid rgba(255,255,255,.15);padding:8px 6px;text-align:right}
    th{color:#ffe28a}
    .badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:2px}
    .red{background:#dc2626}.amber{background:#f59e0b}.green{background:#16a34a}
    .muted{opacity:.9}
  </style>
</head>
<body>
  <div class="wrap">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
      <h2 style="margin:0">🗂️ دراسة حالة + تشخيص (DSM)</h2>
      <a class="btn" href="{{ url_for('home_bp.index') if 'home_bp' in current_app.blueprints else '/' }}">الواجهة</a>
    </div>
    {{ body|safe }}
  </div>
</body>
</html>
"""

def _form(name="", age="", gender="", duration="", symptoms="", history=""):
    return f"""
    <section class="card">
      <form method="post">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
          <div><label>الاسم</label><input name="name" value="{name}"></div>
          <div><label>العمر</label><input name="age" value="{age}"></div>
          <div><label>الجنس</label>
            <select name="gender">
              <option value="" {"selected" if not gender else ""}>— اختر —</option>
              <option {"selected" if gender=="ذكر" else ""}>ذكر</option>
              <option {"selected" if gender=="أنثى" else ""}>أنثى</option>
            </select>
          </div>
          <div><label>مدة الأعراض (أيام)</label><input name="duration" value="{duration}"></div>
        </div>
        <label>الأعراض/دراسة الحالة</label>
        <textarea name="symptoms" placeholder="مثال: هلوسة سمعية، أوهام اضطهاد، انسحاب اجتماعي، نوم قليل...">{symptoms}</textarea>
        <label>تاريخ ووضع وظيفي (اختياري)</label>
        <textarea name="history" placeholder="أدوية، جلسات سابقة، مشاكل عمل/دراسة، علاقات...">{history}</textarea>
        <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap">
          <button class="btn" type="submit">تشخيص مبدئي</button>
        </div>
      </form>
    </section>
    """

# ======================= المسارات =======================
@dsm_bp.route("/dsm/", methods=["GET","POST"])
def dsm_page():
    if request.method == "GET":
        body = f"""
        <div class="grid">
          {_form()}
          <aside class="card">
            <span class="badge amber">إرشاد</span>
            <p class="muted">استخدم كلمات صريحة مثل: <b>هلوسه</b>، <b>اوهام</b>، <b>نوبة هلع</b>، <b>وسواس</b>، <b>انعدام المتعة</b>…<br>
            اذكر المدة والتأثير الوظيفي لوزنٍ أدق.</p>
          </aside>
        </div>
        """
        return render_template_string(BASE, body=body)

    # POST
    form = request.form
    name     = (form.get("name","") or "").strip()
    age      = (form.get("age","") or "").strip()
    gender   = (form.get("gender","") or "").strip()
    duration = (form.get("duration","") or "").strip()
    symptoms = (form.get("symptoms","") or "").strip()
    history  = (form.get("history","") or "").strip()

    results, flags = score(symptoms, duration_days=duration, history=history)

    if not results:
        res_html = """
        <section class="card">
          <span class="badge amber">لا تطابق كافٍ</span>
          <p class="muted">أضِف مفردات أدق للأعراض الأساسية + المدة + التأثير الوظيفي.</p>
        </section>
        """
    else:
        rows = "".join(
            f"<tr><td>{r['dx']}</td><td>{r['score']}</td><td>{', '.join(r['hits'])}</td></tr>"
            for r in results
        )
        risk_html = ""
        if flags:
            chips = "".join(f"<span class='badge {c}'>{t}</span>" for (t,c) in flags)
            risk_html = f"<div style='margin-top:8px'>{chips}</div>"
        res_html = f"""
        <section class="card">
          <h3 style="margin-top:0">أقرب التشخيصات (أفضل 5)</h3>
          <table>
            <thead><tr><th>التشخيص المقترح</th><th>الدرجة</th><th>أهم المطابقات</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
          {risk_html}
          <p class="muted" style="margin-top:8px">⚠️ هذه نتيجة مساعدة وليست تشخيصًا نهائيًا. يُنصح بالمقابلة الإكلينيكية.</p>
        </section>
        """

    body = f"""
    <div class="grid">
      {_form(name=name, age=age, gender=gender, duration=duration, symptoms=symptoms, history=history)}
      {res_html}
    </div>
    """
    return render_template_string(BASE, body=body)
