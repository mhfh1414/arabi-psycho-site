# app.py — عربي سايكو: واجهة مميزة + دراسة الحالة (حفظ/طباعة/JSON) + DSM + CBT + إدمان + تواصل + تحسينات أمان/SEO
import os, importlib
from flask import Flask, render_template_string, request

app = Flask(__name__)

# ========= إعدادات وروابط =========
BRAND_NAME   = os.environ.get("BRAND_NAME", "عربي سايكو")
TELEGRAM_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WHATSAPP_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966500000000?text=%D8%B9%D9%85%D9%8A%D9%84%20%D8%B9%D8%B1%D8%A8%D9%8A%20%D8%B3%D8%A7%D9%8A%D9%83%D9%88")
LOGO_URL     = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")

# ========= رأس موحّد (SEO/ستايل) =========
BASE_HEAD = f"""
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="description" content="{BRAND_NAME} — واجهة تشخيص مبدئي تعليمية للصحة النفسية (DSM/CBT/إدمان)">
<link rel="icon" href="{LOGO_URL}">
<meta property="og:title" content="{BRAND_NAME}">
<meta property="og:description" content="واجهة أنيقة بالبنفسجي والذهبي — دراسة حالة، DSM، CBT، علاج الإدمان.">
<meta property="og:type" content="website">
<style>
:root{{ --purple:#4B0082; --gold:#FFD700; --ink:#2d1b4e; --bg:#faf7e6 }}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif;color:#222}}
.topbar{{background:var(--purple);color:#fff;padding:10px 14px;display:flex;align-items:center;gap:10px}}
.topbar img{{width:42px;height:42px;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
.brand{{font-weight:800;letter-spacing:.3px}}
.nav{{margin-right:auto}}
.nav a{{color:#fff;text-decoration:none;margin:0 8px;font-weight:700;opacity:.95}}
.nav a:hover{{opacity:1}}
.wrap{{max-width:1100px;margin:28px auto;padding:20px;background:#fff;border:1px solid #eee;border-radius:16px;box-shadow:0 10px 24px rgba(0,0,0,.06)}}
.btn{{display:inline-block;background:var(--purple);color:#fff;text-decoration:none;padding:10px 14px;border-radius:12px;font-weight:700}}
.btn.alt{{background:#5b22a6}}
.btn.gold{{background:var(--gold);color:var(--purple)}}
.btn.whatsapp{{background:#25D366}}
.btn.telegram{{background:#229ED9}}
.grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
.grid-sm{{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}}
.muted{{opacity:.85}}
.footer{{text-align:center;color:#fff;margin-top:24px;padding:14px;background:var(--purple)}}
.footer small{{opacity:.9}}
.hero{{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:58vh;background:var(--purple);color:#fff;text-align:center;padding:28px}}
.hero .card{{background:var(--gold);color:var(--ink);padding:36px 46px;border-radius:22px;width:min(96vw,860px);box-shadow:0 16px 40px rgba(0,0,0,.35)}}
.hero .logo img{{max-width:120px;border-radius:50%;margin-bottom:12px;box-shadow:0 4px 12px rgba(0,0,0,.25)}}
.hero h1{{margin:.3rem 0 1rem}}
.cta{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin-top:10px}}
label.chk{{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:10px}}
input[type="text"],input[type="number"],select,textarea{{width:100%;padding:10px;border:1px solid #ddd;border-radius:10px}}
.note{{background:#fff7d1;border:1px dashed #e5c100;padding:8px 12px;border-radius:10px}}
.section{{margin:10px 0}}
.center{{text-align:center}}
</style>
"""

def site_shell(content: str, title: str):
    page = f"""
    <!DOCTYPE html><html lang="ar" dir="rtl"><head>
      <title>{title}</title>{BASE_HEAD}
    </head><body>
      <header class="topbar">
        <img src="{LOGO_URL}" alt="شعار"/>
        <div class="brand">{BRAND_NAME}</div>
        <nav class="nav">
          <a href="/">الرئيسية</a>
          <a href="/case">دراسة الحالة</a>
          <a href="/dsm">DSM</a>
          <a href="/cbt">CBT</a>
          <a href="/addiction">إدمان</a>
          <a href="/contact">تواصل</a>
        </nav>
      </header>

      <main class="wrap">{content}</main>

      <footer class="footer">
        <small>© جميع الحقوق محفوظة لـ {BRAND_NAME}</small>
      </footer>
    </body></html>
    """
    return render_template_string(page)

