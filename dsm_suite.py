# -*- coding: utf-8 -*-
# dsm_suite.py — قاعدة DSM موسعة + دراسة حالة + مطابقة ذكية للأعراض (تشخيص مرجّح واحد)

from flask import Blueprint, render_template_string, request
import re

dsm_bp = Blueprint("dsm", __name__, url_prefix="/dsm")

# ============================== أدوات نص عربية ==============================
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

def tokens(s: str) -> set:
    return set(normalize(s).split())

def soft_contains(text_norm: str, phrase: str) -> bool:
    """مطابقة ناعمة: تعتبر العبارة موجودة إذا وُجدت كل كلماتها بالنص"""
    ptoks = set(normalize(phrase).split())
    return ptoks.issubset(tokens(text_norm))

# مرادفات مختصرة لزيادة الحساسية
SYN = {
    "حزن": ["كابه","تعاسه","زعل","ضيقه","طفش","غم"],
    "انعدام المتعة": ["فقدان المتعه","ما استمتع","ما عاد يفرحني شي","فقدان الاهتمام"],
    "طاقة منخفضة": ["خمول","كسل","ارهاق","تعب","وهن"],
    "اضطراب نوم": ["ارق","قلة نوم","نوم متقطع","استيقاظ مبكر","كثرة نوم","كوابيس","نعاس"],
    "شهية منخفضة": ["قلة اكل","سدت نفسي","فقدان شهيه"],
    "شهية زائدة": ["نهم","اكل كثير","شراهه"],
    "قلق": ["توتر","توجس","على اعصابي","قلق مفرط"],
    "نوبة هلع": ["خفقان","اختناق","ضيق نفس","ذعر","رجفه","تعرق","دوار"],
    "خوف اجتماعي": ["رهبه مواجهه","خجل شديد","قلق اداء"],
    "خوف شديد": ["فوبيا","خوف طيران","خوف المرتفعات","خوف الظلام","خوف حقن","خوف حشرات","خوف دم"],
    "وسواس": ["افكار متسلطه","اقتحاميه","هواجس","خوف تلوث"],
    "سلوك قهري": ["طقوس","تفقد متكرر","عد قهري","غسل متكرر","تنظيم مفرط"],
    "حدث صادم": ["تعرضت لحادث","اعتداء","كارثه","حرب","فقد عزيز","تنمر قاس"],
    "استرجاع الحدث": ["فلاش باك","ذكريات مؤلمه"],
    "هلوسة": ["هلاوس سمعيه","اسمع اصوات","اشوف اشياء"],
    "اوهام": ["ضلالات","اعتقادات وهميه","اضطهاد","عظمه","غيره وهاميه"],
    "تشتت": ["عدم تركيز","سهو","شرود","نسيان","ضعف تنظيم"],
    "فرط حركة": ["نشاط زائد","اندفاع","مقاطعه","ملل سريع"],
}

def expand_text_with_synonyms(text: str) -> str:
    t = normalize(text)
    for base, syns in SYN.items():
        if any(normalize(w) in t for w in [base] + syns):
            t += " " + " ".join(normalize(s) for s in ([base]+syns))
    return t

