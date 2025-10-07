# app.py — عربي سايكو: واجهة أنيقة + دراسة حالة موسّعة (تشمل ثنائي القطب) + DSM/CBT/إدمان + حجز + نبذة + تواصل + عدّاد زوّار
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

TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696?text=%D8%B9%D8%B1%D8%A8%D9%8A%20%D8%B3%D8%A7%D9%8A%D9%83%D9%88")

PSYCHO_WA = os.environ.get("PSYCHOLOGIST_WA", "https://wa.me/966530565696")
PSYCH_WA  = os.environ.get("PSYCHIATRIST_WA", "https://wa.me/966530565696")
SOCIAL_WA = os.environ.get("SOCIAL_WORKER_WA", "https://wa.me/966530565696")

TG_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID")

# -------- عدّاد الزوّار بسيط (ملف JSON) --------
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
    _save_count(n);  return n

# -------- إطار الصفحات (مع خط عربي وشعار ووضع طباعة) --------
def shell(title: str, content: str, visitors: int | None = None) -> str:
    visitors_html = f"<div class='small' style='margin-top:12px'>👀 عدد الزوّار: <b>{visitors}</b></div>" if visitors is not None else ""
    return f"""<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>
:root{{--p:#4B0082;--g:#FFD700;--bg:#f8f6ff;--ink:#2b1a4c}}
*{{box-sizing:border-box}} html,body{{height:100%}}
body{{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif;color:var(--ink);font-size:16.5px}}
.layout{{display:grid;grid-template-columns:280px 1fr;min-height:100vh}}
.side{{background:linear-gradient(180deg,#4b0082,#3a0d72);color:#fff;padding:18px;position:sticky;top:0;height:100vh}}
.logo{{display:flex;align-items:center;gap:10px;margin-bottom:18px}}
.logo img{{width:48px;height:48px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
.brand{{font-weight:900;letter-spacing:.3px;font-size:20px}}
.nav a{{display:block;color:#fff;text-decoration:none;padding:10px 12px;border-radius:12px;margin:6px 0;font-weight:700;opacity:.95}}
.nav a:hover{{opacity:1;background:rgba(255,255,255,.12)}}
.badge{{display:inline-block;background:var(--g);color:#4b0082;border-radius:999px;padding:2px 10px;font-weight:900;font-size:.8rem}}
.content{{padding:26px}}
.card{{background:#fff;border:1px solid #eee;border-radius:16px;padding:20px;box-shadow:0 10px 24px rgba(0,0,0,.06)}}
.grid{{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}
.tile{{background:#fff;border:1px solid #eee;border-radius:14px;padding:14px}}
h1{{font-weight:900;font-size:28px}} h2{{font-weight:800}} h3{{font-weight:800;margin:.2rem 0 .6rem}}
.note{{background:#fff7d1;border:1px dashed #e5c100;border-radius:12px;padding:10px 12px;margin:10px 0}}
.btn{{display:inline-block;background:var(--p);color:#fff;text-decoration:none;padding:11px 16px;border-radius:12px;font-weight:800}}
.btn.alt{{background:#5b22a6}} .btn.gold{{background:var(--g);color:#4b0082}}
.btn.wa{{background:#25D366}} .btn.tg{{background:#229ED9}}
label.chk{{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:8px}}
input,select,textarea{{width:100%;border:1px solid #ddd;border-radius:10px;padding:10px}}
.small{{font-size:.95rem;opacity:.85}}
.footer{{text-align:center;color:#fff;margin-top:24px;padding:14px;background:#3a0d72}}
hr.sep{{border:none;height:1px;background:#eee;margin:14px 0}}
.row{{display:flex;gap:10px;flex-wrap:wrap}}
.badge2{{display:inline-block;border:1px solid #eee;background:#fafafa;padding:6px 10px;border-radius:999px;margin:4px 4px 0 0;font-weight:700}}
.header-result{{display:flex;align-items:center;gap:12px;margin-bottom:10px}}
.header-result img{{width:44px;height:44px;border-radius:10px}}
.summary-cards{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin-top:8px}}
.scard{{background:#fafafa;border:1px solid #eee;border-radius:14px;padding:12px}}
@media print {{
  .side, .footer {{ display:none !important; }}
  .content {{ padding:0 !important; }}
  body {{ background:#fff; font-size:18px; }}
  .card {{ box-shadow:none; border:none; }}
}}
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
      <a href="/about">ℹ️ نبذة</a>
      <a href="/contact">📞 تواصل</a>
    </nav>
    <div class="small" style="margin-top:18px;opacity:.9">«نراك بعيون الاحترام، ونساندك بخطوات عملية.»</div>
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
      <div class="small">مساحتك الهادئة لفهم الأعراض وبناء خطة أولية محترمة لخصوصيتك.</div>
    </div>
    <div class="grid">
      <div class="tile"><h3>📝 دراسة الحالة</h3><p class="small">قسّم الأعراض بدقة؛ تربطك بنتائج CBT والإدمان.</p><a class="btn gold" href="/case">ابدأ الآن</a></div>
      <div class="tile"><h3>📘 مرجع DSM</h3><p class="small">قوائم تغطي المزاج والقلق والوسواس والذهان والمواد…</p><a class="btn alt" href="/dsm">فتح DSM</a></div>
      <div class="tile"><h3>🧠 CBT</h3><p class="small">خطط اختيارية + خطط جاهزة بنقرة.</p><a class="btn" href="/cbt">افتح CBT</a></div>
      <div class="tile"><h3>🚭 برنامج الإدمان</h3><p class="small">Detox → Rehab → Relapse بخيارات واضحة.</p><a class="btn" href="/addiction">افتح الإدمان</a></div>
      <div class="tile"><h3>📅 احجز موعدًا</h3><p class="small">الأخصائي النفسي / الطبيب النفسي / الأخصائي الاجتماعي.</p><a class="btn gold" href="/book">نموذج الحجز</a></div>
      <div class="tile"><h3>ℹ️ نبذة</h3><p class="small">رسالتنا، منهجيتنا، والخصوصية.</p><a class="btn alt" href="/about">اقرأ النبذة</a></div>
      <div class="tile"><h3>تواصل سريع</h3><a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">تيليجرام عربي سايكو</a> <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">واتساب</a></div>
    </div>
    """
    return shell("الرئيسية — عربي سايكو", content, visitors)

