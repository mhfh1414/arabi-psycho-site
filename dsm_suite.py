# -*- coding: utf-8 -*-
# dsm_suite.py  — DSM Blueprint (دراسة حالة + تشخيص) مع تعزيز قوي للفصام/الذهان

from flask import Blueprint, render_template_string, request
import re

dsm_bp = Blueprint("dsm", __name__)

# ================= أدوات لغوية =================
_AR_DIAC  = r"[ًٌٍَُِّْـ]"
_AR_PUNCT = r"[.,،;؛!?؟()\[\]{}\"\'<>:]"

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
    t = set(tokenize(text)); p = set(tokenize(phrase))
    if not p: return 0.0
    return len(t & p) / max(1, len(p))

# ================= مرادفات موسعة =================
SYNONYMS = {
    # اكتئاب ومزاج
    "حزن": ["زعل","كآبه","تعاسه","ضيقه","طفش","غم"],
    "انعدام المتعة": ["فقدان المتعه","لا استمتع","ما عاد يفرحني شي","فقدان الاهتمام"],
    "طاقة منخفضة": ["خمول","كسل","ارهاق","تعب","وهن","هبوط طاقه"],
    "اضطراب نوم": ["قلة نوم","كثرة نوم","ارق","نوم متقطع","استيقاظ مبكر","كوابيس","نعاس نهاري"],
    "شهية منخفضة": ["قلة اكل","سدت نفسي","فقدان شهية","ما ليا نفس"],
    "انسحاب اجتماعي": ["انعزال","انطواء","تجنب اجتماعي","ما اطلع"],

    # قلق/هلع
    "قلق": ["توتر","توجس","على اعصابي","ترقب","خوف مستمر"],
    "نوبة هلع": ["خفقان","اختناق","ضيق نفس","ذعر","رجفه","تعرق","دوخه"],

    # وسواس
    "وسواس": ["افكار متسلطه","اقتحاميه","هواجس"],
    "سلوك قهري": ["طقوس","تفقد متكرر","عد قهري","غسل متكرر","تنظيم مفرط"],

    # صدمة
    "حدث صادم": ["حادث شديد","اعتداء","كارثه","حرب","فقد عزيز","تنمر قاس"],
    "استرجاع الحدث": ["فلاش باك","ذكريات مؤلمه","كوابيس","فرط تيقظ"],

    # ADHD/توحد
    "تشتت": ["عدم تركيز","سهو","شرود","نسيان"],
    "فرط حركة": ["نشاط زائد","اندفاع","مقاطعه","ملل سريع"],

    # أكل
    "نهم": ["شراهه","نوبات اكل","اكل سرا"],

    # ====== توسيع قوي للذهان/الفصام ======
    "هلوسة": [
        "اسمع اصوات","اسمع صوت","اصوات براسي","اوامر صوتيه","اشوف ناس","اشوف اشياء",
        "هلاوس سمعيه","هلاوس بصريه","اشم روائح مو موجوده","احس احد يلمسني"
    ],
    "اوهام": [
        "يراقبوني","يلاحقوني","يسيطرون علي","افكار اضطهاد","تلفزيون يكلمني","افكار عظمة",
        "افكار غيره","حد يتحكم في افكاري","زرعوا شي في جسمي","اقرا افكار الناس"
    ],
}

