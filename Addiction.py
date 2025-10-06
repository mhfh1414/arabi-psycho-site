# Addiction.py — برنامج الإدمان: فحص ذاتي مبسّط + مسار تعافٍ + تنزيل خطة

def main():
    return """
    <div class='card'>
      <h1>🚭 برنامج الإدمان — مسار تعافٍ واضح</h1>
      <p class='small'>علاج نفسي افتراضي — أدوات مبسطة لدعم اتخاذ القرار، لا تغني عن متابعة مختص عند الحاجة.</p>

      <style>
        .sec{margin:10px 0;padding:10px;background:#fafafa;border:1px solid #eee;border-radius:12px}
        .grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
        label.chk{display:block;background:#fff;border:1px solid #eee;border-radius:10px;padding:8px}
        .row{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}
      </style>

      <div class="sec">
        <h2>1) فحص ذاتي سريع (CAGE-AID مبسّط)</h2>
        <div id="cage" class="grid">
          <label class="chk"><input type="checkbox" data-q="Cut down"> فكرت أن تُخفّف أو تقلّل؟</label>
          <label class="chk"><input type="checkbox" data-q="Annoyed"> انزعجت من انتقاد الآخرين لاستخدامك؟</label>
          <label class="chk"><input type="checkbox" data-q="Guilty"> شعرت بالذنب؟</label>
          <label class="chk"><input type="checkbox" data-q="Eye-opener"> احتجت مادةً صباحًا لتبدأ اليوم؟</label>
        </div>
        <div class="note">نتيجة مبسّطة: إجابتان أو أكثر = احتمال مشكلة استخدام يستحق متابعة.</div>
      </div>

      <div class="sec">
        <h2>2) سلّم الاستعداد للتغيير</h2>
        <div class="grid">
          <label class="chk"><input type="radio" name="stage" value="Precontemplation"> لستُ مقتنعًا بالحاجة للتغيير</label>
          <label class="chk"><input type="radio" name="stage" value="Contemplation"> أفكّر بالتغيير</label>
          <label class="chk"><input type="radio" name="stage" value="Preparation"> أستعد خلال أسبوع/شهر</label>
          <label class="chk"><input type="radio" name="stage" value="Action"> بدأتُ بالفعل</label>
          <label class="chk"><input type="radio" name="stage" value="Maintenance"> أحافظ على الامتناع/الالتزام</label>
        </div>
      </div>

      <div class="sec">
        <h2>3) مسار التعافي المقترح</h2>
        <div class="grid">
          <div class="tile">
            <h3>Detox (سحب منظّم)</h3>
            <ul>
              <li>استشارة طبية عند وجود انسحاب شديد أو أمراض مصاحبة.</li>
              <li>دعم سوائل/تغذية ونوم منتظم.</li>
              <li>خطة يومين–أسبوع حسب المادة والجرعة.</li>
            </ul>
          </div>
          <div class="tile">
            <h3>Rehab (إعادة تأهيل)</h3>
            <ul>
              <li>جلسات فردية/جماعية، مهارات رفض، إدارة محفزات.</li>
              <li>CBT خاص بالإدمان + بدائل صحية للمتعة.</li>
              <li>مشاركة الأسرة/الداعمين إن أمكن.</li>
            </ul>
          </div>
          <div class="tile">
            <h3>Relapse Prevention (منع الانتكاس)</h3>
            <ul>
              <li>تعرّف مبكّر على إشارات الخطر وخطة طوارئ.</li>
              <li>روتين صحي: نوم/رياضة/علاقات مساندة.</li>
              <li>مراجعات دوريّة وتعديل الخطة.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="sec">
        <h2>4) خطتي الشخصية</h2>
        <label>أهداف قصيرة المدى
          <textarea id="goals" rows="3" placeholder="مثال: أسبوع بدون مادة، حضور جلستين دعم..."></textarea>
        </label>
        <label>محفّزات أتوقعها
          <textarea id="triggers" rows="3" placeholder="أماكن/أشخاص/مشاعر..."></textarea>
        </label>
        <label>دعم متاح
          <textarea id="supports" rows="3" placeholder="أسماء داعمين/أنشطة بديلة..."></textarea>
        </label>
        <div class="row">
          <button class="btn" onclick="saveAddictionPlan()">💾 حفظ الخطة (JSON)</button>
          <button class="btn alt" onclick="window.print()">🖨️ طباعة</button>
          <a class="btn gold" href="/book">📅 احجز جلسة</a>
          <a class="btn" href="/cbt">🧠 انتقل لأدوات CBT</a>
        </div>
      </div>

      <script>
        function saveAddictionPlan(){
          const cage=[...document.querySelectorAll('#cage input[type=checkbox]:checked')].map(x=>x.getAttribute('data-q'));
          const stage=(document.querySelector('input[name=stage]:checked')||{}).value||'';
          const goals=document.getElementById('goals').value||'';
          const triggers=document.getElementById('triggers').value||'';
          const supports=document.getElementById('supports').value||'';
          const payload={cage,stage,goals,triggers,supports,created_at:new Date().toISOString()};
          const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
          const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='addiction_plan.json'; a.click();
          URL.revokeObjectURL(a.href);
        }
      </script>

      <div class="note" style="margin-top:12px">
        <b>عبارة دعم:</b> «التغيير سلسلة خطوات صغيرة — والتمسُّك بها هو القوة الحقيقة.»
      </div>
    </div>
    """
