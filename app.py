# -*- coding: utf-8 -*-
# Arabi Psycho — One-File (Purple × Gold) v4.0
# Pages: Home / CBT / Case / DSM

import os
from datetime import datetime
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

# ====== إعدادات عامة قابلة للتغيير من البيئة ======
BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO  = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696")
CACHE_BUST = os.environ.get("CACHE_BUST", datetime.utcnow().strftime("%Y%m%d%H%M%S"))

def shell(title, content, active="home"):
    # نستخدم placeholders ثم نستبدلها لتجنّب تعارض الأقواس
    html = r"""
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>[[TITLE]]</title>
<link rel="icon" href="[[LOGO]]"/>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>
<meta http-equiv="Pragma" content="no-cache"/><meta http-equiv="Expires" content="0"/>
<style>
:root{--p:#4B0082;--g:#FFD700;--bg:#f8f6ff;--ink:#2b1a4c}
*{box-sizing:border-box} html,body{height:100%}
body{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif;color:var(--ink);font-size:16.5px;line-height:1.7}
.layout{display:grid;grid-template-columns:280px 1fr;min-height:100vh}
.side{background:linear-gradient(180deg,#4b0082,#3a0d72);color:#fff;padding:18px;position:sticky;top:0;height:100vh}
.logo{display:flex;align-items:center;gap:10px;margin-bottom:18px}
.logo img{width:48px;height:48px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.25)}
.brand{font-weight:900;letter-spacing:.3px;font-size:20px}
.nav a{display:block;color:#fff;text-decoration:none;padding:10px 12px;border-radius:12px;margin:6px 0;font-weight:700;opacity:.9}
.nav a.active{background:rgba(255,255,255,.18)}
.nav a:hover{opacity:1;background:rgba(255,255,255,.12)}
.badge{display:inline-block;background:var(--g);color:#4b0082;border-radius:999px;padding:2px 10px;font-weight:900;font-size:.8rem}
.content{padding:26px}
.card{background:#fff;border:1px solid #eee;border-radius:16px;padding:22px;box-shadow:0 10px 24px rgba(0,0,0,.06)}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.tile{background:#fff;border:1px solid #eee;border-radius:14px;padding:14px}
h1{font-weight:900;font-size:28px} h2{font-weight:800;margin:.2rem 0 .6rem} h3{font-weight:800;margin:.2rem 0 .6rem}
.btn{display:inline-block;background:var(--p);color:#fff;text-decoration:none;padding:11px 16px;border-radius:12px;font-weight:800;cursor:pointer}
.btn.alt{background:#5b22a6} .btn.gold{background:var(--g);color:#4b0082}
.btn.wa{background:#25D366} .btn.tg{background:#229ED9}
.small{font-size:.95rem;opacity:.85}
.table{width:100%;border-collapse:collapse}
.table th,.table td{border:1px solid #eee;padding:8px;text-align:center}
.row{display:flex;gap:10px;flex-wrap:wrap}
.badge2{display:inline-block;border:1px solid #eee;background:#fafafa;padding:6px 10px;border-radius:999px;margin:4px 4px 0 0;font-weight:700}
.note{background:#fff7d1;border:1px dashed #e5c100;border-radius:12px;padding:10px 12px;margin:10px 0}
.footer{color:#fff;margin-top:24px;padding:14px;background:#3a0d72;text-align:center}
.header-result{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.header-result img{width:44px;height:44px;border-radius:10px}
@media print {
  @page { size: A4; margin: 16mm 14mm; }
  .side, .footer, .screen-only { display:none !important; }
  body { background:#fff; font-size:18px; line-height:1.8; }
  .content { padding:0 !important; }
  .card { box-shadow:none; border:none; padding:0; }
  h1{font-size:26px} h2{font-size:22px} h3{font-size:18px}
}
</style></head><body>
<script>window.__BUILD__='[[BUILD]]';</script>
<div class="layout">
  <aside class="side">
    <div class="logo"><img src="[[LOGO]]" alt="شعار"/><div>
      <div class="brand">[[BRAND]]</div>
      <div class="small">«نراك بعيون الاحترام، ونساندك بخطوات عملية.»</div>
      <div class="badge">بنفسجي × ذهبي</div>
    </div></div>
    <nav class="nav">
      <a href="/" class="[[A_HOME]]">🏠 الرئيسية</a>
      <a href="/cbt" class="[[A_CBT]]">🧠 CBT</a>
      <a href="/case" class="[[A_CASE]]">📝 دراسة الحالة</a>
      <a href="/dsm" class="[[A_DSM]]">📘 DSM</a>
      <a href="[[TG_URL]]" target="_blank" rel="noopener">✈️ تيليجرام</a>
      <a href="[[WA_URL]]" target="_blank" rel="noopener">🟢 واتساب</a>
    </nav>
  </aside>
  <main class="content">[[CONTENT]]</main>
</div>
<div class="footer"><small>© جميع الحقوق محفوظة لـ [[BRAND]]</small></div>
</body></html>
""".replace("[[TITLE]]", title)\
     .replace("[[LOGO]]", LOGO)\
     .replace("[[BUILD]]", CACHE_BUST)\
     .replace("[[BRAND]]", BRAND)\
     .replace("[[TG_URL]]", TG_URL)\
     .replace("[[WA_URL]]", WA_URL)\
     .replace("[[A_HOME]]", "active" if active=="home" else "")\
     .replace("[[A_CBT]]", "active" if active=="cbt" else "")\
     .replace("[[A_CASE]]", "active" if active=="case" else "")\
     .replace("[[A_DSM]]", "active" if active=="dsm" else "")\
     .replace("[[CONTENT]]", content)
    return html

