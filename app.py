# app.py — عربي سايكو: تخطيط أنيق + دراسة حالة + DSM/CBT/إدمان + تواصل + حجز + عداد زوار
import os, importlib, urllib.parse, json
from flask import Flask, request, redirect
try:
    import requests
except Exception:
    requests = None

app = Flask(__name__)

# -------- إعدادات عامة --------
BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO  = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")

TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")  # تيليجرام عربي سايكو
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696?text=%D8%B9%D8%B1%D8%A8%D9%8A%20%D8%B3%D8%A7%D9%8A%D9%83%D9%88")

PSYCHO_WA = os.environ.get("PSYCHOLOGIST_WA", "https://wa.me/966530565696")
PSYCH_WA  = os.environ.get("PSYCHIATRIST_WA", "https://wa.me/966530565696")
SOCIAL_WA = os.environ.get("SOCIAL_WORKER_WA", "https://wa.me/966530565696")

TG_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID")

# -------- عدّاد الزوّار البسيط --------
COUNTER_FILE = "visitors.json"
def _load_count():
    try:
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            return int(json.load(f).get("count", 0))
    except Exception:
        return 0

def _save_count(n):
    try:
        with open(COUNTER_FILE, "w", encoding="utf-8") as f:
            json.dump({"count": int(n)}, f, ensure_ascii=False)
    except Exception:
        pass

def bump_visitors():
    n = _load_count() + 1
    _save_count(n)
    return n

# -------- إطار صفحات (بدون Jinja) --------
def shell(title: str, content: str, visitors: int | None = None) -> str:
    visitors_html = f"<div class='small' style='margin-top:12px'>👀 عدد الزوّار: <b>{visitors}</b></div>" if visitors is not None else ""
    return f"""<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<style>
:root{{--p:#4B0082;--g:#FFD700;--bg:#f8f6ff;--ink:#2b1a4c}}
*{{box-sizing:border-box}}
html,body{{height:100%}} body{{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif;color:var(--ink)}}
.layout{{display:grid;grid-template-columns:280px 1fr;min-height:100vh}}
/* Sidebar */
.side{{background:linear-gradient(180deg,#4b0082,#3a0d72);color:#fff;padding:18px;position:sticky;top:0;height:100vh}}
.logo{{display:flex;align-items:center;gap:10px;margin-bottom:18px}}
.logo img{{width:42px;height:42px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
.brand{{font-weight:900;letter-spacing:.3px}}
.nav a{{display:block;color:#fff;text-decoration:none;padding:10px 12px;border-radius:12px;margin:6px 0;font-weight:700;opacity:.95}}
.nav a:hover{{opacity:1;background:rgba(255,255,255,.12)}}
.badge{{display:inline-block;background:var(--g);color:#4b0082;border-radius:999px;padding:2px 10px;font-weight:900;font-size:.8rem}}
/* Content */
.content{{padding:24px}}
.card{{background:#fff;border:1px solid #eee;border-radius:16px;padding:18px;box-shadow:0 10px 24px rgba(0,0,0,.06)}}
.grid{{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}
.tile{{background:#fff;border:1px solid #eee;border-radius:14px;padding:14px}}
h1,h2,h3{{margin:.2rem 0 .6rem}}
.note{{background:#fff7d1;border:1px dashed #e5c100;border-radius:12px;padding:10px 12px;margin:10px 0}}
/* Controls */
.btn{{display:inline-block;background:var(--p);color:#fff;text-decoration:none;padding:10px 14px;border-radius:12px;font-weight:800}}
.btn.alt{{background:#5b22a6}} .btn.gold{{background:var(--g);color:#4b0082}}
.btn.wa{{background:#25D366}} .btn.tg{{background:#229ED9}}
label.chk{{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:8px}}
input,select,textarea{{width:100%;border:1px solid #ddd;border-radius:10px;padding:10px}}
.small{{font-size:.92rem;opacity:.85}}
.footer{{text-align:center;color:#fff;margin-top:24px;padding:14px;background:#3a0d72}}
hr.sep{{border:none;height:1px;background:#eee;margin:14px 0}}
.row{{display:flex;gap:10px;flex-wrap:wrap}}
</style></head><body>
<div class="layout">
  <aside class="side">
    <div class="logo"><img src="{LOGO}" alt="شعار"/><div>
      <div class="brand">{BRAND}</div>
      <div class="small">علاج نفسي افتراضي <span class="badge">بنفسجي × ذهبي</span></div>
    </div></div>
    <nav class="nav">
      <a href="/">الرئيسية</a>
      <a href="/case">📝 دراسة الحالة</a>
      <a href="/dsm">📘 DSM</a>
      <a href="/cbt">🧠 CBT</a>
      <a href="/addiction">🚭 الإدمان</a>
      <a href="/book">📅 احجز موعد</a>
      <a href="/contact">📞 تواصل</a>
    </nav>
    <div class="small" style="margin-top:18px;opacity:.9">
      «نراك بعيون الاحترام، ونساندك بخطوات عملية، خطوة بخطوة.»
    </div>
    {visitors_html}
  </aside>
  <main class="content">{content}</main>
</div>
<div class="footer"><small>© جميع الحقوق محفوظة لـ {BRAND}</small></div>
</body></html>"""

