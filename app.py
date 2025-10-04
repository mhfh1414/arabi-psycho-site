# app.py — عربي سايكو: واجهة مميزة + قائمة جانبية + علاج نفسي افتراضي + دراسة الحالة + DSM + CBT + إدمان + تواصل
import os, importlib
from flask import Flask, render_template_string, request

app = Flask(__name__)

# ========= إعدادات وروابط =========
BRAND_NAME   = os.environ.get("BRAND_NAME", "عربي سايكو")
TELEGRAM_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WHATSAPP_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966500000000?text=%D8%A3%D8%B1%D9%8A%D8%AF%20%D8%A7%D9%84%D8%AA%D9%88%D8%A7%D8%B5%D9%84%20%D9%85%D8%B9%20%D8%B9%D8%B1%D8%A8%D9%8A%20%D8%B3%D8%A7%D9%8A%D9%83%D9%88")
LOGO_URL     = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")

# ========= رأس موحّد (SEO/ستايل) =========
BASE_HEAD = f"""
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="description" content="{BRAND_NAME} — منصتك للعلاج النفسي الافتراضي: دراسة حالة، DSM، CBT، وخطط دعم الإدمان.">
<link rel="icon" href="{LOGO_URL}">
<meta property="og:title" content="{BRAND_NAME}">
<meta property="og:description" content="عربي سايكو — علاج نفسي افتراضي بتصميم أنيق بالبنفسجي والذهبي.">
<meta property="og:type" content="website">
<style>
:root{{ --purple:#4B0082; --gold:#FFD700; --ink:#2d1b4e; --bg:#faf7e6 }}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif;color:#222}}
a{{text-decoration:none}}

.topbar{{position:sticky;top:0;z-index:5;background:var(--purple);color:#fff;padding:10px 14px;display:flex;align-items:center;gap:10px;box-shadow:0 2px 14px rgba(0,0,0,.18)}}
.topbar img{{width:42px;height:42px;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
.brand{{font-weight:800;letter-spacing:.3px}}
.toplinks a{{color:#fff;margin:0 6px;font-weight:700;opacity:.95}}
.toplinks a:hover{{opacity:1}}

.layout{{display:grid;grid-template-columns:280px 1fr;gap:18px;max-width:1300px;margin:22px auto;padding:0 14px}}
.sidebar{{background:#fff;border:1px solid #eee;border-radius:16px;box-shadow:0 10px 24px rgba(0,0,0,.06);padding:16px}}
.side-title{{font-weight:800;color:var(--purple);margin:4px 0 10px}}
.navlink{{display:block;padding:10px 12px;border-radius:12px;font-weight:700;color:#222;border:1px solid #f0f0f0;margin-bottom:8px}}
.navlink:hover{{background:#fafafa}}
.navlink.primary{{background:var(--purple);color:#fff;border-color:var(--purple)}}
.contact-box{{margin-top:10px;display:grid;gap:8px}}
.btn{{display:inline-block;background:var(--purple);color:#fff;padding:10px 14px;border-radius:12px;font-weight:700;text-align:center}}
.btn.alt{{background:#5b22a6}}
.btn.gold{{background:var(--gold);color:var(--purple)}}
.btn.whatsapp{{background:#25D366}}
.btn.telegram{{background:#229ED9}}
.card{{background:#fff;border:1px solid #eee;border-radius:16px;box-shadow:0 10px 24px rgba(0,0,0,.06);padding:20px}}
.footer{{text-align:center;color:#fff;margin-top:24px;padding:14px;background:var(--purple)}}
.footer small{{opacity:.9}}

.hero{{background:linear-gradient(160deg, rgba(75,0,130,.96), rgba(75,0,130,.85)), url('https://images.unsplash.com/photo-1518199266791-5375a83190b7?q=80&w=1400&auto=format') center/cover no-repeat; color:#fff}}
.hero .inner{{max-width:1000px;margin:0 auto;padding:56px 14px;display:grid;grid-template-columns:1fr;gap:12px}}
.hero .badge{{background:var(--gold);color:var(--ink);display:inline-block;padding:6px 10px;border-radius:999px;font-weight:800}}
.hero h1{{margin:.2rem 0 0;font-size:2.2rem}}
.hero p{{opacity:.95;line-height:1.8}}

.grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
.grid-sm{{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}}
label.chk{{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:10px}}
input[type="text"],input[type="number"],select,textarea{{width:100%;padding:10px;border:1px solid #ddd;border-radius:10px}}
.section{{margin:10px 0}}
.note{{background:#fff7d1;border:1px dashed #e5c100;padding:8px 12px;border-radius:10px}}
.center{{text-align:center}}
</style>
"""