# ====== Home ======
@app.get("/")
def home():
    content = """
    <div class="card" style="margin-bottom:14px">
      <h1>مرحبًا بك في [[BRAND]]</h1>
      <div class="small">اختر أداتك: CBT، دراسة الحالة، أو مرجع DSM — كلها في ملف واحد.</div>
    </div>
    <div class="grid">
      <div class="tile"><h3>🧠 CBT</h3><p class="small">مولّد جدول 7/10/14 يوم و 15 خطة.</p><a class="btn" href="/cbt">افتح CBT</a></div>
      <div class="tile"><h3>📝 دراسة الحالة</h3><p class="small">نموذج تفاعلي يحفظ محليًا + ملخّص جاهز للطباعة والمشاركة.</p><a class="btn gold" href="/case">ابدأ الآن</a></div>
      <div class="tile"><h3>📘 DSM</h3><p class="small">ملخّص سريع للمحاور الكبرى.</p><a class="btn alt" href="/dsm">فتح DSM</a></div>
    </div>
    """.replace("[[BRAND]]", BRAND)
    return shell("الرئيسية — " + BRAND, content, "home")

# ====== CBT (نفس النسخة المستقرة) ======
CBT_HTML = r"""
<div class="card">
  <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
  <p class="small">اختر خطة/خطة+خطة ثم أنشئ جدول 7/10/14 يوم مع مربعات إنجاز، تنزيل/طباعة/مشاركة. <b>يتم الحفظ محليًا</b>.</p>

  <h2>خطط جاهزة (15 خطة)</h2>
  <div class="grid">

    <div class="tile"><h3>BA — تنشيط سلوكي</h3><ol>
      <li>3 نشاطات مُجزية يوميًا.</li><li>قياس مزاج قبل/بعد.</li><li>رفع الصعوبة تدريجيًا.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ba')">اختيار</button><button class="btn" onclick="dl('ba')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>TR — سجل أفكار</h3><ol>
      <li>موقف→فكرة.</li><li>دلائل مع/ضد.</li><li>بديل متوازن + تجربة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('thought_record')">اختيار</button><button class="btn" onclick="dl('thought_record')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>SH — نظافة النوم</h3><ol>
      <li>أوقات ثابتة.</li><li>إيقاف الشاشات 60د.</li><li>لا كافيين قبل 6س.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('sleep_hygiene')">اختيار</button><button class="btn" onclick="dl('sleep_hygiene')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>IE — تعرّض داخلي</h3><ol>
      <li>إحداث إحساس آمن.</li><li>منع الطمأنة.</li><li>تكرار حتى الانطفاء.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('interoceptive_exposure')">اختيار</button><button class="btn" onclick="dl('interoceptive_exposure')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>GE — تعرّض تدرّجي</h3><ol>
      <li>سُلّم 0→100.</li><li>تعرّض تصاعدي.</li><li>منع التجنّب/الطمأنة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('graded_exposure')">اختيار</button><button class="btn" onclick="dl('graded_exposure')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>ERP — وسواس قهري</h3><ol>
      <li>قائمة وساوس/طقوس.</li><li>ERP 3× أسبوع.</li><li>قياس القلق.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ocd_erp')">اختيار</button><button class="btn" onclick="dl('ocd_erp')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>PTSD — تأريض/تنظيم</h3><ol>
      <li>5-4-3-2-1.</li><li>تنفّس هادئ ×10.</li><li>روتين أمان.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ptsd_grounding')">اختيار</button><button class="btn" onclick="dl('ptsd_grounding')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>PS — حل المشكلات</h3><ol>
      <li>تعريف دقيق.</li><li>عصف وتقييم.</li><li>خطة ومراجعة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('problem_solving')">اختيار</button><button class="btn" onclick="dl('problem_solving')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>WT — وقت القلق</h3><ol>
      <li>تأجيل القلق.</li><li>تدوين وسياق.</li><li>عودة للنشاط.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('worry_time')">اختيار</button><button class="btn" onclick="dl('worry_time')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>MB — يقظة ذهنية</h3><ol>
      <li>تنفّس 5د.</li><li>فحص جسدي.</li><li>وعي غير حاكم.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('mindfulness')">اختيار</button><button class="btn" onclick="dl('mindfulness')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>BE — تجارب سلوكية</h3><ol>
      <li>فرضية.</li><li>تجربة صغيرة.</li><li>مراجعة دلائل.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('behavioral_experiments')">اختيار</button><button class="btn" onclick="dl('behavioral_experiments')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>SA — إيقاف سلوكيات آمنة</h3><ol>
      <li>حصر السلوكيات.</li><li>تقليل تدريجي.</li><li>بدائل تكيفية.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('safety_behaviors')">اختيار</button><button class="btn" onclick="dl('safety_behaviors')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>IPSRT — روتين ثنائي القطب</h3><ol>
      <li>ثبات نوم/طعام/نشاط.</li><li>مراقبة مزاج.</li><li>إنذارات مبكرة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('bipolar_routine')">اختيار</button><button class="btn" onclick="dl('bipolar_routine')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>RP — منع الانتكاس</h3><ol>
      <li>مثيرات شخصية.</li><li>بدائل فورية.</li><li>شبكة تواصل.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('relapse_prevention')">اختيار</button><button class="btn" onclick="dl('relapse_prevention')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>SS — مهارات اجتماعية</h3><ol>
      <li>رسائل حازمة.</li><li>تواصل بصري/نبرة.</li><li>تعرّض اجتماعي.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('social_skills')">اختيار</button><button class="btn" onclick="dl('social_skills')">تنزيل JSON</button></div></div>

  </div>

  <h2 style="margin-top:18px">📅 مولّد جدول الأيام (دمج خطتين)</h2>
  <div class="tile">
    <div class="row">
      <label>الخطة A: <select id="planA"></select></label>
      <label>الخطة B (اختياري): <select id="planB"><option value="">— بدون —</option></select></label>
      <label>مدة الجدول:
        <select id="daysSelect"><option value="7">7</option><option value="10">10</option><option value="14">14</option></select>
      </label>
      <button class="btn gold" onclick="buildChecklist()">إنشاء الجدول</button>
      <button class="btn alt" onclick="window.print()">طباعة</button>
      <button class="btn" onclick="saveChecklist()">تنزيل JSON</button>
      <a class="btn wa" id="share-wa" target="_blank" rel="noopener">واتساب</a>
      <a class="btn tg" id="share-tg" target="_blank" rel="noopener">تيليجرام</a>
    </div>
    <div id="checklist" style="margin-top:12px"></div>
  </div>

  <script>
    const PLANS = {
      ba:{title:"BA — تنشيط سلوكي",steps:["3 نشاطات مجزية","قياس مزاج قبل/بعد","رفع الصعوبة تدريجيًا"]},
      thought_record:{title:"TR — سجل أفكار",steps:["موقف→فكرة","دلائل مع/ضد","بديل متوازن/تجربة"]},
      sleep_hygiene:{title:"SH — نظافة النوم",steps:["مواعيد ثابتة","قطع الشاشات 60د","لا كافيين 6س قبل"]},
      interoceptive_exposure:{title:"IE — تعرّض داخلي",steps:["إحداث إحساس آمن","منع الطمأنة","تكرار حتى الانطفاء"]},
      graded_exposure:{title:"GE — تعرّض تدرّجي",steps:["سُلّم 0→100","تعرّض تصاعدي","منع التجنّب/الطمأنة"]},
      ocd_erp:{title:"ERP — وسواس قهري",steps:["قائمة وساوس/طقوس","ERP 3× أسبوع","قياس القلق"]},
      ptsd_grounding:{title:"PTSD — تأريض/تنظيم",steps:["5-4-3-2-1","تنفّس هادئ ×10","روتين أمان"]},
      problem_solving:{title:"PS — حل المشكلات",steps:["تعريف دقيق","عصف وتقييم","خطة ومراجعة"]},
      worry_time:{title:"WT — وقت القلق",steps:["تأجيل القلق","تدوين وسياق","عودة للنشاط"]},
      mindfulness:{title:"MB — يقظة ذهنية",steps:["تنفّس 5د","فحص جسدي","وعي غير حاكم"]},
      behavioral_experiments:{title:"BE — تجارب سلوكية",steps:["فرضية","تجربة صغيرة","مراجعة دلائل"]},
      safety_behaviors:{title:"SA — إيقاف سلوكيات آمنة",steps:["حصر السلوكيات","تقليل تدريجي","بدائل تكيفية"]},
      bipolar_routine:{title:"IPSRT — روتين ثنائي القطب",steps:["ثبات نوم/طعام/نشاط","مراقبة مزاج يومي","إشارات مبكرة"]},
      relapse_prevention:{title:"RP — منع الانتكاس (إدمان)",steps:["مثيرات شخصية","بدائل فورية","شبكة تواصل"]},
      social_skills:{title:"SS — مهارات اجتماعية",steps:["رسائل حازمة","تواصل بصري/نبرة","تعرّض اجتماعي"]}
    };

    const selectA=document.getElementById('planA');
    const selectB=document.getElementById('planB');

    (function fill(){
      for(const k in PLANS){
        const o=document.createElement('option'); o.value=k; o.textContent=PLANS[k].title; selectA.appendChild(o);
        const o2=document.createElement('option'); o2.value=k; o2.textContent=PLANS[k].title; selectB.appendChild(o2);
      }
      const saved=JSON.parse(localStorage.getItem('cbt_state')||'{}');
      selectA.value=saved.planA||'ba';
      if(saved.planB) selectB.value=saved.planB;
      if(saved.days) document.getElementById('daysSelect').value=String(saved.days);
    })();

    function persist(){
      const state={planA:selectA.value, planB:selectB.value||'', days:parseInt(document.getElementById('daysSelect').value,10)||7};
      localStorage.setItem('cbt_state', JSON.stringify(state));
    }

    function pick(key){ selectA.value=key; persist(); window.scrollTo({top:document.getElementById('daysSelect').offsetTop-60,behavior:'smooth'}); }

    function dl(key){
      const data=PLANS[key]||{};
      const a=document.createElement('a');
      a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
      a.download= key + ".json"; a.click(); URL.revokeObjectURL(a.href);
    }

    function buildChecklist(){
      persist();
      const a = selectA.value; const b = selectB.value; const days = parseInt(document.getElementById('daysSelect').value,10);
      const A = PLANS[a]; const B = PLANS[b] || null;
      const steps = [...A.steps, ...(B?B.steps:[])];
      const titles = [A.title].concat(B?[B.title]:[]).join(" + ");

      let html="<h3 style='margin:6px 0'>"+titles+" — جدول "+days+" يوم</h3>";
      html += "<table class='table'><thead><tr><th>اليوم</th>";
      steps.forEach((s,i)=> html += "<th>"+(i+1)+". "+s+"</th>");
      html += "</tr></thead><tbody>";
      for(let d=1; d<=days; d++) {
        html+="<tr><td><b>"+d+"</b></td>";
        for(let i=0;i<steps.length;i++) html+="<td><input type='checkbox' /></td>";
        html+="</tr>";
      }
      html+="</tbody></table>";
      document.getElementById('checklist').innerHTML=html;
      updateShareLinks(titles, days);
    }

    function saveChecklist(){
      const rows = document.querySelectorAll('#checklist tbody tr');
      if(!rows.length) return;
      const head = document.querySelector('#checklist h3')?.innerText || '';
      const parts = head.split(' — جدول ');
      const days = parseInt((parts[1]||'7').split(' ')[0],10);
      const headerCells = [...document.querySelectorAll('#checklist thead th')].slice(1).map(th=>th.innerText);
      const progress = [];
      rows.forEach((tr, idx)=>{
        const done=[...tr.querySelectorAll('input[type=checkbox]')].map(ch=>ch.checked);
        progress.push({day:(idx+1), done});
      });
      const data = { title:parts[0]||'', steps:headerCells, days, progress, created_at:new Date().toISOString(), build: window.__BUILD__ };
      const a=document.createElement('a');
      a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
      a.download='cbt_checklist.json'; a.click(); URL.revokeObjectURL(a.href);
    }

    function updateShareLinks(title, days){
      const url = location.origin + '/cbt';
      const msg = "خطة CBT: "+title+"\\nمدة: "+days+" يوم\\n— من [[BRAND]]\\n"+url;
      const text = encodeURIComponent(msg);
      document.getElementById('share-wa').href='[[WA_BASE]]'+'?text='+text;
      document.getElementById('share-tg').href='https://t.me/share/url?url='+encodeURIComponent(url)+'&text='+text;
    }
  </script>
</div>
"""

