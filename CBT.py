# CBT.py — صفحة خطة علاج معرفي سلوكي (سجل أفكار + أهداف + واجبات)

def main():
    return """
    <h1>خطة العلاج المعرفي السلوكي (CBT)</h1>
    <p>املأ السجل التالي بنموذج ABC/سجل الأفكار، وحدد الأهداف والواجبات المنزلية.</p>

    <style>
      .section{background:#fff; border:1px solid #ddd; border-radius:12px; padding:14px; margin:12px 0}
      label{display:block; margin:6px 0}
      input[type=text], input[type=date], textarea{width:100%; padding:8px; border:1px solid #ccc; border-radius:8px}
      textarea{min-height:70px}
      table{width:100%; border-collapse:collapse; margin-top:8px}
      th,td{border:1px solid #eee; padding:8px; text-align:right}
      th{background:#faf7e6}
      .action{margin:12px 6px 0 0; padding:8px 12px; border-radius:10px; border:0; background:#4B0082; color:#fff; font-weight:700}
      .action.gold{background:#FFD700; color:#4B0082}
    </style>

    <div id="cbt">

      <div class="section">
        <h3>1) الأهداف العلاجية</h3>
        <label>هدف قصير المدى: <input type="text" name="goal_short" placeholder="مثال: تقليل نوبات القلق إلى 1/أسبوع"></label>
        <label>هدف متوسط المدى: <input type="text" name="goal_mid" placeholder="تحسين مهارات المواجهة اليومية"></label>
        <label>هدف طويل المدى: <input type="text" name="goal_long" placeholder="العودة للعمل/الدراسة بثبات"></label>
        <label>تاريخ البدء: <input type="date" name="start_date"></label>
      </div>

      <div class="section">
        <h3>2) سجل الأفكار (Thought Record — ABC)</h3>
        <table id="tr">
          <thead>
            <tr>
              <th>الوضع/الموقف (A)</th>
              <th>الفكرة التلقائية (B)</th>
              <th>المشاعر (شدة 0–100)</th>
              <th>الأدلة مع/ضد</th>
              <th>الفكرة المتوازنة (بديلة)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td contenteditable="true" placeholder="مثال: اجتماع في العمل"></td>
              <td contenteditable="true" placeholder="سأفشل أمامهم"></td>
              <td contenteditable="true" placeholder="قلق 80/100"></td>
              <td contenteditable="true" placeholder="مع: ... ضد: ..."></td>
              <td contenteditable="true" placeholder="أنا مستعد وقد أتعلم من أي خطأ"></td>
            </tr>
          </tbody>
        </table>
        <button class="action" onclick="addRow()">إضافة سطر</button>
      </div>

      <div class="section">
        <h3>3) التجارب السلوكية / التعرّض</h3>
        <label>الخطة: <textarea name="behavioral_plan" placeholder="تجربة سلوكية أو تعرّض تدريجي..."></textarea></label>
        <label>المؤشرات/النتائج: <textarea name="behavioral_result" placeholder="ماذا حدث؟ ماذا تعلمت؟"></textarea></label>
      </div>

      <div class="section">
        <h3>4) الواجبات المنزلية</h3>
        <label>الواجب: <input type="text" name="homework" placeholder="تطبيق تمرين تنفس 4×4 مرتين يومياً"></label>
        <label>مستوى الالتزام المتوقع (0–10): <input type="text" name="adherence" placeholder="7/10"></label>
      </div>

      <button class="action" onclick="window.print()">طباعة</button>
      <button class="action gold" onclick="saveCBT()">حفظ JSON</button>
    </div>

    <script>
      function addRow(){
        const tr = document.querySelector('#tr tbody');
        const row = document.createElement('tr');
        for(let i=0;i<5;i++){
          const td = document.createElement('td');
          td.contentEditable = 'true';
          tr.appendChild(row);
          row.appendChild(td);
        }
      }

      function saveCBT(){
        const data = {};
        const root = document.getElementById('cbt');
        // أهداف
        ['goal_short','goal_mid','goal_long','start_date','behavioral_plan','behavioral_result','homework','adherence']
          .forEach(name=>{
            const el = root.querySelector(`[name=\"${name}\"]`);
            data[name] = el ? el.value : '';
          });

        // سجل الأفكار
        data['thought_record'] = [];
        document.querySelectorAll('#tr tbody tr').forEach(tr=>{
          const cells = tr.querySelectorAll('td');
          data['thought_record'].push({
            situation: cells[0]?.innerText || '',
            automatic_thought: cells[1]?.innerText || '',
            feelings: cells[2]?.innerText || '',
            evidence: cells[3]?.innerText || '',
            balanced_thought: cells[4]?.innerText || ''
          });
        });

        const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'cbt_plan.json';
        a.click();
        URL.revokeObjectURL(a.href);
      }
    </script>
    """
