# Addiction.py — صفحة علاج الإدمان (HTML + طباعة/JSON)

def main():
    return """
    <h1>خطة علاج الإدمان</h1>
    <p>هذه الصفحة تلخص أنواع المواد، مراحل العلاج، عوامل الخطر/الحماية، وخطة المتابعة.</p>

    <style>
      .section{background:#fff; border:1px solid #ddd; border-radius:12px; padding:14px; margin:12px 0}
      label{display:block; margin:6px 0}
      textarea{width:100%; min-height:70px; padding:8px; border:1px solid #ccc; border-radius:8px}
      .grid{display:grid; gap:8px; grid-template-columns: repeat(auto-fit, minmax(220px,1fr));}
      .action{margin:12px 6px 0 0; padding:8px 12px; border-radius:10px; border:0; background:#4B0082; color:#fff; font-weight:700}
      .action.gold{background:#FFD700; color:#4B0082}
    </style>

    <div id="addiction">

      <div class="section">
        <h3>1) أنواع المواد</h3>
        <div class="grid">
          <label><input type="checkbox" name="alcohol"> كحول</label>
          <label><input type="checkbox" name="opioids"> أفيونات (هيروين، مورفين)</label>
          <label><input type="checkbox" name="stimulants"> منبهات (أمفيتامين، كوكايين)</label>
          <label><input type="checkbox" name="cannabis"> حشيش / ماريجوانا</label>
          <label><input type="checkbox" name="sedatives"> مهدئات / منومات</label>
          <label><input type="checkbox" name="nicotine"> نيكوتين (تدخين)</label>
          <label><input type="checkbox" name="hallucinogens"> مهلوسات (LSD، فطر)</label>
        </div>
      </div>

      <div class="section">
        <h3>2) مراحل العلاج</h3>
        <div class="grid">
          <label><input type="checkbox" name="detox"> إزالة السموم (Detox)</label>
          <label><input type="checkbox" name="rehab"> إعادة التأهيل (Rehabilitation)</label>
          <label><input type="checkbox" name="therapy"> العلاج النفسي (CBT، دعم جماعي)</label>
          <label><input type="checkbox" name="relapse"> الوقاية من الانتكاس (Relapse Prevention)</label>
          <label><input type="checkbox" name="followup"> المتابعة طويلة المدى</label>
        </div>
      </div>

      <div class="section">
        <h3>3) عوامل الخطر / الحماية</h3>
        <textarea name="risk" placeholder="عوامل الخطر: ضغط أقران، تاريخ عائلي، صدمات..."></textarea>
        <textarea name="protect" placeholder="عوامل الحماية: دعم أسري، التزام ديني، بيئة صحية..."></textarea>
      </div>

      <div class="section">
        <h3>4) خطة المتابعة</h3>
        <textarea name="plan" placeholder="ضع خطة للمتابعة: جلسات، علاج داعم، متابعة طبية..."></textarea>
      </div>

      <button class="action" onclick="window.print()">طباعة</button>
      <button class="action gold" onclick="saveAddiction()">حفظ JSON</button>
    </div>

    <script>
      function saveAddiction(){
        const root = document.getElementById('addiction');
        const data = {};
        root.querySelectorAll('input[type=checkbox]').forEach(cb=>{
          data[cb.name] = cb.checked;
        });
        ['risk','protect','plan'].forEach(name=>{
          const el = root.querySelector(`[name=\"${name}\"]`);
          data[name] = el ? el.value : '';
        });
        const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'addiction_plan.json';
        a.click();
        URL.revokeObjectURL(a.href);
      }
    </script>
    """