# ============================== قاعدة DSM موسّعة ==============================
# لكل اضطراب قائمة أعراض نموذجية. (بدون فهرس، فقط أمراض + أعراض)
DSM_DATA = {
    # -------- اضطرابات المزاج --------
    "اضطراب اكتئابي جسيم": [
        "حزن", "انعدام المتعة", "طاقة منخفضة", "اضطراب نوم", "شهية منخفضة", "شهية زائدة",
        "انسحاب اجتماعي", "تركيز ضعيف", "شعور بالذنب", "يأس", "افكار انتحارية"
    ],
    "اكتئاب مستمر (عسر المزاج)": [
        "مزاج مكتئب مزمن", "طاقة منخفضة", "نوم ضعيف", "شهية قليلة", "ثقه منخفضه", "انتاجية ضعيفه"
    ],
    "اضطراب ثنائي القطب I/II": [
        "نوبة هوس", "قليل نوم", "اندفاع", "تهور", "افكار سباق", "طلاقة الكلام", "عظمة", "نوبات اكتئاب"
    ],

    # -------- اضطرابات القلق والرهاب --------
    "اضطراب القلق العام": [
        "قلق", "قلق مفرط", "توتر", "شد عضلي", "صعوبة تركيز", "أرق", "تعب", "قابلية استفزاز"
    ],
    "اضطراب الهلع": [
        "نوبة هلع", "خفقان", "اختناق", "ضيق نفس", "رجفه", "تعرق", "دوار", "خوف الموت", "خوف فقدان السيطرة"
    ],
    "رهاب اجتماعي": [
        "خوف اجتماعي", "خجل شديد", "قلق اداء", "تجنب اجتماعي", "احمرار", "رجفه"
    ],
    "رهاب الساحة": [
        "خوف من الاماكن المفتوحه", "خوف من الازدحام", "تجنب مواصلات", "صعوبه الخروج وحيدا"
    ],
    "رهاب محدد": [
        "خوف شديد", "فوبيا", "خوف طيران", "خوف المرتفعات", "خوف الظلام", "خوف حشرات", "خوف حقن", "خوف دم"
    ],

    # -------- وسواس/أفعال قهرية --------
    "اضطراب الوسواس القهري": [
        "وسواس", "سلوك قهري", "تفقد متكرر", "غسل متكرر", "تنظيم مفرط", "عد قهري", "خوف تلوث"
    ],
    "تشوه صورة الجسد": [
        "انشغال بالمظهر", "عيوب متخيله", "تفقد المرآه", "تعديل مظهر مفرط"
    ],
    "اكتناز": [
        "اكتناز", "صعوبة رمي", "تكديس", "فوضى منزل"
    ],

    # -------- صدمة وضغوط --------
    "اضطراب ما بعد الصدمة": [
        "حدث صادم", "استرجاع الحدث", "كابوس", "تجنب", "خدر عاطفي", "يقظه مفرطه", "ذنب الناجي"
    ],
    "اضطراب كرب حاد": [
        "اعراض صدمة قصيرة", "يقظه مفرطه", "تجنب", "اضطراب ضغط حاد"
    ],
    "اضطراب تكيف": [
        "توتر موقف", "حزن بعد حدث", "قلق ظرفي", "تراجع اداء بعد ضغط"
    ],

    # -------- طيف ذهاني --------
    "فصام": [
        "هلوسة", "اوهام", "تفكير غير منظم", "انسحاب اجتماعي", "تسطح وجداني", "انعدام اراده"
    ],
    "اضطراب فصامي عاطفي": [
        "اعراض ذهانيه", "اكتئاب شديد", "نوبة هوس", "تذبذب مزاج"
    ],
    "اضطراب وهامي": [
        "ضلالات ثابتة", "غيرة وهامية", "اضطهاد", "عظمة", "شك مرضي"
    ],

    # -------- نمائية/عصبية --------
    "اضطراب نقص الانتباه وفرط الحركة": [
        "تشتت", "عدم تركيز", "فرط حركة", "اندفاع", "نسيان", "تنظيم ضعيف", "مقاطعه", "ملل سريع"
    ],
    "اضطراب طيف التوحد": [
        "تواصل اجتماعي ضعيف", "سلوك نمطي", "روتين", "حساسيات حسيه", "اهتمامات مقيده", "لغة متأخره", "حركات نمطيه"
    ],
    "متلازمة توريت/عرات": [
        "عرات", "حركات لا إرادية", "أصوات لا إرادية", "تفريغ توتر"
    ],

    # -------- نوم/يقظة --------
    "أرق مزمن": [
        "صعوبه نوم", "استيقاظ مبكر", "نوم متقطع", "عدم راحه", "اجهاد نهاري"
    ],
    "فرط نعاس/ناركوليبسي": [
        "نعاس نهاري", "غفوات مفاجئة", "شلل نوم", "هلوسات نعاس"
    ],
    "انقطاع نفس اثناء النوم": [
        "شخير", "توقف تنفس", "اختناق ليلي", "نعاس نهاري"
    ],

    # -------- أكل --------
    "قهم عصبي": [
        "نقص وزن شديد", "خوف من زياده الوزن", "صورة جسد سلبيه", "تقييد طعام"
    ],
    "نهام عصبي": [
        "نهم متكرر", "تطهير", "استفراغ", "ملينات", "ذنب بعد الاكل"
    ],
    "اضطراب نهم الطعام": [
        "نهم", "اكل بشراهه", "فقدان تحكم", "اكل سرا", "زيادة وزن"
    ],

    # -------- أعراض جسدية --------
    "اضطراب الاعراض الجسدية": [
        "الم غير مفسر", "اعراض جسدية متعددة", "انشغال صحي", "زياره اطباء كثيره"
    ],
    "قلق المرض": [
        "قلق صحي", "خوف مرض خطير", "تفقد جسد", "طمأنه متكرره", "بحث طبي مستمر"
    ],
    "اضطراب تحولي": [
        "اعراض عصبية بدون سبب عضوي", "شلل وظيفي", "نوبات غير صرعية", "فقدان احساس"
    ],

    # -------- شخصية --------
    "شخصية حدية": [
        "تقلب عاطفي", "اندفاع", "خوف هجر", "ايذاء ذاتي", "فراغ مزمن", "علاقات غير مستقرة"
    ],
    "شخصية نرجسية": [
        "عظمة", "حاجة اعجاب", "تعاطف قليل", "حساس للنقد"
    ],
    "شخصية وسواسية قهرية": [
        "انشغال بالتفاصيل", "كماليه", "صرامه", "قواعد", "عناد"
    ],

    # -------- مواد/إدمان --------
    "اضطراب تعاطي الكحول": [
        "كحول", "سكر متكرر", "تحمل", "اعراض انسحاب", "فقدان سيطرة"
    ],
    "اضطراب تعاطي القنب": [
        "حشيش", "قنب", "استخدام يومي", "تسامح", "انسحاب"
    ],
    "اضطراب تعاطي المنبهات": [
        "منشطات", "امفيتامين", "كوكايين", "سهر", "فقدان شهيه", "بارانويا"
    ],
    "اضطراب تعاطي الأفيونات": [
        "هيروين", "مورفين", "اوكسيدودون", "انسحاب", "تحمل", "رغبه ملحه"
    ],
}