# ================= قاعدة DSM =================
DSM_DB = {
    # ذهان
    "فصام": {
        "keywords": ["هلوسة","اوهام","تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني","انعدام اراده"],
        "required": ["هلوسة","اوهام"],
        "weight": 2.6,          # أعلى وزن
        "onset": "بلوغ مبكر"
    },
    "اضطراب فصامي عاطفي": {
        "keywords": ["اعراض ذهانيه","اكتئاب شديد","هوس","تذبذب مزاج"],
        "required": ["اعراض ذهانيه"], "weight": 1.7
    },

    # اكتئاب/مزاج
    "اضطراب اكتئابي جسيم": {
        "keywords": ["حزن","مزاج منخفض","انعدام المتعة","فقدان المتعة","بكاء","انسحاب اجتماعي",
                     "طاقة منخفضة","ارهاق","تعب","بطء نفسي حركي","اضطراب نوم","ارق","نوم متقطع",
                     "استيقاظ مبكر","كثرة نوم","شهية منخفضة","قلة اكل","فقدان شهية","فقدان وزن","زيادة وزن",
                     "تركيز ضعيف","شعور بالذنب","يأس","تفكير انتحاري"],
        "required": ["حزن","انعدام المتعة"], "weight": 1.9
    },
    "اكتئاب مستمر (عسر المزاج)": {
        "keywords": ["مزاج مكتئب مزمن","تشاؤم مزمن","طاقة قليلة","نوم ضعيف","شهية قليلة","ثقه منخفضه","انتاجية ضعيفه"],
        "required": ["مزاج مكتئب مزمن"], "weight": 1.5
    },
    "اضطراب ثنائي القطب": {
        "keywords": ["نوبة هوس","طاقة عالية","قليل نوم","اندفاع","تهور","افكار سباق","طلاقة الكلام","عظمة","نوبات اكتئاب"],
        "required": ["نوبة هوس"], "weight": 1.8
    },

    # قلق/هلع/رهاب
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

    # وسواس
    "اضطراب الوسواس القهري": {
        "keywords": ["وسواس","افكار اقتحاميه","سلوك قهري","طقوس","تفقد متكرر","غسل متكرر","تنظيم مفرط","عد قهري","خوف تلوث"],
        "required": ["وسواس","سلوك قهري"], "weight": 1.7
    },

    # صدمة
    "اضطراب ما بعد الصدمة": {
        "keywords": ["حدث صادم","استرجاع الحدث","فلاش باك","كابوس","تجنب","خدر عاطفي","يقظه مفرطه","حساسيه صوت"],
        "required": ["حدث صادم","استرجاع الحدث"], "weight": 1.8
    },

    # جسدية/تحولي
    "اعراض جسدية": {
        "keywords": ["الم غير مفسر","اعراض جسدية متعدده","انشغال صحي","زياره اطباء كثيره"],
        "required": ["الم غير مفسر"], "weight": 1.5
    },

    # أكل
    "قهم عصبي": {
        "keywords": ["نقص وزن شديد","خوف من زياده الوزن","صورة جسد سلبيه","تقييد طعام"],
        "required": ["نقص وزن شديد","خوف من زياده الوزن"], "weight": 1.7
    },

    # نوم (نقلل الوزن كي لا يطغى على الذهان)
    "فرط نعاس/ناركوليبسي": {
        "keywords": ["نعاس نهاري","غفوات مفاجئة","شلل نوم","هلوسات نعاس"],
        "required": ["نعاس نهاري"], "weight": 1.1
    },
}

# تجهيز سريع
def prep_db(db):
    out = {}
    for name, meta in db.items():
        kws = meta["keywords"]
        out[name] = {
            "req": [normalize(x) for x in meta.get("required", [])],
            "kwn": [normalize(x) for x in kws],
            "kwr": kws,
            "w": float(meta.get("weight", 1.0)),
            "onset": meta.get("onset","")
        }
    return out

DSM = prep_db(DSM_DB)

# =============== محرك الدرجات ===============
_PSYCOTIC_FLAGS = {normalize("هلوسة"), normalize("اوهام")}
_RED_WEIGHTS = {
    normalize("هلوسة"): 2.4,
    normalize("اوهام"): 2.4,
    normalize("نوبة هلع"): 2.0,
    normalize("تفكير انتحاري"): 2.2,
}

def score(symptoms: str, age: str="", gender: str="", duration_days: str="", history: str=""):
    text = normalize(symptoms or "")

    # ضخ مرادفات إلى النص لالتقاط العامي
    for base, syns in SYNONYMS.items():
        if any(normalize(w) in text for w in [base] + syns):
            text += " " + " ".join(set(normalize(s) for s in ([base] + syns)))

    # عوامل مساعدة بسيطة
    try: dur = float(duration_days)
    except: dur = 0.0
    durB = 1.25 if dur>=365 else 1.15 if dur>=90 else 1.08 if dur>=30 else 1.0

    h = normalize(history or "")
    histB = 1.1 if any(k in h for k in ["مشاكل عمل","مشاكل زواج","طلاق","تعثر دراسي","غياب متكرر"]) else 1.0

    out = []
    for dx, meta in DSM.items():
        # المطلوبات
        req = meta["req"]
        if req and not all((r in text) or (similarity(text, r) >= 0.66) for r in req):
            continue

        sc = 0.0; hits = []
        for raw_kw, kw in zip(meta["kwr"], meta["kwn"]):
            if kw in text:
                w = _RED_WEIGHTS.get(kw, 1.0)
                sc += w; hits.append(raw_kw)
            else:
                sim = similarity(text, kw)
                if sim >= 0.66:
                    sc += 0.8; hits.append(raw_kw+"~")
                elif sim >= 0.4:
                    sc += 0.35

        if sc == 0: 
            continue

        # تعزيز قوي في حال وجود علامة ذهانية
        if any(flag in text for flag in _PSYCOTIC_FLAGS) and dx == "فصام":
            sc *= 1.8

        sc *= meta["w"]; sc *= durB; sc *= histB
        out.append({"name": dx, "score": round(sc,2), "hits": hits[:12]})

    out.sort(key=lambda x: x["score"], reverse=True)
    return out[:5]

