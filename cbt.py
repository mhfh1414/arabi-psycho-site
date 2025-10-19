# -*- coding: utf-8 -*-
# cbt.py — صفحة CBT مستقلة تُسجَّل داخل app.py
# لا تُشغَّل مباشرة. يُستدعى منها register_cbt(app, shell, ...)

def register_cbt(app, shell, BRAND, LOGO, TG_URL, WA_URL):
    # نستخدم قالب HTML خام ونستبدل المتغيّرات بأمان بدون f-strings داخل السكربت
    CBT_HTML = r"""
<div class="card">
  <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
  <p class="small">اختر خطة/خطة+خطة ثم أنشئ جدول 7/10/14 يوم تلقائيًا مع مربعات إنجاز وتنزيل/طباعة/مشاركة. <b>حفظ تلقائي</b>.</p>

  <h2>خطط جاهزة (15 خطة)</h2>
  <div class="grid">

    <div class="tile"><h3>BA — تنشيط سلوكي</h3><ol>
      <li>جدولة 3 نشاطات مُجزية يوميًا.</li><li>قياس مزاج قبل/بعد (0–10).</li><li>رفع الصعوبة تدريجيًا.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ba')">اختيار</button><button class="btn" onclick="dl('ba')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>TR — سجل أفكار</h3><ol>
      <li>موقف ← فكرة تلقائية.</li><li>دلائل مع/ضد.</li><li>بديل متوازن + تجربة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('thought_record')">اختيار</button><button class="btn" onclick="dl('thought_record')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>SH — نظافة النوم</h3><ol>
      <li>مواعيد ثابتة.</li><li>إيقاف الشاشات 60د قبل النوم.</li><li>لا كافيين قبل 6س.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('sleep_hygiene')">اختيار</button><button class="btn" onclick="dl('sleep_hygiene')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>IE — تعرّض داخلي</h3><ol>
      <li>إحداث إحساس آمن.</li><li>منع الطمأنة.</li><li>تكرار حتى الانطفاء.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('interoceptive_exposure')">اختيار</button><button class="btn" onclick="dl('interoceptive_exposure')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>GE — تعرّض تدرّجي</h3><ol>
      <li>سُلّم 0→100.</li><li>تعرّض تصاعدي.</li><li>منع التجنّب/الطمأنة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('graded_exposure')">اختيار</button><button class="btn" onclick="dl('graded_exposure')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>ERP — وسواس</h3><ol>
      <li>قائمة وساوس/طقوس.</li><li>ERP 3× أسبوع.</li><li>قياس القلق قبل/بعد.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ocd_erp')">اختيار</button><button class="btn" onclick="dl('ocd_erp')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>PTSD — تأريض</h3><ol>
      <li>5-4-3-2-1.</li><li>تنفّس هادئ ×10.</li><li>روتين أمان.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ptsd_grounding')">اختيار</button><button class="btn" onclick="dl('ptsd_grounding')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>PS — حل المشكلات</h3><ol>
      <li>تعريف دقيق.</li><li>عصف وتقييم.</li><li>خطة ومراجعة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('problem_solving')">اختيار</button><button class="btn" onclick="dl('problem_solving')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>WT — وقت القلق</h3><ol>
      <li>تأجيل القلق.</li><li>تدوين وسياق.</li><li>عودة للنشاط.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('worry_time')">اختيار</button><button class="btn" onclick="dl('worry_time')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>MB — يقظة</h3><ol>
      <li>تنفّس 5د.</li><li>فحص جسدي.</li><li>وعي غير حاكم.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('mindfulness')">اختيار</button><button class="btn" onclick="dl('mindfulness')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>BE — تجارب</h3><ol>
      <li>فرضية.</li><li>تجربة صغيرة.</li><li>مراجعة دلائل.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('behavioral_experiments')">اختيار</button><button class="btn" onclick="dl('behavioral_experiments')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>SA — سلوكيات آمنة</h3><ol>
      <li>حصر السلوكيات.</li><li>تقليل تدريجي.</li><li>بدائل.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('safety_behaviors')">اختيار</button><button class="btn" onclick="dl('safety_behaviors')">تنزيل JSON</button></div></div>

    <div class="tile"><h3>IPSRT — ثنائي القطب</h3><ol>
      <li>ثبات نوم/طعام/نشاط.</li><li>مراقبة مزاج.</li><li>إنذار مبكر.</li></ol>
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
      <label>الخطة A:
        <select id="planA"></select>
      </label>
      <label>الخطة B (اختياري):
        <select id="planB"><option value="">— بدون —</option></select>
      </label>
      <label>المدّة:
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

  <div class="row" style="margin-top:12px">
    <a class="btn gold" href="/case">اربط مع دراسة الحالة</a>
    <a class="btn" href="/book">📅 احجز جلسة</a>
  </div>

  <script>
    const PLANS = {{
      ba: {{title:"BA — تنشيط سلوكي",steps:["3 نشاطات مجزية","قياس مزاج قبل/بعد","رفع الصعوبة تدريجيًا"]}},
      thought_record: {{title:"TR — سجل أفكار",steps:["موقف→فكرة","دلائل مع/ضد","بديل متوازن/تجربة"]}},
      sleep_hygiene: {{title:"SH — نظافة النوم",steps:["مواعيد ثابتة","قطع الشاشات 60د","لا كافيين 6س قبل"]}},
      interoceptive_exposure: {{title:"IE — تعرّض داخلي",steps:["إحداث إحساس آمن","منع الطمأنة","تكرار حتى الانطفاء"]}},
      graded_exposure: {{title:"GE — تعرّض تدرّجي",steps:["سُلّم 0→100","تعرّض تصاعدي","منع التجنّب/الطمأنة"]}},
      ocd_erp: {{title:"ERP — وسواس قهري",steps:["قائمة وساوس/طقوس","ERP 3× أسبوع","قياس القلق قبل/بعد"]}},
      ptsd_grounding: {{title:"PTSD — تأريض/تنظيم",steps:["5-4-3-2-1","تنفّس هادئ ×10","روتين أمان"]}},
      problem_solving: {{title:"PS — حلّ المشكلات",steps:["تعريف دقيق","عصف وتقييم","خطة ومراجعة"]}},
      worry_time: {{title:"WT — وقت القلق",steps:["تأجيل القلق","تدوين وسياق","عودة للنشاط"]}},
      mindfulness: {{title:"MB — يقظة ذهنية",steps:["تنفّس 5د","فحص جسدي","وعي غير حاكم"]}},
      behavioral_experiments: {{title:"BE — تجارب سلوكية",steps:["فرضية","تجربة صغيرة","مراجعة دلائل"]}},
      safety_behaviors: {{title:"SA — إيقاف سلوكيات آمنة",steps:["حصر السلوكيات","تقليل تدريجي","بدائل تكيفية"]}},
      bipolar_routine: {{title:"IPSRT — روتين ثنائي القطب",steps:["ثبات نوم/طعام/نشاط","مراقبة مزاج يومي","إشارات مبكرة"]}},
      relapse_prevention: {{title:"RP — منع الانتكاس",steps:["مثيرات شخصية","بدائل فورية","شبكة تواصل"]}},
      social_skills: {{title:"SS — مهارات اجتماعية",steps:["رسائل حازمة","تواصل بصري/نبرة","تعرّض اجتماعي"]}},
    }};

    const selectA=document.getElementById('planA');
    const selectB=document.getElementById('planB');

    (function fill(){{
      for(const k in PLANS){{
        const o=document.createElement('option'); o.value=k; o.textContent=PLANS[k].title; selectA.appendChild(o);
        const o2=document.createElement('option'); o2.value=k; o2.textContent=PLANS[k].title; selectB.appendChild(o2);
      }}
      const saved=JSON.parse(localStorage.getItem('cbt_state')||'{{}}');
      selectA.value=saved.planA||'ba';
      if(saved.planB) selectB.value=saved.planB;
      if(saved.days) document.getElementById('daysSelect').value=String(saved.days);
    }})();

    function persist(){{
      const state={{planA:selectA.value, planB:selectB.value||'', days:parseInt(document.getElementById('daysSelect').value,10)||7}};
      localStorage.setItem('cbt_state', JSON.stringify(state));
    }}

    function pick(key){{ selectA.value=key; persist(); window.scrollTo({{top:document.getElementById('daysSelect').offsetTop-60,behavior:'smooth'}}); }}

    function dl(key){{
      const data=PLANS[key]||{{}};
      const a=document.createElement('a');
      a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}}));
      a.download= key + ".json"; a.click(); URL.revokeObjectURL(a.href);
    }}

    function buildChecklist(){{
      persist();
      const a = selectA.value; const b = selectB.value; const days = parseInt(document.getElementById('daysSelect').value,10);
      const A = PLANS[a]; const B = PLANS[b] || null;
      const steps = [...A.steps, ...(B?B.steps:[])];
      const titles = [A.title].concat(B?[B.title]:[]).join(" + ");

      let html="<h3 style='margin:6px 0'>"+titles+" — جدول "+days+" يوم</h3>";
      html += "<table class='table'><thead><tr><th>اليوم</th>";
      steps.forEach((s,i)=> html += "<th>"+(i+1)+". "+s+"</th>");
      html += "</tr></thead><tbody>";
      for(let d=1; d<=days; d++) {{
        html+="<tr><td><b>"+d+"</b></td>";
        for(let i=0;i<steps.length;i++) html+="<td><input type='checkbox' /></td>";
        html+="</tr>";
      }}
      html+="</tbody></table>";
      document.getElementById('checklist').innerHTML=html;
      updateShareLinks(titles, days);
    }}

    function saveChecklist(){{
      const rows = document.querySelectorAll('#checklist tbody tr');
      if(!rows.length) return;
      const head = document.querySelector('#checklist h3')?.innerText || '';
      const parts = head.split(' — جدول ');
      const days = parseInt((parts[1]||'7').split(' ')[0],10);
      const headerCells = [...document.querySelectorAll('#checklist thead th')].slice(1).map(th=>th.innerText);
      const progress = [];
      rows.forEach((tr, idx)=>{{
        const done=[...tr.querySelectorAll('input[type=checkbox]')].map(ch=>ch.checked);
        progress.push({{day:(idx+1), done}});
      }});
      const data = {{ title:parts[0]||'', steps:headerCells, days, progress, created_at: new Date().toISOString(), build: window.__BUILD__ }};
      const a=document.createElement('a');
      a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}}));
      a.download='cbt_checklist.json'; a.click(); URL.revokeObjectURL(a.href);
    }}

    function updateShareLinks(title, days){{
      const url = location.origin + '/cbt';
      const msg = "خطة CBT: "+title+"\\nمدة: "+days+" يوم\\n— من [[BRAND]]\\n"+url;
      const text = encodeURIComponent(msg);
      document.getElementById('share-wa').href='[[WA_BASE]]'+'?text='+text;
      document.getElementById('share-tg').href='https://t.me/share/url?url='+encodeURIComponent(url)+'&text='+text;
    }}
  </script>
</div>
""".replace("[[BRAND]]", BRAND).replace("[[WA_BASE]]", WA_URL.split("?")[0])

    @app.get("/cbt")
    def cbt_page():
        return shell("CBT — خطط وتمارين", CBT_HTML, None)