# -------- ربط DSM / CBT / Addiction من الملفات الخارجية إن وُجدت --------
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

# -------- إشعار تيليجرام اختياري --------
def _telegram_notify(text: str):
    if not (TG_BOT_TOKEN and TG_CHAT_ID and requests):
        return False
    try:
        requests.post(f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
                      data={"chat_id": TG_CHAT_ID, "text": text})
        return True
    except Exception:
        return False

# -------- نموذج الحجز --------
BOOK_FORM = """
<div class="card">
  <h1>📅 احجز موعدك</h1>
  <div class="note">«موعدٌ واحد قد يغيّر مسار أسبوعك.»</div>
  <form method="post" action="/book" novalidate>
    <h3>1) بيانات أساسية</h3>
    <div class="grid">
      <div class="tile"><label>الاسم الكامل<input name="name" required placeholder="مثال: محمد أحمد"></label></div>
      <div class="tile"><label>العمر<input name="age" type="number" min="5" max="120" placeholder="28"></label></div>
      <div class="tile"><label>نوع الموعد
        <select name="type" required>
          <option value="الأخصائي النفسي">الأخصائي النفسي</option>
          <option value="الطبيب النفسي">الطبيب النفسي</option>
          <option value="الأخصائي الاجتماعي">الأخصائي الاجتماعي</option>
        </select></label>
      </div>
    </div>
    <hr class="sep"/>
    <h3>2) طريقة التواصل</h3>
    <div class="grid">
      <div class="tile"><label>الوسيلة
        <select name="channel" required>
          <option value="واتساب">واتساب</option>
          <option value="اتصال">اتصال</option>
          <option value="تيليجرام">تيليجرام</option>
        </select></label>
      </div>
      <div class="tile"><label>رقم التواصل<input name="phone" required placeholder="9665xxxxxxxx" pattern="\\d{9,15}"></label></div>
      <div class="tile"><label>أفضل وقت للتواصل<input name="best_time" placeholder="مساءً 7-9"></label></div>
    </div>
    <div class="tile" style="margin-top:10px"><label>نبذة موجزة<textarea name="summary" rows="5" placeholder="اكتب بإيجاز ما يهمك متابعته في الجلسة"></textarea></label></div>
    <div class="row"><button class="btn gold" type="submit">إرسال الطلب عبر واتساب</button><a class="btn alt" href="/">رجوع</a></div>
  </form>
</div>
"""

