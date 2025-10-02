# app.py — عربي سايكو: رئيسية + دراسة حالة + DSM + تواصل (تيليجرام/واتس)
import os, importlib
from flask import Flask, render_template_string, request

app = Flask(__name__)

# روابط التواصل (من متغيرات البيئة أو قيم افتراضية)
TELEGRAM_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WHATSAPP_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966500000000?text=%D8%B9%D9%85%D9%8A%D9%84%20%D8%B9%D8%B1%D8%A8%D9%8A%20%D8%B3%D8%A7%D9%8A%D9%83%D9%88")

# ===== الصفحة الرئيسية =====
HTML_HOME = f"""
<!DOCTYPE html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>عربي سايكو — الرئيسية</title>
<style>
  :root{{ --purple:#4B0082; --gold:#FFD700; --white:#ffffff; }}
  *{{box-sizing:border-box}}
  body{{ margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
        background:var(--purple); font-family:"Tajawal","Segoe UI",system-ui,sans-serif; color:var(--white);}}
  .card{{ background:var(--gold); color:var(--purple); padding:44px 60px; border-radius:22px;
         box-shadow:0 10px 30px rgba(0,0,0,.35); text-align:center; width:min(92vw,640px) }}
  .brand{{font-weight:800; letter-spacing:.3px; opacity:.9}}
  .title{{margin:.4rem 0 1rem; font-size:2.1rem}}
  .btn{{ display:block; margin:12px auto; padding:12px 18px; border-radius:14px;
        background:var(--purple); color:var(--white); text-decoration:none; font-weight:700; width:100%; max-width:320px }}
  .btn:hover{{opacity:.92}}
  .row{{display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:8px}}
  .btn.alt{{background:#5b22a6}}
  .btn.contact{{background:#1e1b4b}}
  .btn.whats{{background:#25D366; color:#fff}}
  .btn.tg{{background:#229ED9; color:#fff}}
  .copy{{margin-top:14px; font-size:.9rem; opacity:.85}}
</style></head><body>
  <main class="card">
    <div class="brand">عربي سايكو</div>
    <h1 class="title">واجهة التشخيص المبدئي</h1>
    <a class="btn" href="/case">📝 دراسة الحالة</a>
    <a class="btn alt" href="/dsm">📘 DSM (مرجع)</a>
    <div class="row">
      <a class="btn tg" href="{TELEGRAM_URL}" target="_blank" rel="noopener">✈️ تواصل تيليجرام</a>
      <a class="btn whats" href="{WHATSAPP_URL}" target="_blank" rel="noopener">🟢 تواصل واتساب</a>
    </div>
    <a class="btn contact" href="/contact">📞 صفحة التواصل</a>
    <div class="copy">© جميع الحقوق محفوظة لعربي سايكو</div>
  </main>
</body></html>
"""

