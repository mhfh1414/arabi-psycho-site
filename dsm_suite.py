# -*- coding: utf-8 -*-
# dsm_suite.py — ملف واحد: دراسة حالة + DSM + تشخيص بالذكاء الاصطناعي (اختياري)

from flask import Blueprint, request, render_template_string, redirect
import os, re, json, requests

dsm_bp = Blueprint("dsm", __name__, url_prefix="/dsm")

# ================== أدوات لغوية ==================
_AR_DIAC  = r"[ًٌٍَُِّْـ]"
_AR_PUNCT = r"[.,،;؛!?؟()\[\]{}\"\'<>]"

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
    return len(t & p)/len(p)

# ================== مرادفات مختصرة ==================
SYNONYMS = {
    "حزن": ["كآبه","تعاسه","ضيقه","طفش","غم"],
    "انعدام المتعة": ["فقدان المتعه","لا استمتع","فقدان الاهتمام"],
    "طاقة منخفضة": ["خمول","كسل","ارهاق","تعب","وهن"],
    "اضطراب نوم": ["قلة نوم","كثرة نوم","ارق","نوم متقطع","استيقاظ مبكر"],
    "شهية منخفضة": ["قلة اكل","سدت نفسي","فقدان شهية"],
    "انسحاب اجتماعي": ["انعزال","انطواء","تجنب اجتماعي"],
    "تفكير انتحاري": ["افكار انتحار","تمني الموت"],
    "قلق": ["توتر","توجس","خوف مستمر"],
    "نوبة هلع": ["خفقان","اختناق","ضيق نفس","رجفه","تعرق","دوخه"],
    "وسواس": ["افكار متسلطه","اقتحاميه","هواجس"],
    "سلوك قهري": ["طقوس","تفقد متكرر","عد قهري","غسل متكرر"],
    "هلوسة": ["اسمع اصوات","هلاوس سمعيه/بصريه"],
    "اوهام": ["ضلالات","اضطهاد","عظمه"],
}

# ================== قاعدة DSM مختصرة وعملية ==================
DSM_DB = {
    "اضطراب اكتئابي جسيم": {
        "keywords": ["حزن","مزاج منخفض","انعدام المتعة","بكاء","انسحاب اجتماعي",
                     "طاقة منخفضة","ارهاق","بطء نفسي حركي",
                     "اضطراب نوم","ارق","نوم متقطع","استيقاظ مبكر","كثرة نوم",
                     "شهية منخفضة","فقدان وزن","زيادة وزن",
                     "تركيز ضعيف","شعور بالذنب","يأس","تفكير انتحاري"],
        "required": ["حزن","انعدام المتعة"], "weight": 1.85
    },
    "اضطراب القلق العام": {
        "keywords": ["قلق","قلق مفرط","توتر","توجس","افكار سلبية","شد عضلي",
                     "صعوبة تركيز","قابلية استفزاز","ارق","تعب"],
        "required": ["قلق مفرط"], "weight": 1.45
    },
    "اضطراب الهلع": {
        "keywords": ["نوبة هلع","خفقان","اختناق","ضيق نفس","تعرق","رجفه","دوار","خوف الموت","خدر","غثيان"],
        "required": ["نوبة هلع"], "weight": 1.6
    },
    "اضطراب الوسواس القهري": {
        "keywords": ["وسواس","افكار اقتحاميه","سلوك قهري","طقوس","تفقد متكرر","غسل متكرر","تنظيم مفرط","عد قهري","خوف تلوث"],
        "required": ["وسواس","سلوك قهري"], "weight": 1.7
    },
    "فصام": {
        "keywords": ["هلوسة","اوهام","تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني","انعدام اراده"],
        "required": ["هلوسة","اوهام"], "weight": 1.8
    },
    "رهاب اجتماعي": {
        "keywords": ["خوف اجتماعي","خوف التقييم","خجل شديد","تجنب اجتماعي","قلق اداء","احمرار"],
        "required": ["خوف اجتماعي"], "weight": 1.4
    },
    "قهم عصبي": {
        "keywords": ["نقص وزن شديد","خوف من زياده الوزن","صورة جسد سلبيه","تقييد طعام"],
        "required": ["نقص وزن شديد","خوف من زياده الوزن"], "weight": 1.7
    },
    "أرق مزمن": {
        "keywords": ["صعوبه نوم","استيقاظ مبكر","نوم متقطع","عدم راحه","اجهاد نهاري"],
        "required": ["صعوبه نوم"], "weight": 1.4
    },
}

