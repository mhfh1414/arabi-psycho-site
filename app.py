# -*- coding: utf-8 -*-
# app.py — Arabi Psycho (v3.0 Stable, Full Version — Part 1 of 2)

import os, json, tempfile, urllib.parse
from datetime import datetime
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

# ===== إعدادات عامة =====
BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO  = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696?text=عربي%20سايكو")

# ===== عداد الزوّار =====
COUNTER_FILE = "visitors.json"

def _load_count():
    try:
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            return int(json.load(f).get("count", 0))
    except Exception:
        return 0

def _save_count(n: int):
    try:
        with open(COUNTER_FILE, "w", encoding="utf-8") as f:
            json.dump({"count": n}, f, ensure_ascii=False)
    except Exception:
        pass

def bump_visitors():
    n = _load_count() + 1
    _save_count(n)
    return n

CACHE_BUST = datetime.utcnow().strftime("%Y%m%d%H%M%S")

def shell(title, content, visitors=None):
    visitors_html = f"<div class='small'>👀 عدد الزوّار: <b>{visitors}</b></div>" if visitors else ""
    return f"""<!DOCTYPE html><html lang="ar" dir="rtl">
<head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<link rel="icon" href="{LOGO}"/>
<style>
body{{font-family:'Tajawal',sans-serif;background:#f8f6ff;color:#222;direction:rtl;margin:0}}
.layout{{display:grid;grid-template-columns:280px 1fr;min-height:100vh}}
.side{{background:linear-gradient(180deg,#4b0082,#3a0d72);color:#fff;padding:18px}}
.nav a{{display:block;color:#fff;text-decoration:none;margin:6px 0;padding:8px 10px;border-radius:10px}}
.nav a:hover{{background:rgba(255,255,255,.15)}}
.card{{background:#fff;padding:20px;border-radius:14px;margin-bottom:14px}}
.btn{{padding:10px 14px;border-radius:10px;color:#fff;background:#4b0082;text-decoration:none;cursor:pointer;display:inline-block}}
.btn.gold{{background:#FFD700;color:#4b0082;font-weight:800}}
.btn.alt{{background:#5b22a6}}
.btn.wa{{background:#25D366}}
.btn.tg{{background:#229ED9}}
.table{{width:100%;border-collapse:collapse}}
.table th,.table td{{border:1px solid #ddd;padding:6px;text-align:center}}
</style></head>
<body>
<div class="layout">
  <aside class="side">
    <h2>{BRAND}</h2>
    <nav class="nav">
      <a href="/">🏠 الرئيسية</a>
      <a href="/case">📝 دراسة الحالة</a>
      <a href="/dsm">📘 DSM</a>
      <a href="/cbt">🧠 CBT</a>
      <a href="/addiction">🚭 الإدمان</a>
      <a href="/book">📅 احجز موعد</a>
      <a href="/contact">📞 تواصل</a>
    </nav>
    {visitors_html}
  </aside>
  <main style="padding:20px">{content}</main>
</div></body></html>"""

# ===== الرئيسية =====
@app.get("/")
def home():
    v = bump_visitors()
    content = f"""
    <div class='card'><h1>مرحبًا بك في {BRAND}</h1>
    <p>مساحتك الهادئة لفهم الأعراض وبناء خطة علاجية آمنة.</p></div>
    <div class='card'><a href='/cbt' class='btn gold'>ابدأ برنامج CBT</a></div>"""
    return shell("الرئيسية", content, v)

# ===== DSM =====
DSM_HTML = """
<div class='card'><h1>📘 DSM</h1>
<ul>
<li>الاكتئاب: ≥5 أعراض لمدة أسبوعين مع تأثير وظيفي.</li>
<li>القلق المعمم: قلق زائد ≥6 أشهر مع توتر وأرق.</li>
<li>الوسواس القهري: وساوس وأفعال قهرية مؤثرة على الأداء.</li>
<li>PTSD: كوابيس واسترجاع وتجنّب.</li>
</ul></div>
"""

@app.get("/dsm")
def dsm():
    return shell("DSM", DSM_HTML, _load_count())

