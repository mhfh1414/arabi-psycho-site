# CBT.py — صفحة تفاعلية مختصرة للطباعة (Works offline)

HTML = """
<h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
<p class="muted">نموذج عملي للطباعة/الحفظ PDF. للاستخدام التعليمي والإرشادي.</p>

<h2>1) تعريف المشكلة</h2>
<textarea style="width:100%;height:90px" placeholder="الوصف المختصر للموقف/المشكلة"></textarea>

<h2>2) الأفكار التلقائية السلبية</h2>
<textarea style="width:100%;height:90px" placeholder="ما الفكرة؟ متى تظهر؟"></textarea>

<h2>3) الأدلة مع/ضد</h2>
<div class="grid">
  <textarea style="width:100%;height:90px" placeholder="أدلة تؤيد الفكرة"></textarea>
  <textarea style="width:100%;height:90px" placeholder="أدلة تنقض الفكرة"></textarea>
</div>

<h2>4) الفكرة البديلة المتوازنة</h2>
<textarea style="width:100%;height:80px" placeholder="صياغة أكثر واقعية وتوازناً"></textarea>

<h2>5) خطة سلوكية (SMART)</h2>
<div class="grid">
  <input placeholder="الخطوة 1" />
  <input placeholder="المدة/التكرار" />
  <input placeholder="المكان" />
  <input placeholder="التوقيت" />
</div>

<h2>6) مقياس الشدة (0–10)</h2>
<div class="grid">
  <label>قبل: <input type="number" min="0" max="10" value="6"/></label>
  <label>بعد: <input type="number" min="0" max="10" value="3"/></label>
</div>

<h2>7) متابعة أسبوعية (اختياري)</h2>
<div class="grid">
  <input placeholder="عدد مرات التطبيق هذا الأسبوع"/>
  <input placeholder="عائق واجهته وكيف تعاملت معه"/>
</div>

<button class="submit" onclick="window.print()">🖨️ طباعة الخطة</button>
"""

def main() -> str:
    return HTML
