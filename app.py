# app.py — عربي سايكو: رئيسية + دراسة حالة تستدعي DSM.diagnose + طباعة/حفظ
import os, importlib
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ===== الصفحة الرئيسية =====
HTML_HOME = """
<!DOCTYPE html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>عربي سايكو — الرئيسية</title>
<style>
  :root{ --purple:#4B0082; --gold:#FFD700; --white:#ffffff; }
  body{ margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
        background:var(--purple); font-family:"Tajawal","Segoe UI",system-ui,sans-serif; color:var(--white);}
  .card{ background:var(--gold); color:var(--purple); padding:40px 60px; border-radius:20px;
         box-shadow:0 8px 25px rgba(0,0,0,.3); text-align:center; }
  .card h1{margin:0 0 10px; font-size:2rem}
  .brand{font-weight:800; letter-spacing:.5px}
  .btn{ display:block; margin:12px auto; padding:12px 18px; border-radius:14px;
        background:var(--purple); color:var(--white); text-decoration:none; font-weight:700; width:280px; }
  .btn:hover{opacity:.9}
  .copy{margin-top:12px; font-size:.9rem}
</style></head><body>
  <main class="card">
    <div class="brand">عربي سايكو</div>
    <h1>واجهة التشخيص المبدئي</h1>
    <a class="btn" href="/case">📝 دراسة الحالة (البدء)</a>
    <a class="btn" href="/dsm">📘 DSM (مرجع)</a>
    <a class="btn" href="/cbt">🧠 CBT (خطة علاج)</a>
    <a class="btn" href="/addiction">💊 Addiction (الإدمان)</a>
    <div class="copy">© جميع الحقوق محفوظة لعربي سايكو</div>
  </main>
</body></html>
"""

def render_simple_page(content: str, title: str):
    page = f"""
    <!DOCTYPE html><html lang="ar" dir="rtl"><head>
      <meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
      <title>{title}</title>
      <style>
        body{{font-family:"Tajawal","Segoe UI",system-ui,sans-serif; margin:0; background:#faf7e6}}
        .back{{position:fixed; top:16px; right:16px}}
        .back a{{background:#FFD700; color:#4B0082; padding:8px 12px; border-radius:10px; text-decoration:none; font-weight:700}}
        .wrap{{max-width:1000px; margin:40px auto; padding:20px; background:#fff; border:1px solid #eee; border-radius:14px}}
      </style>
    </head><body>
      <div class="back"><a href="/">⬅ الرجوع</a></div>
      <div class="wrap">{content}</div>
    </body></html>
    """
    return render_template_string(page)

@app.get("/")
def home():
    return render_template_string(HTML_HOME)

# صفحات مرجعية إن وجدت لديك CBT/Addiction بــ main()
@app.get("/dsm")
def dsm():
    DSM = importlib.import_module("DSM")
    content = DSM.main() if hasattr(DSM, "main") else "<p>DSM reference.</p>"
    return render_simple_page(content, "DSM — مرجع")

@app.get("/cbt")
def cbt():
    try:
        m = importlib.import_module("CBT")
        content = m.main() if hasattr(m, "main") else "<p>CBT reference.</p>"
    except Exception:
        content = "<p>CBT module غير متوفر.</p>"
    return render_simple_page(content, "CBT — خطة علاج")

@app.get("/addiction")
def addiction():
    try:
        m = importlib.import_module("Addiction")
        content = m.main() if hasattr(m, "main") else "<p>Addiction reference.</p>"
    except Exception:
        content = "<p>Addiction module غير متوفر.</p>"
    return render_simple_page(content, "Addiction — الإدمان")

