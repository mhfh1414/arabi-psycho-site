# CBT.py — أدوات وخطط CBT: اختيارية + خطط جاهزة + تنزيل JSON/طباعة

def main():
    return """
    <div class='card'>
      <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
      <p class='small'>علاج نفسي افتراضي — اختر الأدوات المناسبة لك، ثم احفظ الخطة كملف JSON أو اطبعها. تتوفر أيضًا خطط جاهزة بنقرة.</p>

      <style>
        .plan{display:flex;gap:10px;align-items:flex-start;background:#fafafa;border:1px solid #eee;border-radius:12px;padding:10px;margin:8px 0}
        .plan h4{margin:.2rem 0 .2rem}
        .row{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}
        .col{flex:1;min-width:260px}
        .hint{font-size:.9rem;opacity:.85}
      </style>

      <div class="grid">
        <div class="col">
          <h2>اختر أدواتك</h2>

          <div id="plans">
            <div class="plan"><label><input type="checkbox" data-name="تنشيط سلوكي (BA)">
              <div><h4>تنشيط سلوكي (BA)</h4><div class="hint">قائمة أنشطة ممتعة ومُفيدة. نفّذ 2–3 يوميًا وقيّم المزاج قبل/بعد.</div></div></label></div>

            <div class="plan"><label><input type="checkbox" data-name="سجل الأفكار (TR)">
              <div><h4>سجل الأفكار (Thought Record)</h4><div class="hint">الموقف—الفكرة—الدليل معها/ضدها—الفكرة المتوازنة—شدة الانفعال قبل/بعد.</div></div></label></div>

            <div class="plan"><label><input type="checkbox" data-name="ERP للوسواس">
              <div><h4>ERP للوسواس القهري</h4><div class="hint">هرم مواقف، تعرّض تدريجي 60–90 دقيقة، مع منع الاستجابة.</div></div></label></div>

            <div class="plan"><label><input type="checkbox" data-name="تعرّض اجتماعي">
              <div><h4>تعرّض اجتماعي (الرهاب الاجتماعي)</h4><div class="hint">سُلّم 10 درجات: تواصل بصري → سؤال بسيط → مكالمة → عرض قصير…</div></div></label></div>

            <div class="plan"><label><input type="checkbox" data-name="تنظيم النوم">
              <div><h4>تنظيم النوم</h4><div class="hint">ثبات مواقيت، ضوء صباحي، إيقاف الشاشات قبل النوم بساعة.</div></div></label></div>

            <div class="plan"><label><input type="checkbox" data-name="حل المشكلات">
              <div><h4>حل المشكلات</h4><div class="hint">تعريف المشكلة → أفكار حلول → اختيار وتنفيذ → مراجعة.</div></div></label></div>

            <div class="plan"><label><input type="checkbox" data-name="تنفّس + تأريض">
              <div><h4>تنفّس 4-4-6 + التأريض 5-4-3-2-1</h4><div class="hint">5 دقائق تنفّس + يقظة حسية لخفض الاستثارة.</div></div></label></div>

            <div class="plan"><label><input type="checkbox" data-name="مراقبة المزاج">
              <div><h4>مراقبة المزاج</h4><div class="hint">مقياس 0–10 صباحًا/مساءً مع ملاحظة المحفزات.</div></div></label></div>
          </div>

          <div class="tile" style="margin-top:10px">
            <label>ملاحظات الخطة
              <textarea id="notes" rows="4" placeholder="مثال: 20 دقيقة مشي يوميًا، سجل أفكار ثلاث مرات بالأسبوع…"></textarea>
            </label>
          </div>

          <div class="row">
            <button class="btn" onclick="savePlan()">💾 حفظ خطتي (JSON)</button>
            <button class="btn alt" onclick="window.print()">🖨️ طباعة</button>
          </div>
        </div>

        <div class="col">
          <h2>📦 خطط جاهزة</h2>
          <div class="row">
            <button class="btn gold" onclick="downloadTemplate('خطة 7 أيام للاكتئاب', [
              'تنشيط سلوكي يومي (نشاط ممتع + نشاط مفيد)',
              'تنظيم النوم (ثبات المواقيت + قطع الشاشات ساعة قبل النوم)',
              'سجل أفكار 3 مرات/الأسبوع'
            ])">⬇️ اكتئاب (7 أيام)</button>

            <button class="btn gold" onclick="downloadTemplate('خطة 10 أيام للقلق الاجتماعي', [
              'سلم تعرّض اجتماعي من 10 درجات',
              'تجربة درجتين يوميًا مع منع الطمأنة',
              'تنفّس 4-4-6 صباحًا ومساءً'
            ])">⬇️ قلق اجتماعي (10 أيام)</button>

            <button class="btn gold" onclick="downloadTemplate('خطة ERP أسبوعين للوسواس', [
              'بناء هرم مواقف 10 درجات',
              'ERP يومي 60 دقيقة مع منع الاستجابة',
              'مراجعة أسبوعية للتقدّم'
            ])">⬇️ ERP (أسبوعين)</button>

            <button class="btn gold" onclick="downloadTemplate('خطة 14 يوم للتوازن العام', [
              'تنشيط سلوكي خفيف يومي',
              'تمرين تنفّس + تأريض مرتين يوميًا',
              'مراقبة المزاج وتعديل الروتين'
            ])">⬇️ توازن عام (14 يوم)</button>
          </div>

          <div class="note" style="margin-top:12px">
            <b>عبارة داعمة:</b> «خطوة صغيرة اليوم تُسهّل خطوة أكبر غدًا.»
          </div>
          <div style="margin-top:10px">
            <a class="btn gold" href="/book">📅 احجز جلسة</a>
            <a class="btn" href="/addiction">🚭 انتقل لبرنامج الإدمان</a>
          </div>
        </div>
      </div>

      <script>
        function savePlan(){
          const picks=[...document.querySelectorAll('#plans input[type=checkbox]:checked')]
                      .map(cb=>cb.getAttribute('data-name'));
          const notes=document.getElementById('notes').value||'';
          const payload={selected_plans:picks,notes:notes,created_at:new Date().toISOString()};
          const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
          const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='cbt_plan.json'; a.click();
          URL.revokeObjectURL(a.href);
        }
        function downloadTemplate(name,tasks){
          const payload={template:name,tasks:tasks,created_at:new Date().toISOString()};
          const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
          const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name.replace(/\\s+/g,'_')+'.json'; a.click();
          URL.revokeObjectURL(a.href);
        }
      </script>
    </div>
    """