def shell_page(content: str, title: str):
    page = f"""
    <!DOCTYPE html><html lang="ar" dir="rtl"><head>
      <meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
      <title>{title}</title>
      <style>
        body{{font-family:"Tajawal","Segoe UI",system-ui,sans-serif; margin:0; background:#faf7e6}}
        .back{{position:fixed; top:16px; right:16px}}
        .back a{{background:#FFD700; color:#4B0082; padding:8px 12px; border-radius:10px; text-decoration:none; font-weight:700}}
        .wrap{{max-width:1000px; margin:40px auto; padding:20px; background:#fff; border:1px solid #eee; border-radius:14px}}
        .grid2{{display:grid; gap:12px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); margin-top:10px}}
        .btn{{display:inline-block; padding:10px 14px; border-radius:12px; text-decoration:none; font-weight:700}}
        .tg{{background:#229ED9; color:#fff}}
        .wa{{background:#25D366; color:#fff}}
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

# ===== صفحة DSM (من الملف الخارجي) =====
@app.get("/dsm")
def dsm():
    DSM = importlib.import_module("DSM")
    content = DSM.main() if hasattr(DSM, "main") else "<p>DSM reference.</p>"
    return shell_page(content, "DSM — مرجع")

# ===== دراسة الحالة =====
FORM_HTML = """
<h1>📝 دراسة الحالة — إدخال الأعراض</h1>
<p class="note">⚠️ النتيجة تعليمية/إرشادية وليست تشخيصًا طبيًا.</p>
<style>
  .grid{display:grid; gap:10px; grid-template-columns: repeat(auto-fit, minmax(240px,1fr));}
  label{display:block; background:#fafafa; border:1px solid #eee; border-radius:10px; padding:10px}
  .submit{margin-top:14px; padding:10px 16px; border-radius:12px; background:#4B0082; color:#fff; border:0; font-weight:700}
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

  <h3>نوبات/اجتماعي/وسواس/صدمات</h3>
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
    <label><input type="checkbox" name="elevated_mood"> مزاج مرتفع</label>
    <label><input type="checkbox" name="impulsivity"> اندفاع/تهوّر</label>
    <label><input type="checkbox" name="grandiosity"> شعور بالعظمة</label>
    <label><input type="checkbox" name="decreased_sleep_need"> قلة النوم</label>
    <label><input type="checkbox" name="hallucinations"> هلوسات</label>
    <label><input type="checkbox" name="delusions"> أوهام ثابتة</label>
    <label><input type="checkbox" name="disorganized_speech"> اضطراب كلام</label>
    <label><input type="checkbox" name="functional_decline"> تدهور وظيفي</label>
  </div>

  <h3>أكل/انتباه/تعاطي</h3>
  <div class="grid">
    <label><input type="checkbox" name="restriction"> تقييد الأكل</label>
    <label><input type="checkbox" name="underweight"> نقص وزن</label>
    <label><input type="checkbox" name="body_image_distort"> صورة جسد مشوهة</label>
    <label><input type="checkbox" name="binges"> نوبات أكل</label>
    <label><input type="checkbox" name="compensatory"> سلوك تعويضي</label>

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
  <label>الشدّة: <input type="number" name="distress" min="0" max="10" value="5"></label>

  <button class="submit" type="submit">اعرض الترشيح</button>
</form>
"""

# ===== نتيجة الترشيح (نهرب أقواس JS إذا احتجنا لاحقًا) =====
RESULT_HTML = """
<h1>📌 ترشيحات أولية</h1>
<ul style="line-height:1.9">{items}</ul>
<p class="note">⚠️ هذه النتائج تعليمية/إرشادية فقط. يُفضّل مراجعة مختص.</p>
<button onclick="window.print()" style="margin-top:10px;padding:10px 16px;border-radius:12px;background:#4B0082;color:#fff;border:0;font-weight:700">طباعة</button>
"""

# ===== صفحة التواصل =====
CONTACT_HTML = f"""
<h1>📞 التواصل مع عربي سايكو</h1>
<p>اختر القناة المناسبة لك وسنتواصل معك في أقرب وقت:</p>
<div class="grid2">
  <a class="btn tg" href="{TELEGRAM_URL}" target="_blank" rel="noopener">✈️ تيليجرام</a>
  <a class="btn wa" href="{WHATSAPP_URL}" target="_blank" rel="noopener">🟢 واتساب</a>
</div>
<p style="margin-top:14px">يمكنك دائمًا العودة للرئيسية ومتابعة <a href="/case">دراسة الحالة</a> أو تصفّح <a href="/dsm">DSM</a>.</p>
"""

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell_page(FORM_HTML, "دراسة الحالة")
    data = {k: v for k, v in request.form.items()}
    try:
        DSM = importlib.import_module("DSM")
        picks = DSM.diagnose(data) if hasattr(DSM, "diagnose") else [("تعذر التشخيص", "DSM.diagnose غير متوفر", 0.0)]
    except Exception as e:
        picks = [("خطأ", str(e), 0.0)]
    items = "".join([f"<li><b>{name}</b> — {why} <small>(Score: {score:.0f})</small></li>" for name, why, score in picks])
    return shell_page(RESULT_HTML.format(items=items), "نتيجة الترشيح")

@app.get("/contact")
def contact():
    return shell_page(CONTACT_HTML, "التواصل")

@app.get("/health")
def health():
    return {"status":"ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
