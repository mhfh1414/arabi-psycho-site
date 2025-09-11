# -*- coding: utf-8 -*-
# cbt_suite.py — لوحة CBT متكاملة: اختبارات (PHQ-9, GAD-7, PCL-5, DASS-21)
# + أدوات علاجية (سجل الأفكار، التنشيط السلوكي، التعرض) + خطة جلسات

from __future__ import annotations
from flask import Blueprint, render_template_string, request, redirect, url_for
from datetime import datetime

cbt_bp = Blueprint("cbt", __name__, url_prefix="/cbt")

# ============================== أدوات عامة ==============================
def now_year():
    try:
        return datetime.now().year
    except Exception:
        return 2025

def _val_int(v, default=0):
    try:
        return int(v)
    except Exception:
        return default

# ============================== القالب العام ==============================
BASE = """
<!doctype html><html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{{title}}</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400;--w:#fff}
*{box-sizing:border-box}
body{margin:0;font-family:"Tajawal",system-ui;background:linear-gradient(135deg,var(--bg1),var(--bg2)) fixed;color:var(--w)}
.wrap{max-width:1180px;margin:24px auto;padding:16px}
.bar{display:flex;justify-content:space-between;gap:10px;align-items:center}
a.btn,button.btn{display:inline-block;background:linear-gradient(180deg,#ffd86a,#f4b400);color:#2b1b02;border-radius:14px;padding:10px 14px;text-decoration:none;font-weight:800;border:none;cursor:pointer}
.card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:18px;margin:10px 0}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
@media(max-width:980px){.grid{grid-template-columns:1fr}}
label{display:block;margin:6px 0 4px;color:#ffe28a}
input[type=text],textarea,select{width:100%;background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.25);border-radius:12px;padding:10px}
textarea{min-height:120px;resize:vertical}
small{opacity:.85}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:2px 0}
.ok{background:#16a34a}.warn{background:#ef4444}.mid{background:#f59e0b}.info{background:#0284c7}
table{width:100%;border-collapse:collapse}
th,td{border-bottom:1px solid rgba(255,255,255,.18);padding:8px;text-align:right}
th{color:#ffe28a}
</style>
</head>
<body>
<div class="wrap">
  <div class="bar">
    <h2 style="margin:0">{{heading}}</h2>
    <div>
      <a class="btn" href="/">الواجهة</a>
      <a class="btn" href="{{ url_for('cbt.dashboard') }}">لوحة CBT</a>
    </div>
  </div>
  {{ body|safe }}
  <p style="opacity:.7;margin-top:18px">© {{year}} عربي سايكو — العلاج السلوكي المعرفي</p>
</div>
</body></html>
"""

# ============================== لوحة CBT ==============================
@cbt_bp.route("/")
def dashboard():
    body = """
    <div class="card">
      <p>لوحة متكاملة تشمل اختبارات قياسية + أدوات CBT عملية + توليد خطة جلسات أولية.</p>
    </div>
    <div class="grid">
      <div class="card">
        <h3>🧪 اختبارات القياس</h3>
        <ul>
          <li><a class="btn" href="{{ url_for('cbt.phq9') }}">PHQ-9 — الاكتئاب</a></li>
          <li><a class="btn" href="{{ url_for('cbt.gad7') }}">GAD-7 — القلق العام</a></li>
          <li><a class="btn" href="{{ url_for('cbt.pcl5') }}">PCL-5 — ما بعد الصدمة</a></li>
          <li><a class="btn" href="{{ url_for('cbt.dass21') }}">DASS-21 — اكتئاب/قلق/توتر</a></li>
        </ul>
      </div>
      <div class="card">
        <h3>💡 أدوات CBT</h3>
        <ul>
          <li><a class="btn" href="{{ url_for('cbt.thought_record') }}">سجل الأفكار (REBT/CBT)</a></li>
          <li><a class="btn" href="{{ url_for('cbt.behavioral_activation') }}">التنشيط السلوكي (BA)</a></li>
          <li><a class="btn" href="{{ url_for('cbt.exposures') }}">سلم التعرض (ERP)</a></li>
          <li><a class="btn" href="{{ url_for('cbt.session_plan') }}">توليد خطة جلسات</a></li>
        </ul>
      </div>
    </div>
    <div class="card">
      <h3>روابط سريعة</h3>
      <div style="display:flex;flex-wrap:wrap;gap:10px">
        <a class="btn" href="/dsm">دراسة الحالة + DSM</a>
        <a class="btn" href="{{ url_for('cbt.phq9') }}">PHQ-9</a>
        <a class="btn" href="{{ url_for('cbt.gad7') }}">GAD-7</a>
        <a class="btn" href="{{ url_for('cbt.pcl5') }}">PCL-5</a>
        <a class="btn" href="{{ url_for('cbt.dass21') }}">DASS-21</a>
      </div>
    </div>
    """
    return render_template_string(BASE, title="CBT | لوحة", heading="لوحة CBT المتكاملة", body=body, year=now_year())

