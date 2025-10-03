# app.py — عربي سايكو (واجهة داكنة محسّنة)
import os, importlib, datetime
from flask import Flask, render_template_string, request, make_response, jsonify

app = Flask(__name__)

BRAND_NAME   = os.environ.get("BRAND_NAME", "عربي سايكو")
TELEGRAM_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WHATSAPP_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966500000000?text=%D8%B9%D9%85%D9%8A%D9%84%20%D8%B9%D8%B1%D8%A8%D9%8A%20%D8%B3%D8%A7%D9%8A%D9%83%D9%88")
LOGO_URL     = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
APP_VERSION  = os.environ.get("APP_VERSION", "v1.1")

BASE_CSS = """
:root{
  --ink:#0d0b14; --card:#141224; --muted:#bdb7d9; --brand:#8a63ff; --brand2:#caa23a; --ok:#25D366; --tg:#229ED9;
}
*{box-sizing:border-box} html{scroll-behavior:smooth}
body{margin:0;background:radial-gradient(1200px 700px at 10% 0%, #1c1733, #0d0b14);
     font-family:"Tajawal","Segoe UI",system-ui,sans-serif;color:#f7f7fb}
a{color:inherit}
.topbar{background:rgba(20,18,36,.8);backdrop-filter:blur(6px);border-bottom:1px solid #2b2744;color:#fff;
       padding:10px 14px;display:flex;align-items:center;gap:10px;position:sticky;top:0;z-index:50}
.topbar img{width:42px;height:42px;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,.35)}
.brand{font-weight:800;letter-spacing:.3px}
.nav{margin-right:auto}
.nav a{color:#e8e6ff;text-decoration:none;margin:0 8px;font-weight:700;opacity:.9}
.nav a:hover{opacity:1;text-decoration:underline}
.wrap{max-width:1120px;margin:28px auto;padding:20px;background:rgba(20,18,36,.75);border:1px solid #2b2744;
      border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.45)}
.btn{display:inline-block;background:linear-gradient(135deg,var(--brand),#5b3dff);color:#fff;text-decoration:none;
     padding:11px 16px;border-radius:14px;font-weight:800;text-align:center}
.btn.alt{background:linear-gradient(135deg,#3c2b7f,#6c57cc)}
.btn.gold{background:linear-gradient(135deg,var(--brand2),#f0d26b);color:#1a1336}
.btn.whatsapp{background:var(--ok)}
.btn.telegram{background:var(--tg)}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.muted{color:var(--muted);font-size:.96rem}
.footer{text-align:center;color:#bdb7d9;margin-top:24px;padding:16px;background:#141224;border-top:1px solid #2b2744}
.footer small{opacity:.95}
label.chk{display:block;background:#181532;border:1px solid #2b2744;border-radius:12px;padding:10px}
label.chk input{transform:scale(1.1);margin-left:8px}
.submit{margin-top:14px;padding:11px 16px;border-radius:14px;background:linear-gradient(135deg,#6c57cc,#8a63ff);
        color:#fff;border:0;font-weight:800}
.links-row{display:grid;gap:10px;grid-template-columns:1fr 1fr;margin-top:10px}
.hero{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:62vh;text-align:center;padding:28px}
.hero .card{background:linear-gradient(180deg,#f3eaff,#fff);color:#1a1336;padding:38px 46px;border-radius:22px;
            width:min(96vw,860px);box-shadow:0 28px 60px rgba(0,0,0,.5);border:1px solid #e7dcff}
.hero .logo img{max-width:120px;border-radius:50%;margin-bottom:12px;box-shadow:0 6px 16px rgba(0,0,0,.35)}
.hero h1{margin:.3rem 0 1rem}
.cta{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin-top:12px}
.notice{background:#fff6d6;color:#2b2100;border:1px dashed #e0b100;padding:10px;border-radius:10px}
textarea,input{background:#0f0d1d;color:#f1eeff;border:1px solid #2b2744;border-radius:10px;padding:10px}
"""