# ========= الصفحة الرئيسية =========
@app.get("/")
def home():
    content = f"""
    <section class="hero">
      <div class="card">
        <div class="logo"><img src="{LOGO_URL}" alt="شعار {BRAND_NAME}"/></div>
        <h1>واجهة التشخيص المبدئي</h1>
        <p class="muted">منصة تعليمية/إرشادية تساعد على تنظيم الأعراض ومراجعتها — ليست بديلاً عن التشخيص الطبي.</p>
        <div class="cta">
          <a class="btn" href="/case">📝 دراسة الحالة</a>
          <a class="btn alt" href="/dsm">📘 DSM (مرجع)</a>
          <a class="btn gold" href="/cbt">🧠 CBT</a>
          <a class="btn gold" href="/addiction">🚭 علاج الإدمان</a>
          <a class="btn telegram" href="{TELEGRAM_URL}" target="_blank" rel="noopener">✈️ تيليجرام</a>
          <a class="btn whatsapp" href="{WHATSAPP_URL}" target="_blank" rel="noopener">🟢 واتساب</a>
        </div>
      </div>
    </section>
    """
    # نعرض البطاقة كاملة بدون الغلاف الأبيض
    return render_template_string(f"<!DOCTYPE html><html lang='ar' dir='rtl'><head><title>{BRAND_NAME} — الرئيسية</title>{BASE_HEAD}</head><body>{content}<footer class='footer'><small>© جميع الحقوق محفوظة لـ {BRAND_NAME}</small></footer></body></html>")

# ========= DSM/CBT/إدمان =========
@app.get("/dsm")
def dsm():
    try:
        DSM = importlib.import_module("DSM")
        html = DSM.main() if hasattr(DSM, "main") else "<p>مرجع DSM غير متوفر.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل DSM: {e}</p>"
    return site_shell(html, "DSM — مرجع")

@app.get("/cbt")
def cbt():
    try:
        CBT = importlib.import_module("CBT")
        html = CBT.main() if hasattr(CBT, "main") else "<h2>CBT</h2><p>خطة العلاج السلوكي المعرفي غير متوفرة.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل CBT: {e}</p>"
    return site_shell(html, "CBT — خطة علاج")

@app.get("/addiction")
def addiction():
    try:
        ADD = importlib.import_module("Addiction")
        html = ADD.main() if hasattr(ADD, "main") else "<h2>علاج الإدمان</h2><p>الصفحة غير متوفرة.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل صفحة الإدمان: {e}</p>"
    return site_shell(html, "علاج الإدمان")