@app.route("/book", methods=["GET","POST"])
def book():
    if request.method == "GET":
        return shell("احجز موعد", BOOK_FORM, _load_count())
    f = request.form
    name, age, typ = (f.get("name","").strip(), f.get("age","").strip(), f.get("type","").strip())
    channel, phone, best_time, summary = (f.get("channel","").strip(), f.get("phone","").strip(),
                                          f.get("best_time","").strip(), f.get("summary","").strip())
    msg = ( "طلب حجز جديد — عربي سايكو\n"
            f"👤 الاسم: {name}\n🎯 نوع الموعد: {typ}\n📞 وسيلة التواصل: {channel}\n"
            f"📱 الرقم: {phone}\n⏰ أفضل وقت: {best_time}\n📝 نبذة: {summary}\n— أُرسل من نموذج الحجز." )
    _telegram_notify(msg)
    encoded = urllib.parse.quote_plus(msg)
    if "الطبيب" in typ: wa_base = PSYCH_WA
    elif "الاجتماعي" in typ: wa_base = SOCIAL_WA
    else: wa_base = PSYCHO_WA
    wa_link = wa_base + ("&" if "?" in wa_base else "?") + f"text={encoded}"
    return redirect(wa_link, code=302)

# -------- أدوات مساعدة لدراسة الحالة --------
def c(data,*keys):  # count true
    return sum(1 for k in keys if data.get(k) is not None)

