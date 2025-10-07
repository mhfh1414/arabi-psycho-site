# CBT.py — CBT واضح ومقسم: بدء سريع، اختيار الأدوات، خطط جاهزة، تتبّع تقدّم وتنزيل JSON

def main():
    return """
    <div class='card'>
      <h1>🧠 العلاج المعرفي السلوكي (CBT) — خطة عملية واضحة</h1>
      <p class='small'>علاج نفسي افتراضي: اختر الأدوات المناسبة لك، أو ابدأ بخطة جاهزة، ثم تابِع تقدّمك ونزّل الخطة.</p>

      <style>
        .tabs{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
        .tab{padding:8px 12px;border-radius:10px;border:1px solid #ddd;cursor:pointer;font-weight:800}
        .tab.active{background:#4B0082;color:#fff;border-color:#4B0082}
        .sec{display:none;margin-top:10px}
        .sec.active{display:block}
        .grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
        .tool{background:#fafafa;border:1px solid #eee;border-radius:12px;padding:10px}
        .tool h4{margin:.2rem 0 .3rem}
        .hint{font-size:.92rem;opacity:.85}
        .row{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}
        table{width:100%;border-collapse:collapse}
        th,td{border:1px solid #eee;padding:8px;text-align:center}
        th{background:#f7f3ff}
        .btn{display:inline-block;background:#4B0082;color:#fff;text-decoration:none;padding:10px 14px;border-radius:12px;font-weight:800}
        .btn.alt{background:#5b22a6} .btn.gold{background:#FFD700;color:#4B0082}
      </style>

      <div class="tabs">
        <div class="tab active" data-target="#t1">🚀 بدء سريع</div>
        <div class="tab" data-target="#t2">🧰 اختر أدواتك</div>
        <div class="tab" data-target="#t3">📦 خطط جاهزة</div>
        <div class="tab" data-target="#t4">📊 تتبّع التقدّم</div>
        <div class="tab" data-target="#t5">ℹ️ إرشادات</div>
      </div>

      <!-- t1 -->
      <div id="t1" class="sec active">
        <h2>خمس خطوات مباشرة اليوم</h2>
        <ol>
          <li>اختر نشاطًا ممتعًا + نشاطًا مفيدًا (20–30 دقيقة لكلٍ).</li>
          <li>سجّل موقفًا وفكرة تلقائية واحدة في <b>سجلّ الأفكار</b> مع الدليل معها/ضدها.</li>
          <li>تنفّس 4-4-6 خمس دقائق صباحًا ومساءً + تمرين <b>التأريض 5-4-3-2-1</b> عند القلق.</li>
          <li>نم مبكّرًا: اغلاق الشاشات قبل النوم بساعة، وثبّت موعد الاستيقاظ.</li>
          <li>قيّم مزاجك 0–10 صباحًا ومساءً. <u>التحسّن يُقاس بالتكرار.</u></li>
        </ol>
        <div class="row">
          <a class="btn" href="#t2" onclick="openTab('#t2')">انتقل لاختيار الأدوات</a>
          <a class="btn gold" href="#t3" onclick="openTab('#t3')">اختر خطة جاهزة</a>
        </div>
      </div>

      <!-- t2 -->
      <div id="t2" class="sec">
        <h2>اختر أدواتك</h2>
        <div id="tools" class="grid">
          <label class="tool"><input type="checkbox" data-name="تنشيط سلوكي"> 
            <h4>تنشيط سلوكي (BA)</h4><div class="hint">قائمة نشاط ممتع + نشاط مفيد يوميًا، وتقييم المزاج قبل/بعد.</div>
          </label>
          <label class="tool"><input type="checkbox" data-name="سجلّ الأفكار (TR)">
            <h4>سجلّ الأفكار (Thought Record)</h4><div class="hint">الموقف → الفكرة → الدليل معها/ضدها → الفكرة المتوازنة → شدة الانفعال.</div>
          </label>
          <label class="tool"><input type="checkbox" data-name="ERP للوسواس">
            <h4>ERP للوسواس القهري</h4><div class="hint">بناء هرم 10 درجات + تعرّض تدريجي 60–90 دقيقة مع منع الاستجابة.</div>
          </label>
          <label class="tool"><input type="checkbox" data-name="تعرّض اجتماعي">
            <h4>تعرّض اجتماعي (قلق اجتماعي)</h4><div class="hint">سُلّم مواقف من 10 درجات؛ درجتان يوميًا مع منع الطمأنة.</div>
          </label>
          <label class="tool"><input type="checkbox" data-name="تنظيم النوم">
            <h4>تنظيم النوم</h4><div class="hint">ثبات مواقيت + ضوء صباحي + تقليل منبّهات + قطع الشاشات.</div>
          </label>
          <label class="tool"><input type="checkbox" data-name="حلّ المشكلات">
            <h4>حلّ المشكلات</h4><div class="hint">تعريف المشكلة → خيارات → اختيار → تنفيذ → مراجعة.</div>
          </label>
          <label class="tool"><input type="checkbox" data-name="تنفّس + تأريض">
            <h4>تنفّس 4-4-6 + تأريض 5-4-3-2-1</h4><div class="hint">خفض الاستثارة والعودة للحظة الراهنة.</div>
          </label>
          <label class="tool"><input type="checkbox" data-name="مراقبة المزاج">
            <h4>مراقبة المزاج</h4><div class="hint">مقياس 0–10 مرتين يوميًا مع ملاحظات قصيرة.</div>
          </label>
        </div>

        <div class="tool" style="margin-top:10px">
          <label>ملاحظاتك
            <textarea id="notes" rows="4" placeholder="مثال: مشي 20 دقيقة + مكالمة صديق + سجلّ أفكار مساء الثلاثاء"></textarea>
          </label>
        </div>
        <div class="row">
          <button class="btn" onclick="saveCBT()">💾 حفظ خطتي (JSON)</button>
          <button class="btn alt" onclick="window.print()">🖨️ طباعة</button>
        </div>
      </div>

      <!-- t3 -->
      <div id="t3" class="sec">
        <h2>خطط جاهزة وواضحة</h2>
        <div class="grid">
          <div class="tool">
            <h4>📅 خطة 7 أيام للاكتئاب</h4>
            <ul>
              <li>يوميًا: نشاط ممتع + نشاط مفيد (20–30 د).</li>
              <li>3× أسبوعيًا: سجلّ أفكار لموقف مزعج.</li>
              <li>روتين نوم ثابت وقطع الشاشات قبل النوم بساعة.</li>
            </ul>
            <button class="btn gold" onclick="tpl('خطة 7 أيام للاكتئاب',[
              'تنشيط سلوكي يومي (ممتع + مفيد)',
              'سجلّ أفكار 3 مرات/الأسبوع',
              'تنظيم النوم: ثبات المواقيت + قطع الشاشات'
            ])">⬇️ تنزيل الخطة</button>
          </div>

          <div class="tool">
            <h4>📅 خطة 10 أيام للقلق الاجتماعي</h4>
            <ul>
              <li>بناء سُلّم 10 مواقف من الأسهل للأصعب.</li>
              <li>درجتان يوميًا مع منع الطمأنة.</li>
              <li>تنفّس 4-4-6 صباحًا ومساءً.</li>
            </ul>
            <button class="btn gold" onclick="tpl('خطة 10 أيام للقلق الاجتماعي',[
              'سُلّم 10 مواقف اجتماعية',
              'تنفيذ درجتين يوميًا + منع الطمأنة',
              'تنفّس 4-4-6 صباحًا ومساءً'
            ])">⬇️ تنزيل الخطة</button>
          </div>

          <div class="tool">
            <h4>📅 ERP أسبوعين للوسواس</h4>
            <ul>
              <li>هرم 10 درجات (منع الاستجابة).</li>
              <li>جلسة ERP يومية 60–90 دقيقة.</li>
              <li>مراجعة أسبوعية للتقدّم.</li>
            </ul>
            <button class="btn gold" onclick="tpl('ERP أسبوعين للوسواس',[
              'بناء هرم 10 درجات',
              'ERP يومي 60–90 دقيقة + منع الاستجابة',
              'مراجعة أسبوعية'
            ])">⬇️ تنزيل الخطة</button>
          </div>

          <div class="tool">
            <h4>📅 خطة 14 يوم للتوازن العام</h4>
            <ul>
              <li>تنشيط سلوكي خفيف يومي.</li>
              <li>تنفّس + تأريض مرتين يوميًا.</li>
              <li>مراقبة المزاج وتعديل الروتين.</li>
            </ul>
            <button class="btn gold" onclick="tpl('خطة 14 يوم للتوازن العام',[
              'تنشيط سلوكي خفيف يومي',
              'تنفّس + تأريض مرتين يوميًا',
              'مراقبة المزاج وتعديل الروتين'
            ])">⬇️ تنزيل الخطة</button>
          </div>
        </div>
      </div>

      <!-- t4 -->
      <div id="t4" class="sec">
        <h2>تتبّع التقدّم الأسبوعي</h2>
        <table id="track">
          <thead><tr><th>اليوم</th><th>نشاط ممتع</th><th>نشاط مفيد</th><th>سجلّ أفكار</th><th>ERP/تعرّض</th><th>مزاج صباح</th><th>مزاج مساء</th></tr></thead>
          <tbody></tbody>
        </table>
        <div class="row" style="margin-top:10px">
          <button class="btn" onclick="addRow()">➕ إضافة يوم</button>
          <button class="btn alt" onclick="saveTracking()">💾 حفظ التقدّم (JSON)</button>
        </div>
      </div>

      <!-- t5 -->
      <div id="t5" class="sec">
        <h2>عبارات داعمة وإرشادات</h2>
        <ul>
          <li>«التكرار يبني عادة، والعادة تفتح باب التغيير.»</li>
          <li>قسّم الهدف الكبير إلى خطوات صغيرة قابلة للتنفيذ.</li>
          <li>دوّن ما نجح اليوم ولو كان بسيطًا — التقدّم يُلاحظ.</li>
        </ul>
        <div class="row"><a class="btn gold" href="/book">📅 احجز جلسة</a></div>
      </div>

      <script>
        function openTab(sel){
          document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
          document.querySelectorAll('.sec').forEach(s=>s.classList.remove('active'));
          document.querySelector('.tab[data-target="'+sel+'"]').classList.add('active');
          document.querySelector(sel).classList.add('active');
          history.replaceState(null,'',sel);
        }
        document.querySelectorAll('.tab').forEach(t=>{
          t.addEventListener('click',()=>openTab(t.getAttribute('data-target')));
        });
        if(location.hash && document.querySelector(location.hash)) openTab(location.hash);

        function saveCBT(){
          const picks=[...document.querySelectorAll('#tools input[type=checkbox]:checked')].map(cb=>cb.getAttribute('data-name'));
          const notes=document.getElementById('notes')?.value||'';
          const payload={selected:picks,notes,created_at:new Date().toISOString()};
          const a=document.createElement('a');
          a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));
          a.download='cbt_plan.json'; a.click(); URL.revokeObjectURL(a.href);
        }
        function tpl(name,tasks){
          const payload={template:name,tasks,created_at:new Date().toISOString()};
          const a=document.createElement('a');
          a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));
          a.download=name.replace(/\\s+/g,'_')+'.json'; a.click(); URL.revokeObjectURL(a.href);
        }
        function addRow(){
          const tbody=document.querySelector('#track tbody');
          const r=tbody.insertRow();
          const days=['السبت','الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة'];
          const next=tbody.rows.length-1; const day=days[next%7];
          r.innerHTML='<td>'+day+'</td>'+('<td contenteditable></td>'.repeat(7-1));
        }
        function saveTracking(){
          const rows=[...document.querySelectorAll('#track tbody tr')].map(tr=>[...tr.children].map(td=>td.innerText));
          const payload={week:rows,created_at:new Date().toISOString()};
          const a=document.createElement('a');
          a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));
          a.download='cbt_tracking.json'; a.click(); URL.revokeObjectURL(a.href);
        }
      </script>
    </div>
    """