@app.get("/cbt")
def cbt():
    wa_base = WA_URL.split("?")[0]
    html = CBT_HTML.replace("[[BRAND]]", BRAND).replace("[[WA_BASE]]", wa_base)
    return shell("CBT — خطط وتمارين", html, "cbt")

# ====== دراسة الحالة (Form + نتيجة) ======
CASE_FORM = r"""
<div class="card">
  <h1>📝 دراسة الحالة</h1>
  <div class="small">املأ ما يناسبك؛ تُحفظ اختياراتك محليًا. ثم اضغط «عرض الترشيحات» لطباعة/مشاركة النتيجة.</div>

  <form method="post" action="/case" oninput="persistCase()">
    <h3>1) بيانات عامة</h3>
    <div class="grid">
      <div class="tile"><label>العمر<input name="age" type="number" min="5" max="120" placeholder="28"></label></div>
      <div class="tile"><label>الحالة الاجتماعية
        <select name="marital"><option value="">—</option><option>أعزب/عزباء</option><option>متزوج/ة</option><option>منفصل/ة</option></select>
      </label></div>
      <div class="tile"><label>العمل/الدراسة<input name="work" placeholder="طالب/موظف/باحث..."></label></div>
    </div>

    <h3>2) الأعراض</h3>
    <div class="grid">
      <div class="tile"><h4>مزاج</h4>
        <label class="badge2"><input type="checkbox" name="low_mood"> مزاج منخفض</label>
        <label class="badge2"><input type="checkbox" name="anhedonia"> فقد المتعة</label>
        <label class="badge2"><input type="checkbox" name="fatigue"> إرهاق</label>
        <label class="badge2"><input type="checkbox" name="sleep_issue"> نوم مضطرب</label>
        <label class="badge2"><input type="checkbox" name="appetite_change"> شهية/وزن</label>
        <label class="badge2"><input type="checkbox" name="worthlessness"> ذنب/عدم قيمة</label>
        <label class="badge2"><input type="checkbox" name="poor_concentration"> تشتت</label>
        <label class="badge2"><input type="checkbox" name="suicidal"> أفكار إيذاء</label>
      </div>

      <div class="tile"><h4>قلق/هلع/اجتماعي</h4>
        <label class="badge2"><input type="checkbox" name="worry"> قلق زائد</label>
        <label class="badge2"><input type="checkbox" name="tension"> توتر جسدي</label>
        <label class="badge2"><input type="checkbox" name="panic"> نوبات هلع</label>
        <label class="badge2"><input type="checkbox" name="social_fear"> قلق اجتماعي</label>
      </div>

      <div class="tile"><h4>وسواس/صدمات</h4>
        <label class="badge2"><input type="checkbox" name="obsessions"> وساوس</label>
        <label class="badge2"><input type="checkbox" name="compulsions"> أفعال قهرية</label>
        <label class="badge2"><input type="checkbox" name="flashbacks"> استرجاعات</label>
        <label class="badge2"><input type="checkbox" name="hypervigilance"> يقظة مفرطة</label>
        <label class="badge2"><input type="checkbox" name="avoidance"> تجنّب</label>
      </div>

      <div class="tile"><h4>مواد</h4>
        <label class="badge2"><input type="checkbox" name="craving"> اشتهاء</label>
        <label class="badge2"><input type="checkbox" name="withdrawal"> انسحاب</label>
        <label class="badge2"><input type="checkbox" name="use_harm"> استمرار رغم الضرر</label>
      </div>
    </div>

    <div class="tile" style="margin-top:10px"><label>ملاحظات<textarea name="notes" rows="4" placeholder="أي تفاصيل إضافية مهمة لك"></textarea></label></div>
    <div class="row">
      <button class="btn gold" type="submit">عرض الترشيحات</button>
      <a class="btn alt" href="/dsm">📘 DSM</a>
      <a class="btn" href="/cbt">🧠 CBT</a>
    </div>
  </form>

  <script>
    const KEY='case_state_v1';
    function persistCase(){
      const form=document.querySelector('form[action="/case"]');
      const data={};
      form.querySelectorAll('input[type=checkbox]').forEach(ch=>{ if(ch.checked) data[ch.name]=true; });
      ["age","marital","work","notes"].forEach(n=>{ const el=form.querySelector('[name="'+n+'"]'); if(el) data[n]=el.value||''; });
      localStorage.setItem(KEY, JSON.stringify(data));
    }
    (function restore(){
      try{
        const data=JSON.parse(localStorage.getItem(KEY)||'{}');
        Object.keys(data).forEach(k=>{
          const el=document.querySelector('[name="'+k+'"]');
          if(!el) return;
          if(el.type==='checkbox' && data[k]) el.checked=true;
          else if(el.tagName==='INPUT' || el.tagName==='TEXTAREA' || el.tagName==='SELECT') el.value=data[k];
        });
      }catch(e){}
    })();
  </script>
</div>
"""

