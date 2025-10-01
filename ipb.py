# ipb.py — Case Study simple form (returns HTML string)

def main():
    return """
    <h1>نموذج دراسة حالة — Intake</h1>
    <p>عبّئ الحقول التالية ثم اطبع النموذج أو احفظه PDF.</p>

    <form id="caseForm" onsubmit="return false" style="background:#fff; border:1px solid #ddd; padding:16px; border-radius:12px">
      <h3>البيانات العامة</h3>
      <label>الاسم الكامل: <input type="text" name="name" required></label><br><br>
      <label>العمر: <input type="number" name="age" min="5" max="120"></label>
      <label style="margin-inline-start:20px">الجنس:
        <select name="gender"><option>ذكر</option><option>أنثى</option></select>
      </label><br><br>

      <h3>التواصل</h3>
      <label>الهاتف: <input type="tel" name="phone"></label>
      <label style="margin-inline-start:20px">البريد: <input type="email" name="email"></label><br><br>

      <h3>الشكوى الرئيسية</h3>
      <textarea name="chief" rows="4" style="width:100%" placeholder="صف المشكلة الأساسية، مدة ظهورها، شدتها..."></textarea><br><br>

      <h3>تاريخ طبي/نفسي مختصر</h3>
      <textarea name="history" rows="4" style="width:100%" placeholder="سوابق طبية/نفسية، أدوية، دخول سابق للمستشفى..."></textarea><br><br>

      <h3>قياس سريع (نعم/لا)</h3>
      <label><input type="checkbox" name="sleep"> صعوبات نوم</label>
      <label style="margin-inline-start:14px"><input type="checkbox" name="appetite"> تغيّر شهية</label>
      <label style="margin-inline-start:14px"><input type="checkbox" name="panic"> نوبات هلع</label>
      <label style="margin-inline-start:14px"><input type="checkbox" name="suicidal"> أفكار انتحارية</label><br><br>

      <h3>تقدير ذاتي (0–10)</h3>
      القلق: <input type="number" name="anxiety" min="0" max="10" value="0">
      المزاج: <input type="number" name="mood" min="0" max="10" value="5">
      التركيز: <input type="number" name="focus" min="0" max="10" value="5"><br><br>

      <h3>ملاحظات المعالج</h3>
      <textarea name="notes" rows="4" style="width:100%" placeholder="ملخص الانطباع الأولي، عوامل الخطر/الحماية، توصيات مبدئية..."></textarea><br><br>

      <button onclick="printForm()">طباعة</button>
      <button onclick="downloadJSON()">حفظ JSON</button>
    </form>

    <script>
      function printForm(){
        window.print();
      }
      function downloadJSON(){
        const form = document.getElementById('caseForm');
        const data = {};
        Array.from(form.elements).forEach(el=>{
          if(!el.name) return;
          if(el.type==='checkbox'){ data[el.name] = el.checked; }
          else { data[el.name] = el.value; }
        });
        const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'case_study.json';
        a.click();
        URL.revokeObjectURL(a.href);
      }
    </script>
    """