# ============================== PHQ-9 ==============================
PHQ9_Q = [
"قلة الاهتمام أو المتعة بالقيام بالأشياء",
"الشعور بالاكتئاب أو اليأس",
"صعوبة النوم أو فرط النوم",
"الإرهاق أو قلة الطاقة",
"قلة الشهية أو فرط الأكل",
"الشعور بالسوء تجاه نفسك أو أنك فاشل",
"صعوبة التركيز (قراءة/مشاهدة)",
"الحركة أو الكلام ببطء شديد أو العكس (توتر)",
"أفكار بأنك تود إيذاء نفسك أو الموت"
]
PHQ_OPTS = [("0","أبدًا"),("1","عدة أيام"),("2","أكثر من نصف الأيام"),("3","تقريبًا كل يوم")]

def phq9_level(score:int)->str:
    if score<=4: return "خفيف جدًا"
    if score<=9: return "خفيف"
    if score<=14: return "متوسط"
    if score<=19: return "متوسط-شديد"
    return "شديد"

@cbt_bp.route("/phq9", methods=["GET","POST"])
def phq9():
    total,html_result = 0,""
    if request.method=="POST":
        total = sum(_val_int(request.form.get(f"q{i}",0)) for i in range(1,10))
        level = phq9_level(total)
        note = "يفضّل متابعة تقييم سريري إن كانت الشدة متوسطة فأعلى."
        html_result = f"""
        <div class="card">
          <h3>النتيجة</h3>
          <p>المجموع: <strong>{total}</strong> — الشدة:
            <span class="badge {'warn' if total>=15 else 'mid' if total>=10 else 'ok'}">{level}</span></p>
          <small>{note}</small>
        </div>"""
    qs = "".join(f"""
      <div class="card">
        <label>({i}) {PHQ9_Q[i-1]}</label>
        <select name="q{i}">{"".join([f'<option value="{v}">{t}</option>' for v,t in PHQ_OPTS])}</select>
      </div>""" for i in range(1,10))
    body = f"""
    <form method="post">
      {qs}
      <button class="btn" type="submit">حساب PHQ-9</button>
    </form>
    {html_result}
    """
    return render_template_string(BASE, title="PHQ-9", heading="PHQ-9 — مقياس الاكتئاب", body=body, year=now_year())

# ============================== GAD-7 ==============================
GAD7_Q = [
"الشعور بالتوتر أو القلق أو على الأعصاب",
"عدم القدرة على التوقف عن القلق أو التحكم به",
"القلق المفرط حول مختلف الأمور",
"صعوبة الاسترخاء",
"التململ أو عدم القدرة على الجلوس بهدوء",
"سهولة الانزعاج أو التهيج",
"الشعور بالخوف كأن شيئًا فظيعًا سيحدث"
]
def gad7_level(s:int)->str:
    if s<=4: return "خفيف"
    if s<=9: return "متوسط"
    if s<=14:return "متوسط-شديد"
    return "شديد"

