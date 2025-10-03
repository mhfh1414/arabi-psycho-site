# CBT.py — خطة علاج احترافية مع حفظ تلقائي
HTML = """
<h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
<p class="muted">ورقة عمل عملية للطباعة والحفظ PDF. (يتم الحفظ تلقائيًا على جهازك)</p>

<form id="cbtForm" onsubmit="event.preventDefault();window.print()">
  <h2>1) تعريف المشكلة</h2>
  <textarea name="p1" style="width:100%;height:90px" placeholder="الوصف المختصر للموقف/المشكلة"></textarea>

  <h2>2) الأفكار التلقائية السلبية</h2>
  <textarea name="p2" style="width:100%;height:90px" placeholder="ما الفكرة؟ متى تظهر؟ الدليل الذي تعتمد عليه؟"></textarea>

  <h2>3) الأدلة مع/ضد</h2>
  <div class="grid">
    <textarea name="p3a" style="width:100%;height:90px" placeholder="أدلة تؤيد الفكرة"></textarea>
    <textarea name="p3b" style="width:100%;height:90px" placeholder="أدلة تنقض الفكرة"></textarea>
  </div>

  <h2>4) إعادة البناء المعرفي</h2>
  <textarea name="p4" style="width:100%;height:80px" placeholder="صياغة بديلة متوازنة وواقعية"></textarea>

  <h2>5) خطة سلوكية (SMART)</h2>
  <div class="grid">
    <input name="s1" placeholder="الخطوة المحددة" />
    <input name="s2" placeholder="المكان/الزمن" />
    <input name="s3" placeholder="التكرار/المدة" />
    <input name="s4" placeholder="المعيار للنجاح" />
  </div>

  <h2>6) مقياس الشدة (0–10)</h2>
  <div class="grid">
    <label>قبل: <input name="pre" type="number" min="0" max="10" value="6"/></label>
    <label>بعد: <input name="post" type="number" min="0" max="10" value="3"/></label>
  </div>

  <h2>7) متابعة أسبوعية</h2>
  <div class="grid">
    <input name="w1" placeholder="عدد مرات التطبيق" />
    <input name="w2" placeholder="عائق وكيف تعاملت معه" />
  </div>

  <button class="submit" type="submit">🖨️ طباعة</button>
</form>

<script>
  const f = document.getElementById('cbtForm');
  const key = 'cbt_sheet_autosave_v1';
  function load(){ try{ const d=JSON.parse(localStorage.getItem(key)||'{}'); for(const k in d){ if(f[k]) f[k].value=d[k]; } }catch(e){} }
  function save(){ const d={}; for(const el of f.elements){ if(el.name) d[el.name]=el.value; } localStorage.setItem(key, JSON.stringify(d)); }
  f.addEventListener('input', save); window.addEventListener('DOMContentLoaded', load);
</script>
"""

def main() -> str:
  return HTML