def shell(content: str, title: str):
    page = f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head>
      <meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
      <title>{title}</title>
      <style>{BASE_CSS}</style>
      <meta name="description" content="{BRAND_NAME} — DSM / CBT / إدمان / دراسة حالة">
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
        <small>© جميع الحقوق محفوظة لـ {BRAND_NAME} — {APP_VERSION}</small>
      </footer>
    </body></html>"""
    return render_template_string(page)

@app.get("/")
def home():
    content = f"""
    <section class="hero" aria-label="واجهة {BRAND_NAME}">
      <div class="card">
        <div class="logo"><img src="{LOGO_URL}" alt="شعار {BRAND_NAME}"/></div>
        <h1>واجهة التشخيص المبدئي</h1>
        <p class="muted" style="color:#2a2055">منصة تعليمية/إرشادية — ليست بديلاً عن التشخيص الطبي.</p>
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
    page = f"<!DOCTYPE html><html lang='ar' dir='rtl'><head><meta charset='utf-8'/>" \
           f"<meta name='viewport' content='width=device-width, initial-scale=1'/>" \
           f"<title>{BRAND_NAME} — الرئيسية</title><style>{BASE_CSS}</style></head><body>{content}</body></html>"
    return render_template_string(page)

@app.get("/dsm")
def dsm():
    try:
        DSM = importlib.import_module("DSM")
        html = DSM.main() if hasattr(DSM, "main") else "<p>مرجع DSM غير متوفر.</p>"
    except Exception:
        html = "<p>تعذر تحميل DSM.py</p>"
    return shell(html, "DSM — مرجع")

def _cbt_fallback():
    return """
    <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
    <p class="muted">نموذج عملي للطباعة والحفظ. يتم الحفظ تلقائيًا على جهازك.</p>
    <form id="cbtForm" onsubmit="event.preventDefault();window.print()">
      <h3>1) تعريف المشكلة</h3>
      <textarea name="p1" style="width:100%;height:90px" placeholder="الوصف المختصر"></textarea>

      <h3>2) الأفكار التلقائية السلبية</h3>
      <textarea name="p2" style="width:100%;height:90px" placeholder="ما هي الفكرة؟ متى تظهر؟"></textarea>

      <h3>3) الأدلة مع/ضد</h3>
      <div class="grid">
        <textarea name="p3a" style="width:100%;height:90px" placeholder="أدلة تؤيد الفكرة"></textarea>
        <textarea name="p3b" style="width:100%;height:90px" placeholder="أدلة تنقض الفكرة"></textarea>
      </div>

      <h3>4) الفكرة البديلة المتوازنة</h3>
      <textarea name="p4" style="width:100%;height:80px" placeholder="صياغة أكثر واقعية وتوازناً"></textarea>

      <h3>5) خطة سلوكية (SMART)</h3>
      <div class="grid">
        <input name="s1" placeholder="الخطوة" />
        <input name="s2" placeholder="المدة/التكرار" />
        <input name="s3" placeholder="المكان" />
        <input name="s4" placeholder="التوقيت" />
      </div>

      <h3>6) مقياس الشدة (0–10)</h3>
      <div class="grid">
        <label>قبل: <input name="pre" type="number" min="0" max="10" value="6" /></label>
        <label>بعد: <input name="post" type="number" min="0" max="10" value="3" /></label>
      </div>

      <button class="submit" type="submit">🖨️ طباعة الخطة</button>
    </form>
    <script>
      const f = document.getElementById('cbtForm');
      const key = 'cbt_auto_save_v1';
      const load = ()=>{ try{ const d=JSON.parse(localStorage.getItem(key)||'{}'); for(const k in d){ if(f[k]) f[k].value=d[k]; } }catch(e){} };
      const save = ()=>{ const d={}; for(const el of f.elements){ if(el.name) d[el.name]=el.value; } localStorage.setItem(key, JSON.stringify(d)); };
      f.addEventListener('input', save); window.addEventListener('DOMContentLoaded', load);
    </script>
    """

@app.get("/cbt")
def cbt():
    try:
        CBT = importlib.import_module("CBT")
        html = CBT.main() if hasattr(CBT, "main") else _cbt_fallback()
    except Exception:
        html = _cbt_fallback()
    return shell(html, "CBT — خطة علاج")