@cbt_bp.route("/gad7", methods=["GET","POST"])
def gad7():
    total,html_result = 0,""
    if request.method=="POST":
        total = sum(_val_int(request.form.get(f"q{i}",0)) for i in range(1,8))
        level = gad7_level(total)
        html_result = f"""
        <div class="card">
          <h3>النتيجة</h3>
          <p>المجموع: <strong>{total}</strong> — الشدة:
            <span class="badge {'warn' if total>=15 else 'mid' if total>=10 else 'ok'}">{level}</span></p>
        </div>"""
    qs = "".join(f"""
      <div class="card">
        <label>({i}) {GAD7_Q[i-1]}</label>
        <select name="q{i}">{"".join([f'<option value="{v}">{t}</option>' for v,t in PHQ_OPTS])}</select>
      </div>""" for i in range(1,8))
    body = f"""
    <form method="post">
      {qs}
      <button class="btn" type="submit">حساب GAD-7</button>
    </form>
    {html_result}
    """
    return render_template_string(BASE, title="GAD-7", heading="GAD-7 — مقياس القلق العام", body=body, year=now_year())

# ============================== PCL-5 (PTSD) ==============================
PCL5_Q = [
"ذكريات اقتحامية مزعجة حول الحدث الصادم",
"أحلام/كوابيس مزعجة تتعلق بالحدث",
"تصرفات أو شعور وكأن الحدث يتكرر (فلاش باك)",
"انزعاج شديد عند التعرّض لمذكّرات الحدث",
"تفاعل جسدي قوي عند التعرّض للمذكرات",
"تجنّب الذكريات أو الأفكار أو المشاعر المتعلقة بالحدث",
"تجنّب التذكيرات الخارجية (أماكن/أشخاص/أنشطة)",
"صعوبة تذكر جوانب مهمة من الحدث",
"معتقدات سلبية مستمرّة عن الذات/الآخرين/العالم",
"لوم الذات أو الآخرين بشكل مفرط",
"حالة عاطفية سلبية مستمرّة (خوف/غضب/ذنب/عار)",
"انعدام الاهتمام/الابتعاد عن الأنشطة",
"الابتعاد عن الآخرين",
"صعوبة الشعور بالمشاعر الإيجابية",
"تهيج/نوبات غضب",
"سلوك متهور أو مدمّر للذات",
"فرط اليقظة",
"مشاكل التركيز",
"صعوبة النوم"
]
PCL_OPTS = [("0","أبدًا"),("1","قليلًا"),("2","متوسط"),("3","كثيرًا"),("4","شديد جدًا")]

def pcl5_flag(total:int)->str:
    if total>=33: return "مؤشرات قوية لاحتمال PTSD — يلزم تقييم سريري"
    if total>=20: return "أعراض ملحوظة تحتاج متابعة"
    return "منخفض"

@cbt_bp.route("/pcl5", methods=["GET","POST"])
def pcl5():
    total,html_result = 0,""
    if request.method=="POST":
        total = sum(_val_int(request.form.get(f"q{i}",0)) for i in range(1,20))
        flag = pcl5_flag(total)
        html_result = f"""
        <div class="card">
          <h3>النتيجة</h3>
          <p>المجموع: <strong>{total}</strong> — إشارة:
            <span class="badge {'warn' if total>=33 else 'mid' if total>=20 else 'ok'}">{flag}</span></p>
        </div>"""
    qs = "".join(f"""
      <div class="card">
        <label>({i}) {PCL5_Q[i-1]}</label>
        <select name="q{i}">{"".join([f'<option value="{v}">{t}</option>' for v,t in PCL_OPTS])}</select>
      </div>""" for i in range(1,20))
    body = f"""
    <form method="post">
      {qs}
      <button class="btn" type="submit">حساب PCL-5</button>
    </form>
    {html_result}
    """
    return render_template_string(BASE, title="PCL-5", heading="PCL-5 — مقياس ما بعد الصدمة", body=body, year=now_year())

# ============================== DASS-21 ==============================
DASS_Q = [
"أجد صعوبة في تهدئة نفسي", "أشعر بجفاف في الفم", "لا أرى أي متعة في الأشياء",
"أعاني صعوبة في التنفس دون مجهود", "أجد صعوبة في المبادرة بالأشياء",
"أبالغ في ردود فعلي على المواقف", "أشعر بالارتجاف", "أستخدم الكثير من الطاقة العصبية",
"لا أستطيع تحمّل أي شيء", "أشعر بانهيار عصبي على وشك الحدوث",
"غير قادر على الشعور بأي إيجابية", "أشعر بخوف بدون سبب وجيه",
"أشعر بالحزن والاكتئاب", "أفقد الصبر بسهولة", "أشعر بالذعر",
"لا أستمتع بأي شيء", "منزعج وصعب الاسترخاء", "أشعر بإحساس القلق",
"لا أيّ حماس لأي شيء", "أشعر كأني على حافة الانهيار", "لا معنى للحياة"
]
DASS_OPTS = [("0","لا ينطبق مطلقًا"),("1","ينطبق بعض الشيء"),("2","ينطبق كثيرًا"),("3","ينطبق جدًا")]
DASS_IDX_DEP = [3,5,11,13,16,19,21]
DASS_IDX_ANX = [2,4,7,12,15,18,20]
DASS_IDX_STR = [1,6,8,9,10,14,17]