# ===== CBT =====
CBT_HTML = r"""
<div class='card'>
  <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
  <p>اختر خطة واحدة أو خطتين ومدة الجدول لإنشاء مهامك اليومية.</p>

  <label>الخطة A:<select id='planA'></select></label>
  <label>الخطة B (اختياري):<select id='planB'><option value=''>— بدون —</option></select></label>
  <label>مدة الجدول:<select id='daysSelect'>
    <option value='7'>7 أيام</option><option value='10'>10 أيام</option><option value='14'>14 يوم</option>
  </select></label>
  <button class='btn gold' onclick='buildChecklist()'>إنشاء الجدول</button>
  <button class='btn alt' onclick='window.print()'>🖨️ طباعة</button>

  <div id='checklist' style='margin-top:14px'></div>

  <script>
  const PLANS = {
    ba:{title:"BA — تنشيط سلوكي",steps:["3 نشاطات مجزية","قياس مزاج قبل/بعد","رفع الصعوبة تدريجيًا"]},
    tr:{title:"TR — سجل أفكار",steps:["موقف→فكرة","دلائل مع/ضد","بديل متوازن"]},
    sh:{title:"SH — نظافة النوم",steps:["مواعيد ثابتة","قطع الشاشات","لا كافيين بعد 6س"]},
    ps:{title:"PS — حل المشكلات",steps:["تعريف المشكلة","عصف أفكار","خطة عمل"]},
    rp:{title:"RP — منع الانتكاس",steps:["تحديد المثيرات","استبدال فوري","شبكة تواصل"]}
  };

  const a=document.getElementById('planA'), b=document.getElementById('planB');
  for(const k in PLANS){
    const o1=document.createElement('option');o1.value=k;o1.textContent=PLANS[k].title;a.appendChild(o1);
    const o2=document.createElement('option');o2.value=k;o2.textContent=PLANS[k].title;b.appendChild(o2);
  }

  function buildChecklist(){
    const A=a.value, B=b.value;
    const days=parseInt(document.getElementById('daysSelect').value)||7;
    const planA=PLANS[A], planB=B?PLANS[B]:null;
    if(!planA){document.getElementById('checklist').innerHTML='<p>اختر خطة أولاً.</p>';return;}
    const steps=[...planA.steps,...(planB?planB.steps:[])];
    let html=`<h3>${planA.title}${planB?(' + '+planB.title):''} — ${days} يوم</h3>`;
    html+="<table class='table'><thead><tr><th>اليوم</th>";
    steps.forEach(s=>html+=`<th>${s}</th>`); html+="</tr></thead><tbody>";
    for(let d=1;d<=days;d++){html+=`<tr><td>${d}</td>`;steps.forEach(()=>html+="<td><input type='checkbox'></td>");html+="</tr>";}
    html+="</tbody></table>";
    document.getElementById('checklist').innerHTML=html;
  }
  </script>
</div>
"""

@app.get("/cbt")
def cbt():
    return shell("CBT", CBT_HTML, _load_count())
        # ===== برنامج الإدمان =====
ADDICTION_HTML = """
<div class='card'>
  <h1>🚭 علاج الإدمان</h1>
  <ul>
    <li>التقييم الأولي: نوع المادة، الشدة، الفحوصات.</li>
    <li>Detox: سحب آمن بإشراف طبي.</li>
    <li>Rehab: جلسات CBT + مهارات الرفض.</li>
    <li>Aftercare: متابعة أسبوعية 3 أشهر.</li>
    <li>منع الانتكاس: تحديد المثيرات + خطة بدائل.</li>
  </ul>
  <a href='/case' class='btn gold'>اربط مع دراسة الحالة</a>
</div>
"""

@app.get("/addiction")
def addiction():
    return shell("علاج الإدمان", ADDICTION_HTML, _load_count())

# ===== نموذج الحجز =====
BOOK_FORM = """
<div class='card'>
  <h1>📅 احجز موعدك</h1>
  <form method='post' action='/book'>
    <label>الاسم:<input name='name' required></label><br>
    <label>العمر:<input name='age' type='number'></label><br>
    <label>النوع:
      <select name='type'>
        <option>الأخصائي النفسي</option>
        <option>الطبيب النفسي</option>
        <option>الأخصائي الاجتماعي</option>
      </select>
    </label><br>
    <label>وسيلة التواصل:<input name='channel' value='واتساب'></label><br>
    <label>الرقم:<input name='phone' required></label><br>
    <label>أفضل وقت:<input name='best_time'></label><br>
    <label>نبذة:<textarea name='summary'></textarea></label><br>
    <button class='btn gold' type='submit'>إرسال عبر واتساب</button>
  </form>
</div>
"""

@app.route("/book", methods=["GET","POST"])
def book():
    if request.method == "GET":
        return shell("احجز موعد", BOOK_FORM, _load_count())

    f = request.form
    msg = f"طلب جديد من {f.get('name','')} — نوع الجلسة: {f.get('type','')} — رقم: {f.get('phone','')}"
    encoded = urllib.parse.quote_plus(msg)
    wa = f"{WA_URL.split('?')[0]}?text={encoded}"
    return redirect(wa, code=302)

