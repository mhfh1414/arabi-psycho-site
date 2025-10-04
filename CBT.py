# CBT.py — صفحة CBT تفاعلية (تعليمي/إرشادي)
def main():
    return """
    <h1>العلاج المعرفي السلوكي (CBT)</h1>
    <p class="muted">خطة عملية مبسطة: تحديد الأفكار التلقائية، إعادة الهيكلة المعرفية، تجارب سلوكية، تفعيل سلوكي، وتقنيات قلق.</p>
    <style>
      .card{background:#fff;border:1px solid #eee;border-radius:14px;padding:14px;margin:12px 0}
      .grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
      textarea,input[type=text]{width:100%;padding:8px;border:1px solid #ddd;border-radius:8px}
      .btn{margin-top:10px;padding:10px 14px;border-radius:12px;border:0;background:#4B0082;color:#fff;font-weight:700}
      .btn.gold{background:#FFD700;color:#4B0082}
      .pill{display:inline-block;background:#faf7e6;border:1px solid #eee;border-radius:999px;padding:6px 10px;margin:4px 6px}
    </style>

    <div class="card">
      <h3>1) مذكّرة الأفكار (Thought Record)</h3>
      <div class="grid">
        <div><label>الموقف:<br><input type="text" id="situation"></label></div>
        <div><label>المشاعر (0–100):<br><input type="text" id="emotions" placeholder="قلق 70%، حزن 40%"></label></div>
      </div>
      <label>الفكرة التلقائية:<br><textarea id="automatic"></textarea></label>
      <label>الأدلة مع/ضد:<br><textarea id="evidence"></textarea></label>
      <label>الفكرة البديلة المتوازنة:<br><textarea id="balanced"></textarea></label>
    </div>

    <div class="card">
      <h3>2) تفعيل سلوكي</h3>
      <div class="pill">رياضة</div><div class="pill">تواصل اجتماعي</div><div class="pill">نوم منتظم</div><div class="pill">هواية</div>
      <label>خطة الأسبوع:<br><textarea id="ba_plan" placeholder="متى/أين/مع من/كم دقيقة؟"></textarea></label>
    </div>

    <div class="card">
      <h3>3) تجارب سلوكية (للقناعات)</h3>
      <label>الاعتقاد المستهدف:<br><input type="text" id="belief" placeholder="سيفشل الجميع إن أخطأت"></label>
      <label>التجربة المقترحة:<br><textarea id="experiment"></textarea></label>
      <label>النتائج/الملاحظات:<br><textarea id="exp_result"></textarea></label>
    </div>

    <div class="card">
      <h3>4) أدوات قلق سريعة</h3>
      <div class="pill">تنفس 4-7-8</div><div class="pill">أرض نفسك 5-4-3-2-1</div><div class="pill">يقظة ذهنية 3 دقائق</div>
      <label>مفضلاتي:<br><textarea id="anx_tools"></textarea></label>
    </div>

    <div style="margin-top:10px">
      <button class="btn" onclick="window.print()">طباعة</button>
      <button class="btn gold" onclick="saveCBT()">حفظ JSON</button>
    </div>

    <script>
      function saveCBT(){
        const get=(id)=>document.getElementById(id)?.value||"";
        const data={
          situation:get('situation'), emotions:get('emotions'), automatic:get('automatic'),
          evidence:get('evidence'), balanced:get('balanced'),
          ba_plan:get('ba_plan'), belief:get('belief'), experiment:get('experiment'),
          exp_result:get('exp_result'), anx_tools:get('anx_tools')
        };
        const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
        const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='cbt_plan.json'; a.click(); URL.revokeObjectURL(a.href);
      }
    </script>
    """