def _count(d,*keys):
    return sum(1 for k in keys if d.get(k))

def _recommend(d):
    picks = []
    cbt  = []
    add  = False

    dep_core = _count(d,"low_mood","anhedonia")
    dep_more = _count(d,"fatigue","sleep_issue","appetite_change","worthlessness","poor_concentration","suicidal")
    if dep_core>=1 and (dep_core+dep_more)>=5:
        picks.append(("نوبة اكتئابية جسيمة","كتلة أعراض مع تأثير وظيفي","درجة 80"))
        cbt += ["BA — تنشيط سلوكي","TR — سجل أفكار","SH — نظافة النوم"]
    elif dep_core>=1 and (dep_core+dep_more)>=3:
        picks.append(("اكتئاب خفيف/متوسط","مجموعة أعراض مزاجية","درجة 60"))
        cbt += ["BA — تنشيط سلوكي","TR — سجل أفكار"]

    if d.get("suicidal"): picks.insert(0,("تنبيه أمان","وجود أفكار إيذاء — فضّل تواصلًا فوريًا مع مختص","درجة 99"))

    if _count(d,"worry","tension")>=2: 
        picks.append(("قلق معمّم","قلق زائد مع توتر","درجة 70")); cbt+=["WT — وقت القلق","MB — يقظة","PS — حل المشكلات"]
    if d.get("panic"): 
        picks.append(("نوبات هلع","نوبات مفاجئة","درجة 70")); cbt+=["IE — تعرّض داخلي","SA — إيقاف سلوكيات آمنة"]
    if d.get("social_fear"): 
        picks.append(("قلق اجتماعي","خشية تقييم الآخرين","درجة 65")); cbt+=["GE — تعرّض اجتماعي","SS — مهارات اجتماعية","TR — سجل أفكار"]

    if d.get("obsessions") and d.get("compulsions"):
        picks.append(("وسواس قهري","وساوس + أفعال قهرية","درجة 80")); cbt+=["ERP — وسواس","SA — إيقاف سلوكيات آمنة"]
    if _count(d,"flashbacks","hypervigilance","avoidance")>=2:
        picks.append(("آثار صدمة","استرجاعات/يقظة/تجنّب","درجة 70")); cbt+=["PTSD — تأريض/تنظيم","MB — يقظة"]

    if _count(d,"craving","withdrawal","use_harm")>=2:
        picks.append(("تعاطي مواد","اشتهاء/انسحاب/استمرار رغم الضرر","درجة 80")); add=True; cbt+=["RP — منع الانتكاس","PS — حل المشكلات"]

    cbt = sorted(set(cbt))
    return picks, cbt, add