def _sum_indices(vals, idxs): return sum(vals[i-1] for i in idxs)
def dass_level_dep(s):
    if s<10: return "طبيعي"
    if s<14: return "خفيف"
    if s<21: return "متوسط"
    if s<28: return "شديد"
    return "شديد جدًا"
def dass_level_anx(s):
    if s<8: return "طبيعي"
    if s<10: return "خفيف"
    if s<15: return "متوسط"
    if s<20: return "شديد"
    return "شديد جدًا"
def dass_level_str(s):
    if s<15: return "طبيعي"
    if s<19: return "خفيف"
    if s<26: return "متوسط"
    if s<34: return "شديد"
    return "شديد جدًا"

@cbt_bp.route("/dass21", methods=["GET","POST"])
def dass21():
    html_result = ""
    if request.method=="POST":
        vals = [_val_int(request.form.get(f"q{i}",0)) for i in range(1,22)]
        dep = _sum_indices(vals, DASS_IDX_DEP)*2
        anx = _sum_indices(vals, DASS_IDX_ANX)*2
        st  = _sum_indices(vals, DASS_IDX_STR)*2
        html_result = f"""
        <div class="card">
          <h3>النتيجة</h3>
          <table>
            <tr><th>اكتئاب</th><td>{dep}</td><td><span class="badge {'warn' if dep>=28 else 'mid' if dep>=14 else 'ok'}">{dass_level_dep(dep)}</span></td></tr>
            <tr><th>قلق</th><td>{anx}</td><td><span class="badge {'warn' if anx>=20 else 'mid' if anx>=10 else 'ok'}">{dass_level_anx(anx)}</span></td></tr>
            <tr><th>توتر</th><td>{st}</td><td><span class="badge {'warn' if st>=34 else 'mid' if st>=19 else 'ok'}">{dass_level_str(st)}</span></td></tr>
          </table>
        </div>
        """
    qs = "".join(f"""
      <div class="card">
        <label>({i}) {DASS_Q[i-1]}</label>
        <select name="q{i}">{"".join([f'<option value="{v}">{t}</option>' for v,t in DASS_OPTS])}</select>
      </div>""" for i in range(1,22))
    body = f"""
    <form method="post">
      {qs}
      <button class="btn" type="submit">حساب DASS-21</button>
    </form>
    {html_result}
    """
    return render_template_string(BASE, title="DASS-21", heading="DASS-21 — اكتئاب/قلق/توتر", body=body, year=now_year())