def _prep(db):
    out={}
    for name,m in db.items():
        out[name]={
            "req":[normalize(x) for x in m.get("required",[])],
            "kwn":[normalize(x) for x in m["keywords"]],
            "kwr":m["keywords"],
            "w":float(m.get("weight",1.0)),
        }
    return out

DSM = _prep(DSM_DB)

# ================== محرك الدرجات ==================
def score(symptoms: str, duration_days: str="", history: str=""):
    text = normalize(symptoms or "")
    # تعزيز مرادفات
    for base, syns in SYNONYMS.items():
        if any(normalize(w) in text for w in [base] + syns):
            text += " " + " ".join(set(normalize(s) for s in ([base] + syns)))

    try: dur = float(duration_days)
    except: dur = 0.0
    durB = 1.25 if dur>=365 else 1.15 if dur>=90 else 1.08 if dur>=30 else 1.0

    histB = 1.0
    h = normalize(history or "")
    if any(k in h for k in ["مشاكل","طلاق","تعثر","غياب","قضيه","اضطراب عمل","تدني دراسي"]):
        histB = 1.1

    out=[]
    for dx, meta in DSM.items():
        req=meta["req"]
        if req and not all((r in text) or (similarity(text, r)>=0.6) for r in req):
            continue
        sc=0.0; hits=[]
        for raw_kw, kw in zip(meta["kwr"], meta["kwn"]):
            if kw in text:
                w=1.0
                if kw in [normalize("تفكير انتحاري"), normalize("نوبة هلع"), normalize("هلوسة"), normalize("اوهام")]:
                    w=1.8
                sc+=w; hits.append(raw_kw)
            else:
                sim=similarity(text, kw)
                if sim>=0.66: sc+=0.8; hits.append(raw_kw+"~")
                elif sim>=0.4: sc+=0.4
        if sc==0: continue
        sc*=meta["w"]; sc*=durB; sc*=histB
        out.append({"name":dx,"score":round(sc,2),"hits":hits[:12]})
    out.sort(key=lambda x:x["score"], reverse=True)
    return out[:5]

