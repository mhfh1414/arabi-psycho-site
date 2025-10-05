# Addiction.py — برنامج علاج الإدمان: مراحل + خطة منع انتكاسة قابلة للحفظ
def main():
    return """
    <h1>🚭 برنامج علاج الإدمان</h1>
    <p>خطة بثلاث مراحل: إزالة السُمّية (Detox) → التأهيل (Rehab) → منع الانتكاسة (Relapse Prevention).</p>

    <style>
      .grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
      .box{background:#fafafa;border:1px solid #eee;border-radius:12px;padding:12px}
      textarea,input{width:100%;border:1px solid #ddd;border-radius:10px;padding:8px}
      .btn{padding:10px 14px;border-radius:12px;border:0;background:#4B0082;color:#fff;font-weight:700}
      .btn.gold{background:#FFD700;color:#4B0082}
      details{background:#fff;border:1px solid #eee;border-radius:12px;margin:10px 0;padding:10px}
      summary{cursor:pointer;font-weight:800;color:#4B0082}
    </style>

    <div id="addict">
      <details open>
        <summary>1) إزالة السُمّية (Detox) — بإشراف طبي</summary>
        <div class="grid">
          <div class="box">
            <b>معلومات طبية/أدوية (يملؤها طبيب)</b>
            <textarea name="detox_med" rows="3" placeholder="أدوية انسحاب، علامات حيوية، متابعة المخاطر..."></textarea>
          </div>
          <div class="box">
            <b>دعم يومي</b>
            <textarea name="detox_support" rows="3" placeholder="شخص داعم، إزالة محفزات/مواد من المنزل، سوائل وغذاء..."></textarea>
          </div>
        </div>
      </details>

      <details>
        <summary>2) التأهيل (Rehab)</summary>
        <div class="grid">
          <div class="box">
            <b>روتين يومي صحّي</b>
            <textarea name="rehab_routine" rows="3" placeholder="نوم منتظم، رياضة خفيفة، عبادات/تأمل، تواصل اجتماعي صحي..."></textarea>
          </div>
          <div class="box">
            <b>بدائل فورية للاشتهاء</b>
            <textarea name="rehab_altern" rows="3" placeholder="ماء بارد، استحمام، اتصال بصديق، مشي 10د، تمرين تنفس..."></textarea>
          </div>
        </div>
      </details>

      <details>
        <summary>3) منع الانتكاسة (Relapse Prevention)</summary>
        <div class="grid">
          <div class="box">
            <b>إشارات إنذار مبكر</b>
            <textarea name="rp_triggers" rows="3" placeholder="أماكن/أشخاص/مشاعر..."></textarea>
          </div>
          <div class="box">
            <b>خطة 24 ساعة</b>
            <textarea name="rp_24h" rows="3" placeholder="ماذا أفعل في أوّل 24 ساعة عند الخطر؟"></textarea>
          </div>
          <div class="box">
            <b>شبكة دعم واتصال</b>
            <textarea name="rp_supports" rows="3" placeholder="أسماء/أرقام داعمين، مواعيد مجموعات دعم..."></textarea>
          </div>
        </div>
      </details>

      <div style="margin-top:10px">
        <button class="btn" onclick="saveAdd()">حفظ خطة الإدمان (JSON)</button>
        <button class="btn gold" onclick="window.print()">طباعة</button>
      </div>
    </div>

    <script>
      function saveAdd(){
        const root=document.getElementById('addict');
        const data={}; root.querySelectorAll('textarea,input').forEach(el=>data[el.name]=el.value||"");
        const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
        const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='addiction_plan.json'; a.click(); URL.revokeObjectURL(a.href);
      }
    </script>
    """