# =============== واجهة HTML ===============
_PAGE = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>DSM | دراسة حالة وتشخيص</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap" rel="stylesheet">
<style>
:root{--b1:#0b3a75;--b2:#0a65b0;--gold:#f4b400}
*{box-sizing:border-box}body{margin:0;font-family:Tajawal,system-ui;background:linear-gradient(135deg,var(--b1),var(--b2));color:#fff}
.wrap{max-width:1180px;margin:26px auto;padding:16px}
.card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px}
.grid{display:grid;grid-template-columns:1.05fr .95fr;gap:16px} @media(max-width:1000px){.grid{grid-template-columns:1fr}}
label{display:block;margin:8px 2px 6px;color:#ffe28a}
input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:12px 14px}
textarea{min-height:130px;resize:vertical} .btn{background:var(--gold);color:#2b1b02;border:none;border-radius:14px;padding:12px 16px;font-weight:800;cursor:pointer}
.result{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:4px 0}
.ok{background:#16a34a}.warn{background:#ef4444}
table{width:100%;border-collapse:collapse;margin-top:8px}
th,td{border-bottom:1px solid rgba(255,255,255,.15);padding:8px 6px;text-align:right}
th{color:#ffe28a}
</style></head><body><div class="wrap">{{ body|safe }}</div></body></html>
"""

def _form(initial=None, result_html=""):
    f = initial or {}
    body = f"""
    <div class="grid">
      <section class="card">
        <form method="post">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label>الاسم الكامل</label><input name="name" value="{f.get('name','')}"></div>
            <div><label>العمر</label><input name="age" value="{f.get('age','')}"></div>
            <div><label>الجنس</label>
              <select name="gender">
                <option value="" {'selected' if not f.get('gender') else ''}>— اختر —</option>
                <option {'selected' if f.get('gender')=='ذكر' else ''}>ذكر</option>
                <option {'selected' if f.get('gender')=='أنثى' else ''}>أنثى</option>
              </select>
            </div>
            <div><label>مدة الأعراض (بالأيام)</label><input name="duration" value="{f.get('duration','')}"></div>
          </div>
          <label>الأعراض (اكتب بحرّية: مثلاً "اسمع أصوات/ يشوف أشياء / مراقبة")</label>
          <textarea name="symptoms">{f.get('symptoms','')}</textarea>
          <label>التاريخ/الأثر الوظيفي</label>
          <textarea name="history">{f.get('history','')}</textarea>
          <div style="margin-top:10px"><button class="btn" type="submit">تشخيص مبدئي</button></div>
        </form>
      </section>
      <aside class="result">{result_html or '<span class="badge warn">لا توجد نتيجة بعد</span>'}</aside>
    </div>
    """
    return render_template_string(_PAGE, body=body)

# =============== المسار ===============
@dsm_bp.route("/dsm", methods=["GET","POST"])
def dsm_page():
    if request.method == "GET":
        return _form()
    form = {k: (request.form.get(k,"") or "").strip() for k in ["name","age","gender","duration","symptoms","history"]}
    details = score(form["symptoms"], age=form["age"], gender=form["gender"], duration_days=form["duration"], history=form["history"])
    if not details:
        res_html = """
          <h3>📋 النتيجة</h3>
          <p><span class="badge warn">لا تطابقات مباشرة كافية</span> — حاول كتابة مفردات أدق (مثلاً: هلوسة/ أوهام/ نوبة هلع/ وسواس...).</p>
        """
    else:
        rows = [f"<tr><td>{d['name']}</td><td>{d['score']}</td><td>{', '.join(d['hits'])}</td></tr>" for d in details]
        table = "<table><thead><tr><th>التشخيص المقترح</th><th>الدرجة</th><th>مطابقات</th></tr></thead><tbody>"+"".join(rows)+"</tbody></table>"
        res_html = f"<h3>📋 أقرب التشخيصات</h3>{table}<p style='opacity:.8;margin-top:8px'>⚠️ أداة مساعدة وليست تشخيصًا نهائيًا.</p>"
    return _form(form, res_html)
