# -*- coding: utf-8 -*-
# addiction/__init__.py — حزمة تقييم وعلاج الإدمان: فحص الشدة + انسحاب + خطة تدخل + إحالة

from __future__ import annotations
from flask import Blueprint, render_template_string, request, redirect, url_for
from datetime import datetime

addiction_bp = Blueprint("addiction", __name__, url_prefix="/addiction")

# ===== أدوات عامة بسيطة =====
def now_year():
    try: return datetime.now().year
    except: return 2025

def _i(v, d=0):
    try: return int(v)
    except: return d

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
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:2px 0}
.ok{background:#16a34a}.warn{background:#ef4444}.mid{background:#f59e0b}.info{background:#0284c7}
table{width:100%;border-collapse:collapse}
th,td{border-bottom:1px solid rgba(255,255,255,.18);padding:8px;text-align:right}
th{color:#ffe28a}
small{opacity:.84}
</style>
</head>
<body>
<div class="wrap">
  <div class="bar">
    <h2 style="margin:0">{{heading}}</h2>
    <div>
      <a class="btn" href="/">الواجهة</a>
      <a class="btn" href="{{ url_for('addiction.dashboard') }}">لوحة الإدمان</a>
    </div>
  </div>
  {{ body|safe }}
  <p style="opacity:.7;margin-top:18px">© {{year}} عربي سايكو — برامج علاج الإدمان</p>
</div>
</body></html>
"""

# ===== اللوحة الرئيسية =====
@addiction_bp.route("/")
def dashboard():
    body = """
    <div class="grid">
      <div class="card">
        <h3>🧪 فحص الشدة حسب المادة</h3>
        <p>اختر المادة وقيّم التكرار، الرغبة الملحّة، فقدان السيطرة، التأثير الوظيفي…</p>
        <a class="btn" href="{{ url_for('addiction.screen') }}">ابدأ الفحص</a>
      </div>
      <div class="card">
        <h3>⚕️ فحص أعراض الانسحاب</h3>
        <p>أعراض انسحاب شائعة (رجفة/تعَرّق/أرق/قلق…)</p>
        <a class="btn" href="{{ url_for('addiction.withdrawal') }}">فحص الانسحاب</a>
      </div>
      <div class="card">
        <h3>📝 خطة تدخل أولية</h3>
        <p>تثقيف + خفض ضرر + امتناع/تقليل + دعم/متابعة</p>
        <a class="btn" href="{{ url_for('addiction.plan') }}">ابنِ خطة</a>
      </div>
      <div class="card">
        <h3>📨 إحالة سريعة</h3>
        <p>نموذج إحالة لطبيب/مركز متخصص مع ملخص نقاط الخطر</p>
        <a class="btn" href="{{ url_for('addiction.referral') }}">إنشاء إحالة</a>
      </div>
    </div>
    """
    return render_template_string(BASE, title="علاج الإدمان | لوحة", heading="لوحة علاج الإدمان", body=body, year=now_year())

# ===== فحص الشدة =====
SUBSTANCES = [
    ("alcohol","كحول"), ("cannabis","قنب/حشيش"), ("stimulants","منبهات (أمفيتامين/كوكايين)"),
    ("opioids","أفيونات"), ("nicotine","نيكوتين/تدخين"), ("sedatives","مهدئات/بنزوديازبينات"), ("other","أخرى")
]
FREQ = [("0","أبدًا"),("1","مرة/أسبوع"),("2","2-3/أسبوع"),("3","4-6/أسبوع"),("4","يوميًا")]
YESNO = [("0","لا"),("1","نعم")]

def severity_label(total:int)->str:
    if total<=3: return "خفيف"
    if total<=7: return "متوسط"
    if total<=11: return "مرتفع"
    return "شديد"

@addiction_bp.route("/screen", methods=["GET","POST"])
def screen():
    result = ""
    if request.method=="POST":
        sub = request.form.get("sub","other")
        freq = _i(request.form.get("freq","0"))
        craving = _i(request.form.get("craving","0"))
        loss    = _i(request.form.get("loss","0"))
        time    = _i(request.form.get("time","0"))
        role    = _i(request.form.get("role","0"))
        risky   = _i(request.form.get("risky","0"))
        legal   = _i(request.form.get("legal","0"))
        health  = _i(request.form.get("health","0"))
        total = freq + craving + loss + time + role + risky + legal + health
        lvl = severity_label(total)
        tag = "warn" if total>=12 else "mid" if total>=8 else "ok"
        result = f"""
        <div class="card">
          <h3>النتيجة</h3>
          <table>
            <tr><th>المادة</th><td>{dict(SUBSTANCES).get(sub,'أخرى')}</td></tr>
            <tr><th>المجموع</th><td>{total}</td></tr>
            <tr><th>الشدّة</th><td><span class="badge {tag}">{lvl}</span></td></tr>
          </table>
          <small>دلالة فحصية أولية — تحتاج خطة علاجية ومتابعة.</small>
        </div>
        """
    opts_sub = "".join([f'<option value="{k}">{v}</option>' for k,v in SUBSTANCES])
    opts_freq = "".join([f'<option value="{v}">{t}</option>' for v,t in FREQ])
    opts_yesno = "".join([f'<option value="{v}">{t}</option>' for v,t in YESNO])
    body = f"""
    <form method="post">
      <div class="card">
        <label>المادة</label>
        <select name="sub">{opts_sub}</select>
      </div>
      <div class="grid">
        <div class="card"><label>التكرار</label><select name="freq">{opts_freq}</select></div>
        <div class="card"><label>رغبة ملحّة (Craving)</label><select name="craving">{opts_yesno}</select></div>
        <div class="card"><label>فقدان السيطرة</label><select name="loss">{opts_yesno}</select></div>
        <div class="card"><label>وقت طويل حول المادة</label><select name="time">{opts_yesno}</select></div>
        <div class="card"><label>تأثير على العمل/الدراسة/العلاقات</label><select name="role">{opts_yesno}</select></div>
        <div class="card"><label>استخدام في مواقف خطرة</label><select name="risky">{opts_yesno}</select></div>
        <div class="card"><label>مشاكل قانونية/مالية</label><select name="legal">{opts_yesno}</select></div>
        <div class="card"><label>مشاكل صحية مرتبطة</label><select name="health">{opts_yesno}</select></div>
      </div>
      <button class="btn">حساب الشدة</button>
    </form>
    {result}
    """
    return render_template_string(BASE, title="فحص الشدة", heading="فحص شدة التعاطي/الاعتمادية", body=body, year=now_year())

# ===== فحص الانسحاب =====
WITHDRAW_Q = [
    ("رجفة/ارتعاش","0-لا / 1-نعم"),
    ("تعرّق زائد","0-لا / 1-نعم"),
    ("أرق/مشاكل نوم","0-لا / 1-نعم"),
    ("قلق/تهيج شديد","0-لا / 1-نعم"),
    ("غثيان/قيء","0-لا / 1-نعم"),
    ("صداع/آلام جسدية","0-لا / 1-نعم"),
    ("تشنّجات/اختلاجات","0-لا / 1-نعم"),
    ("أفكار انتحارية/خطر أمان","0-لا / 1-نعم")
]

def withdrawal_flag(total:int)->str:
    if total>=5: return "انسحاب مرتفع الخطورة — يلزم إشراف طبي"
    if total>=2: return "انسحاب ملحوظ — راقب الأعراض واطلب دعمًا طبيًا"
    return "خفيف/غير واضح"

@addiction_bp.route("/withdrawal", methods=["GET","POST"])
def withdrawal():
    result = ""
    if request.method=="POST":
        vals = [_i(request.form.get(f"q{i}",0)) for i in range(1, len(WITHDRAW_Q)+1)]
        total = sum(vals)
        flag = withdrawal_flag(total)
        tag = "warn" if total>=5 else "mid" if total>=2 else "ok"
        rows = "".join([f"<tr><td>{WITHDRAW_Q[i-1][0]}</td><td>{vals[i-1]}</td></tr>" for i in range(1,len(WITHDRAW_Q)+1)])
        result = f"""
        <div class="card">
          <h3>نتيجة الانسحاب</h3>
          <p>المجموع: <strong>{total}</strong> — التقييم: <span class="badge {tag}">{flag}</span></p>
          <table><tr><th>العرض</th><th>0/1</th></tr>{rows}</table>
        </div>
        """
    qs = "".join(f"""
      <div class="card">
        <label>({i}) {q}</label>
        <select name="q{i}">
          <option value="0">0 — لا</option>
          <option value="1">1 — نعم</option>
        </select>
      </div>""" for i,(q,_) in enumerate(WITHDRAW_Q, start=1))
    body = f"""
    <form method="post">
      {qs}
      <button class="btn">تقييم الانسحاب</button>
    </form>
    {result}
    """
    return render_template_string(BASE, title="فحص الانسحاب", heading="فحص أعراض الانسحاب", body=body, year=now_year())

# ===== خطة تدخل أولية =====
@addiction_bp.route("/plan", methods=["GET","POST"])
def plan():
    result = ""
    if request.method=="POST":
        substance = request.form.get("sub","")
        goals     = request.form.get("goals","")
        harm      = request.form.get("harm","")
        supports  = request.form.get("supports","")
        followup  = request.form.get("followup","")
        result = f"""
        <div class="card">
          <h3>خطة تدخل مبدئية</h3>
          <table>
            <tr><th>المادة المستهدفة</th><td>{substance}</td></tr>
            <tr><th>أهداف العلاج</th><td>{goals}</td></tr>
            <tr><th>خفض الضرر</th><td>{harm}</td></tr>
            <tr><th>الدعم/البيئة</th><td>{supports}</td></tr>
            <tr><th>خطة المتابعة</th><td>{followup}</td></tr>
          </table>
          <ol>
            <li>تثقيف حول الآثار والمخاطر والانسحاب.</li>
            <li>اختيار مسار: امتناع كامل أو تقليل تدريجي بإشراف.</li>
            <li>دعم سلوكي: CBT للإدمان + إدارة رغبات + مهارات تأقلم.</li>
            <li>مراقبة طبية عند الحاجة (خاصة الكحول/الأفيونات/المهدئات).</li>
            <li>متابعة أسبوعية أول شهر، ثم نصف شهرية.</li>
          </ol>
          <small>الخطة تتعدل حسب الاستجابة والنتائج.</small>
        </div>
        """
    body = f"""
    <div class="card">
      <form method="post">
        <label>المادة المستهدفة</label><input name="sub" placeholder="كحول/قنب/منبهات/أفيونات...">
        <label>أهداف العلاج</label><textarea name="goals" placeholder="امتناع كامل/تقليل… مؤشرات نجاح محددة"></textarea>
        <label>خفض الضرر</label><textarea name="harm" placeholder="تجنّب قيادة، رفيق أمين، ترطيب، غذاء…"></textarea>
        <label>الدعم/البيئة</label><textarea name="supports" placeholder="عائلة/صديق داعم، مجموعة دعم، علاج فردي/جماعي"></textarea>
        <label>المتابعة</label><textarea name="followup" placeholder="مواعيد، إعادة فحص، قياسات دورية"></textarea>
        <div style="margin-top:10px"><button class="btn">توليد الخطة</button></div>
      </form>
    </div>
    {result}
    """
    return render_template_string(BASE, title="خطة تدخل", heading="بناء خطة تدخل أولية", body=body, year=now_year())

# ===== إحالة سريعة =====
@addiction_bp.route("/referral", methods=["GET","POST"])
def referral():
    result = ""
    if request.method=="POST":
        name   = request.form.get("name","")
        age    = request.form.get("age","")
        sub    = request.form.get("sub","")
        risk   = request.form.get("risk","")
        notes  = request.form.get("notes","")
        result = f"""
        <div class="card">
          <h3>نموذج إحالة</h3>
          <table>
            <tr><th>الاسم</th><td>{name}</td></tr>
            <tr><th>العمر</th><td>{age}</td></tr>
            <tr><th>المادة</th><td>{sub}</td></tr>
            <tr><th>نقاط خطورة</th><td>{risk}</td></tr>
            <tr><th>ملاحظات</th><td>{notes}</td></tr>
          </table>
          <small>تُرسل إلى الجهة المختصة وفق سياسة المركز.</small>
        </div>
        """
    body = f"""
    <div class="card">
      <form method="post">
        <div class="grid">
          <div><label>الاسم</label><input name="name"></div>
          <div><label>العمر</label><input name="age"></div>
        </div>
        <label>المادة</label><input name="sub" placeholder="كحول/أفيونات/منبهات...">
        <label>نقاط خطورة</label><textarea name="risk" placeholder="انسحاب شديد، أمراض مصاحبة، حوادث، أفكار انتحارية…"></textarea>
        <label>ملاحظات</label><textarea name="notes"></textarea>
        <div style="margin-top:10px"><button class="btn">إنشاء إحالة</button></div>
      </form>
    </div>
    {result}
    """
    return render_template_string(BASE, title="إحالة", heading="نموذج إحالة سريعة", body=body, year=now_year())
