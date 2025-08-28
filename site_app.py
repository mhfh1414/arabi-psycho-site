# -*- coding: utf-8 -*-
from __future__ import annotations
from flask import Flask, Response
import os, datetime

app = Flask(__name__)

# ================== الصفحة الرئيسية ==================
INDEX_HTML = u"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>عربي سايكو | منصة نفسية احترافية</title>
  <style>
    body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,"Noto Naskh Arabic UI",Tahoma,Arial;background:#0a0f1a;color:#e5e7eb}
    header{padding:18px;border-bottom:1px solid rgba(255,255,255,.08);display:flex;align-items:center;gap:10px}
    .logo{inline-size:32px;block-size:32px;border-radius:10px;background:conic-gradient(from 210deg at 55% 40%, #0ea5a4, #1dd6c9 40%, #22c55e 70%, #86efac 88%, #0ea5a4)}
    main{max-width:920px;margin:24px auto;padding:0 16px}
    .cards{display:grid;grid-template-columns:1fr;gap:16px}
    @media(min-width:800px){.cards{grid-template-columns:1fr 1fr}}
    .card{background:linear-gradient(180deg,#0f172a,#111827);border:1px solid rgba(255,255,255,.06);border-radius:18px;padding:16px}
    .muted{color:#a1a1aa}
    .btn{display:inline-block;margin:8px 0;padding:10px 14px;border-radius:12px;background:#0e1726;border:1px solid rgba(255,255,255,.08);color:#e5e7eb;text-decoration:none}
    .btn:hover{transform:translateY(-1px)}
    footer{opacity:.7;text-align:center;font-size:12px;margin:28px 0}
  </style>
</head>
<body>
  <header><div class="logo"></div><b>عربي سايكو</b> — منصة نفسية احترافية</header>
  <main>
    <h1>مرحبًا بك 👋</h1>
    <p class="muted">هذه النسخة مخصصة للعرض في المراكز الطبية: خطة تعافي CBT تفاعلية + صفحات جاهزة للطباعة.</p>
    <div class="cards">
      <div class="card">
        <h3>🧠 خطة التعافي السلوكي المعرفي (CBT)</h3>
        <p>نموذج عملي لحفظ وطباعة خطة التعافي، يشمل رصد ABC، الأهداف، ومراحل الرصد/العلاج/المتابعة.</p>
        <a class="btn" href="/cbt-plan">فتح الخطة</a>
      </div>
      <div class="card">
        <h3>🗓️ الاستخدام داخل المنشآت الطبية</h3>
        <p class="muted">يناسب العيادات والمراكز: يمكن تخصيص الهوية وربط زر للتواصل مع الأخصائي.</p>
        <a class="btn" href="https://t.me/Mhfh1414" target="_blank">التواصل عبر تيليجرام</a>
      </div>
    </div>
    <footer>© عربي سايكو — {year}</footer>
  </main>
</body>
</html>""".replace("{year}", str(datetime.datetime.utcnow().year))

# ================== صفحة خطة التعافي (كاملة) ==================
CBT_PLAN_SECTION = u"""<section id="cbt-plan" class="cbt-plan" dir="rtl" aria-label="خطة التعافي السلوكي المعرفي">
  <style>
    .cbt-plan{--primary:#0ea5a4;--ink:#0b1324;--muted:#9ca3af;--card:#0f172a;--card2:#111827;color:#e5e7eb}
    .cbt-plan *{box-sizing:border-box}
    .cbt-plan .wrap{max-width:1050px;margin:24px auto;padding:0 16px}
    .cbt-plan .hdr{display:flex;align-items:center;gap:12px;margin:10px 0}
    .cbt-plan .logo{inline-size:36px;block-size:36px;border-radius:10px;background:conic-gradient(from 210deg at 55% 40%, var(--primary), #1dd6c9 40%, #22c55e 70%, #86efac 88%, var(--primary))}
    .cbt-plan h2{margin:0;font-size:18px;color:#f3f4f6}
    .cbt-plan .toolbar{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 18px}
    .cbt-plan .btn{appearance:none;border:1px solid rgba(255,255,255,.08);background:#0e1726;color:#e5e7eb;padding:9px 12px;border-radius:12px;cursor:pointer;transition:.2s}
    .cbt-plan .btn:hover{transform:translateY(-1px)}
    .cbt-plan .btn.primary{background:linear-gradient(180deg,var(--primary),#0b9897);border-color:transparent;color:#031316;font-weight:700}
    .cbt-plan .grid{display:grid;gap:16px}
    @media(min-width:900px){.cbt-plan .grid{grid-template-columns:1fr 1fr}}
    .cbt-plan .card{background:linear-gradient(180deg,var(--card),var(--card2));border:1px solid rgba(255,255,255,.06);border-radius:16px;padding:16px}
    .cbt-plan label{display:block;font-size:13px;color:var(--muted);margin:10px 0 6px}
    .cbt-plan input,.cbt-plan textarea,.cbt-plan select{width:100%;padding:10px 12px;border-radius:12px;border:1px solid rgba(255,255,255,.08);background:#0b1324;color:#e5e7eb;outline:none}
    .cbt-plan textarea{min-height:100px;resize:vertical}
    .cbt-plan .two{display:grid;gap:10px}
    @media(min-width:680px){.cbt-plan .two{grid-template-columns:1fr 1fr}}
    .cbt-plan .pill{display:inline-flex;align-items:center;gap:8px;padding:6px 10px;border-radius:999px;border:1px solid rgba(255,255,255,.08);font-size:12px;color:#a1a1aa;margin:4px}
    .cbt-plan table{width:100%;border-collapse:separate;border-spacing:0;font-size:13px}
    .cbt-plan th,.cbt-plan td{border-bottom:1px solid rgba(255,255,255,.06);padding:10px;text-align:right}
    .cbt-plan th{background:#0e1726;color:#cbd5e1}
    .cbt-plan .add-row{margin-top:8px}
  </style>

  <div class="wrap">
    <div class="hdr">
      <div class="logo" aria-hidden="true"></div>
      <div>
        <h2>خطة التعافي السلوكي المعرفي (CBT)</h2>
        <div class="muted">نموذج عملي — قابل للحفظ والطباعة — مخصص للمراكز الطبية</div>
      </div>
    </div>

    <div class="toolbar">
      <button class="btn primary" onclick="CBTPlan.save()">💾 حفظ الخطة (JSON)</button>
      <label class="btn" for="cbtplan-file">📂 تحميل خطة محفوظة</label>
      <input id="cbtplan-file" type="file" accept="application/json" style="display:none" />
      <button class="btn" onclick="CBTPlan.print()">🖨️ طباعة</button>
      <button class="btn" onclick="CBTPlan.clear()">🧹 تفريغ</button>
    </div>

    <div class="grid">
      <section class="card">
        <h3>١) معلومات الحالة</h3>
        <div class="two">
          <div><label>الاسم</label><input id="cbtplan-name" placeholder="اسم المستفيد" /></div>
          <div><label>العمر</label><input id="cbtplan-age" type="number" min="1" placeholder="بالسنوات" /></div>
          <div><label>الجنس</label>
            <select id="cbtplan-gender"><option value="">— اختر —</option><option>ذكر</option><option>أنثى</option><option>آخر</option></select>
          </div>
          <div><label>التاريخ</label><input id="cbtplan-date" type="date" /></div>
        </div>
        <label>التشخيص / الحالة</label>
        <input id="cbtplan-diagnosis" placeholder="مثال: اضطراب القلق المعمم (GAD)" />
        <label>ملاحظات أساسية</label>
        <textarea id="cbtplan-notes" placeholder="ملخص الحالة والخلفية"></textarea>
      </section>

      <section class="card">
        <h3>٢) السلوك المستهدف والأهداف</h3>
        <label>السلوك المستهدف</label>
        <textarea id="cbtplan-target" placeholder="وصف السلوك وشدته وتكراره"></textarea>
        <div class="two">
          <div>
            <label>Antecedents</label>
            <textarea id="cbtplan-A" placeholder="A: المثيرات"></textarea>
          </div>
          <div>
            <label>Consequences</label>
            <textarea id="cbtplan-C" placeholder="C: النتائج"></textarea>
          </div>
        </div>
        <label>الهدف العام</label>
        <input id="cbtplan-goal" placeholder="تقليل السلوك واستبداله بسلوك متكيف" />
        <label>الأهداف الفرعية</label>
        <div id="cbtplan-subgoals"></div>
        <button class="btn add-row" onclick="CBTPlan.addSubGoal()">➕ إضافة هدف فرعي</button>
      </section>

      <section class="card">
        <h3>٣) تقنيات وتدخلات CBT</h3>
        <div>
          <label class="pill"><input type="checkbox" class="cbt-tech" value="إعادة البناء المعرفي" checked> إعادة البناء المعرفي</label>
          <label class="pill"><input type="checkbox" class="cbt-tech" value="التعرض التدريجي"> التعرض التدريجي</label>
          <label class="pill"><input type="checkbox" class="cbt-tech" value="التعزيز الإيجابي"> التعزيز الإيجابي</label>
          <label class="pill"><input type="checkbox" class="cbt-tech" value="حل المشكلات"> حل المشكلات</label>
          <label class="pill"><input type="checkbox" class="cbt-tech" value="تدريب الاسترخاء"> تدريب الاسترخاء</label>
          <label class="pill"><input type="checkbox" class="cbt-tech" value="إدارة الغضب"> إدارة الغضب</label>
          <label class="pill"><input type="checkbox" class="cbt-tech" value="اليقظة الذهنية"> اليقظة الذهنية</label>
          <label class="pill"><input type="checkbox" class="cbt-tech" value="واجبات منزلية"> واجبات منزلية</label>
        </div>
        <label>تفاصيل الإجراءات</label>
        <textarea id="cbtplan-proc" placeholder="وصف مختصر لطريقة التطبيق"></textarea>
      </section>

      <section class="card">
        <h3>٤) رصد السلوك (ABC)</h3>
        <table id="cbtplan-abc">
          <thead><tr><th style="width:15%">التاريخ</th><th style="width:27%">A</th><th style="width:31%">B — السلوك</th><th style="width:27%">C — عواقب</th></tr></thead>
          <tbody></tbody>
        </table>
        <button class="btn add-row" onclick="CBTPlan.addABC()">➕ إضافة صف</button>
      </section>

      <section class="card">
        <h3>٥) الرصد — العلاج — المتابعة</h3>
        <div class="two">
          <div>
            <h4 class="muted">مرحلة الرصد</h4>
            <table id="cbtplan-observe"><thead><tr><th>الجلسة</th><th>عدد مرات السلوك</th><th>ملاحظات</th></tr></thead><tbody></tbody></table>
            <button class="btn add-row" onclick="CBTPlan.addPhase('observe')">➕ صف</button>
          </div>
          <div>
            <h4 class="muted">مرحلة العلاج</h4>
            <table id="cbtplan-treat"><thead><tr><th>الجلسة</th><th>عدد مرات السلوك</th><th>ملاحظات</th></tr></thead><tbody></tbody></table>
            <button class="btn add-row" onclick="CBTPlan.addPhase('treat')">➕ صف</button>
          </div>
        </div>
        <div style="margin-top:12px">
          <h4 class="muted">مرحلة المتابعة</h4>
          <table id="cbtplan-follow"><thead><tr><th>الجلسة</th><th>عدد مرات السلوك</th><th>ملاحظات</th></tr></thead><tbody></tbody></table>
          <button class="btn add-row" onclick="CBTPlan.addPhase('follow')">➕ صف</button>
        </div>
      </section>

      <section class="card">
        <h3>٦) خطة الوقاية من الانتكاس & ٧) قياس التقدم</h3>
        <label>خطة الوقاية من الانتكاس</label>
        <textarea id="cbtplan-relapse" placeholder="مثيرات الخطر، إشارات مبكرة، خطة عمل"></textarea>
        <label style="margin-top:10px">قياس التقدم</label>
        <textarea id="cbtplan-progress" placeholder="مقاييس موضوعية/ذاتية، معيار النجاح"></textarea>
      </section>
    </div>
  </div>

  <script>
    (function(){
      const $  = (s,sc=document)=>sc.querySelector(s);
      const qa = (s,sc=document)=>Array.from(sc.querySelectorAll(s));
      const ids = n => $('#cbtplan-'+n);

      function addSubGoal(){
        const box = ids('subgoals');
        const row = document.createElement('div');
        row.style.cssText='display:flex;gap:8px;align-items:center;margin:6px 0';
        const input = document.createElement('input'); input.placeholder='هدف فرعي'; input.dataset.key='subgoal';
        const del = document.createElement('button'); del.className='btn'; del.textContent='🗑️ حذف'; del.type='button'; del.onclick=()=>row.remove();
        row.append(input,del); box.append(row);
      }

      function addABC(){
        const tb = $('#cbtplan-abc tbody');
        const tr = document.createElement('tr');
        tr.innerHTML = '<td><input type="date"/></td><td><input placeholder="قبل/أثناء"/></td><td><input placeholder="وصف مختصر"/></td><td><input placeholder="ما الذي حدث بعد؟"/></td>';
        tb.append(tr);
      }

      function addPhase(kind){
        const tb = ids(kind).querySelector('tbody');
        const idx = tb.children.length + 1;
        const tr = document.createElement('tr');
        tr.innerHTML = `<td><input value="${idx}"/></td><td><input type="number" min="0" placeholder="0"/></td><td><input placeholder="ملاحظة"/></td>`;
        tb.append(tr);
      }

      function collect(){
        return {
          name: ids('name')?.value || '', age: ids('age')?.value || '', gender: ids('gender')?.value || '', date: ids('date')?.value || '',
          diagnosis: ids('diagnosis')?.value || '', notes: ids('notes')?.value || '',
          target: ids('target')?.value || '', A: ids('A')?.value || '', C: ids('C')?.value || '',
          goal: ids('goal')?.value || '',
          subGoals: qa('#cbtplan-subgoals input').map(i=>i.value).filter(Boolean),
          tech: qa('.cbt-tech:checked').map(i=>i.value), proc: ids('proc')?.value || '',
          abc: qa('#cbtplan-abc tbody tr').map(tr=>{const [d,a,b,c]=qa('input',tr);return {date:d.value,A:a.value,B:b.value,C:c.value}}),
          observe: qa('#cbtplan-observe tbody tr').map(tr=>{const [s,c,n]=qa('input',tr);return {session:s.value,count:c.value,note:n.value}}),
          treat: qa('#cbtplan-treat tbody tr').map(tr=>{const [s,c,n]=qa('input',tr);return {session:s.value,count:c.value,note:n.value}}),
          follow: qa('#cbtplan-follow tbody tr').map(tr=>{const [s,c,n]=qa('input',tr);return {session:s.value,count:c.value,note:n.value}}),
          relapse: ids('relapse')?.value || '', progress: ids('progress')?.value || ''
        }
      }

      function fill(data){
        if(!data) return;
        const set=(id,v)=>{const el=ids(id); if(el) el.value = (v || '');};
        set('name',data.name); set('age',data.age); set('gender',data.gender); set('date',data.date);
        set('diagnosis',data.diagnosis); set('notes',data.notes); set('target',data.target); set('A',data.A); set('C',data.C);
        set('goal',data.goal);
        $('#cbtplan-subgoals').innerHTML='';
        (data.subGoals||[]).forEach(v=>{ addSubGoal(); const last=$('#cbtplan-subgoals input:last-of-type'); last.value=v; });
        qa('.cbt-tech').forEach(cb=>cb.checked=(data.tech||[]).includes(cb.value));
        set('proc',data.proc);

        const fillRows=(id,arr,cb)=>{const tb=ids(id).querySelector('tbody'); tb.innerHTML=''; (arr||[]).forEach(x=>cb(tb,x));};
        fillRows('abc',data.abc,(tb,r)=>{addABC(); const last=tb.lastElementChild; const ins=qa('input',last); ins[0].value=r.date||''; ins[1].value=r.A||''; ins[2].value=r.B||''; ins[3].value=r.C||'';});
        fillRows('observe',data.observe,(tb,r)=>{addPhase('observe'); const last=tb.lastElementChild; const ins=qa('input',last); ins[0].value=r.session||''; ins[1].value=r.count||''; ins[2].value=r.note||'';});
        fillRows('treat',data.treat,(tb,r)=>{addPhase('treat'); const last=tb.lastElementChild; const ins=qa('input',last); ins[0].value=r.session||''; ins[1].value=r.count||''; ins[2].value=r.note||'';});
        fillRows('follow',data.follow,(tb,r)=>{addPhase('follow'); const last=tb.lastElementChild; const ins=qa('input',last); ins[0].value=r.session||''; ins[1].value=r.count||''; ins[2].value=r.note||'';});
        set('relapse',data.relapse); set('progress',data.progress);
      }

      function save(){
        const data = collect();
        const blob = new Blob([JSON.stringify(data,null,2)], {type:'application/json'});
        const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
        a.download = `CBT_Plan_${data.name||'client'}_${new Date().toISOString().slice(0,10)}.json`;
        a.click();
        try{ localStorage.setItem('cbt_plan_autosave', JSON.stringify(data)); }catch(e){}
      }

      function clearAll(){
        if(!confirm('هل تريد تفريغ كافة الحقول؟')) return;
        qa('#cbt-plan input, #cbt-plan textarea, #cbt-plan select').forEach(el=>{
          if(el.type==='checkbox') el.checked=false; else el.value='';
        });
        qa('#cbtplan-abc tbody, #cbtplan-observe tbody, #cbtplan-treat tbody, #cbtplan-follow tbody').forEach(tb=>tb.innerHTML='');
        $('#cbtplan-subgoals').innerHTML='';
      }

      function printPlan(){ window.print(); }

      // تحميل JSON محفوظ
      document.addEventListener('change',(ev)=>{
        if(ev.target && ev.target.id==='cbtplan-file'){
          const f = ev.target.files && ev.target.files[0]; if(!f) return;
          const r = new FileReader();
          r.onload = e => { try { fill(JSON.parse(e.target.result)); } catch(err){ alert('تعذر قراءة الملف'); } };
          r.readAsText(f,'utf-8');
        }
      });

      // تمهيد أولي
      (function bootstrap(){
        for(let i=0;i<2;i++) addABC();
        for(let i=0;i<3;i++) addPhase('observe');
        for(let i=0;i<3;i++) addPhase('treat');
        for(let i=0;i<2;i++) addPhase('follow');
        addSubGoal();
        try{ const raw=localStorage.getItem('cbt_plan_autosave'); if(raw) fill(JSON.parse(raw)); }catch(e){}
      })();

      // API عام
      window.CBTPlan = {
        addSubGoal, addABC, addPhase, collect, fill, save, clear: clearAll, print: printPlan,
        toggle(){ const sec = document.getElementById('cbt-plan'); sec.style.display = (sec.style.display==='none')?'block':'none'; }
      };
    })();
  </script>
</section>"""

# ================== مسارات Flask ==================
@app.get("/")
def index():
    return Response(INDEX_HTML, mimetype="text/html; charset=utf-8")

@app.get("/cbt-plan")
def cbt_plan():
    html = f"<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>خطة التعافي CBT | عربي سايكو</title></head><body style='background:#0a0f1a;margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,\"Noto Naskh Arabic UI\",Tahoma,Arial;color:#e5e7eb'>{CBT_PLAN_SECTION}</body></html>"
    return Response(html, mimetype="text/html; charset=utf-8")

@app.get("/healthz")
def healthz():
    return {"status": "ok", "time": datetime.datetime.utcnow().isoformat()}

# (اختياري) هيدر بسيط للحماية
@app.after_request
def add_headers(resp: Response):
    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp

# ================== تشغيل محلي ==================
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
