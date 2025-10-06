# Addiction.py — برنامج علاج الإدمان: اختيار مادة → خطة Detox/Rehab/Relapse مخصصة

def main():
    return """
<h1>🚭 برنامج علاج الإدمان (اختياري)</h1>
<p>اختر المادة أولًا ليتم تحميل خطة مناسبة بثلاث مراحل: إزالة السمّية (Detox) ← التأهيل (Rehab) ← منع الانتكاسة (Relapse Prevention).</p>

<style>
  :root{ --p:#4B0082; --g:#FFD700 }
  .row{display:grid; gap:10px; grid-template-columns: repeat(auto-fit, minmax(240px,1fr)); margin:10px 0}
  details{background:#fff; border:1px solid #eee; border-radius:12px; padding:10px; margin:12px 0}
  summary{cursor:pointer; font-weight:800; color:var(--p)}
  .box{width:100%; min-height:140px; border:1px solid #ddd; border-radius:10px; padding:10px}
  .btn{margin:10px 6px 0 0; padding:9px 14px; border-radius:12px; border:0; font-weight:800; background:var(--p); color:#fff}
  .gold{background:var(--g); color:var(--p)}
  .warn{background:#fff7d1; border:1px dashed #e5c100; padding:8px 12px; border-radius:10px}
</style>

<div id="submod">
  <div class="row">
    <label>المادة (اختياري):
      <select id="sub">
        <option value="">— اختر —</option>
        <option value="alcohol">الكحول</option>
        <option value="opioid">الأفيونات</option>
        <option value="stimulant">المنبّهات</option>
        <option value="cannabis">القنّب</option>
        <option value="benzo">المهدئات/البنزوديازيبينات</option>
        <option value="nicotine">النيكوتين (تدخين)</option>
      </select>
    </label>
  </div>

  <p class="warn">⚠️ مرحلة <b>إزالة السمّية (Detox)</b> يجب أن تكون بإشراف طبي عند الكحول/الأفيونات/البنزوديازيبينات أو أي عوامل خطر.</p>

  <details open>
    <summary>1) إزالة السمّية (Detox) — بإشراف طبي</summary>
    <textarea id="detox" class="box" placeholder="سيتم ملؤها تلقائيًا حسب المادة المختارة"></textarea>
  </details>

  <details>
    <summary>2) التأهيل (Rehab) — 4–12 أسبوعًا</summary>
    <textarea id="rehab" class="box" placeholder="خطة التأهيل، مهارات التعامل، علاج فردي/جماعي"></textarea>
  </details>

  <details>
    <summary>3) منع الانتكاسة (Relapse Prevention)</summary>
    <textarea id="relapse" class="box" placeholder="مثيرات/أشخاص/أماكن، خطة الطوارئ 24 ساعة، شبكة الدعم"></textarea>
  </details>

  <div class="row">
    <button class="btn gold" onclick="fillBySub()">إدراج القوالب حسب المادة</button>
    <button class="btn" onclick="saveAdd()">حفظ الخطة (JSON)</button>
    <button class="btn" onclick="window.print()">طباعة</button>
  </div>
</div>

<script>
const TPL = {
  alcohol: {
    detox:
`الكحول — Detox:
- تقييم CIWA-Ar + ثيامين قبل الجلوكوز، سوائل، مراقبة علامات انسحاب.
- أدوية حسب الطبيب: بنزوديازيبينات قصيرة المفعول/كلورديازيبوكسيد.
- فحص مخاطر نوبات/هذيان انسحابي.`,
    rehab:
`Rehab:
- علاج فردي/جماعي، مهارات رفض العَرض، إعادة بناء الروتين.
- علاج مرافِق للاكتئاب/قلق إن وُجد. نشاط بديل يومي (رياضة/مجتمع).
- دعم عائلي وتثقيف حول المشغلات.`,
    relapse:
`منع الانتكاسة:
- محفّزات: الحفلات/الأصدقاء/التوتر. خطة بدائل: مشروبات خالية/انسحاب اجتماعي آمن.
- دوائي (يقرره الطبيب): نالتريكسون/أكامبروسيت عند الحاجة.
- خطة طوارئ 24 ساعة واتصال داعم.`
  },
  opioid: {
    detox:
`الأفيونات — Detox:
- تقييم انسحاب COWS، سوائل/تغذية.
- بدء برنامج استبدال (قرار طبي): بوبـرينورفين/ميثادون.
- معالجة ألم/أرق داعمة، وقاية جرعة زائدة (نالوكسون متاح للأسرة).`,
    rehab:
`Rehab:
- علاج فردي/جماعي، إدارة رغبة (اشتهاء) ببدائل صحية.
- توظيف/تعليم/علاقات: أهداف أسبوعية واقعية.
- متابعة التزام دوائي وتثقيف الأسرة.`,
    relapse:
`منع الانتكاسة:
- محفزات: ألم/توتر/أصدقاء سابقون. بيئة آمنة، تخلّي عن أدوات الحقن.
- خطة طوارئ: تواصل فوري، تذكير بالهدف والقيم، حضور مجموعات دعم.`
  },
  stimulant: {
    detox:
`المنبّهات — Detox:
- لا توجد بروتوكولات دوائية قياسية؛ دعم النوم والتغذية وترطيب.
- مراقبة اكتئاب ما بعد الانسحاب/أفكار انتحارية.`,
    rehab:
`Rehab:
- CBT للطلب/الإغراء، نشاط بدني منظّم، روتين يومي، بدائل ممتعة.
- معالجة مشاعر الخواء/الملل، تدريب مهارات اجتماعية.`,
    relapse:
`منع الانتكاسة:
- محفّزات: سهر/حفلات/توتر. خطة بدائل سريعة: تواصل داعم/جري قصير/حمّام دافئ.
- حذف جهات/مسارات قديمة، خط ساخن دعم.`
  },
  cannabis: {
    detox:
`القنّب — Detox (غالبًا داعم):
- أرق/تهيج/أحلام حيّة: روتين نوم، تقليل منبّهات، رياضة خفيفة.`,
    rehab:
`Rehab:
- تحديد وظائف التعاطي (ملل/قلق/اجتماعي) وبناء بدائل.
- تعرّض لمثيرات بدون استخدام + تأمّل/تنفّس 4-4-6.`,
    relapse:
`منع الانتكاسة:
- أماكن/أصدقاء/روائح محفّزة — خطة تجنّب وبدائل.
- يوميات إنجازات قصيرة + مراقبة المزاج.`
  },
  benzo: {
    detox:
`البنزوديازيبينات — Detox:
- تخفيض تدريجي بطيء تحت إشراف طبي لتجنب نوبات/ارتكاس.
- تحويل إلى بديل طويل المفعول وفق قرار الطبيب + جدول نقص 5–10% كل 1–2 أسبوع.`,
    rehab:
`Rehab:
- إدارة قلق بـ CBT (تعرّض بين الجلسات، تنفّس، يقظة ذهنية).
- تدريب على النوم الصحي دون مهدئات، شبكة دعم.`,
    relapse:
`منع الانتكاسة:
- تجنّب صرف جديد بدون ضرورة، بطاقة تنبيه طبية.
- خطّة بدائل: جلسة تنفّس/تأريض/اتصال داعم عند اشتداد القلق.`
  },
  nicotine: {
    detox:
`النيكوتين:
- لصقات/علكة بديلة وفق إرشادات، تحديد تاريخ الإقلاع، إزالة المنبّهات (قدّاحات/علب).`,
    rehab:
`Rehab:
- عادِل النفس عند الزلات (ليس فشلًا)، فم مشغول (لبان/خضار)، شرب ماء، رياضة خفيفة.
- تتبّع الرغبة 0–10 ودقائقها (غالبًا تزول خلال 3–5 دقائق).`,
    relapse:
`منع الانتكاسة:
- مواقف حرجة: قهوة/قيادة/بعد الطعام — بدائل محددة مسبقًا.
- مكافآت أسبوعية لنجاحات صغيرة.`
  }
};

function fillBySub(){
  const s = document.getElementById('sub').value;
  if(!s || !TPL[s]){ alert('اختر مادة أولًا'); return; }
  document.getElementById('detox').value   = TPL[s].detox;
  document.getElementById('rehab').value   = TPL[s].rehab;
  document.getElementById('relapse').value = TPL[s].relapse;
}

function saveAdd(){
  const data={
    substance: document.getElementById('sub').value,
    detox: document.getElementById('detox').value || '',
    rehab: document.getElementById('rehab').value || '',
    relapse: document.getElementById('relapse').value || ''
  };
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='addiction_plan.json'; a.click();
  URL.revokeObjectURL(a.href);
}
</script>
"""