# ===== دراسة الحالة =====
CASE_FORM = """
<div class='card'>
  <h1>📝 دراسة الحالة</h1>
  <form method='post' action='/case'>
    <label><input type='checkbox' name='low_mood'> مزاج منخفض</label><br>
    <label><input type='checkbox' name='anhedonia'> فقد المتعة</label><br>
    <label><input type='checkbox' name='anxiety'> قلق وتوتر</label><br>
    <label><input type='checkbox' name='panic'> نوبات هلع</label><br>
    <label><input type='checkbox' name='ocd'> وساوس وأفعال قهرية</label><br>
    <label><input type='checkbox' name='substance'> استخدام مواد</label><br>
    <textarea name='notes' rows='3' placeholder='ملاحظاتك'></textarea><br>
    <button class='btn gold'>عرض النتيجة</button>
  </form>
</div>
"""

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell("دراسة الحالة", CASE_FORM, _load_count())

    data = request.form
    results = []

    if data.get("low_mood") and data.get("anhedonia"):
        results.append("احتمال اكتئاب — راجع خطة BA أو TR.")
    if data.get("anxiety"):
        results.append("قلق عام — جرب خطة WT أو MB.")
    if data.get("panic"):
        results.append("نوبات هلع — CBT (تعرض داخلي IE).")
    if data.get("ocd"):
        results.append("وسواس قهري — ERP مناسب.")
    if data.get("substance"):
        results.append("احتمال إدمان — اربط مع برنامج الإدمان.")

    notes = data.get("notes", "")
    if not results:
        results = ["لا توجد مؤشرات قوية."]

    html = "<div class='card'><h1>نتيجة الترشيح</h1><ul>"
    for r in results:
        html += f"<li>{r}</li>"
    html += "</ul>"
    if notes:
        html += f"<p><b>ملاحظات:</b> {notes}</p>"
    html += "<a class='btn gold' href='/cbt'>🧠 افتح CBT</a></div>"
    return shell("نتيجة دراسة الحالة", html, _load_count())

# ===== صفحة التواصل =====
CONTACT_HTML = f"""
<div class='card'>
  <h1>📞 تواصل معنا</h1>
  <a href='{TG_URL}' class='btn tg'>تيليجرام</a>
  <a href='{WA_URL}' class='btn wa'>واتساب</a>
</div>
"""

@app.get("/contact")
def contact():
    return shell("التواصل", CONTACT_HTML, _load_count())

# ===== الصحة & الأمان =====
@app.get("/health")
def health():
    return {"status": "ok", "brand": BRAND, "build": CACHE_BUST}, 200