# ================== واجهات HTML ==================
SHELL = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"/>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<title>DSM | دراسة حالة وتشخيص</title>
<style>
:root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400}
*{box-sizing:border-box}body{margin:0;font-family:Tajawal,system-ui;background:linear-gradient(135deg,var(--bg1),var(--bg2)) fixed;color:#fff}
.wrap{max-width:1180px;margin:22px auto;padding:16px}
.card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px}
a.btn,button.btn{display:inline-block;background:var(--gold);color:#2b1b02;border-radius:14px;padding:10px 14px;text-decoration:none;font-weight:800;border:none;cursor:pointer}
label{display:block;color:#ffe28a;margin:8px 2px 6px}
input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:10px 12px}
textarea{min-height:130px;resize:vertical}
.grid{display:grid;grid-template-columns:1.1fr .9fr;gap:16px} @media(max-width:992px){.grid{grid-template-columns:1fr}}
.result{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:4px 0}
.ok{background:#16a34a}.warn{background:#ef4444}
table{width:100%;border-collapse:collapse;margin-top:8px}th,td{border-bottom:1px solid rgba(255,255,255,.15);padding:8px 6px;text-align:right}th{color:#ffe28a}
.bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
</style></head><body><div class="wrap"><div class="bar"><h2 style="margin:0">🗂️ دراسة حالة + تشخيص</h2><a class="btn" href="/">الواجهة</a></div>{BODY}</div></body></html>
"""

def page_form():
    body = """
    <div class="grid">
      <section class="card">
        <form method="post" action="/dsm">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label>الاسم</label><input name="name"></div>
            <div><label>العمر</label><input name="age" placeholder="مثال: 27"></div>
            <div><label>الجنس</label>
              <select name="gender"><option value="">— اختر —</option><option>ذكر</option><option>أنثى</option></select>
            </div>
            <div><label>مدة الأعراض (بالأيام)</label><input name="duration" placeholder="90"></div>
          </div>
          <label>الأعراض (اكتب بدقة + كلمات عامية)</label>
          <textarea name="symptoms" placeholder="حزن شديد، خمول، قلة نوم، فقدان شهية، انسحاب عن الناس…"></textarea>
          <label>التاريخ الطبي/الأثر الوظيفي</label>
          <textarea name="history" placeholder="أدوية، جلسات، مشاكل عمل/دراسة أو علاقات…"></textarea>
          <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px">
            <button class="btn" type="submit">تشخيص مبدئي</button>
            <button class="btn" formaction="/dsm/ai" formmethod="post" title="يستخدم الذكاء الاصطناعي إن توفّر المفتاح">تشخيص بالذكاء الاصطناعي (تجريبي)</button>
          </div>
        </form>
      </section>
      <aside class="result"><span class="badge warn">لا توجد نتيجة بعد</span><p>املأ الأعراض ثم اختر نوع التشخيص.</p></aside>
    </div>
    """
    return SHELL.replace("{BODY}", body)

def page_result(form, details, ai=None):
    name     = (form.get("name","") or "")
    age      = (form.get("age","") or "")
    gender   = (form.get("gender","") or "")
    duration = (form.get("duration","") or "")
    symptoms = (form.get("symptoms","") or "")
    history  = (form.get("history","") or "")

    if not details:
        res_html = """
        <div class="result"><h3>📋 النتيجة</h3>
          <p><span class="badge warn">لا تطابقات كافية</span> — زِد مفردات مثل: وسواس/نوبة هلع/هلوسة/رهاب/أرق…</p>
        </div>"""
    else:
        rows = [f"<tr><td>{d['name']}</td><td>{d['score']}</td><td>{', '.join(d['hits'])}</td></tr>" for d in details]
        table = "<table><thead><tr><th>التشخيص المقترح</th><th>الدرجة</th><th>مطابقات</th></tr></thead><tbody>"+"".join(rows)+"</tbody></table>"
        res_html = f'<div class="result"><h3>📋 أقرب التشخيصات (أفضل 5)</h3>{table}<p style="opacity:.8">⚠️ نتيجة مساعدة وليست نهائية.</p></div>'

    ai_html = ""
    if ai:
        ai_html = f"""
        <div class="result" style="margin-top:10px">
          <h3>🤖 تشخيص الذكاء الاصطناعي (تجريبي)</h3>
          <p><b>التشخيص الأرجح:</b> {ai.get('primary','—')}</p>
          <p><b>الثقة:</b> {ai.get('confidence','—')}</p>
          <p><b>تفريق تشخيصي:</b> {', '.join(ai.get('differential',[]) or [])}</p>
          <p><b>عوامل خطورة:</b> {', '.join(ai.get('risk_flags',[]) or [])}</p>
          <p><b>مقترحات أولية:</b> {ai.get('plan','—')}</p>
        </div>
        """

    body = f"""
    <div class="grid">
      <section class="card">
        <form method="post" action="/dsm">
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
            <div><label>مدة الأعراض (بالأيام)</label><input name="duration" value="{duration}"></div>
          </div>
          <label>الأعراض</label><textarea name="symptoms">{symptoms}</textarea>
          <label>التاريخ الطبي/الأثر الوظيفي</label><textarea name="history">{history}</textarea>
          <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px">
            <button class="btn" type="submit">إعادة التشخيص</button>
            <button class="btn" formaction="/dsm/ai" formmethod="post">تشخيص بالذكاء الاصطناعي</button>
            <a class="btn" href="/">الواجهة</a>
          </div>
        </form>
      </section>
      {res_html}
      {ai_html}
    </div>
    """
    return SHELL.replace("{BODY}", body)

# ================== تكامل الذكاء الاصطناعي (اختياري) ==================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # ضع المفتاح في الإعدادات إن رغبت

AI_PROMPT = """أنت أخصائي نفسي. استقبل دراسة حالة مختصرة بالعربية ونتيجة مطابقة أولية من قاموس DSM.
حلّلها وأعد تشخيصاً منظماً بصيغة JSON بالمفاتيح:
primary (string), confidence (0-100), differential (list of 3-6), risk_flags (list), plan (string مختصر).

قواعد:
- اعتمد الأعراض والزمن والأثر الوظيفي.
- إن وُجدت أفكار انتحار/ذهان ضع تحذير في risk_flags.
- كن مختصراً ودقيقاً.

نص الحالة:
{case}

أفضل التطابقات القاموسية:
{rule_top}
"""

def llm_diagnose(case_text: str, rule_top: list):
    """يرجع dict أو None. يستخدم واجهة OpenAI عبر HTTP. لو ما فيه مفتاح يرجّع None."""
    if not OPENAI_API_KEY:
        return None
    try:
        top_str = "\n".join([f"- {d['name']} (score={d['score']})" for d in rule_top]) or "- لا يوجد"
        payload = {
            "model": "gpt-4o-mini",  # أي موديل متاح لحسابك
            "messages": [
                {"role":"system","content":"You are a careful Arabic-speaking clinical assistant."},
                {"role":"user","content": AI_PROMPT.format(case=case_text, rule_top=top_str)}
            ],
            "response_format": {"type":"json_object"},
            "temperature": 0.2,
        }
        res = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type":"application/json"},
            data=json.dumps(payload),
            timeout=30
        )
        res.raise_for_status()
        data = res.json()
        txt = data["choices"][0]["message"]["content"]
        return json.loads(txt)
    except Exception:
        return None

# ================== المسارات ==================
@dsm_bp.route("", methods=["GET","POST"])
def dsm_home():
    if request.method == "GET":
        return page_form()
    # POST — تشخيص قاعدي
    form = request.form
    details = score(form.get("symptoms",""), duration_days=form.get("duration",""), history=form.get("history",""))
    return page_result(form, details)

@dsm_bp.route("/ai", methods=["POST"])
def dsm_ai():
    """ينفّذ التشخيص القاعدي أولاً ثم يحاول AI؛ إن فشل يعرض القاعدي فقط."""
    form = request.form
    details = score(form.get("symptoms",""), duration_days=form.get("duration",""), history=form.get("history",""))
    # نبني نص حالة مرتب
    case_text = f"""الاسم: {form.get('name','—')}
العمر/الجنس: {form.get('age','—')} / {form.get('gender','—')}
المدة (يوم): {form.get('duration','—')}
الأعراض: {form.get('symptoms','—')}
التاريخ/الأثر: {form.get('history','—')}"""
    ai = llm_diagnose(case_text, details)
    return page_result(form, details, ai=ai)

# ============= تعليمات الدمج مع ملف التشغيل الرئيسي =============
# في site_app.py:
# from dsm_suite import dsm_bp
# app.register_blueprint(dsm_bp)
#
# لا يحتاج أي قوالب خارجية — كل HTML داخل هذا الملف.
# إن لم تضع OPENAI_API_KEY سيعمل التشخيص القاعدي فقط بدون أي أخطاء.