# -------- الرئيسية --------
@app.get("/")
def home():
    visitors = bump_visitors()
    content = f"""
    <div class="card" style="margin-bottom:14px">
      <h1>مرحبًا بك في {BRAND}</h1>
      <div class="small">مساحتك الهادئة لفهم الأعراض، وبناء خطة أولية محترمة لخصوصيتك.<br/>«كل تحسّن صغير اليوم هو خطوة كبيرة لغدٍ أهدأ»</div>
    </div>

    <div class="grid">
      <div class="tile"><h3>📝 دراسة الحالة</h3>
        <p class="small">قسّم الأعراض، احصل على ترشيحات أولية وروابط لأدوات CBT وبرنامج الإدمان.</p>
        <a class="btn gold" href="/case">ابدأ الآن</a>
      </div>

      <div class="tile"><h3>📘 مرجع DSM</h3>
        <p class="small">قوائم منظّمة تغطي المزاج، القلق، الوسواس، الذهان، التعاطي، النمو…</p>
        <a class="btn alt" href="/dsm">فتح DSM</a>
      </div>

      <div class="tile"><h3>🧠 CBT</h3>
        <p class="small">أدوات عملية مرتَّبة بحسب المشكلة.</p>
        <a class="btn" href="/cbt">افتح CBT</a>
      </div>

      <div class="tile"><h3>🚭 برنامج الإدمان</h3>
        <p class="small">Detox → Rehab → Relapse بخيارات واضحة.</p>
        <a class="btn" href="/addiction">افتح الإدمان</a>
      </div>

      <div class="tile"><h3>📅 احجز موعدًا</h3>
        <p class="small">اختر نوع المختص وأرسل بياناتك بسهولة.</p>
        <a class="btn gold" href="/book">نموذج الحجز</a>
      </div>

      <div class="tile"><h3>تواصل سريع</h3>
        <a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">تيليجرام عربي سايكو</a>
        <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">واتساب</a>
      </div>
    </div>
    """
    return shell("الرئيسية — عربي سايكو", content, visitors)

# -------- DSM / CBT / Addiction --------
@app.get("/dsm")
def dsm():
    try:
        DSM = importlib.import_module("DSM")
        html = DSM.main() if hasattr(DSM, "main") else "<div class='card'>DSM غير متوفر.</div>"
    except Exception as e:
        html = f"<div class='card'>تعذر تحميل DSM: {e}</div>"
    return shell("DSM — مرجع", html, _load_count())

@app.get("/cbt")
def cbt():
    try:
        CBT = importlib.import_module("CBT")
        html = CBT.main() if hasattr(CBT, "main") else "<div class='card'>CBT غير متوفر.</div>"
    except Exception as e:
        html = f"<div class='card'>تعذر تحميل CBT: {e}</div>"
    return shell("CBT — خطط وتمارين", html, _load_count())

@app.get("/addiction")
def addiction():
    try:
        ADD = importlib.import_module("Addiction")
        html = ADD.main() if hasattr(ADD, "main") else "<div class='card'>صفحة الإدمان غير متوفرة.</div>"
    except Exception as e:
        html = f"<div class='card'>تعذر تحميل صفحة الإدمان: {e}</div>"
    return shell("علاج الإدمان", html, _load_count())