# أعراض لازمة لبعض التشخيصات لرفع دقّة الاختيار (اختياري)
REQUIRED = {
    "اضطراب اكتئابي جسيم": ["حزن", "انعدام المتعة"],
    "فصام": ["هلوسة", "اوهام"],
    "اضطراب الهلع": ["نوبة هلع"],
    "اضطراب الوسواس القهري": ["وسواس", "سلوك قهري"],
    "اضطراب ما بعد الصدمة": ["حدث صادم", "استرجاع الحدث"],
    "قهم عصبي": ["نقص وزن شديد", "خوف من زياده الوزن"],
    "نهام عصبي": ["نهم متكرر", "تطهير"],
}

# تعزيزات: رايات حرجة + مدة
CRITICAL_SYM = {"هلوسة","اوهام","نوبة هلع","افكار انتحارية"}
DURATION_BOOSTS = [(365*2,1.25),(180,1.18),(90,1.1),(30,1.05)]

def score_diagnoses(symptoms_text: str, duration_days: int) -> list[dict]:
    """يحسب درجات لكل اضطراب ويرجع أفضل 3"""
    text = expand_text_with_synonyms(symptoms_text or "")
    dur_boost = 1.0
    for d, b in DURATION_BOOSTS:
        if duration_days >= d:
            dur_boost = b; break

    out = []
    for dx, kws in DSM_DATA.items():
        # تحقق المطلوبات (إن وُجدت)
        req = REQUIRED.get(dx, [])
        if req and not all(soft_contains(text, r) for r in req):
            continue

        sc = 0.0; hits=[]
        # المطلوبات أثقل
        for r in req:
            if soft_contains(text, r):
                sc += 1.2; hits.append(r)
        # بقية الكلمات
        for k in kws:
            if soft_contains(text, k):
                sc += 0.7; hits.append(k)

        # رايات حرجة
        if any(soft_contains(text, c) for c in CRITICAL_SYM):
            sc *= 1.15

        if sc>0:
            sc *= dur_boost
            out.append({"name": dx, "score": round(sc,2), "hits": list(dict.fromkeys(hits))[:12]})

    out.sort(key=lambda x: x["score"], reverse=True)
    return out[:3]

def pick_top(cands: list[dict], min_score: float = 2.2):
    if not cands: return None
    return cands[0] if cands[0]["score"] >= min_score else None

