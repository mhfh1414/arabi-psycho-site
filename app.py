# -*- coding: utf-8 -*-
# Arabi Psycho — CBT Only (Purple × Gold) v1.0

import os
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

# ======= إعدادات بسيطة قابلة للتغيير من البيئة =======
BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO  = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696")
CACHE_BUST = os.environ.get("CACHE_BUST", datetime.utcnow().strftime("%Y%m%d%H%M%S"))

def shell(title, content):
    # ملاحظة: لا نستخدم f-strings داخل القالب الداخلي لتجنّب أي تعارض مع { } الخاصة بالجافاسكربت
    html = """
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
.nav a{display:block;color:#fff;text-decoration:none;padding:10px 12px;border-radius:12px;margin:6px 0;font-weight:700;opacity:.95}
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
.table{width:100%;border-collapse:collapse}
.table th,.table td{border:1px solid #eee;padding:8px;text-align:center}
.row{display:flex;gap:10px;flex-wrap:wrap}
.small{font-size:.95rem;opacity:.85}
.footer{color:#fff;margin-top:24px;padding:14px;background:#3a0d72;text-align:center}
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
      <div class="small">العلاج المعرفي السلوكي <span class="badge">CBT</span></div>
    </div></div>
    <nav class="nav">
      <a href="/">🧠 صفحة الـ CBT</a>
      <a href="[[TG_URL]]" target="_blank" rel="noopener">✈️ تيليجرام</a>
      <a href="[[WA_URL]]" target="_blank" rel="noopener">🟢 واتساب</a>
    </nav>
    <div class="small" style="margin-top:18px;opacity:.9">«نراك بعيون الاحترام، ونساندك بخطوات عملية.»</div>
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
     .replace("[[CONTENT]]", content)
    return html

CBT_HTML = r"""
<div class="card">
  <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
  <p class="small">اختر خطة/خطة+خطة ثم أنشئ جدول أيام 7/10/14 تلقائيًا مع مربعات إنجاز، وتنزيل/طباعة/مشاركة. <b>الحفظ محليًا على جهازك</b>.</p>

  <h2>خطط جاهزة (15 خطة)</h2>
  <div class="grid">

    <div class="tile"><h3>BA — تنشيط سلوكي</h3><ol>
      <li>3 نشاطات مُجزية يوميًا.</li><li>قياس مزاج قبل/بعد (0–10).</li><li>رفع الصعوبة تدريجيًا.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ba')">اختيار</button><button class="btn" onclick="dl('ba')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>TR — سجل أفكار (إعادة هيكلة)</h3><ol>
      <li>موقف ← فكرة تلقائية.</li><li>دلائل مع/ضد.</li><li>بديل متوازن + تجربة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('thought_record')">اختيار</button><button class="btn" onclick="dl('thought_record')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>SH — نظافة النوم</h3><ol>
      <li>أوقات ثابتة.</li><li>إيقاف الشاشات 60د قبل النوم.</li><li>لا كافيين قبل 6س.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('sleep_hygiene')">اختيار</button><button class="btn" onclick="dl('sleep_hygiene')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>IE — تعرّض داخلي للهلع</h3><ol>
      <li>إحداث إحساس آمن.</li><li>منع الطمأنة.</li><li>تكرار حتى الانطفاء.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('interoceptive_exposure')">اختيار</button><button class="btn" onclick="dl('interoceptive_exposure')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>GE — تعرّض تدرّجي</h3><ol>
      <li>سُلّم 0→100.</li><li>تعرّض تصاعدي.</li><li>منع التجنّب.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('graded_exposure')">اختيار</button><button class="btn" onclick="dl('graded_exposure')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>ERP — وسواس قهري</h3><ol>
      <li>قائمة وساوس/طقوس.</li><li>ERP 3× أسبوع.</li><li>قياس القلق.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ocd_erp')">اختيار</button><button class="btn" onclick="dl('ocd_erp')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>PTSD — تأريض وتنظيم</h3><ol>
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
      <li>ثبات نوم/طعام/نشاط.</li><li>مراقبة مزاج 0–10.</li><li>إنذارات مبكرة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('bipolar_routine')">اختيار</button><button class="btn" onclick="dl('bipolar_routine')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>RP — منع الانتكاس</h3><ol>
      <li>مثيرات شخصية.</li><li>بدائل فورية.</li><li>شبكة تواصل.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('relapse_prevention')">اختيار</button><button class="btn" onclick="dl('relapse_prevention')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>SS — مهارات اجتماعية</h3><ol>
      <li>رسائل حازمة.</li><li>تواصل بصري/نبرة.</li><li>تعرّض اجتماعي.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('social_skills')">اختيار</button><button class="btn" onclick="dl('social_skills')">تنزيل JSON</button></div></div>

  </div>

  <h2 style="margin-top:18px">📅 مولّد جدول الأيام (يدعم دمج خطتين)</h2>
  <div class="tile">
    <div class="row">
      <label>الخطة A: <select id="planA"></select></label>
      <label>الخطة B (اختياري): <select id="planB"><option value="">— بدون —</option></select></label>
      <label>مدة الجدول: 
        <select id="daysSelect">
          <option value="7">7 أيام</option>
          <option value="10">10 أيام</option>
          <option value="14">14 يوم</option>
        </select>
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
    // تعريف الخطط
    const PLANS = {
      ba: {title:"BA — تنشيط سلوكي",steps:["3 نشاطات مجزية","قياس مزاج قبل/بعد","رفع الصعوبة تدريجيًا"]},
      thought_record: {title:"TR — سجل أفكار",steps:["موقف→فكرة","دلائل مع/ضد","بديل متوازن/تجربة"]},
      sleep_hygiene: {title:"SH — نظافة النوم",steps:["مواعيد ثابتة","قطع الشاشات 60د","لا كافيين 6س قبل"]},
      interoceptive_exposure: {title:"IE — تعرّض داخلي",steps:["إحداث إحساس آمن","منع الطمأنة","تكرار حتى الانطفاء"]},
      graded_exposure: {title:"GE — تعرّض تدرّجي",steps:["سُلّم 0→100","تعرّض تصاعدي","منع التجنّب/الطمأنة"]},
      ocd_erp: {title:"ERP — وسواس قهري",steps:["قائمة وساوس/طقوس","ERP 3× أسبوع","قياس القلق قبل/بعد"]},
      ptsd_grounding: {title:"PTSD — تأريض/تنظيم",steps:["5-4-3-2-1","تنفّس هادئ ×10","روتين أمان"]},
      problem_solving: {title:"PS — حلّ المشكلات",steps:["تعريف دقيق","عصف وتقييم","خطة ومراجعة"]},
      worry_time: {title:"WT — وقت القلق",steps:["تأجيل القلق","تدوين وسياق","عودة للنشاط"]},
      mindfulness: {title:"MB — يقظة ذهنية",steps:["تنفّس 5د","فحص جسدي","وعي غير حاكم"]},
      behavioral_experiments: {title:"BE — تجارب سلوكية",steps:["فرضية","تجربة صغيرة","مراجعة دلائل"]},
      safety_behaviors: {title:"SA — إيقاف سلوكيات آمنة",steps:["حصر السلوكيات","تقليل تدريجي","بدائل تكيفية"]},
      bipolar_routine: {title:"IPSRT — روتين ثنائي القطب",steps:["ثبات نوم/طعام/نشاط","مراقبة مزاج يومي","إشارات مبكرة"]},
      relapse_prevention: {title:"RP — منع الانتكاس (إدمان)",steps:["مثيرات شخصية","بدائل فورية","شبكة تواصل"]},
      social_skills: {title:"SS — مهارات اجتماعية",steps:["رسائل حازمة","تواصل بصري/نبرة","تعرّض اجتماعي"]},
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
      const url = location.origin + '/';
      const msg = "خطة CBT: "+title+"\\nمدة: "+days+" يوم\\n— من [[BRAND]]\\n"+url;
      const text = encodeURIComponent(msg);
      document.getElementById('share-wa').href='[[WA_BASE]]'+'?text='+text;
      document.getElementById('share-tg').href='https://t.me/share/url?url='+encodeURIComponent(url)+'&text='+text;
    }
  </script>
</div>
"""

@app.get("/")
def cbt_home():
    # تعبئة العلامات مكانها بدون f-strings لتجنّب أخطاء الأقواس
    wa_base = WA_URL.split("?")[0]
    html = CBT_HTML.replace("[[BRAND]]", BRAND).replace("[[WA_BASE]]", wa_base)
    return shell("CBT — خطط وتمارين", html)

@app.get("/health")
def health():
    return jsonify({"ok": True, "brand": BRAND, "build": CACHE_BUST}), 200

@app.after_request
def add_headers(resp):
    # السماح بالـ inline scripts الضرورية
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
