# -*- coding: utf-8 -*-
# app.py — Arabi Psycho (v3.0 One-File Stable)

import os, json, tempfile, urllib.parse
from datetime import datetime
from typing import Optional
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

# ========== إعدادات عامة ==========
BRAND = "عربي سايكو"
LOGO  = "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg"
TG_URL = "https://t.me/arabipsycho"
WA_BASE = "https://wa.me/966530565696"

# ========== عداد الزوار ==========
def bump_visitors():
    file = "visitors.json"
    try:
        n = json.load(open(file, encoding="utf-8")).get("count", 0) + 1
    except Exception: n = 1
    json.dump({"count": n}, open(file, "w", encoding="utf-8"), ensure_ascii=False)
    return n

# ========== القالب العام ==========
def shell(title, content, visitors=None):
    v_html = f"<div class='small'>👀 الزوار: <b>{visitors}</b></div>" if visitors else ""
    return f"""<!doctype html><html lang='ar' dir='rtl'><head>
<meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/>
<title>{title}</title>
<style>
body{{margin:0;font-family:'Tajawal',sans-serif;background:#f6f4ff;color:#222}}
.side{{background:#4b0082;color:#fff;padding:16px;position:fixed;top:0;bottom:0;width:260px}}
.content{{margin-right:260px;padding:24px}}
.nav a{{display:block;color:#fff;text-decoration:none;padding:8px 10px;border-radius:8px;margin:4px 0}}
.nav a:hover{{background:rgba(255,255,255,.15)}}
.card{{background:#fff;border-radius:12px;padding:18px;box-shadow:0 4px 8px rgba(0,0,0,.1)}}
.btn{{background:#4b0082;color:#fff;border:none;padding:10px 14px;border-radius:10px;cursor:pointer;font-weight:700}}
.btn.gold{{background:#ffd700;color:#4b0082}}
.table{{width:100%;border-collapse:collapse;margin-top:10px}}
.table th,.table td{{border:1px solid #ddd;padding:6px;text-align:center}}
label.chk{{display:block;margin-bottom:4px}}
</style></head><body>
<div class='side'>
  <h2>{BRAND}</h2>
  <div class='nav'>
    <a href='/'>🏠 الرئيسية</a>
    <a href='/case'>📝 دراسة الحالة</a>
    <a href='/cbt'>🧠 CBT</a>
  </div>
  {v_html}
</div>
<div class='content'>{content}</div></body></html>"""

# ========== الصفحة الرئيسية ==========
@app.get("/")
def home():
    v = bump_visitors()
    html = """
    <div class='card'>
      <h1>مرحبًا بك في عربي سايكو</h1>
      <p>اختر ما يناسبك:</p>
      <ul>
        <li><a href='/case'>📝 دراسة الحالة</a></li>
        <li><a href='/cbt'>🧠 العلاج المعرفي السلوكي</a></li>
      </ul>
    </div>
    """
    return shell("الرئيسية", html, v)

# ========== CBT ==========
CBT_HTML = """
<div class='card'>
  <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
  <p>اختر خطة أو خطتين ومدة الجدول لإنشاء خطة عمل ذاتية.</p>
  <div>
    <label>الخطة A:
      <select id='planA'></select>
    </label>
    <label>الخطة B (اختياري):
      <select id='planB'><option value=''>— بدون —</option></select>
    </label>
    <label>الأيام:
      <select id='days'><option>7</option><option>10</option><option>14</option></select>
    </label>
    <button class='btn gold' onclick='build()'>إنشاء الجدول</button>
  </div>
  <div id='out' style='margin-top:12px'></div>
</div>

<script>
const plans={{
  ba:["3 نشاطات ممتعة","قياس المزاج قبل/بعد","رفع الصعوبة تدريجيًا"],
  tr:["موقف→فكرة","دلائل مع/ضد","فكرة متوازنة"],
  sh:["مواعيد نوم ثابتة","لا شاشات قبل النوم","لا كافيين قبل 6س"],
  ps:["تعريف المشكلة","عصف حلول","خطة تنفيذ"],
  wt:["تأجيل القلق","تدوين","عودة للنشاط"],
  mb:["تنفس واعٍ","فحص جسدي","وعي بالأفكار"],
  rp:["مثيرات شخصية","بدائل فورية","شبكة دعم"]
}};
const A=document.getElementById('planA'),B=document.getElementById('planB');
for(const k in plans){{
  const o1=document.createElement('option');o1.value=k;o1.textContent=k.toUpperCase();A.appendChild(o1);
  const o2=document.createElement('option');o2.value=k;o2.textContent=k.toUpperCase();B.appendChild(o2);
}}
function build(){{
  const a=A.value,b=B.value,d=parseInt(document.getElementById('days').value);
  if(!a) return alert('اختر خطة أولاً');
  const steps=[...plans[a],...(b?plans[b]:[])];
  let html="<h3>خطة "+a.toUpperCase()+(b?(" + "+b.toUpperCase()):"")+" — "+d+" يوم</h3>";
  html+="<table class='table'><tr><th>اليوم</th>"+steps.map(s=>"<th>"+s+"</th>").join('')+"</tr>";
  for(let i=1;i<=d;i++) html+="<tr><td>"+i+"</td>"+steps.map(()=>"<td><input type='checkbox'></td>").join('')+"</tr>";
  html+="</table>";
  document.getElementById('out').innerHTML=html;
}}
</script>
"""

@app.get("/cbt")
def cbt():
    return shell("CBT", CBT_HTML, bump_visitors())

# ========== دراسة الحالة ==========
CASE_HTML = """
<div class='card'>
  <h1>📝 دراسة الحالة</h1>
  <form method='post' action='/case'>
    <label class='chk'><input type='checkbox' name='low_mood'> مزاج منخفض</label>
    <label class='chk'><input type='checkbox' name='anhedonia'> فقد المتعة</label>
    <label class='chk'><input type='checkbox' name='worry'> قلق مفرط</label>
    <label class='chk'><input type='checkbox' name='panic'> نوبات هلع</label>
    <label class='chk'><input type='checkbox' name='addiction'> استخدام مواد</label>
    <textarea name='notes' rows='3' placeholder='ملاحظات إضافية'></textarea><br>
    <button class='btn gold' type='submit'>عرض النتيجة</button>
  </form>
</div>
"""

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method=="GET": return shell("دراسة الحالة", CASE_HTML, bump_visitors())
    f=request.form; notes=f.get("notes","")
    results=[]
    if f.get("low_mood") and f.get("anhedonia"): results.append("مؤشرات اكتئاب")
    if f.get("worry"): results.append("قلق عام")
    if f.get("panic"): results.append("نوبات هلع")
    if f.get("addiction"): results.append("احتمال إدمان، يفضل ربط بخطة الإدمان")
    html="<div class='card'><h1>نتيجة الدراسة</h1><ul>"+ "".join(f"<li>{r}</li>" for r in results or ["لا مؤشرات واضحة"]) +"</ul>"
    html+=f"<p><b>ملاحظات:</b> {notes}</p><a class='btn' href='/cbt'>فتح CBT</a></div>"
    return shell("نتيجة الحالة", html, bump_visitors())

# ========== تشغيل ==========
if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT","10000")))