@app.after_request
def add_headers(resp):
    csp = (
        "default-src 'self' data: blob: https://t.me https://wa.me; "
        "script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    )
    resp.headers['Content-Security-Policy'] = csp
    return resp

# ===== تشغيل السيرفر =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
    # ===== دراسة الحالة (موسّعة) ====        <h3>مواد</h3>
        <label class='chk'><input type='checkbox' name='craving'> اشتهاء</label>
        <label class='chk'><input type='checkbox' name='withdrawal'> انسحاب</label>
        <label class='chk'><input type='checkbox' name='use_harm'> استخدام رغم الضرر</label>
      </div>

    </div>

    <div class='tile' style='margin-top:12px'>
      <label>ملاحظاتك<textarea name='notes' rows='4' placeholder='أي تفاصيل إضافية مهمة لك'></textarea></label>
    </div>

    <div class='row'>
      <button class='btn gold' type='submit'>عرض الترشيحات</button>
      <a class='btn' href='/cbt'>🧠 فتح CBT</a>
    </div>
  </form>
</div>
"""
@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
            # ذهانية/طيف
    psych_count = sum(d.get(k, False) for k in ["hallucinations","delusions","disorganized_speech","negative_symptoms","catatonia"])
    if psych_count >= 2 and (d.get("duration_ge_6m") or (d.get("duration_ge_1m") and d.get("decline_function"))):
        results.append("فصام محتمل — احالة طبية + تثقيف أسري + SH.")
        cbt.update(["SH"])
    elif psych_count >= 2 and dep_total >= 3:
        results.append("فصامي وجداني محتمل — تقييم مختص.")
    elif psych_cou
         @app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell("دراسة الحالة", CASE_FORM, _load_count())

    d = {k: True for k in request.form.keys()}  # وجود المفتاح يكفي

    results = []
    cbt = set()
    add_prog = False

    # اكتئاب
    dep_core = sum(d.get(k, False) for k in ["low_mood","anhedonia"])
    dep_more = sum(d.get(k, False) for k in ["fatigue","sleep_issue","appetite_change","psychomotor","worthlessness","poor_concentration","suicidal"])
    dep_total = dep_core + dep_more
    if dep_total >= 5 and d.get("dep_2w"):
        results.append("نوبة اكتئاب — راجع BA + TR + SH + PS.")
        cbt.update(["BA","TR","SH","PS"])
    elif dep_total >= 3 and d.get("dep_2w"):
        results.append("اكتئاب خفيف/متوسط — BA + TR.")
        cbt.update(["BA","TR"])
    elif dep_core >= 1 and dep_total >= 2:
        results.append("كتلة أعراض مزاجية — BA وروتين يومي.")
        cbt.update(["BA"])

    if d.get("suicidal"):
        results.append("⚠️ تنبيه أمان: أفكار إيذاء/انتحار — يفضّل تواصل فوري مع مختص.")

    # قلق/هلع/اجتماعي/رُهاب
    if sum(d.get(k, False) for k in ["worry","tension","restlessness"]) >= 2:
        results.append("قلق معمّم — WT + MB + PS.")
        cbt.update(["WT","MB","PS"])
    if d.get("panic_attacks"):
        results.append("نوبات هلع — IE + إيقاف سلوكيات آمنة.")
        cbt.update(["IE","SA"])
    if d.get("social_fear") or d.get("phobia_specific"):
        results.append("قلق اجتماعي/رُهاب — تعرّض تدرّجي GE + مهارات SS + TR.")
        cbt.update(["GE","SS","TR"])

    # وسواس/صدمات
    if d.get("obsessions") and d.get("compulsions"):
        results.append("وسواس قهري — ERP + إيقاف سلوكيات آمنة.")
        cbt.update(["ERP","SA"])
    if sum(d.get(k, False) for k in ["flashbacks","hypervigilance","avoidance"]) >= 2:
        results.append("آثار صدمة — تمارين تأريض PTSD + يقظة MB.")
        cbt.update(["PTSD","MB"])

    # نوم/أكل/انتباه
    if d.get("insomnia") or d.get("hypersomnia"):
        cbt.add("SH")
    if d.get("binge_eating") or d.get("restrict_eating"):
        results.append("مخاوف الأكل — PS + MB (خطوات منظمة مع مختص).")
        cbt.update(["PS","MB"])
    if d.get("adhd_inattention") and d.get("adhd_hyper"):
        results.append("سمات ADHD مؤثرة — تنظيم وقت/مهام + PS.")
        cbt.add("PS")

    # مواد
    if sum(d.get(k, False) for k in ["craving","withdrawal","use_harm"]) >= 2:
        results.append("تعاطي مواد — برنامج الإدمان + RP + PS.")
        cbt.update(["RP","PS"])
        add_prog = True

    # ذهانية/طيف
    psych_count = sum(d.get(k, False) for k in ["hallucinations","delusions","disorganized_speech","negative_symptoms","catatonia"])
    if psych_count >= 2 and (d.get("duration_ge_6m") or (d.get("duration_ge_1m") and d.get("decline_function"))):
        results.append("فصام محتمل — احالة طبية + تثقيف أسري + SH.")
        cbt.update(["SH"])
    elif psych_count >= 2 and dep_total >= 3:
        results.append("فصامي وجداني محتمل — تقييم مختص.")
    elif psych_count >= 2 and d.get("duration_lt_1m"):
        results.append("اضطراب ذهاني وجيز — تقييم مختص.")
    elif d.get("delusions") and psych_count == 1 and d.get("duration_ge_1m") and not d.get("decline_function"):
        results.append("اضطراب وهامي — تقييم مختص.")

    if not results:
        results = ["لا توجد مؤشرات قوية."]

    # عرض النتيجة
    notes = (request.form.get("notes") or "").strip()
    html = "<div class='card'><h1>نتيجة دراسة الحالة</h1><ul>"
    for r in results:
        html += f"<li>{r}</li>"
    html += "</ul>"

    if cbt:
        html += "<h3>🔧 أدوات CBT المقترحة</h3><div>"
        for tag in sorted(cbt):
            html += f"<span class='badge2'>🔧 {tag}</span> "
        html += "</div>"

    if add_prog:
        html += "<p><span class='badge2'>🚭 برنامج الإدمان مُقترح</span></p>"

    if notes:
        html += f"<div class='tile' style='margin-top:10px'><b>ملاحظاتك:</b><br>{notes}</div>"

    html += "<div class='row' style='margin-top:12px'>"
    html += "<a class='btn' href='/cbt'>🧠 فتح CBT</a>"
    html += "<a class='btn gold' href='/book'>📅 حجز سريع</a>"
    html += "</div></div>"

    return shell("نتيجة دراسة الحالة", html, _load_count()) 
