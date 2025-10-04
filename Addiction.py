# Addiction.py — خطة علاج الإدمان (تعليمي/إرشادي)
def main():
    return """
    <h1>خطة علاج الإدمان</h1>
    <p class="muted">ثلاث مراحل: إزالة السموم (Detox) → التأهيل (Rehab) → الوقاية من الانتكاس (Relapse Prevention).</p>
    <style>
      .sec{background:#fff;border:1px solid #eee;border-radius:14px;padding:14px;margin:12px 0}
      .grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
      label{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:8px}
      .btn{margin-top:10px;padding:10px 14px;border-radius:12px;border:0;background:#4B0082;color:#fff;font-weight:700}
      .btn.gold{background:#FFD700;color:#4B0082}
      textarea,input[type=text]{width:100%;padding:8px;border:1px solid #ddd;border-radius:8px}
    </style>

    <div class="sec">
      <h3>1) نوع المادة وشدّة الاضطراب</h3>
      <div class="grid">
        <label><input type="checkbox" id="alcohol"> كحول</label>
        <label><input type="checkbox" id="opioid"> أفيونات</label>
        <label><input type="checkbox" id="stimulant"> منبهات</label>
        <label><input type="checkbox" id="cannabis"> قنب</label>
        <label><input type="checkbox" id="sedative"> مهدئات/منومات</label>
      </div>
      <label>الشدّة (خفيف/متوسط/شديد):<br><input type="text" id="severity" placeholder="مثال: متوسط"></label>
      <label>محفزات/مواقف خطرة:<br><textarea id="triggers"></textarea></label>
    </div>

    <div class="sec">
      <h3>2) إزالة السموم (Detox)</h3>
      <div class="grid">
        <label><input type="checkbox" id="med_supervision"> إشراف طبي</label>
        <label><input type="checkbox" id="withdrawal_plan"> خطة إدارة الانسحاب</label>
        <label><input type="checkbox" id="support_person"> شخص داعم/أسرة</label>
      </div>
      <label>ملاحظات/أدوية مًقترحة (تعليمي):<br><textarea id="detox_notes"></textarea></label>
    </div>

    <div class="sec">
      <h3>3) التأهيل (Rehab)</h3>
      <div class="grid">
        <label><input type="checkbox" id="cbt_prog"> برنامج CBT</label>
        <label><input type="checkbox" id="group_therapy"> مجموعات دعم</label>
        <label><input type="checkbox" id="family_therapy"> علاج أسري</label>
        <label><input type="checkbox" id="vocational"> تأهيل مهني/دراسي</label>
      </div>
      <label>أهداف شهرية:<br><textarea id="rehab_goals"></textarea></label>
    </div>

    <div class="sec">
      <h3>4) الوقاية من الانتكاس</h3>
      <div class="grid">
        <label><input type="checkbox" id="rp_plan"> خطة إدارة المواقف الخطرة</label>
        <label><input type="checkbox" id="urge_surf"> مهارة ركوب الرغبة (Urge Surfing)</label>
        <label><input type="checkbox" id="accountability"> شريك متابعة/مسؤولية</label>
      </div>
      <label>قائمة اتصالات الطوارئ:<br><textarea id="emergency"></textarea></label>
    </div>

    <div style="margin-top:10px">
      <button class="btn" onclick="window.print()">طباعة</button>
      <button class="btn gold" onclick="saveAdd()">حفظ JSON</button>
    </div>

    <script>
      function saveAdd(){
        const ids=['alcohol','opioid','stimulant','cannabis','sedative','severity','triggers','med_supervision','withdrawal_plan','support_person','detox_notes','cbt_prog','group_therapy','family_therapy','vocational','rehab_goals','rp_plan','urge_surf','accountability','emergency'];
        const data={}; ids.forEach(id=>{const el=document.getElementById(id); data[id]= (el.type==='checkbox')? el.checked : (el.value||'');});
        const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
        const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='addiction_plan.json'; a.click(); URL.revokeObjectURL(a.href);
      }
    </script>
    """