def _addiction_fallback():
    return """
    <h1>🚭 برنامج مختصر لعلاج الإدمان</h1>
    <div class="notice">محتوى تعليمي — يُنصح بمراجعة مختص/عيادة.</div>
    <h3>1) التقييم الأولي</h3>
    <ul><li>المادة/المدة/الكمية/المحفزات</li><li>تحمّل/انسحاب/أثر وظيفي</li></ul>
    <h3>2) خطة الإقلاع</h3>
    <ul><li>موعد بدء + دعم</li><li>إزالة المحفزات</li><li>استراتيجيات التعامل</li></ul>
    <h3>3) الوقاية من الانتكاس</h3>
    <div class="grid">
      <textarea style="width:100%;height:80px" placeholder="المحفزات الشخصية"></textarea>
      <textarea style="width:100%;height:80px" placeholder="خطة التعامل مع كل محفز"></textarea>
    </div>
    <h3>4) متابعة أسبوعية</h3>
    <div class="grid">
      <input placeholder="أيام الامتناع"/>
      <input placeholder="مواقف عالية الخطورة"/>
      <input placeholder="مكافأة ذاتية"/>
    </div>
    """

@app.get("/addiction")
def addiction():
    try:
        ADD = importlib.import_module("Addiction")
        html = ADD.main() if hasattr(ADD, "main") else _addiction_fallback()
    except Exception:
        html = _addiction_fallback()
    return shell(html, "علاج الإدمان")

# ----- دراسة الحالة -----
FORM_HTML = """
<h1>📝 دراسة الحالة — إدخال الأعراض</h1>
<p class="muted">⚠️ النتيجة تعليمية/إرشادية وليست تشخيصًا طبيًا.</p>
<form method="post" action="/case">
  <h3>أعراض المزاج</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="low_mood"> مزاج منخفض</label>
    <label class="chk"><input type="checkbox" name="anhedonia"> فقدان المتعة</label>
    <label class="chk"><input type="checkbox" name="sleep_issue"> صعوبات نوم</label>
    <label class="chk"><input type="checkbox" name="appetite_change"> تغيّر شهية</label>
    <label class="chk"><input type="checkbox" name="fatigue"> إرهاق/خمول</label>
  </div>

  <h3>أعراض القلق</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="worry"> قلق مستمر</label>
    <label class="chk"><input type="checkbox" name="tension"> توتر جسدي</label>
    <label class="chk"><input type="checkbox" name="focus_issue"> صعوبة تركيز</label>
    <label class="chk"><input type="checkbox" name="restlessness"> تململ</label>
  </div>

  <h3>نوبات/اجتماعي/وسواس/صدمات</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="panic_attacks"> نوبات هلع</label>
    <label class="chk"><input type="checkbox" name="fear_of_attacks"> خوف من تكرار النوبات</label>
    <label class="chk"><input type="checkbox" name="panic_avoidance"> تجنّب بسبب النوبات</label>
    <label class="chk"><input type="checkbox" name="social_avoid"> تجنب اجتماعي</label>
    <label class="chk"><input type="checkbox" name="fear_judgment"> خوف من تقييم الآخرين</label>
    <label class="chk"><input type="checkbox" name="obsessions"> أفكار ملحّة</label>
    <label class="chk"><input type="checkbox" name="compulsions"> أفعال قهرية</label>
    <label class="chk"><input type="checkbox" name="trauma_event"> حدث صادمي</label>
    <label class="chk"><input type="checkbox" name="flashbacks"> استرجاع/فلاشباك</label>
    <label class="chk"><input type="checkbox" name="nightmares"> كوابيس</label>
    <label class="chk"><input type="checkbox" name="trauma_avoid"> تجنّب مرتبط</label>
    <label class="chk"><input type="checkbox" name="hypervigilance"> يقظة مفرطة</label>
  </div>

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
    <label class="chk"><input type="checkbox" name="functional_impair"> أثر وظيفي</label>

    <label class="chk"><input type="checkbox" name="craving"> اشتهاء</label>
    <label class="chk"><input type="checkbox" name="tolerance"> تحمّل</label>
    <label class="chk"><input type="checkbox" name="withdrawal"> انسحاب</label>
    <label class="chk"><input type="checkbox" name="use_despite_harm"> استخدام رغم الضرر</label>
  </div>

  <h3>تقدير الشدة (0–10)</h3>
  <label>الشدّة العامة: <input type="number" name="distress" min="0" max="10" value="5"></label>
  <button class="submit" type="submit">اعرض الترشيح</button>
</form>
"""