# ============================== سجل الأفكار ==============================
@cbt_bp.route("/thought-record", methods=["GET","POST"])
def thought_record():
    result = ""
    if request.method=="POST":
        situation = request.form.get("situation","").strip()
        thought   = request.form.get("thought","").strip()
        emotion   = request.form.get("emotion","").strip()
        belief    = _val_int(request.form.get("belief","0"))
        evidence_for = request.form.get("evidence_for","").strip()
        evidence_against = request.form.get("evidence_against","").strip()
        alt_thought = request.form.get("alt_thought","").strip()
        new_belief = _val_int(request.form.get("new_belief","0"))
        shift = belief - new_belief
        tag = "ok" if shift>=3 else "mid" if shift>=1 else "info"
        result = f"""
        <div class="card">
          <h3>النتيجة</h3>
          <p>انخفضت قناعة الفكرة من <strong>{belief}/10</strong> إلى <strong>{new_belief}/10</strong>
             — التحول: <span class="badge {tag}">{shift:+}</span></p>
          <table>
            <tr><th>الموقف</th><td>{situation}</td></tr>
            <tr><th>الفكرة التلقائية</th><td>{thought}</td></tr>
            <tr><th>المشاعر</th><td>{emotion}</td></tr>
            <tr><th>أدلة تأييد</th><td>{evidence_for}</td></tr>
            <tr><th>أدلة نفي</th><td>{evidence_against}</td></tr>
            <tr><th>الفكرة البديلة</th><td>{alt_thought}</td></tr>
          </table>
        </div>
        """
    body = f"""
    <div class="card">
      <form method="post">
        <label>الموقف</label><input type="text" name="situation" placeholder="أين/متى/مع من؟">
        <label>الفكرة التلقائية</label><input type="text" name="thought" placeholder="ما الذي خطر ببالك؟">
        <label>المشاعر</label><input type="text" name="emotion" placeholder="حزن، قلق، غضب …">
        <label>درجة القناعة (قبل) 0–10</label><input type="text" name="belief" value="7">
        <label>أدلة تأييد</label><textarea name="evidence_for"></textarea>
        <label>أدلة نفي</label><textarea name="evidence_against"></textarea>
        <label>الفكرة البديلة المتوازنة</label><textarea name="alt_thought"></textarea>
        <label>درجة القناعة (بعد) 0–10</label><input type="text" name="new_belief" value="4">
        <div style="margin-top:10px"><button class="btn">حفظ السجل</button></div>
      </form>
    </div>
    {result}
    """
    return render_template_string(BASE, title="سجل الأفكار", heading="سجل الأفكار (CBT/REBT)", body=body, year=now_year())

# ============================== التنشيط السلوكي (BA) ==============================
@cbt_bp.route("/ba", methods=["GET","POST"])
def behavioral_activation():
    result = ""
    if request.method=="POST":
        activities = request.form.get("activities","").strip()
        schedule   = request.form.get("schedule","").strip()
        barriers   = request.form.get("barriers","").strip()
        solutions  = request.form.get("solutions","").strip()
        result = f"""
        <div class="card">
          <h3>خطة تنشيط</h3>
          <table>
            <tr><th>أنشطة ممتعة/ذات معنى</th><td>{activities}</td></tr>
            <tr><th>جدولة أسبوعية</th><td>{schedule}</td></tr>
            <tr><th>عوائق</th><td>{barriers}</td></tr>
            <tr><th>حلول/خطوات صغيرة</th><td>{solutions}</td></tr>
          </table>
          <small>ابدأ بخطوات صغيرة قابلة للقياس والمتابعة.</small>
        </div>
        """
    body = f"""
    <div class="card">
      <form method="post">
        <label>أنشطة ممتعة/ذات معنى</label><textarea name="activities" placeholder="رياضة خفيفة، اتصال بصديق، هواية..."></textarea>
        <label>جدولة أسبوعية</label><textarea name="schedule" placeholder="السبت: مشي 20 دقيقة…"></textarea>
        <label>عوائق متوقعة</label><textarea name="barriers"></textarea>
        <label>حلول وخطوات صغيرة</label><textarea name="solutions"></textarea>
        <div style="margin-top:10px"><button class="btn">بناء خطة</button></div>
      </form>
    </div>
    {result}
    """
    return render_template_string(BASE, title="التنشيط السلوكي", heading="التنشيط السلوكي (BA)", body=body, year=now_year())

# ============================== التعرض التدريجي (ERP) ==============================
@cbt_bp.route("/exposures", methods=["GET","POST"])
def exposures():
    result = ""
    if request.method=="POST":
        items = [s.strip() for s in (request.form.get("ladder","") or "").split("\n") if s.strip()]
        ladder = "".join(f"<tr><td>{i+1}</td><td>{x}</td></tr>" for i,x in enumerate(items))
        result = f"""
        <div class="card">
          <h3>سُلّم التعرض</h3>
          <table><tr><th>#</th><th>مهمة التعرض</th></tr>{ladder}</table>
          <small>ابدأ من الأدنى قلقًا وتدرّج للأعلى مع منع سلوكيات الأمان/الطقوس.</small>
        </div>
        """
    body = f"""
    <div class="card">
      <form method="post">
        <label>اكتب سُلّم التعرض (عنصر في كل سطر، من الأسهل للأصعب)</label>
        <textarea name="ladder" placeholder="مثال:\nالسلام على جار أعرفه\nالتحدث دقيقتين في اجتماع صغير\nعرض قصير أمام الفريق\nكلمة أمام جمهور"></textarea>
        <div style="margin-top:10px"><button class="btn">بناء السُلّم</button></div>
      </form>
    </div>
    {result}
    """
    return render_template_string(BASE, title="التعرض التدريجي", heading="التعرض التدريجي (ERP)", body=body, year=now_year())