# ===== دراسة الحالة (Form) =====
FORM_HTML = """
<h1>📝 دراسة الحالة — إدخال الأعراض</h1>
<p class="note">النتيجة تعليمية/إرشادية وليست تشخيصًا طبيًا. إذا كانت الأعراض شديدة، يُرجى مراجعة مختص.</p>

<style>
  .grid{{display:grid; gap:10px; grid-template-columns: repeat(auto-fit, minmax(240px,1fr));}}
  label{{display:block; background:#fafafa; border:1px solid #eee; border-radius:10px; padding:10px}}
  .submit{{margin-top:14px; padding:10px 16px; border-radius:12px; background:#4B0082; color:#fff; border:0; font-weight:700}}
  .note{{font-size:.9rem; color:#555}}
</style>

<form method="post" action="/case">
  <h3>أعراض المزاج</h3>
  <div class="grid">
    <label><input type="checkbox" name="low_mood"> مزاج منخفض</label>
    <label><input type="checkbox" name="anhedonia"> فقدان المتعة</label>
    <label><input type="checkbox" name="sleep_issue"> صعوبات نوم</label>
    <label><input type="checkbox" name="appetite_change"> تغيّر شهية</label>
    <label><input type="checkbox" name="fatigue"> إرهاق/خمول</label>
  </div>

  <h3>أعراض القلق</h3>
  <div class="grid">
    <label><input type="checkbox" name="worry"> قلق مستمر</label>
    <label><input type="checkbox" name="tension"> توتر جسدي</label>
    <label><input type="checkbox" name="focus_issue"> صعوبة تركيز</label>
    <label><input type="checkbox" name="restlessness"> تململ</label>
  </div>

  <h3>هلع/اجتماعي/وسواس/صدمات</h3>
  <div class="grid">
    <label><input type="checkbox" name="panic_attacks"> نوبات هلع</label>
    <label><input type="checkbox" name="fear_of_attacks"> خوف من تكرار النوبات</label>
    <label><input type="checkbox" name="panic_avoidance"> تجنّب بسبب النوبات</label>
    <label><input type="checkbox" name="social_avoid"> تجنب اجتماعي</label>
    <label><input type="checkbox" name="fear_judgment"> خوف من تقييم الآخرين</label>
    <label><input type="checkbox" name="obsessions"> أفكار ملحّة</label>
    <label><input type="checkbox" name="compulsions"> أفعال قهرية</label>
    <label><input type="checkbox" name="trauma_event"> تعرّض لحدث صادمي</label>
    <label><input type="checkbox" name="flashbacks"> استرجاع/فلاشباك</label>
    <label><input type="checkbox" name="nightmares"> كوابيس</label>
    <label><input type="checkbox" name="trauma_avoid"> تجنّب مرتبط بالحدث</label>
    <label><input type="checkbox" name="hypervigilance"> يقظة مفرطة</label>
  </div>

  <h3>مزاج مرتفع/ذهان</h3>
  <div class="grid">
    <label><input type="checkbox" name="elevated_mood"> مزاج مرتفع/مبالغ</label>
    <label><input type="checkbox" name="impulsivity"> اندفاع/تهوّر</label>
    <label><input type="checkbox" name="grandiosity"> شعور بالعظمة</label>
    <label><input type="checkbox" name="decreased_sleep_need"> قلة الحاجة للنوم</label>
    <label><input type="checkbox" name="hallucinations"> هلوسات</label>
    <label><input type="checkbox" name="delusions"> أوهام ثابتة</label>
    <label><input type="checkbox" name="disorganized_speech"> اضطراب كلام/تفكير</label>
    <label><input type="checkbox" name="functional_decline"> تدهور وظيفي</label>
  </div>

  <h3>اضطرابات أكل/انتباه/تعاطي</h3>
  <div class="grid">
    <label><input type="checkbox" name="restriction"> تقييد الأكل</label>
    <label><input type="checkbox" name="underweight"> نقص وزن ملحوظ</label>
    <label><input type="checkbox" name="body_image_distort"> صورة جسد مشوّهة</label>
    <label><input type="checkbox" name="binges"> نوبات أكل كبيرة</label>
    <label><input type="checkbox" name="compensatory"> سلوك تعويضي (تقيؤ/مسهلات/رياضة مفرطة)</label>

    <label><input type="checkbox" name="inattention"> عدم انتباه</label>
    <label><input type="checkbox" name="hyperactivity"> فرط حركة</label>
    <label><input type="checkbox" name="impulsivity_symp"> اندفاعية</label>
    <label><input type="checkbox" name="since_childhood"> منذ الطفولة</label>
    <label><input type="checkbox" name="functional_impair"> تأثير وظيفي</label>

    <label><input type="checkbox" name="craving"> اشتهاء</label>
    <label><input type="checkbox" name="tolerance"> تحمّل</label>
    <label><input type="checkbox" name="withdrawal"> انسحاب</label>
    <label><input type="checkbox" name="use_despite_harm"> استخدام رغم الضرر</label>
  </div>

  <h3>تقدير الشدة (0–10)</h3>
  <label>الشدّة العامة: <input type="number" name="distress" min="0" max="10" value="5"></label>

  <button class="submit" type="submit">اعرض الترشيح</button>
</form>
"""

RESULT_HTML = """
<h1>📌 ترشيحات أولية</h1>
<ul style="line-height:1.9">{items}</ul>
<p class="note">هذه النتائج تعليمية/إرشادية وليست تشخيصًا طبيًا. يُفضّل مراجعة مختص للتقييم الكامل.</p>

<button onclick="window.print()" style="margin-top:10px;padding:10px 16px;border-radius:12px;background:#4B0082;color:#fff;border:0;font-weight:700">
  طباعة النتيجة
</button>
<button onclick='downloadJSON()' style="margin-top:10px;padding:10px 16px;border-radius:12px;background:#FFD700;color:#4B0082;border:0;font-weight:700">
  حفظ JSON
</button>

<script>
function downloadJSON(){
  const data = {items: Array.from(document.querySelectorAll('li')).map(li => li.innerText)};
  const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'diagnosis_result.json';
  a.click();
  URL.revokeObjectURL(a.href);
}
</script>
"""

@app.route("/case", methods=["GET", "POST"])
def case():
    if request.method == "GET":
        return render_simple_page(FORM_HTML, "دراسة الحالة")
    # POST: جمع المدخلات
    data = {k: v for k, v in request.form.items()}
    # checkboxes ترسل "on" للقيم المؤشرة: نحتفظ بها كما هي
    try:
        DSM = importlib.import_module("DSM")
        picks = DSM.diagnose(data) if hasattr(DSM, "diagnose") else [("تعذر التشخيص", "DSM.diagnose غير متوفر", 0.0)]
    except Exception as e:
        picks = [("خطأ في الاستدعاء", str(e), 0.0)]

    items = "".join([f"<li><b>{name}</b> — {why} <small>(Score: {score:.0f})</small></li>" for name, why, score in picks])
    return render_simple_page(RESULT_HTML.format(items=items), "نتيجة الترشيح")

# صحة الخدمة
@app.get("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