# ============================== واجهة HTML ==============================
PAGE = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>DSM | دراسة حالة وتشخيص</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400}
    *{box-sizing:border-box}
    body{font-family:"Tajawal",system-ui;background:linear-gradient(135deg,var(--bg1),var(--bg2));color:#fff;margin:0}
    .wrap{max-width:1180px;margin:26px auto;padding:16px}
    .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px}
    label{display:block;color:#ffe28a;margin:6px 2px}
    input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:11px}
    textarea{min-height:120px;resize:vertical}
    .btn{background:var(--gold);color:#2b1b02;border:none;padding:12px 16px;border-radius:12px;font-weight:800;cursor:pointer;text-decoration:none;display:inline-block}
    .grid{display:grid;grid-template-columns:1.1fr .9fr;gap:14px}
    @media(max-width:1000px){.grid{grid-template-columns:1fr}}
    .badge{display:inline-block;padding:4px 10px;border-radius:999px}
    .ok{background:#16a34a}.warn{background:#ef4444}.mid{background:#f59e0b}
    table{width:100%;border-collapse:collapse;margin-top:8px}
    th,td{border-bottom:1px solid rgba(255,255,255,.15);padding:8px;text-align:right}
    th{color:#ffe28a}
    ul{margin:0 0 0 1rem}
  </style>
</head>
<body>
  <div class="wrap">
    <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px">
      <h2 style="margin:0">🗂️ دراسة حالة + تشخيص (DSM)</h2>
      <a class="btn" href="/">الواجهة</a>
    </div>
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

          <label>الأعراض (حرّ/عامي)</label>
          <textarea name="symptoms" placeholder="اكتب الأعراض بحرّية: حزن، ما استمتع، قلة نوم، وسواس + طقوس، نوبة هلع...">{{symptoms}}</textarea>

          <label>أو اختر يدويًا (اختياري)</label>
          <select name="picked">
            <option value="">— بدون اختيار —</option>
            {% for k in options %}
              <option value="{{k}}" {{'selected' if picked==k else ''}}>{{k}}</option>
            {% endfor %}
          </select>

          <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap">
            <button class="btn" type="submit">إصدار تشخيص</button>
          </div>
        </form>
      </section>

      <aside class="card">
        {% if picked %}
          <div><span class="badge ok">اختيار يدوي</span></div>
          <h3 style="margin:.4rem 0 0">{{picked}}</h3>
          <p>الأعراض النموذجية:</p>
          <ul>
            {% for s in DSM_DATA[picked] %}
              <li>{{s}}</li>
            {% endfor %}
          </ul>
          <p style="opacity:.8;margin-top:8px">⚠️ يلزم تقييم سريري للتأكيد.</p>
        {% elif best %}
          <div><span class="badge ok">التشخيص المرجّح</span></div>
          <h3 style="margin:.4rem 0 0">{{best.name}}</h3>
          <div style="opacity:.85">الدرجة: {{best.score}}</div>
          <table>
            <thead><tr><th>مطابقات</th></tr></thead>
            <tbody>
              {% for h in best.hits %}
                <tr><td>{{h}}</td></tr>
              {% endfor %}
            </tbody>
          </table>

          {% if top3 and top3|length>1 %}
          <div style="margin-top:10px">
            <span class="badge mid">مراجعة سريعة (أقرب 3)</span>
            <ul>
              {% for c in top3 %}
                {% if c.name != best.name %}
                  <li><b>{{c.name}}</b> — {{c.score}}</li>
                {% endif %}
              {% endfor %}
            </ul>
          </div>
          {% endif %}
          <p style="opacity:.8;margin-top:8px">⚠️ نتيجة تقديرية للمساعدة ولا تُغني عن التقييم السريري.</p>
        {% else %}
          <div><span class="badge warn">لا تشخيص مؤكد بعد</span></div>
          <p>اكتب مفردات أدق (مثال: <b>هلوسة/أوهام/نوبة هلع/وسواس+طقوس/نهم+تطهير/انقطاع نفس</b>) واذكر المدة.</p>
        {% endif %}
      </aside>
    </div>
  </div>
</body>
</html>
"""

# ============================== المسار الرئيسي ==============================
@dsm_bp.route("/", methods=["GET","POST"])
def dsm_home():
    form = request.form if request.method=="POST" else {}
    name     = (form.get("name") or "").strip()
    age      = (form.get("age") or "").strip()
    gender   = (form.get("gender") or "").strip()
    duration = (form.get("duration") or "").strip()
    symptoms = (form.get("symptoms") or "").strip()
    picked   = (form.get("picked") or "").strip()

    best = None
    top3 = []
    if not picked and request.method=="POST":
        try:
            d = int(float(duration)) if duration else 0
        except:
            d = 0
        cands = score_diagnoses(symptoms, d)
        if cands:
            top3 = [type("C",(object,),c)() for c in cands]
            b = cands[0]
            if pick_top(cands):
                best = type("B",(object,),b)()

    return render_template_string(
        PAGE,
        name=name, age=age, gender=gender, duration=duration, symptoms=symptoms, picked=picked,
        best=best, top3=top3, options=sorted(DSM_DATA.keys()), DSM_DATA=DSM_DATA
    )