RESULT_HTML = """
<h1>📌 ترشيحات أولية</h1>
<ul style="line-height:1.9">{items}</ul>
<p class="muted">⚠️ النتائج تعليمية/إرشادية فقط.</p>
<button onclick="window.print()" class="btn">🖨️ طباعة</button>
"""

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell(FORM_HTML, "دراسة الحالة")
    data = {k: v for k, v in request.form.items()}
    try:
        DSM = importlib.import_module("DSM")
        picks = DSM.diagnose(data) if hasattr(DSM, "diagnose") else []
    except Exception:
        picks = []
    if not picks:  # fallback سريع
        items = []
        if any(k in data for k in ["low_mood","anhedonia","sleep_issue","fatigue"]):
            items.append(("اكتئاب — ترشيح","أعراض مزاجية متعددة",70))
        if any(k in data for k in ["worry","tension","focus_issue","restlessness"]):
            items.append(("قلق عام — ترشيح","قلق مستمر مع توتر/تركيز",60))
        if data.get("panic_attacks"):
            items.append(("اضطراب هلع — ترشيح","نوبات + خوف/تجنّب",65))
        if data.get("obsessions") or data.get("compulsions"):
            items.append(("وسواس قهري — ترشيح","أفكار ملحّة/أفعال قهرية",60))
        if data.get("trauma_event") and (data.get("flashbacks") or data.get("nightmares") or data.get("trauma_avoid")):
            items.append(("PTSD — ترشيح","حدث صادمي + أعراض لاحقة",70))
        if data.get("elevated_mood") and (data.get("decreased_sleep_need") or data.get("impulsivity")):
            items.append(("ثنائي القطب — ترشيح","مزاج مرتفع + مؤشرات هوس",55))
        if data.get("restriction") or data.get("binges"):
            items.append(("اضطراب أكل — ترشيح","نوبات/تقييد/صورة جسد",55))
        if data.get("inattention") and data.get("since_childhood"):
            items.append(("ADHD — ترشيح","عدم انتباه منذ الطفولة مع أثر",60))
        if data.get("craving") or data.get("withdrawal") or data.get("use_despite_harm"):
            items.append(("تعاطي مواد — ترشيح","اشتهاء/انسحاب/رغم الضرر",65))
        picks = items or [("لا توجد ترشيحات قوية","البيانات غير كافية",0)]
    items_html = "".join([f"<li><b>{n}</b> — {w} <small>(Score: {s:.0f})</small></li>" for n,w,s in picks])
    return shell(RESULT_HTML.format(items=items_html), "نتيجة الترشيح")

CONTACT_HTML = f"""
<h1>📞 التواصل مع {BRAND_NAME}</h1>
<p class="muted">اختر الطريقة المناسبة:</p>
<div class="links-row">
  <a class="btn telegram" href="{TELEGRAM_URL}" target="_blank" rel="noopener">✈️ تيليجرام</a>
  <a class="btn whatsapp" href="{WHATSAPP_URL}" target="_blank" rel="noopener">🟢 واتساب</a>
</div>
"""
@app.get("/contact")
def contact():
    return shell(CONTACT_HTML, "التواصل")

@app.get("/health")
def health():
    return jsonify(status="ok", time=datetime.datetime.utcnow().isoformat()+"Z"), 200

@app.get("/version")
def version():
    return jsonify(version=APP_VERSION), 200

@app.get("/robots.txt")
def robots():
    resp = make_response("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n")
    resp.headers["Content-Type"] = "text/plain; charset=utf-8"
    return resp

@app.get("/sitemap.xml")
def sitemap():
    base = request.url_root.rstrip("/")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{base}/</loc></url>
  <url><loc>{base}/case</loc></url>
  <url><loc>{base}/dsm</loc></url>
  <url><loc>{base}/cbt</loc></url>
  <url><loc>{base}/addiction</loc></url>
  <url><loc>{base}/contact</loc></url>
</urlset>"""
    resp = make_response(xml); resp.headers["Content-Type"]="application/xml; charset=utf-8"; return resp

@app.after_request
def security_headers(resp):
    resp.headers["X-Content-Type-Options"]="nosniff"
    resp.headers["X-Frame-Options"]="DENY"
    resp.headers["Referrer-Policy"]="strict-origin-when-cross-origin"
    resp.headers["Permissions-Policy"]="geolocation=(), microphone=(), camera=()"
    resp.headers["Content-Security-Policy"]="default-src 'self' 'unsafe-inline' https: data:; img-src 'self' https: data:; frame-ancestors 'none';"
    return resp

@app.errorhandler(404)
def not_found(_):
    return shell("<h1>404</h1><p>الصفحة غير موجودة.</p><p><a class='btn' href='/'>عودة</a></p>", "غير موجود"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