# -------- نموذج دراسة الحالة (موسّعة) --------
FORM_HTML = """
<div class="card">
  <h1>📝 دراسة الحالة</h1>
  <div class="small">قسّم الأعراض بدقة؛ ستظهر ترشيحات أولية وروابط لأدوات CBT وبرنامج الإدمان.</div>

  <form method="post" action="/case">
    <div class="grid">
      <div class="tile"><h3>المزاج العام</h3>
        <label class="chk"><input type="checkbox" name="low_mood"> مزاج منخفض معظم اليوم</label>
        <label class="chk"><input type="checkbox" name="anhedonia"> فقدان المتعة</label>
        <label class="chk"><input type="checkbox" name="fatigue"> إرهاق/انخفاض طاقة</label>
        <label class="chk"><input type="checkbox" name="sleep_issue"> نوم مضطرب</label>
        <label class="chk"><input type="checkbox" name="appetite_change"> تغيّر الشهية/الوزن</label>
      </div>

      <div class="tile"><h3>اكتئاب — أعراض إضافية</h3>
        <label class="chk"><input type="checkbox" name="psychomotor"> تباطؤ/تهيج حركي</label>
        <label class="chk"><input type="checkbox" name="worthlessness"> شعور بالذنب/عدم القيمة</label>
        <label class="chk"><input type="checkbox" name="poor_concentration"> تركيز ضعيف/تردّد</label>
        <label class="chk"><input type="checkbox" name="suicidal"> أفكار إيذاء/انتحار</label>
        <label class="chk"><input type="checkbox" name="dep_2w"> استمرار ≥ أسبوعين</label>
        <label class="chk"><input type="checkbox" name="dep_function"> تأثير على الدراسة/العمل/العلاقات</label>
      </div>

      <div class="tile"><h3>قلق/هلع/اجتماعي</h3>
        <label class="chk"><input type="checkbox" name="worry"> قلق مفرط</label>
        <label class="chk"><input type="checkbox" name="tension"> توتر جسدي</label>
        <label class="chk"><input type="checkbox" name="panic_attacks"> نوبات هلع</label>
        <label class="chk"><input type="checkbox" name="social_fear"> خوف من تقييم اجتماعي</label>
      </div>

      <div class="tile"><h3>وسواس وصدمات</h3>
        <label class="chk"><input type="checkbox" name="obsessions"> أفكار مُلِحّة</label>
        <label class="chk"><input type="checkbox" name="compulsions"> أفعال قهرية</label>
        <label class="chk"><input type="checkbox" name="flashbacks"> استرجاعات/كوابيس</label>
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

      <div class="tile"><h3>ثنائي القطب / أعراض الهوس</h3>
        <label class="chk"><input type="checkbox" name="elevated_mood"> مزاج مرتفع/متهوّر</label>
        <label class="chk"><input type="checkbox" name="decreased_sleep_need"> قلة الحاجة للنوم</label>
        <label class="chk"><input type="checkbox" name="grandiosity"> شعور بالعظمة</label>
        <label class="chk"><input type="checkbox" name="racing_thoughts"> أفكار متسارعة</label>
        <label class="chk"><input type="checkbox" name="pressured_speech"> كلام ضاغط</label>
        <label class="chk"><input type="checkbox" name="risky_behavior"> سلوك محفوف بالمخاطر/صرف زائد</label>
        <label class="chk"><input type="checkbox" name="mania_ge_7d"> استمرار الأعراض ≥ 7 أيام</label>
        <label class="chk"><input type="checkbox" name="mania_hospital"> احتاج دخول/تدخل طبي</label>
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

# -------- منطق الترشيحات --------
def build_recommendations(data):
    picks, go_cbt, go_add = [], [], []

    # اكتئاب (قريب من PHQ-9)
    dep_core = c(data,"low_mood","anhedonia")
    dep_more = c(data,"fatigue","sleep_issue","appetite_change","psychomotor","worthlessness","poor_concentration","suicidal")
    dep_total = dep_core + dep_more
    dep_2w = bool(data.get("dep_2w"))
    dep_fx = bool(data.get("dep_function"))

    if dep_total >= 5 and dep_2w and dep_core >= 1:
        picks.append(("نوبة اكتئابية جسيمة (MDD)", "≥5 أعراض لمدة ≥ أسبوعين مع تأثير وظيفي", 90 if dep_fx else 80))
        go_cbt += ["تنشيط سلوكي", "سجل الأفكار", "تنظيم النوم", "حل المشكلات"]
    elif dep_total >= 3 and dep_2w:
        picks.append(("نوبة اكتئابية خفيفة/متوسطة", "مجموعة أعراض مستمرة أسبوعين", 70))
        go_cbt += ["تنشيط سلوكي", "سجل الأفكار", "مراقبة المزاج"]
    elif dep_core >= 1 and dep_total >= 2:
        picks.append(("مزاج منخفض/فتور", "كتلة أعراض مزاجية جزئية", 55))
        go_cbt += ["تنشيط سلوكي", "روتين يومي لطيف"]

    if data.get("suicidal"):
        picks.append(("تنبيه أمان", "وجود أفكار إيذاء/انتحار — فضّل تواصلًا فوريًا مع مختص", 99))

    # قلق/هلع/اجتماعي
    if c(data,"worry","tension") >= 2:
        picks.append(("قلق معمّم", "قلق مفرط مع توتر جسدي", 75)); go_cbt += ["تنفّس 4-4-6","منع الطمأنة"]
    if data.get("panic_attacks"):
        picks.append(("نوبات هلع", "نوبات مفاجئة مع خوف من التكرار", 70)); go_cbt += ["تعرّض داخلي","منع السلوكيات الآمنة"]
    if data.get("social_fear"):
        picks.append(("قلق اجتماعي", "خشية تقييم الآخرين وتجنّب", 70)); go_cbt += ["سُلم مواقف اجتماعية"]

    # وسواس/صدمات
    if data.get("obsessions") and data.get("compulsions"):
        picks.append(("وسواس قهري (OCD)", "وساوس + أفعال قهرية", 80)); go_cbt += ["ERP (التعرّض مع منع الاستجابة)"]
    if c(data,"flashbacks","hypervigilance") >= 2:
        picks.append(("آثار صدمة (PTSD/ASD)", "استرجاعات ويقظة مفرطة", 70)); go_cbt += ["تقنية التأريض 5-4-3-2-1","تنظيم التنفس"]

    # مواد
    if c(data,"craving","withdrawal","use_harm") >= 2:
        picks.append(("تعاطي مواد", "اشتهاء/انسحاب/استمرار رغم الضرر", 80)); go_add.append("generic")

    # ذهانية/طيف الفصام
    pc = c(data,"hallucinations","delusions","disorganized_speech","negative_symptoms","catatonia")
    dur_lt_1m  = bool(data.get("duration_lt_1m"))
    dur_ge_1m  = bool(data.get("duration_ge_1m"))
    dur_ge_6m  = bool(data.get("duration_ge_6m"))
    decline    = bool(data.get("decline_function"))
    if pc >= 2 and (dur_ge_6m or (dur_ge_1m and decline)):
        picks.append(("فصام", "ذهانية أساسية مع استمرار/تدهور وظيفي", 85)); go_cbt += ["تثقيف + مهارات التعامل","تنظيم الروتين والنوم","دعم أسري"]
    elif pc >= 2 and (dep_total >= 3):
        picks.append(("فصامي وجداني", "ذهانية مع كتلة مزاجية واضحة", 75))
    elif pc >= 2 and dur_lt_1m:
        picks.append(("اضطراب ذهاني وجيز", "ذهانية قصيرة المدة", 65))
    elif data.get("delusions") and pc == 1 and dur_ge_1m and not decline:
        picks.append(("اضطراب وهامي", "أوهام ثابتة مع أداء وظيفي مقبول", 60))

    # ثنائي القطب
    mania_count = c(data,"elevated_mood","decreased_sleep_need","grandiosity","racing_thoughts","pressured_speech","risky_behavior")
    mania_7d    = bool(data.get("mania_ge_7d"))
    mania_hosp  = bool(data.get("mania_hospital"))
    if mania_count >= 3 and (mania_7d or mania_hosp):
        picks.append(("اضطراب ثنائي القطب I (نوبة هوس)", "≥3 أعراض هوس مع مدة ≥7 أيام أو حاجة لتدخل/دخول", 85))
        go_cbt += ["تنظيم النوم الصارم","روتين يومي ثابت","تثقيف نفسي للأسرة"]
    elif mania_count >= 3 and dep_core >= 1 and not mania_hosp:
        picks.append(("ثنائي القطب II (هوس خفيف + اكتئاب)", "مجموعة أعراض هوس خفيف مع عناصر اكتئاب", 75))
        go_cbt += ["تنظيم النوم","تخطيط نشاط متوازن","مراقبة المزاج"]

    go_cbt = sorted(set(go_cbt)); go_add = sorted(set(go_add))
    return picks, go_cbt, go_add

# -------- صفحة نتائج منسّقة للطباعة والمشاركة --------
def render_results(picks, go_cbt, go_add, notes):
    items_li = "".join([f"<li><b>{t}</b> — {w} <small>(درجة: {s:.0f})</small></li>" for (t,w,s) in picks]) or "<li>لا توجد مؤشرات كافية.</li>"
    cbt_badges = "".join([f"<span class='badge2'>🔧 {x}</span>" for x in sorted(set(go_cbt))])
    add_badge  = "<span class='badge2'>🚭 برنامج الإدمان مُقترح</span>" if go_add else ""

    header = f"""
    <div class='header-result'>
      <img src='{LOGO}' alt='logo'/>
      <div>
        <div style='font-weight:900;font-size:20px'>{BRAND}</div>
        <div class='small'>نتيجة دراسة الحالة — تلخيص أولي قابل للطباعة والمشاركة</div>
      </div>
    </div>
    """

    summary = f"""
    <div class='summary-cards'>
      <div class='scard'><b>الترشيحات</b><br/><span class='small'>{len(picks)} نتيجة</span></div>
      <div class='scard'><b>CBT المقترح</b><br/>{(cbt_badges or "<span class='small'>لا شيء محدد</span>")}</div>
      <div class='scard'><b>الإدمان</b><br/>{(add_badge or "<span class='small'>لا مؤشرات</span>")}</div>
    </div>
    """

    note_html = f"<div class='tile' style='margin-top:10px'><b>ملاحظاتك:</b><br/>{notes}</div>" if notes else ""

    actions = f"""
    <div class='row' style='margin-top:12px'>
      <button class='btn alt' onclick='window.print()'>🖨️ طباعة</button>
      <button class='btn' onclick='saveJSON()'>💾 تنزيل JSON</button>
      <a class='btn wa' id='share-wa' target='_blank' rel='noopener'>🟢 مشاركة واتساب</a>
      <a class='btn tg' id='share-tg' target='_blank' rel='noopener'>✈️ مشاركة تيليجرام</a>
      <a class='btn gold' href='/book'>📅 حجز سريع</a>
      <a class='btn' href='/cbt'>🧠 فتح CBT</a>
      <a class='btn alt' href='/addiction'>🚭 برنامج الإدمان</a>
    </div>
    <script>
      function buildShareText(){{
        const items=[...document.querySelectorAll('#diag-items li')].map(li=>'- '+li.innerText).join('\\n');
        const notes={json.dumps(notes or "")!r};
        let msg = 'نتيجة دراسة الحالة — {BRAND}\\n' + items;
        if(notes) msg += '\\n\\nملاحظات: ' + notes;
        return msg;
      }}
      function saveJSON(){{
        const data={{items:[...document.querySelectorAll('#diag-items li')].map(li=>li.innerText),
                     cbt:[...document.querySelectorAll('.badge2')].map(b=>b.innerText),
                     notes:{json.dumps(notes or "")!r},
                     created_at:new Date().toISOString()}};
        const a=document.createElement('a');
        a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}}));
        a.download='case_result.json'; a.click(); URL.revokeObjectURL(a.href);
      }}
      const text = encodeURIComponent(buildShareText());
      document.getElementById('share-wa').href = '{WA_URL.split("?")[0]}' + '?text=' + text;
      document.getElementById('share-tg').href = 'https://t.me/share/url?url=' + encodeURIComponent('') + '&text=' + text;
    </script>
    """

    return f"""
    <div class='card'>
      {header}
      {summary}
      <h2 style='margin-top:12px'>📌 الترشيحات</h2>
      <ul id='diag-items' style='line-height:1.9'>{items_li}</ul>
      {note_html}
      {actions}
    </div>
    """

# -------- المسار: دراسة الحالة --------
@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell("دراسة الحالة", FORM_HTML, _load_count())
    data  = {k: v for k, v in request.form.items()}
    picks, go_cbt, go_add = build_recommendations(data)
    notes = (request.form.get("notes") or "").strip()
    return shell("نتيجة الترشيح", render_results(picks, go_cbt, go_add, notes), _load_count())

# -------- نبذة --------
ABOUT_HTML = f"""
<div class="card">
  <h1>ℹ️ نبذة عن {BRAND}</h1>
  <p class="small">«نراك بعيون الاحترام، ونساندك بخطوات عملية.» — علاج نفسي افتراضي يربط بين دراسة الحالة وCBT وبرنامج الإدمان والحجز السريع.</p>
  <h2>رسالتنا</h2>
  <p>مساحة هادئة ومنظّمة لفهم الأعراض وبناء خطة أولية محترمة للخصوصية.</p>
  <h2>ماذا نقدّم؟</h2>
  <ul>
    <li><b>دراسة حالة موسّعة:</b> اكتئاب، قلق، وسواس، ذهان، ثنائي القطب، مواد — مع ترشيحات مرتبطة بالأدوات.</li>
    <li><b>CBT مُيسّر:</b> خطط اختيارية وخطط جاهزة قابلة للتنزيل أو الطباعة.</li>
    <li><b>إدمان:</b> مسار واضح Detox → Rehab → Relapse.</li>
    <li><b>حجز:</b> الأخصائي النفسي/الطبيب النفسي/الأخصائي الاجتماعي.</li>
  </ul>
  <div class="row">
    <a class="btn gold" href="/case">📝 ابدأ دراسة الحالة</a>
    <a class="btn" href="/cbt">🧠 أدوات CBT</a>
    <a class="btn alt" href="/addiction">🚭 برنامج الإدمان</a>
    <a class="btn tg" href="{TG_URL}" target="_blank">✈️ تيليجرام</a>
    <a class="btn wa" href="{WA_URL}" target="_blank">🟢 واتساب</a>
    <a class="btn gold" href="/book">📅 احجز موعد</a>
  </div>
</div>
"""
@app.get("/about")
def about():
    return shell("نبذة — عربي سايكو", ABOUT_HTML, _load_count())

# -------- تواصل --------
@app.get("/contact")
def contact():
    html = f"""
    <div class="card">
      <h1>📞 التواصل</h1>
      <div class="grid">
        <div class="tile"><h3>قنوات عامة</h3>
          <a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">تيليجرام عربي سايكو</a>
          <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">واتساب</a>
        </div>
        <div class="tile"><h3>حجز سريع</h3><a class="btn gold" href="/book">📅 افتح نموذج الحجز</a></div>
      </div>
    </div>
    """
    return shell("التواصل", html, _load_count())

# -------- صحة الخدمة --------
@app.get("/health")
def health():
    return {"status":"ok"}, 200

# -------- تشغيل محلي --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