# -------- إشعار تيليجرام (اختياري) --------
def _telegram_notify(text: str):
    if not (TG_BOT_TOKEN and TG_CHAT_ID and requests):
        return False
    try:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TG_CHAT_ID, "text": text})
        return True
    except Exception:
        return False

# -------- نموذج الحجز --------
BOOK_FORM = """
<div class="card">
  <h1>📅 احجز موعدك</h1>
  <div class="note">«موعدٌ واحد قد يغيّر مسار أسبوعك، ونحن هنا لنمشي معك خطوة بخطوة.»</div>

  <form method="post" action="/book" novalidate>
    <h3>1) بيانات أساسية</h3>
    <div class="grid">
      <div class="tile"><label>الاسم الكامل<input name="name" required placeholder="مثال: محمد أحمد"></label></div>
      <div class="tile"><label>العمر<input name="age" type="number" min="5" max="120" placeholder="مثال: 28"></label></div>
      <div class="tile">
        <label>نوع الموعد
          <select name="type" required>
            <option value="الأخصائي النفسي">الأخصائي النفسي</option>
            <option value="الطبيب النفسي">الطبيب النفسي</option>
            <option value="الأخصائي الاجتماعي">الأخصائي الاجتماعي</option>
          </select>
        </label>
      </div>
    </div>
    <hr class="sep"/>
    <h3>2) طريقة التواصل</h3>
    <div class="grid">
      <div class="tile">
        <label>الوسيلة
          <select name="channel" required>
            <option value="واتساب">واتساب</option>
            <option value="اتصال">اتصال</option>
            <option value="تيليجرام">تيليجرام</option>
          </select>
        </label>
      </div>
      <div class="tile"><label>رقم التواصل (مطلوب)<input name="phone" required placeholder="9665xxxxxxxx" pattern="\\d{9,15}"></label></div>
      <div class="tile"><label>أفضل وقت للتواصل<input name="best_time" placeholder="مثال: مساءً 7-9"></label></div>
    </div>

    <div class="tile" style="margin-top:10px">
      <label>نبذة موجزة عن المشكلة أو الهدف العلاجي
        <textarea name="summary" rows="5" placeholder="اكتب بإيجاز ما يهمك متابعته في الجلسة"></textarea>
      </label>
    </div>

    <div class="row">
      <button class="btn gold" type="submit">إرسال الطلب عبر واتساب</button>
      <a class="btn alt" href="/">رجوع</a>
    </div>
  </form>
</div>
"""

@app.route("/book", methods=["GET","POST"])
def book():
    if request.method == "GET":
        return shell("احجز موعد", BOOK_FORM, _load_count())

    f = request.form
    name       = (f.get("name") or "").strip()
    age        = (f.get("age") or "").strip()
    typ        = (f.get("type") or "").strip()
    channel    = (f.get("channel") or "").strip()
    phone      = (f.get("phone") or "").strip()
    best_time  = (f.get("best_time") or "").strip()
    summary    = (f.get("summary") or "").strip()

    msg = (
        "طلب حجز جديد — عربي سايكو\n"
        f"👤 الاسم: {name}\n🎯 نوع الموعد: {typ}\n📞 وسيلة التواصل: {channel}\n"
        f"📱 الرقم: {phone}\n⏰ أفضل وقت: {best_time}\n📝 نبذة: {summary}\n"
        "— أُرسل من نموذج الحجز بالموقع."
    )

    _telegram_notify(msg)

    encoded = urllib.parse.quote_plus(msg)
    if "الطبيب" in typ:
        wa_base = PSYCH_WA
    elif "الاجتماعي" in typ:
        wa_base = SOCIAL_WA
    else:
        wa_base = PSYCHO_WA
    wa_link = wa_base + ("&" if "?" in wa_base else "?") + f"text={encoded}"
    return redirect(wa_link, code=302)

# -------- دراسة الحالة المختصرة (تبقى لديك النسخة الموسعة إن رغبت) --------
def score_true(data, keys): return sum(1 for k in keys if data.get(k) is not None)

