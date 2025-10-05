# CBT.py — تمارين وخطط عملية قابلة للحفظ (HTML + JS)
def main():
    return """
    <h1>🧠 العلاج المعرفي السلوكي (CBT) — أدوات عملية</h1>
    <p>اختر الأداة المناسبة، دوّن تطبيقاتك، ثم احفظها كملف JSON لتشاركها مع مختصك.</p>

    <style>
      details{background:#fff;border:1px solid #eee;border-radius:12px;margin:10px 0;padding:10px}
      summary{cursor:pointer;font-weight:800;color:#4B0082}
      .grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
      textarea,input{width:100%;border:1px solid #ddd;border-radius:10px;padding:8px}
      .btn{padding:10px 14px;border-radius:12px;border:0;background:#4B0082;color:#fff;font-weight:700}
      .btn.gold{background:#FFD700;color:#4B0082}
      label{font-weight:700}
      .box{background:#fafafa;border:1px dashed #eee;border-radius:12px;padding:10px}
    </style>

    <div id="cbt">

      <details open>
        <summary>1) تنشيط سلوكي (للانخفاض والانعزال)</summary>
        <div class="grid">
          <div class="box">
            <label>قائمة أنشطة (ممتع/مفيد/قيمة):</label>
            <textarea name="ba_list" rows="4" placeholder="مثال: مشي 15د، اتصال بصديق، قراءة سورة/كتاب، أعمال منزلية بسيطة..."></textarea>
          </div>
          <div class="box">
            <label>خطة اليوم:</label>
            <input name="ba_day" placeholder="٣ أنشطة قصيرة موزعة على اليوم"/>
          </div>
        </div>
      </details>

      <details>
        <summary>2) تحدّي الأفكار (القلق/الاكتئاب)</summary>
        <div class="grid">
          <div class="box"><label>الموقف</label><textarea name="c_sit" rows="3"></textarea></div>
          <div class="box"><label>الفكرة التلقائية</label><textarea name="c_th" rows="3"></textarea></div>
          <div class="box"><label>الدليل مع/ضد</label><textarea name="c_ev" rows="3"></textarea></div>
          <div class="box"><label>الفكرة المتوازنة</label><textarea name="c_new" rows="3"></textarea></div>
        </div>
      </details>

      <details>
        <summary>3) تعرّض تدريجي + منع استجابة (الهلع/الوسواس/الرهاب)</summary>
        <div class="box">
          <label>سلم التعرّض (من الأقل للأعلى):</label>
          <textarea name="erp_steps" rows="4" placeholder="10 درجات، مثال للرهاب الاجتماعي: تحية جار، سؤال موظف، مكالمة قصيرة، عرض أمام شخصين..."></textarea>
          <p>أثناء التعرّض: تنفّس 4-4-6 — ومنع سلوكيات الأمان (الهروب/الطمأنة).</p>
        </div>
      </details>

      <details>
        <summary>4) تنظيم الانتباه (ADHD)</summary>
        <div class="grid">
          <div class="box">
            <label>أهم 3 مهام اليوم</label>
            <textarea name="adhd_top3" rows="3"></textarea>
          </div>
          <div class="box">
            <label>جلسات بومودورو</label>
            <input name="adhd_pomo" placeholder="مثال: 4×(25د عمل + 5د راحة)"/>
          </div>
          <div class="box">
            <label>تقليل مشتتات</label>
            <textarea name="adhd_env" rows="3" placeholder="هاتف صامت، تبويب واحد، مؤقت مرئي..."></textarea>
          </div>
        </div>
      </details>

      <details>
        <summary>5) التأريض والصدمات (PTSD)</summary>
        <div class="box">
          <label>خطة تأريض 5-4-3-2-1</label>
          <textarea name="ptsd_ground" rows="3" placeholder="5 أشياء تراها، 4 تلمسها، 3 تسمعها، 2 تشمها، 1 تتذوقها"></textarea>
          <label>سرد آمن (اختياري)</label>
          <textarea name="ptsd_story" rows="3"></textarea>
        </div>
      </details>

      <div style="margin-top:10px">
        <button class="btn" onclick="savePlan()">حفظ خطة CBT (JSON)</button>
        <button class="btn gold" onclick="window.print()">طباعة</button>
      </div>
    </div>

    <script>
      function savePlan(){
        const root=document.getElementById('cbt');
        const data={};
        root.querySelectorAll('textarea,input').forEach(el=>data[el.name]=el.value||"");
        const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
        const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='cbt_plan.json'; a.click(); URL.revokeObjectURL(a.href);
      }
    </script>
    """