# ========= دراسة الحالة (مع حفظ تلقائي/طباعة/JSON) =========
FORM_HTML = """
<h1>📝 دراسة الحالة — إدخال الأعراض</h1>
<p class="note">⚠️ النتيجة تعليمية/إرشادية وليست تشخيصًا طبيًا.</p>

<form id="caseForm" method="post" action="/case">
  <div class="section">
    <h3>أعراض المزاج</h3>
    <div class="grid">
      <label class="chk"><input type="checkbox" name="low_mood"> مزاج منخفض</label>
      <label class="chk"><input type="checkbox" name="anhedonia"> فقدان المتعة</label>
      <label class="chk"><input type="checkbox" name="sleep_issue"> صعوبات نوم</label>
      <label class="chk"><input type="checkbox" name="appetite_change"> تغيّر شهية</label>
      <label class="chk"><input type="checkbox" name="fatigue"> إرهاق/خمول</label>
    </div>
  </div>

  <div class="section">
    <h3>أعراض القلق</h3>
    <div class="grid">
      <label class="chk"><input type="checkbox" name="worry"> قلق مستمر</label>
      <label class="chk"><input type="checkbox" name="tension"> توتر جسدي</label>
      <label class="chk"><input type="checkbox" name="focus_issue"> صعوبة تركيز</label>
      <label class="chk"><input type="checkbox" name="restlessness"> تململ</label>
    </div>
  </div>

  <div class="section">
    <h3>نوبات/اجتماعي/وسواس/صدمات</h3>
    <div class="grid">
      <label class="chk"><input type="checkbox" name="panic_attacks"> نوبات هلع</label>
      <label class="chk"><input type="checkbox" name="fear_of_attacks"> خوف من تكرار النوبات</label>
      <label class="chk"><input type="checkbox" name="panic_avoidance"> تجنّب بسبب النوبات</label>
      <label class="chk"><input type="checkbox" name="social_avoid"> تجنب اجتماعي</label>
      <label class="chk"><input type="checkbox" name="fear_judgment"> خوف من تقييم الآخرين</label>
      <label class="chk"><input type="checkbox" name="obsessions"> أفكار ملحّة</label>
      <label class="chk"><input type="checkbox" name="compulsions"> أفعال قهرية</label>
      <label class="chk"><input type="checkbox" name="trauma_event"> تعرّض لحدث صادمي</label>
      <label class="chk"><input type="checkbox" name="flashbacks"> استرجاع/فلاشباك</label>
      <label class="chk"><input type="checkbox" name="nightmares"> كوابيس</label>
      <label class="chk"><input type="checkbox" name="trauma_avoid"> تجنّب مرتبط بالحدث</label>
      <label class="chk"><input type="checkbox" name="hypervigilance"> يقظة مفرطة</label>
    </div>
  </div>

  <div class="section">
    <h3>مزاج مرتفع/ذهان</h3>
    <div class="grid">
      <label class="chk"><input type="checkbox" name="elevated_mood"> مزاج مرتفع</label>
      <label class="chk"><input type="checkbox" name="impulsivity"> اندفاع/تهوّر</label>
      <label class="chk"><input type="checkbox" name="grandiosity"> شعور بالعظمة</label>
      <label class="chk"><input type="checkbox" name="decreased_sleep_need"> قلة النوم</label>
      <label class="chk"><input type="checkbox" name="hallucinations"> هلوسات</label>
      <label class="chk"><input type="checkbox" name="delusions"> أوهام ثابتة</label>
      <label class="chk"><input type="checkbox" name="disorganized_speech"> اضطراب كلام</label>
      <label class="chk"><input type="checkbox" name="functional_decline"> تدهور وظيفي</label>
    </div>
  </div>

  <div class="section">
    <h3>أكل/انتباه/تعاطي</h3>
    <div class="grid">
      <label class="chk"><input type="checkbox" name="restriction"> تقييد الأكل</label>
      <label class="chk"><input type="checkbox" name="underweight"> نقص وزن</label>
      <label class="chk"><input type="checkbox" name="body_image_distort"> صورة جسد مشوهة</label>
      <label class="chk"><input type="checkbox" name="binges"> نوبات أكل</label>
      <label class="chk"><input type="checkbox" name="compensatory"> سلوك تعويضي</label>

      <label class="chk"><input type="checkbox" name="inattention"> عدم انتباه</label>
      <label class="chk"><input type="checkbox" name="hyperactivity"> فرط حركة</label>
      <label class="chk"><input type="checkbox" name="impulsivity_symp"> اندفاعية</label>
      <label class="chk"><input type="checkbox" name="since_childhood"> منذ الطفولة</label>
      <label class="chk"><input type="checkbox" name="functional_impair"> تأثير وظيفي</label>

      <label class="chk"><input type="checkbox" name="craving"> اشتهاء</label>
      <label class="chk"><input type="checkbox" name="tolerance"> تحمّل</label>
      <label class="chk"><input type="checkbox" name="withdrawal"> انسحاب</label>
      <label class="chk"><input type="checkbox" name="use_despite_harm"> استخدام رغم الضرر</label>
    </div>
  </div>

  <div class="section">
    <h3>تقدير الشدة (0–10)</h3>
    <div class="grid-sm">
      <label>الشدّة العامة: <input type="number" name="distress" min="0" max="10" value="5"></label>
    </div>
  </div>

  <div class="grid-sm">
    <button class="btn" type="submit">اعرض الترشيح</button>
    <button class="btn alt" type="button" onclick="window.print()">طباعة</button>
    <button class="btn gold" type="button" onclick="saveJSON()">حفظ JSON</button>
    <button class="btn" type="button" onclick="clearForm()">مسح النموذج</button>
  </div>
</form>

<script>
const KEY='arabi_psycho_case_form';

function toObj(form){
  const data = {{}};
  new FormData(form).forEach((v,k)=>{{
    if(data[k]!==undefined) {{
      if(!Array.isArray(data[k])) data[k]=[data[k]];
      data[k].push(v);
    }} else {{
      data[k]=v;
    }}
  }});
  // اجعل checkboxes = true/false
  form.querySelectorAll('input[type=checkbox]').forEach(cb=>{{
    data[cb.name]=cb.checked;
  }});
  return data;
}

function fromObj(form, data){{
  if(!data) return;
  Object.keys(data).forEach(k=>{{
    const el = form.querySelector(`[name="${{k}}"]`);
    if(!el) return;
    if(el.type==='checkbox') el.checked = !!data[k];
    else el.value = data[k];
  }});
}}

function saveDraft(){{ localStorage.setItem(KEY, JSON.stringify(toObj(document.getElementById('caseForm')))); }}
function loadDraft(){{ const s=localStorage.getItem(KEY); if(s) fromObj(document.getElementById('caseForm'), JSON.parse(s)); }}
function clearForm(){{ localStorage.removeItem(KEY); document.getElementById('caseForm').reset(); }}
function saveJSON(){{
  const blob=new Blob([JSON.stringify(toObj(document.getElementById('caseForm')),null,2)],{{type:'application/json'}});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='case_form.json'; a.click(); URL.revokeObjectURL(a.href);
}}

document.getElementById('caseForm').addEventListener('change', saveDraft);
window.addEventListener('DOMContentLoaded', loadDraft);
</script>
"""