FORM_HTML = """
<div class="card">
  <h1>📝 دراسة الحالة</h1>
  <div class="small">قسّم الأعراض بوضوح ثم اعرض الترشيحات الأولية مع روابط لأدوات CBT وبرنامج الإدمان.</div>
  <form method="post" action="/case">
    <div class="grid">
      <div class="tile"><h3>المزاج</h3>
        <label class="chk"><input type="checkbox" name="low_mood"> مزاج منخفض</label>
        <label class="chk"><input type="checkbox" name="anhedonia"> فقدان المتعة</label>
        <label class="chk"><input type="checkbox" name="fatigue"> إرهاق</label>
        <label class="chk"><input type="checkbox" name="sleep_issue"> نوم مضطرب</label>
        <label class="chk"><input type="checkbox" name="appetite_change"> تغيّر شهية</label>
      </div>
      <div class="tile"><h3>القلق/الهلع</h3>
        <label class="chk"><input type="checkbox" name="worry"> قلق مفرط</label>
        <label class="chk"><input type="checkbox" name="tension"> توتر جسدي</label>
        <label class="chk"><input type="checkbox" name="panic_attacks"> نوبات هلع</label>
        <label class="chk"><input type="checkbox" name="social_fear"> قلق اجتماعي</label>
      </div>
      <div class="tile"><h3>وسواس/صدمة</h3>
        <label class="chk"><input type="checkbox" name="obsessions"> أفكار مُلِحّة</label>
        <label class="chk"><input type="checkbox" name="compulsions"> أفعال قهرية</label>
        <label class="chk"><input type="checkbox" name="flashbacks"> استرجاعات</label>
        <label class="chk"><input type="checkbox" name="hypervigilance"> يقظة مفرطة</label>
      </div>
      <div class="tile"><h3>ذهانية / طيف الفصام</h3>
        <label class="chk"><input type="checkbox" name="hallucinations"> هلوسات</label>
        <label class="chk"><input type="checkbox" name="delusions"> أوهام ثابتة</label>
        <label class="chk"><input type="checkbox" name="disorganized_speech"> تفكير/كلام غير منظّم</label>
        <label class="chk"><input type="checkbox" name="negative_symptoms"> أعراض سلبية</label>
        <label class="chk"><input type="checkbox" name="catatonia"> سمات كاتاتونية</label>
        <label class="chk"><input type="checkbox" name="decline_function"> تدهور وظيفي</label>
        <label class="chk"><input type="checkbox" name="duration_lt_1m"> المدّة &lt; شهر</label>
        <label class="chk"><input type="checkbox" name="duration_ge_1m"> المدّة ≥ شهر</label>
        <label class="chk"><input type="checkbox" name="duration_ge_6m"> المدّة ≥ 6 أشهر</label>
      </div>
      <div class="tile"><h3>مواد</h3>
        <label class="chk"><input type="checkbox" name="craving"> اشتهاء</label>
        <label class="chk"><input type="checkbox" name="withdrawal"> انسحاب</label>
        <label class="chk"><input type="checkbox" name="use_harm"> استخدام رغم الضرر</label>
      </div>
    </div>
    <div class="tile" style="margin-top:10px">
      <label>ملاحظاتك<textarea name="notes" rows="4" placeholder="أي تفاصيل إضافية مهمة لك"></textarea></label>
    </div>
    <button class="btn gold" type="submit">عرض الترشيحات</button>
  </form>
</div>
"""