RESULT_JS = r"""
<script>
  function saveJSON(){
    const data={
      items:[...document.querySelectorAll('#diag-items li')].map(li=>li.innerText),
      cbt:[...document.querySelectorAll('.badge2')].map(b=>b.innerText),
      notes:[[NOTES_JSON]],
      created_at:new Date().toISOString(), build: window.__BUILD__
    };
    const a=document.createElement('a');
    a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
    a.download='case_result.json'; a.click(); URL.revokeObjectURL(a.href);
  }
  function buildShare(){
    const items=[...document.querySelectorAll('#diag-items li')].map(li=>'- '+li.innerText).join('\n');
    const msg='نتيجة دراسة الحالة — [[BRAND]]\n\n'+items+( [[NOTES_JSON]] ? '\n\nملاحظات: '+[[NOTES_JSON]]:'' )+'\n'+location.origin+'/case';
    const text=encodeURIComponent(msg);
    document.getElementById('share-wa').href='[[WA_BASE]]'+'?text='+text;
    document.getElementById('share-tg').href='https://t.me/share/url?url='+encodeURIComponent(location.origin+'/case')+'&text='+text;
  }
  buildShare();
</script>
"""

def _render_case_result(picks, cbt_list, add_flag, notes):
    lis = "".join([f"<li><b>{t}</b> — {w} <span class='small'>({s})</span></li>" for (t,w,s) in picks]) or "<li>لا توجد مؤشرات كافية.</li>"
    cbt_badges = "".join([f"<span class='badge2'>🔧 {x}</span>" for x in cbt_list]) or "<span class='small'>—</span>"
    add_badge  = "<span class='badge2'>🚭 برنامج الإدمان مُقترح</span>" if add_flag else "<span class='small'>—</span>"

    js = RESULT_JS.replace('[[NOTES_JSON]]', repr((notes or "").replace("\n"," ").strip()))\
                  .replace('[[BRAND]]', BRAND)\
                  .replace('[[WA_BASE]]', WA_URL.split("?")[0])

    html = f"""
    <div class="card">
      <div class='header-result'>
        <img src='{LOGO}' alt='logo' onerror="this.style.display='none'">
        <div><div style='font-weight:900;font-size:22px'>{BRAND}</div>
        <div class='small'>نتيجة دراسة الحالة — تلخيص أولي جاهز للطباعة والمشاركة</div></div>
      </div>

      <h2>📌 الترشيحات</h2>
      <ol id="diag-items" style="line-height:1.95; padding-inline-start: 20px">{lis}</ol>

      <h3>🔧 أدوات CBT المقترحة</h3>
      <div>{cbt_badges}</div>

      <h3 style="margin-top:10px">🚭 الإدمان</h3>
      <div>{add_badge}</div>

      {"<div class='tile' style='margin-top:10px'><b>ملاحظاتك:</b><br/>"+notes+"</div>" if notes else ""}

      <div class="row screen-only" style="margin-top:12px">
        <button class="btn alt" onclick="window.print()">🖨️ طباعة</button>
        <button class="btn" onclick="saveJSON()">💾 تنزيل JSON</button>
        <a class="btn wa" id="share-wa" target="_blank" rel="noopener">🟢 مشاركة واتساب</a>
        <a class="btn tg" id="share-tg" target="_blank" rel="noopener">✈️ مشاركة تيليجرام</a>
        <a class="btn gold" href="/cbt">🧠 فتح CBT</a>
      </div>
      {js}
    </div>
    """
    return html

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell("دراسة الحالة", CASE_FORM, "case")
    # POST
    data = {k: True for k in request.form.keys()}  # checkboxes ستظهر هنا
    # الحقول النصية:
    notes = request.form.get("notes","").strip()
    picks, cbt_list, add_flag = _recommend(data)
    html = _render_case_result(picks, cbt_list, add_flag, notes)
    return shell("نتيجة الترشيح", html, "case")