RESULT_HTML = """
<h1>📌 ترشيحات أولية</h1>
<ul style="line-height:1.9">{items}</ul>
<p class="muted">⚠️ هذه النتائج تعليمية/إرشادية فقط. يُفضّل مراجعة مختص.</p>
<div class="grid-sm">
  <button onclick="window.print()" class="btn">طباعة</button>
  <button class="btn gold" onclick='(function(){{
    const data = {{items: Array.from(document.querySelectorAll("li")).map(li=>li.innerText)}};
    const b = new Blob([JSON.stringify(data,null,2)],{{type:"application/json"}});
    const a = document.createElement("a"); a.href=URL.createObjectURL(b); a.download="diagnosis_result.json"; a.click(); URL.revokeObjectURL(a.href);
  }})()'>حفظ JSON</button>
</div>
"""

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return site_shell(FORM_HTML, "دراسة الحالة")
    data = {k: v for k, v in request.form.items()}
    try:
        DSM = importlib.import_module("DSM")
        picks = DSM.diagnose(data) if hasattr(DSM, "diagnose") else [("تعذر التشخيص", "DSM.diagnose غير متوفر", 0.0)]
    except Exception as e:
        picks = [("خطأ", str(e), 0.0)]
    items = "".join([f"<li><b>{name}</b> — {why} <small>(Score: {score:.0f})</small></li>" for name, why, score in picks])
    return site_shell(RESULT_HTML.format(items=items), "نتيجة الترشيح")

# ========= تواصل =========
CONTACT_HTML = f"""
<h1>📞 التواصل مع {BRAND_NAME}</h1>
<p class="muted">اختر الطريقة المناسبة:</p>
<div class="grid-sm">
  <a class="btn telegram" href="{TELEGRAM_URL}" target="_blank" rel="noopener">✈️ تيليجرام</a>
  <a class="btn whatsapp" href="{WHATSAPP_URL}" target="_blank" rel="noopener">🟢 واتساب</a>
</div>
"""

@app.get("/contact")
def contact():
    return site_shell(CONTACT_HTML, "التواصل")

# ========= صفحات الخطأ بتصميم موحّد =========
@app.errorhandler(404)
def not_found(_):
    return site_shell("<div class='center'><h2>٤٠٤ — الصفحة غير موجودة</h2><p class='muted'>تحقّق من الرابط أو ارجع إلى <a href='/'>الرئيسية</a>.</p></div>", "404"), 404

@app.errorhandler(500)
def server_err(e):
    return site_shell(f"<div class='center'><h2>خطأ داخلي</h2><p class='muted'>حدث خطأ غير متوقع.</p><details><summary>تفاصيل للمطور</summary><pre>{e}</pre></details></div>", "خطأ"), 500

# ========= رؤوس أمان وكاش =========
@app.after_request
def security_headers(resp):
    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    resp.headers["Cache-Control"] = "public, max-age=120"
    return resp

# ========= فحص صحة الخدمة =========
@app.get("/health")
def health():
    return {"status":"ok"}, 200

# ========= تشغيل محلي =========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
   