def build_recommendations(data):
    picks, go_cbt, go_add = [], [], []
    dep = score_true(data, ["low_mood","anhedonia","fatigue","sleep_issue","appetite_change"])
    if dep >= 3:
        picks.append(("اضطراب اكتئابي", "عدة أعراض أساسية للمزاج", min(100, dep*15)))
        go_cbt += ["تنشيط سلوكي", "سجل الأفكار", "نظافة النوم"]
    anx = score_true(data, ["worry","tension"])
    if anx >= 2:
        picks.append(("قلق معمم", "قلق مفرط مع توتر جسدي", 75))
        go_cbt += ["تنفّس 4-4-6", "تعرّض تدريجي + منع طمأنة"]
    if data.get("panic_attacks"):
        picks.append(("نوبات هلع", "نوبات مفاجئة مع خوف من التكرار", 70))
        go_cbt += ["تعرّض داخلي", "منع السلوكيات الآمنة"]
    if data.get("social_fear"):
        picks.append(("قلق اجتماعي", "خشية تقييم الآخرين وتجنّب", 70))
        go_cbt += ["سلم مواقف اجتماعية"]
    if data.get("obsessions") and data.get("compulsions"):
        picks.append(("وسواس قهري", "وساوس + أفعال قهرية", 80))
        go_cbt += ["ERP (التعرّض مع منع الاستجابة)"]
    if score_true(data, ["flashbacks","hypervigilance"]) >= 2:
        picks.append(("آثار صدمة", "استرجاعات ويقظة مفرطة", 70))
        go_cbt += ["تقنية التأريض 5-4-3-2-1", "تنظيم التنفس"]
    if score_true(data, ["craving","withdrawal","use_harm"]) >= 2:
        picks.append(("تعاطي مواد", "اشتهاء/انسحاب/استخدام رغم الضرر", 80))
        go_add += ["generic"]

    psychotic_keys = ["hallucinations","delusions","disorganized_speech","negative_symptoms","catatonia"]
    pc = score_true(data, psychotic_keys)
    dur_lt_1m  = bool(data.get("duration_lt_1m"))
    dur_ge_1m  = bool(data.get("duration_ge_1m"))
    dur_ge_6m  = bool(data.get("duration_ge_6m"))
    decline    = bool(data.get("decline_function"))

    if pc >= 2 and (dur_ge_6m or (dur_ge_1m and decline)):
        picks.append(("فصام", "أعراض ذهانية أساسية مع استمرار/تدهور وظيفي", 85))
        go_cbt += ["تثقيف + مهارات التعامل", "تنظيم روتين ونوم", "دعم أسري"]
    elif pc >= 2 and (dep >= 3):
        picks.append(("فصامي وجداني", "ذهانية مع كتلة مزاجية واضحة", 75))
        go_cbt += ["تنظيم المزاج", "إدارة الضغوط"]
    elif pc >= 2 and dur_lt_1m:
        picks.append(("اضطراب ذهاني وجيز", "ذهانية قصيرة المدة", 65))
    elif data.get("delusions") and pc == 1 and dur_ge_1m and not decline:
        picks.append(("اضطراب وهامي", "أوهام ثابتة مع أداء وظيفي مقبول", 60))

    go_cbt = sorted(set(go_cbt)); go_add = sorted(set(go_add))
    return picks, go_cbt, go_add

def render_results(picks, go_cbt, go_add, notes):
    items = "".join([f"<li><b>{t}</b> — {w} <small>(درجة: {s:.0f})</small></li>" for (t,w,s) in picks]) or "<li>لا توجد مؤشرات كافية.</li>"
    cbt_block = ("<h3>🔧 أدوات CBT المقترحة</h3><ul>" + "".join(f"<li>{x}</li>" for x in go_cbt) +
                 "</ul><a class='btn' href='/cbt'>انتقل إلى CBT</a>") if go_cbt else ""
    add_block = "<h3>🚭 برنامج الإدمان</h3><a class='btn alt' href='/addiction'>افتح برنامج الإدمان</a>" if go_add else ""
    note_html = f"<h3>ملاحظاتك</h3><div class='tile'>{notes}</div>" if notes else ""
    booking = "<h3>📅 احجز جلسة</h3><a class='btn gold' href='/book'>نموذج الحجز</a>"
    return "<div class='card'><h1>📌 ترشيحات أولية</h1><ul style='line-height:1.9'>" + items + "</ul>" + cbt_block + add_block + note_html + booking + "</div>"

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell("دراسة الحالة", FORM_HTML, _load_count())
    data = {k: v for k, v in request.form.items()}
    picks, go_cbt, go_add = build_recommendations(data)
    notes = (request.form.get("notes") or "").strip()
    return shell("نتيجة الترشيح", render_results(picks, go_cbt, go_add, notes), _load_count())

# -------- تواصل --------
@app.get("/contact")
def contact():
    html = f"""
    <div class="card">
      <h1>📞 التواصل</h1>
      <div class="grid">
        <div class="tile">
          <h3>قنوات عامة</h3>
          <a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">تيليجرام عربي سايكو</a>
          <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">واتساب</a>
        </div>
        <div class="tile">
          <h3>حجز سريع</h3>
          <a class="btn gold" href="/book">📅 افتح نموذج الحجز</a>
        </div>
      </div>
    </div>
    """
    return shell("التواصل", html, _load_count())

# -------- صحة --------
@app.get("/health")
def health():
    return {"status":"ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
