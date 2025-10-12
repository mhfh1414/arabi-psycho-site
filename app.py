app.py — نسخة كاملة تعمل على Render

تتضمن دراسة الحالة + خطة CBT + واجهة مرتبة + حفظ وتحميل JSON

from flask import Flask, request, make_response import json

app = Flask(name)

============================ HTML القالب العام ============================

HTML_BASE = """<!doctype html>

<html lang='ar' dir='rtl'>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{title}</title>
<style>
  body{{font-family:system-ui,Segoe UI,Tahoma;max-width:900px;margin:24px auto;padding:16px;line-height:1.7;background:#fafafa;color:#222}}
  .card{{border:1px solid #ddd;border-radius:14px;padding:18px;margin:12px 0;background:white;box-shadow:0 1px 5px rgba(0,0,0,.05)}}
  label{{display:block;margin-top:10px;font-weight:600}}
  input,textarea,select,button{{width:100%;padding:10px;margin-top:6px;border:1px solid #bbb;border-radius:10px;font-size:15px}}
  button{{cursor:pointer;background:#008cff;color:white;border:none;margin-top:14px}}
  a.button{{display:inline-block;padding:10px 14px;border:1px solid #008cff;border-radius:10px;text-decoration:none;color:#008cff;margin-top:8px}}
  pre{{background:#f5f5f5;padding:10px;border-radius:12px}}
</style>
<body>
<h2>{heading}</h2>
<div class='card'>{content}</div>
<p style='opacity:.7'>© عربي سايكو</p>
<script>
  document.querySelectorAll('input, textarea, select').forEach(el=>{{
    el.disabled=false;el.style.pointerEvents='auto';
  }});
</script>
</body>
</html>"""============================ الصفحة الرئيسية ============================

@app.get("/") def home(): return HTML_BASE.format( title="الرئيسية", heading="مرحباً بك في عربي سايكو", content=""" <p>اختر ما تريد:</p> <a class='button' href='/case'>🧠 دراسة الحالة</a> <a class='button' href='/cbt'>💬 خطة CBT</a> """ )

============================ دراسة الحالة ============================

@app.get("/case") def case_form(): form = """ <form method='POST' action='/case'> <label>الاسم الكامل</label> <input name='name' required>

<label>العمر</label>
  <input name='age' type='number' min='1' max='120' required>

  <label>رقم التواصل</label>
  <input name='phone' type='tel' placeholder='05xxxxxxxx'>

  <label>الأعراض الحالية</label>
  <textarea name='symptoms' rows='4'></textarea>

  <label>مدة المعاناة</label>
  <select name='duration'>
    <option value='أيام'>أيام</option>
    <option value='أسابيع'>أسابيع</option>
    <option value='أشهر'>أشهر</option>
  </select>

  <label>هل تتناول أدوية حالياً؟</label>
  <select name='meds'>
    <option>لا</option>
    <option>نعم</option>
  </select>

  <button type='submit'>حفظ وإظهار النتيجة</button>
</form>
"""
return HTML_BASE.format(title="دراسة الحالة", heading="نموذج دراسة الحالة", content=form)

@app.post("/case") def case_submit(): data = {k: request.form.get(k,"") for k in ["name","age","phone","symptoms","duration","meds"]} pretty = json.dumps(data, ensure_ascii=False, indent=2) content = f""" <h3>✅ تم الاستلام</h3> <pre>{pretty}</pre> <form method='GET' action='/case/download'> {''.join([f"<input type='hidden' name='{k}' value='{v}'>" for k,v in data.items()])} <button type='submit'>تنزيل JSON</button> </form> <a class='button' href='/case'>رجوع للنموذج</a> """ return HTML_BASE.format(title="نتيجة الحالة", heading="النتيجة", content=content)

@app.get("/case/download") def case_download(): payload = {k: request.args.get(k,"") for k in ["name","age","phone","symptoms","duration","meds"]} blob = json.dumps(payload, ensure_ascii=False, indent=2) r = make_response(blob) r.headers['Content-Type'] = 'application/json; charset=utf-8' r.headers['Content-Disposition'] = 'attachment; filename="case.json"' return r

============================ خطة CBT ============================

@app.get("/cbt") def cbt_form(): form = """ <form method='POST' action='/cbt'> <label>الموقف</label> <textarea name='situation' rows='3' required></textarea>

<label>الفكرة التلقائية</label>
  <textarea name='thought' rows='2' required></textarea>

  <label>شدة الانفعال (0–100)</label>
  <input name='emotion_intensity' type='number' min='0' max='100' required>

  <label>الدليل مع/ضد الفكرة</label>
  <textarea name='evidence' rows='3'></textarea>

  <label>إعادة الهيكلة المعرفية (فكرة بديلة)</label>
  <textarea name='reframe' rows='3' required></textarea>

  <label>شدة الانفعال بعد التعديل (0–100)</label>
  <input name='post_intensity' type='number' min='0' max='100' required>

  <button type='submit'>حفظ الخطة</button>
</form>
"""
return HTML_BASE.format(title="خطة CBT", heading="نموذج CBT", content=form)

@app.post("/cbt") def cbt_submit(): data = {k: request.form.get(k,"") for k in ["situation","thought","emotion_intensity","evidence","reframe","post_intensity"]} pretty = json.dumps(data, ensure_ascii=False, indent=2) content = f""" <h3>✅ تم حفظ خطة CBT</h3> <pre>{pretty}</pre> <form method='GET' action='/cbt/download'> {''.join([f"<input type='hidden' name='{k}' value='{v}'>" for k,v in data.items()])} <button type='submit'>تنزيل JSON</button> </form> <a class='button' href='/cbt'>رجوع للنموذج</a> """ return HTML_BASE.format(title="نتيجة CBT", heading="النتيجة", content=content)

@app.get("/cbt/download") def cbt_download(): payload = {k: request.args.get(k,"") for k in ["situation","thought","emotion_intensity","evidence","reframe","post_intensity"]} blob = json.dumps(payload, ensure_ascii=False, indent=2) r = make_response(blob) r.headers['Content-Type'] = 'application/json; charset=utf-8' r.headers['Content-Disposition'] = 'attachment; filename="cbt.json"' return r

============================ تشغيل محلي أو عبر Render ============================

if name == 'main': app.run(host='0.0.0.0', port=5000)
 
