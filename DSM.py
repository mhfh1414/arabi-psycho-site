# DSM.py — صفحة DSM مختصرة منظمة (HTML + طباعة/JSON)

def main():
    return """
    <h1>الدليل التشخيصي DSM-5 — نظرة منظمة</h1>
    <p>اختر الفئة لعرض قائمة الاضطرابات الشائعة. بإمكانك وضع ملاحظات ثم طباعتها أو حفظها JSON.</p>

    <style>
      details{background:#fff; border:1px solid #ddd; border-radius:10px; margin:10px 0; padding:10px}
      summary{cursor:pointer; font-weight:700; color:#4B0082}
      .note{width:100%; min-height:70px}
      .action{margin:12px 6px 0 0; padding:8px 12px; border-radius:10px; border:0; background:#4B0082; color:#fff; font-weight:700}
      .action.gold{background:#FFD700; color:#4B0082}
      .grid{display:grid; gap:8px; grid-template-columns: repeat(auto-fit, minmax(220px,1fr));}
      label{display:block; background:#fafafa; border:1px solid #eee; border-radius:8px; padding:8px}
    </style>

    <div id="dsm">
      <details open>
        <summary>الاضطرابات العصابية/القلقية</summary>
        <div class="grid">
          <label><input type="checkbox" name="anxiety_gad"> اضطراب القلق العام (GAD)</label>
          <label><input type="checkbox" name="panic"> اضطراب الهلع</label>
          <label><input type="checkbox" name="phobia"> الرهاب المحدد</label>
          <label><input type="checkbox" name="social"> قلق/رهاب اجتماعي</label>
          <label><input type="checkbox" name="ocd"> الوسواس القهري (OCD)</label>
          <label><input type="checkbox" name="ptsd"> اضطراب ما بعد الصدمة (PTSD)</label>
        </div>
      </details>

      <details>
        <summary>الاضطرابات المزاجية</summary>
        <div class="grid">
          <label><input type="checkbox" name="mdd"> اكتئاب جسيم (MDD)</label>
          <label><input type="checkbox" name="pdd"> عسر المزاج (PDD)</label>
          <label><input type="checkbox" name="bipolar1"> ثنائي القطب I</label>
          <label><input type="checkbox" name="bipolar2"> ثنائي القطب II</label>
          <label><input type="checkbox" name="cyclothymic"> دوروية المزاج</label>
        </div>
      </details>

      <details>
        <summary>اضطرابات الشخصية</summary>
        <div class="grid">
          <label><input type="checkbox" name="paranoid"> شخصية زورانية</label>
          <label><input type="checkbox" name="schizoid"> انعزالية</label>
          <label><input type="checkbox" name="schizotypal"> فصامية نمط</label>
          <label><input type="checkbox" name="antisocial"> معادية للمجتمع</label>
          <label><input type="checkbox" name="borderline"> حدّية</label>
          <label><input type="checkbox" name="histrionic"> هستيرية</label>
          <label><input type="checkbox" name="narcissistic"> نرجسية</label>
          <label><input type="checkbox" name="avoidant"> تجنبية</label>
          <label><input type="checkbox" name="dependent"> اعتمادية</label>
          <label><input type="checkbox" name="ocpd"> قسرية-قهريّة شخصية</label>
        </div>
      </details>

      <details>
        <summary>اضطرابات طيف الفصام</summary>
        <div class="grid">
          <label><input type="checkbox" name="schizophrenia"> فصام</label>
          <label><input type="checkbox" name="schizoaffective"> فصامي وجداني</label>
          <label><input type="checkbox" name="brief_psychotic"> ذهان وجيز</label>
          <label><input type="checkbox" name="delusional"> وهامي</label>
        </div>
      </details>

      <details>
        <summary>اضطرابات عصبية نمائية</summary>
        <div class="grid">
          <label><input type="checkbox" name="adhd"> فرط الحركة وتشتت الانتباه (ADHD)</label>
          <label><input type="checkbox" name="asd"> طيف التوحد (ASD)</label>
          <label><input type="checkbox" name="learning"> صعوبات تعلّم</label>
          <label><input type="checkbox" name="tic"> اضطرابات العرات/تورات</label>
        </div>
      </details>

      <details>
        <summary>تعاطي المواد والإدمان</summary>
        <div class="grid">
          <label><input type="checkbox" name="alcohol"> اضطراب تعاطي الكحول</label>
          <label><input type="checkbox" name="opioid"> أفيونات</label>
          <label><input type="checkbox" name="stimulant"> منبهات</label>
          <label><input type="checkbox" name="cannabis"> قنّب</label>
          <label><input type="checkbox" name="sedative"> مهدئات/منومات</label>
        </div>
      </details>

      <h3>ملاحظات تشخيصية</h3>
      <textarea class="note" name="notes" placeholder="ضع المبررات ودليل الأعراض والمدة والاستبعاد التفريقي..."></textarea><br>
      <button class="action" onclick="window.print()">طباعة</button>
      <button class="action gold" onclick="saveDSM()">حفظ JSON</button>
    </div>

    <script>
      function saveDSM(){
        const root = document.getElementById('dsm');
        const data = {};
        root.querySelectorAll('input[type=checkbox]').forEach(cb=>{
          data[cb.name] = cb.checked;
        });
        data['notes'] = root.querySelector('textarea[name=notes]').value || '';
        const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'dsm_selection.json';
        a.click();
        URL.revokeObjectURL(a.href);
      }
    </script>
    """