# ========= هيكل بsidebar + topbar =========
def site_shell(content_html: str, title: str):
    template = """
    <!DOCTYPE html><html lang="ar" dir="rtl"><head>
      <title>{{ title }}</title>""" + BASE_HEAD + """
    </head><body>
      <header class="topbar">
        <img src=\""""+LOGO_URL+"""\" alt="شعار"/>
        <div class="brand">"""+BRAND_NAME+"""</div>
        <div class="toplinks">
          <a href="/">الرئيسية</a>
          <a href="/case">دراسة الحالة</a>
          <a href="/dsm">DSM</a>
          <a href="/cbt">CBT</a>
          <a href="/addiction">إدمان</a>
          <a href="/contact">تواصل</a>
        </div>
      </header>

      <div class="layout">
        <aside class="sidebar">
          <div class="side-title">القائمة</div>
          <a class="navlink primary" href="/case">📝 دراسة الحالة</a>
          <a class="navlink" href="/dsm">📘 مرجع DSM</a>
          <a class="navlink" href="/cbt">🧠 العلاج المعرفي السلوكي (CBT)</a>
          <a class="navlink" href="/addiction">🚭 خطة علاج الإدمان</a>
          <div class="side-title">تواصل سريع</div>
          <div class="contact-box">
            <a class="btn telegram" href=\""""+TELEGRAM_URL+"""\" target="_blank" rel="noopener">✈️ تيليجرام</a>
            <a class="btn whatsapp" href=\""""+WHATSAPP_URL+"""\" target="_blank" rel="noopener">🟢 واتساب</a>
          </div>
        </aside>

        <main class="card">{{ content|safe }}</main>
      </div>

      <footer class="footer">
        <small>© جميع الحقوق محفوظة لـ """+BRAND_NAME+"""</small>
      </footer>
    </body></html>
    """
    return render_template_string(template, title=title, content=content_html)

# ========= الصفحة الرئيسية =========
@app.get("/")
def home():
    hero = f"""
    <section class="hero">
      <div class="inner">
        <span class="badge">علاج نفسي افتراضي</span>
        <h1>{BRAND_NAME} — راحةٌ نفسية أقرب إليك</h1>
        <p>ابدأ رحلتك بخطواتٍ واضحة: دوِّن أعراضك، استعرض ترشيحات DSM، تدرّب على أدوات CBT، واتّبع خطةً ذكيةً لدعم التعافي من الإدمان.</p>
        <div class="grid-sm">
          <a class="btn gold" href="/case">ابدأ دراسة الحالة الآن</a>
          <a class="btn alt" href="/dsm">استعرض DSM</a>
        </div>
      </div>
    </section>

    <section class="card" style="margin-top:16px">
      <h3>لماذا عربي سايكو؟</h3>
      <div class="grid">
        <div class="note">لغةٌ قريبةٌ منك وهويةٌ عربيةٌ أنيقة.</div>
        <div class="note">مسارٌ عملي: من الأعراض إلى التفسير ثم الأدوات.</div>
        <div class="note">روابط تواصل مباشرة لخطواتٍ أسرع نحو التحسُّن.</div>
      </div>
    </section>
    """
    # نعرض الهيرو + بطاقة التعريف ضمن الهيكل العام
    return site_shell(hero, f"{BRAND_NAME} — الرئيسية")

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
        html = CBT.main() if hasattr(CBT, "main") else "<h2>CBT</h2><p>خطة العلاج المعرفي السلوكي غير متوفرة.</p>"
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

# ========= دراسة الحالة (حفظ تلقائي/طباعة/JSON) =========
FORM_HTML = """
<h1>📝 دراسة الحالة</h1>
<p class="note">خطوة البداية نحو فهمٍ أعمق لذاتك. كن صادقًا مع نفسك، ودعنا نرتّب الصورة بوضوح.</p>

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
function toObj(form){{
  const data = {{}};
  new FormData(form).forEach((v,k)=>{{ data[k]=v; }});
  form.querySelectorAll('input[type=checkbox]').forEach(cb=>{{ data[cb.name]=cb.checked; }});
  return data;
}}
function fromObj(form, data){{
  if(!data) return;
  Object.keys(data).forEach(k=>{{
    const el=form.querySelector(`[name="${{k}}"]`);
    if(!el) return;
    if(el.type==='checkbox') el.checked=!!data[k]; else el.value=data[k];
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
<p class="note">قراءة واضحة لما يظهر من النمط العام، لتقطع الخطوة التالية بثقة.</p>
<ul style="line-height:1.9">{items}</ul>
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
        picks = DSM.diagnose(data) if hasattr(DSM, "diagnose") else [("تعذر الترشيح", "DSM.diagnose غير متوفر", 0.0)]
    except Exception as e:
        picks = [("خطأ", str(e), 0.0)]
    items = "".join([f"<li><b>{name}</b> — {why} <small>(Score: {score:.0f})</small></li>" for name, why, score in picks])
    return site_shell(RESULT_HTML.format(items=items), "نتيجة الترشيح")

# ========= تواصل =========
CONTACT_HTML = f"""
<h1>📞 تواصل معنا</h1>
<p>نحن هنا لنسندك خطوةً بخطوة — رسالتك محل اهتمام.</p>
<div class="grid-sm">
  <a class="btn telegram" href="{TELEGRAM_URL}" target="_blank" rel="noopener">✈️ تيليجرام</a>
  <a class="btn whatsapp" href="{WHATSAPP_URL}" target="_blank" rel="noopener">🟢 واتساب</a>
</div>
"""

@app.get("/contact")
def contact():
    return site_shell(CONTACT_HTML, "التواصل")

# ========= صفحات الخطأ =========
@app.errorhandler(404)
def not_found(_):
    return site_shell("<div class='center'><h2>٤٠٤ — الصفحة غير موجودة</h2><p>تحقّق من الرابط أو عد للرئيسية.</p></div>", "404"), 404

@app.errorhandler(500)
def server_err(e):
    return site_shell(f"<div class='center'><h2>خطأ داخلي</h2><p>حدث شيء غير متوقع.</p><details><summary>تفاصيل للمطوّر</summary><pre>{e}</pre></details></div>", "خطأ"), 500

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
