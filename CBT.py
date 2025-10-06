# CBT.py — خطط وتمارين CBT جاهزة مع قوالب وإخراج JSON/طباعة

def main():
    return """
<h1>🧠 العلاج المعرفي السلوكي (CBT) — أدوات عملية</h1>
<p>اختر الأداة المناسبة، اضغط "إدراج قالب"، ثم عدّل بنقاطك. يمكنك حفظ الخطة كملف JSON أو طباعتها.</p>

<style>
  :root{ --p:#4B0082; --g:#FFD700 }
  details{background:#fff; border:1px solid #eee; border-radius:12px; padding:10px; margin:12px 0}
  summary{cursor:pointer; font-weight:800; color:var(--p)}
  .box{width:100%; min-height:150px; border:1px solid #ddd; border-radius:10px; padding:10px}
  .action{margin:10px 6px 0 0; padding:9px 14px; border-radius:12px; border:0; font-weight:800; background:var(--p); color:#fff}
  .alt{background:#5b22a6}
  .gold{background:var(--g); color:var(--p)}
  .grid{display:grid; gap:10px; grid-template-columns: repeat(auto-fit, minmax(240px,1fr));}
  .hint{background:#fff7d1; border:1px dashed #e5c100; padding:8px 12px; border-radius:10px}
</style>

<div id="cbt">

  <div class="hint">عبارات مُحفِّزة: أنت لست وحدك — خطوة صغيرة ثابتة اليوم أفضل من انتظار الكمال. التقدّم أهم من الكمال.</div>

  <details open>
    <summary>1) تنشيط سلوكي (للإحباط/الاكتئاب)</summary>
    <textarea id="ba" class="box" placeholder="اكتب جدول نشاطات موجّهة بالقيم (ممتع/مفيد/قيمة)..."></textarea><br>
    <button class="action" onclick="tplBA()">إدراج قالب</button>
  </details>

  <details>
    <summary>2) سجل الأفكار (تحدّي الأفكار السلبية)</summary>
    <textarea id="cr" class="box" placeholder="موقف → فكرة تلقائية → دليل معها/ضدّها → فكر بديل → شدّة الشعور"></textarea><br>
    <button class="action" onclick="tplCR()">إدراج قالب</button>
  </details>

  <details>
    <summary>3) تعرّض ومنع الاستجابة ERP (للوسواس القهري)</summary>
    <textarea id="erp" class="box" placeholder="سلّم قلق من 0–100، 10 محفزات تصاعدية، مع منع الاستجابة"></textarea><br>
    <button class="action" onclick="tplERP()">إدراج قالب</button>
  </details>

  <details>
    <summary>4) تعرّض اجتماعي/هلع + تنفّس 4-4-6</summary>
    <textarea id="exp" class="box" placeholder="مواقف اجتماعية/هلع بسلّم صعوبة، تعرّض تدريجي، منع سلوك الأمان"></textarea><br>
    <button class="action" onclick="tplEXP()">إدراج قالب</button>
  </details>

  <details>
    <summary>5) تأريض وتنظيم بعد الصدمة (PTSD)</summary>
    <textarea id="pts" class="box" placeholder="تقنية 5-4-3-2-1، روتين نوم، كتابة سرد آمن تدريجيًا"></textarea><br>
    <button class="action" onclick="tplPTS()">إدراج قالب</button>
  </details>

  <details>
    <summary>6) تنظيم الانتباه (ADHD) — بومودورو</summary>
    <textarea id="adhd" class="box" placeholder="روتين صباحي، 3 أولويات، جلسات 25-5، بيئة قليلة مشتّتات"></textarea><br>
    <button class="action" onclick="tplADHD()">إدراج قالب</button>
  </details>

  <details>
    <summary>7) نظافة النوم وإدارة الإيقاع</summary>
    <textarea id="sleep" class="box" placeholder="مواعيد ثابتة، تعريض للضوء صباحًا، تقليل كافيين، طقوس قبل النوم"></textarea><br>
    <button class="action" onclick="tplSLEEP()">إدراج قالب</button>
  </details>

  <div class="grid">
    <button class="action gold" onclick="savePlan()">حفظ الخطة (JSON)</button>
    <button class="action alt" onclick="window.print()">طباعة</button>
  </div>
</div>

<script>
function tplBA(){
  document.getElementById('ba').value =
`هدف الأسبوع: رفع النشاط 30% وتقليل العزلة.
قائمة أنشطة (ممتع/مفيد/قيمة):
- ممتع: 15 دقيقة مشي خفيف، 10 دقائق موسيقى، مكالمة صديق.
- مفيد: غسيل ملابس، ترتيب سطح المكتب، مراجعة بريد.
- قيمة: قراءة صفحة من القرآن/كتاب قيم، مساعدة أحد بالبيت.
قاعدة البدء الصغير: أقل من 10 دقائق لكل نشاط.
قياس المزاج يوميًا 0–10 قبل/بعد.`;
}
function tplCR(){
  document.getElementById('cr').value =
`اليوم: __ / __
الموقف: ______________________
الفكرة التلقائية: "______________________"
الدليل معها: ____________ / الدليل ضدّها: ____________
التحريف المعرفي المحتمل: تعميم/تطنيش الإيجابي/كارثية/قراءة أفكار/يجب/أبيض-أسود
فكر بديل متوازن: "______________________"
شدّة الشعور قبل %___ وبعد %___`;
}
function tplERP(){
  document.getElementById('erp').value =
`قائمة ERP (0–100):
10- لمس مقبض الباب 10 ثوانٍ بدون غسل.
20- لمس الطاولة العامة دقيقة.
40- لمس صنبور الحمام 30 ثانية.
60- لمس حذاء ثم لمس الهاتف.
80- لمس سلة المهملات/أرض الحمام والجلوس 5 دقائق.
قاعدة: ممنوع أي طقوس/تطمين حتى يهبط القلق ≤ 30. تسجيل الزمن والنتيجة.`;
}
function tplEXP(){
  document.getElementById('exp').value =
`قائمة التعرّض:
10- سؤال بائع عن سلعة.
20- إرسال رسالة قصيرة لمعارف.
40- محادثة 3 دقائق مع زميل.
60- مشاركة رأي قصير في مجموعة.
80- إلقاء فقرة 2 دقائق أمام 3 أشخاص.
تنفّس 4-4-6 (شهيق 4، حبس 4، زفير 6) × 5 قبل التعرّض. منع سلوك الأمان (الهروب/التطمين).`;
}
function tplPTS(){
  document.getElementById('pts').value =
`تأريض 5-4-3-2-1: اذكر 5 أشياء تراها، 4 تلمسها، 3 تسمعها، 2 تشمها، 1 تتذوّقها.
روتين ثابت: نوم/استيقاظ، وجبات، رياضة خفيفة.
سرد تدريجي: كتابة القصة على أجزاء قصيرة مع توقف آمن، مراقبة شدة الانزعاج.
شبكة دعم: شخص موثوق + موعد أسبوعي.`;
}
function tplADHD(){
  document.getElementById('adhd').value =
`صباحًا: 3 أولويات فقط. مؤقّت بومودورو 25-5 × 4 ثم استراحة 20.
البيئة: مكتب خالٍ، إشعارات صامتة، سماعات.
إدارة المهام: تقسيم كل مهمة إلى خطوات 10 دقائق.
المساء: مراجعة ما تم + تجهيز غدًا.`;
}
function tplSLEEP(){
  document.getElementById('sleep').value =
`ثابت: وقت نوم/استيقاظ يومي، ضوء صباحي 10 دقائق، آخر كافيين قبل 2 ظهرًا.
قبل النوم: حمام دافئ/قراءة ورقية/دعاء، بدون شاشات 60 دقيقة.
الغرفة: ظلام/برودة خفيفة/هادئة. إذا لم تنم خلال 20 دقيقة، انهض لعمل هادئ وارجع.`;
}
function savePlan(){
  const ids=['ba','cr','erp','exp','pts','adhd','sleep'];
  const data={}; ids.forEach(id=>data[id]=document.getElementById(id).value||'');
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='cbt_plan.json'; a.click();
  URL.revokeObjectURL(a.href);
}
</script>
"""