# ============================== خطة جلسات آلية ==============================
@cbt_bp.route("/plan", methods=["GET","POST"])
def session_plan():
    result = ""
    if request.method=="POST":
        main_problem = request.form.get("main_problem","").strip()
        goals        = request.form.get("goals","").strip()
        metrics      = request.form.get("metrics","").strip()
        modules      = []
        if request.form.get("use_depression"): modules.append("اكتئاب/BA + سجل أفكار")
        if request.form.get("use_anxiety"):    modules.append("قلق/تعرض + مهارات تنفس/يقظة")
        if request.form.get("use_trauma"):     modules.append("صدمة/تنظيم + معالجة تدريجية")
        schedule = """
        <ol>
          <li><strong>جلسة 1:</strong> بناء علاقة + صياغة حالة + أهداف + قياس أساسي (PHQ-9/GAD-7).</li>
          <li><strong>جلسة 2:</strong> تثقيف نفسي + مهارات تنظيم (تنفّس/يقظة) + واجب منزلي.</li>
          <li><strong>جلسة 3:</strong> سجل أفكار (تحديد تشوهات) + تجربة سلوكية صغيرة.</li>
          <li><strong>جلسة 4:</strong> تنشيط سلوكي/تعرّض تدريجي حسب الحالة.</li>
          <li><strong>جلسة 5:</strong> مراجعة التقدّم + تعديل خطة + قياسات متابعة.</li>
          <li><strong>جلسة 6:</strong> تثبيت مكاسب + خطة انتكاسة + ختام أولي.</li>
        </ol>
        """
        result = f"""
        <div class="card">
          <h3>خطة جلسات مبدئية (6 جلسات)</h3>
          <table>
            <tr><th>المشكلة الرئيسية</th><td>{main_problem}</td></tr>
            <tr><th>الأهداف</th><td>{goals}</td></tr>
            <tr><th>مؤشرات النجاح</th><td>{metrics}</td></tr>
            <tr><th>الوحدات المقترحة</th><td>{'، '.join(modules) if modules else 'تُحدّد بعد القياس'}</td></tr>
          </table>
          {schedule}
          <small>الخطة توجيهية وتتعدل حسب التقييم والمتابعة.</small>
        </div>
        """
    body = f"""
    <div class="card">
      <form method="post">
        <label>المشكلة الرئيسية</label><input name="main_problem" placeholder="مثال: اكتئاب مع قلق اجتماعي">
        <label>الأهداف</label><textarea name="goals" placeholder="رفع النشاط، تحسين النوم، تخفيف القلق الاجتماعي..."></textarea>
        <label>مؤشرات النجاح</label><textarea name="metrics" placeholder="هبوط PHQ-9 تحت 9، حضور نشاطين أسبوعيًا..."></textarea>
        <div class="grid">
          <label><input type="checkbox" name="use_depression"> وحدة اكتئاب (BA + أفكار)</label>
          <label><input type="checkbox" name="use_anxiety"> وحدة قلق (تعرض + تنظيم)</label>
          <label><input type="checkbox" name="use_trauma"> وحدة صدمة (تنظيم + معالجة تدريجية)</label>
        </div>
        <div style="margin-top:10px"><button class="btn">توليد الخطة</button></div>
      </form>
    </div>
    {result}
    """
    return render_template_string(BASE, title="خطة الجلسات", heading="توليد خطة جلسات (CBT)", body=body, year=now_year())

# ============================== روابط مختصرة آمنة (بدون تضارب) ==============================
@cbt_bp.route("/thought")
def thought_alias(): 
    return redirect(url_for("cbt.thought_record"))

@cbt_bp.route("/erp")
def erp_alias(): 
    return redirect(url_for("cbt.exposures"))