# ====== DSM ======
DSM_HTML = r"""
<div class="card">
  <h1>📘 DSM — ملخّص داخلي سريع</h1>
  <p class="small">مرجع مختصر لقراءة النتائج وتوجيه الخطة العلاجية. للاستخدام التعليمي السريع وليـس للتشخيص الطبي النهائي.</p>
  <div class="grid">
    <div class="tile"><h3>الاكتئاب (MDD)</h3><ul>
      <li>مزاج منخفض/فقد المتعة + ≥4 (نوم/شهية/طاقة/ذنب/تركيز/تباطؤ/أفكار إيذاء).</li>
      <li>المدة ≥ أسبوعين + تأثير وظيفي.</li></ul></div>

    <div class="tile"><h3>القلق المعمّم</h3><ul>
      <li>قلق زائد أغلب الأيام لمدة ≥6 أشهر مع ≥3 (توتر/إرهاق/تركيز/نوم...).</li></ul></div>

    <div class="tile"><h3>نوبات الهلع</h3><ul>
      <li>نوبات مفاجئة متكرّرة + خشية/تجنّب لاحق.</li></ul></div>

    <div class="tile"><h3>قلق اجتماعي/رُهاب</h3><ul>
      <li>خشية تقييم الآخرين → تجنّب أو تحمّل بضيق.</li></ul></div>

    <div class="tile"><h3>OCD</h3><ul>
      <li>وساوس/أفعال قهرية تستهلك الوقت أو تؤثر في الأداء.</li></ul></div>

    <div class="tile"><h3>PTSD</h3><ul>
      <li>تعرض لحدث صادمي + استرجاعات/تجنّب/يقظة/أثر وظيفي.</li></ul></div>

    <div class="tile"><h3>طيف الفصام</h3><ul>
      <li>ذهانية (هلوسات/أوهام/تفكك خطاب) ± أعراض سلبية؛ يستمر ≥6 أشهر (فصام)، أقل من شهر (وجيز).</li></ul></div>

    <div class="tile"><h3>ثنائي القطب</h3><ul>
      <li>هوس خفيف/هوس (نوم قليل/اندفاع/أفكار متسارعة...) ± نوبات اكتئاب.</li></ul></div>

    <div class="tile"><h3>تعاطي المواد</h3><ul>
      <li>اشتهاء/انسحاب/استمرار رغم الضرر؛ الشدة حسب عدد المعايير.</li></ul></div>
  </div>
  <div class="note small">هذا ملخص تعليمي — القرار العلاجي النهائي يتطلب تقييمًا سريريًا مباشرًا.</div>
</div>
"""

@app.get("/dsm")
def dsm():
    return shell("DSM — مرجع", DSM_HTML, "dsm")

# ====== Health & Headers ======
@app.get("/health")
def health():
    return jsonify({"ok": True, "brand": BRAND, "build": CACHE_BUST}), 200

@app.after_request
def add_headers(resp):
    csp = (
        "default-src 'self' data: blob: https://t.me https://wa.me https://api.whatsapp.com; "
        "script-src 'self' 'unsafe-inline' data: blob: https://t.me https://wa.me https://api.whatsapp.com; "
        "style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: *; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors *"
    )
    resp.headers['Content-Security-Policy'] = csp
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
