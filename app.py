# app.py — عربي سايكو (تجميعة مع فصل CBT في cbt.py)
import os, urllib.parse, json
from flask import Flask, request, redirect

app = Flask(__name__)

# ===== إعدادات عامة =====
app.config["BRAND"] = os.environ.get("BRAND_NAME", "عربي سايكو")
app.config["LOGO"]  = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
app.config["TG_URL"]= os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
app.config["WA_URL"]= os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696?text=%D8%B9%D8%B1%D8%A8%D9%8A%20%D8%B3%D8%A7%D9%8A%D9%83%D9%88")

PSYCHO_WA = os.environ.get("PSYCHOLOGIST_WA", "https://wa.me/966530565696")
PSYCH_WA  = os.environ.get("PSYCHIATRIST_WA", "https://wa.me/966530565696")
SOCIAL_WA = os.environ.get("SOCIAL_WORKER_WA", "https://wa.me/966530565696")

# ===== عدّاد زوّار =====
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

# ===== إطار الصفحات (shell) =====
def shell(title: str, content: str, visitors: int | None = None) -> str:
    BRAND = app.config["BRAND"]; LOGO = app.config["LOGO"]
    TG_URL = app.config["TG_URL"]; WA_URL = app.config["WA_URL"]
    visitors_html = f"<div class='small' style='margin-top:12px'>👀 عدد الزوّار: <b>{visitors}</b></div>" if visitors is not None else ""
    return f"""<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<style>
:root{{--p:#4B0082;--g:#FFD700;--bg:#f8f6ff;--ink:#2b1a4c}}
*{{box-sizing:border-box}} html,body{{height:100%}}
body{{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif;color:var(--ink);font-size:16.5px;line-height:1.6}}
.layout{{display:grid;grid-template-columns:280px 1fr;min-height:100vh}}
.side{{background:linear-gradient(180deg,#4b0082,#3a0d72);color:#fff;padding:18px;position:sticky;top:0;height:100vh}}
.logo{{display:flex;align-items:center;gap:10px;margin-bottom:18px}}
.logo img{{width:48px;height:48px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
.brand{{font-weight:900;letter-spacing:.3px;font-size:20px}}
.nav a{{display:block;color:#fff;text-decoration:none;padding:10px 12px;border-radius:12px;margin:6px 0;font-weight:700;opacity:.95}}
.nav a:hover{{opacity:1;background:rgba(255,255,255,.12)}}
.badge{{display:inline-block;background:var(--g);color:#4b0082;border-radius:999px;padding:2px 10px;font-weight:900;font-size:.8rem}}
.content{{padding:26px}}
.card{{background:#fff;border:1px solid #eee;border-radius:16px;padding:22px;box-shadow:0 10px 24px rgba(0,0,0,.06)}}
.grid{{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}
.tile{{background:#fff;border:1px solid #eee;border-radius:14px;padding:14px}}
h1{{font-weight:900;font-size:28px}} h2{{font-weight:800;margin:.2rem 0 .6rem}} h3{{font-weight:800;margin:.2rem 0 .6rem}}
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
.table{{width:100%;border-collapse:collapse}}
.table th,.table td{{border:1px solid #eee;padding:8px;text-align:center}}
.screen-only{{display:initial}} .print-only{{display:none}}
@media print {{
  @page {{ size: A4; margin: 16mm 14mm; }}
  .side, .footer, .screen-only {{ display:none !important; }}
  .print-only {{ display:initial !important; }}
  body {{ background:#fff; font-size:18px; line-height:1.8; }}
  .content {{ padding:0 !important; }}
  .card {{ box-shadow:none; border:none; padding:0; }}
  h1{{font-size:26px}} h2{{font-size:22px}} h3{{font-size:18px}}
  ul{{padding-inline-start:20px}}
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
      <a href="/contact">📞 تواصل</a>
    </nav>
    <div class="small" style="margin-top:18px;opacity:.9">«نراك بعيون الاحترام، ونساندك بخطوات عملية.»</div>
    {{visitors_html}}
  </aside>
  <main class="content">{content}</main>
</div>
<div class="footer"><small>© جميع الحقوق محفوظة لـ {BRAND}</small></div>
</body></html>""".replace("{{visitors_html}}", visitors_html)

# اجعل الدوال متاحة للبلوپرنت
app.config["SHELL"] = shell
app.config["LOAD_COUNT"] = _load_count

# ===== الرئيسية =====
@app.get("/")
def home():
    visitors = bump_visitors()
    BRAND = app.config["BRAND"]; TG_URL = app.config["TG_URL"]; WA_URL = app.config["WA_URL"]
    content = f"""
    <div class="card" style="margin-bottom:14px">
      <h1>مرحبًا بك في {BRAND}</h1>
      <div class="small">مساحتك الهادئة لفهم الأعراض وبناء خطة عملية محترمة لخصوصيتك.</div>
    </div>
    <div class="grid">
      <div class="tile"><h3>📝 دراسة الحالة</h3><p class="small">قسّم الأعراض بدقة؛ ترتبط بالـ CBT وبرنامج الإدمان والحجز.</p><a class="btn gold" href="/case">ابدأ الآن</a></div>
      <div class="tile"><h3>📘 مرجع DSM</h3><p class="small">ملخّص منظّم للمحاور الكبرى.</p><a class="btn alt" href="/dsm">فتح DSM</a></div>
      <div class="tile"><h3>🧠 CBT</h3><p class="small">15 خطة علمية + مولّد جدول 7/10/14 يوم (دمج خطتين).</p><a class="btn" href="/cbt">افتح CBT</a></div>
      <div class="tile"><h3>🚭 برنامج الإدمان</h3><p class="small">Detox → Rehab → Aftercare → منع الانتكاس.</p><a class="btn" href="/addiction">افتح الإدمان</a></div>
      <div class="tile"><h3>📅 احجز موعدًا</h3><p class="small">الأخصائي النفسي / الطبيب النفسي / الأخصائي الاجتماعي.</p><a class="btn gold" href="/book">نموذج الحجز</a></div>
      <div class="tile"><h3>تواصل سريع</h3><a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">تيليجرام</a> <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">واتساب</a></div>
    </div>
    """
    return shell("الرئيسية — عربي سايكو", content, visitors)

# ===== DSM مختصر =====
DSM_HTML = """
<div class="card">
  <h1>📘 DSM — ملخّص داخلي</h1>
  <p class="small">مرجع سريع لقراءة النتائج وتوجيه الخطط.</p>
  <div class="grid">
    <div class="tile"><h3>الاكتئاب (MDD)</h3><ul>
      <li>مزاج منخفض/فقد المتعة + ≥4 (نوم/شهية/طاقة/تباطؤ/ذنب/تركيز/أفكار إيذاء).</li>
      <li>المدة ≥ أسبوعين + تأثير وظيفي.</li>
    </ul></div>
    <div class="tile"><h3>القلق المعمّم</h3><ul><li>قلق زائد ≥6 أشهر + توتر/إجهاد/تركيز/نوم..</li></ul></div>
    <div class="tile"><h3>الهلع</h3><ul><li>نوبات مفاجئة + خشية التكرار وتجنّب.</li></ul></div>
    <div class="tile"><h3>القلق الاجتماعي</h3><ul><li>خشية تقييم الآخرين وتجنّب.</li></ul></div>
    <div class="tile"><h3>OCD</h3><ul><li>وساوس + أفعال قهرية تؤثر على الأداء.</li></ul></div>
    <div class="tile"><h3>PTSD</h3><ul><li>استرجاعات/كوابيس/تجنّب/يقظة مفرطة.</li></ul></div>
    <div class="tile"><h3>طيف الفصام</h3><ul><li>ذهانية ± أعراض سلبية؛ النوع حسب المدة والأداء.</li></ul></div>
    <div class="tile"><h3>ثنائي القطب</h3><ul><li>هوس (≥7 أيام/دخول) أو هوس خفيف + اكتئاب.</li></ul></div>
    <div class="tile"><h3>تعاطي المواد</h3><ul><li>اشتهاء/انسحاب/استخدام رغم الضرر… الشدة حسب عدد المعايير.</li></ul></div>
  </div>
</div>
"""
@app.get("/dsm")
def dsm():
    return shell("DSM — مرجع", DSM_HTML, _load_count())

# ===== برنامج الإدمان =====
ADDICTION_HTML = f"""
<div class="card">
  <h1>🚭 برنامج الإدمان — مسار واضح</h1>
  <p class="small">تقييم → سحب آمن → تأهيل → رعاية لاحقة → خطة منع الانتكاس.</p>
  <div class="grid">
    <div class="tile"><h3>التقييم الأولي</h3><ul><li>تاريخ التعاطي والمواد والشدة.</li><li>فحوصات السلامة والمخاطر.</li></ul></div>
    <div class="tile"><h3>Detox</h3><ul><li>سحب آمن بإشراف طبي.</li><li>ترطيب ونوم ودعم غذائي.</li></ul></div>
    <div class="tile"><h3>Rehab</h3><ul><li>CBT للإدمان، مهارات رفض، إدارة مثيرات.</li><li>مجموعات دعم/أسرة.</li></ul></div>
    <div class="tile"><h3>Aftercare</h3><ul><li>متابعة أسبوعية أول 3 أشهر.</li><li>نشاطات بديلة صحية.</li></ul></div>
    <div class="tile"><h3>منع الانتكاس</h3><ul><li>قائمة مثيرات شخصية + بدائل.</li><li>شبكة تواصل فوري.</li></ul></div>
  </div>
  <div class="row" style="margin-top:12px">
    <a class="btn gold" href="/case">اربط مع دراسة الحالة</a>
    <a class="btn" href="/book">📅 احجز جلسة</a>
  </div>
</div>
"""
@app.get("/addiction")
def addiction():
    return shell("علاج الإدمان", ADDICTION_HTML, _load_count())

# ===== نموذج الحجز =====
BOOK_FORM = f"""
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
      <div class="tile"><label>رقم التواصل<input name="phone" required placeholder="9665xxxxxxxx" pattern="\\d{{9,15}}"></label></div>
      <div class="tile"><label>أفضل وقت للتواصل<input name="best_time" placeholder="مساءً 7-9"></label></div>
    </div>
    <div class="tile" style="margin-top:10px"><label>نبذة موجزة<textarea name="summary" rows="5" placeholder="اكتب بإيجاز ما يهمك متابعته في الجلسة"></textarea></label></div>
    <div class="row"><button class="btn gold" type="submit">إرسال عبر واتساب</button><a class="btn alt" href="/">رجوع</a></div>
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
    encoded = urllib.parse.quote_plus(msg)
    if "الطبيب" in typ: wa_base = PSYCH_WA
    elif "الاجتماعي" in typ: wa_base = SOCIAL_WA
    else: wa_base = PSYCHO_WA
    wa_link = wa_base + ("&" if "?" in wa_base else "?") + f"text={encoded}"
    return redirect(wa_link, code=302)

# ===== دراسة الحالة (بالمنطق الذي لديك سابقًا) =====
def c(data,*keys):
    return sum(1 for k in keys if data.get(k) is not None)

FORM_HTML = """
<div class="card">
  <h1>📝 دراسة الحالة</h1>
  <div class="small">قسّم الأعراض بدقة؛ ستظهر ترشيحات أولية وروابط لأدوات CBT وبرنامج الإدمان والحجز.</div>
  <!-- أبقِ نفس الحقول التي اعتمدتها سابقًا -->
  <form method="post" action="/case">
    <!-- ضع بقية حقولك هنا كما هي -->
    <button class="btn gold" type="submit">عرض الترشيحات</button>
  </form>
</div>
"""
@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell("دراسة الحالة", FORM_HTML, _load_count())
    data  = {k: v for k, v in request.form.items()}
    # استدعِ build_recommendations الخاصة بك هنا إن كانت بملف آخر
    picks, go_cbt, go_add = [], [], []
    notes = (request.form.get("notes") or "").strip()
    return shell("نتيجة الترشيح", "<div class='card'>سيتم دمج النتائج هنا.</div>", _load_count())

# ===== تواصل =====
@app.get("/contact")
def contact():
    TG_URL = app.config["TG_URL"]; WA_URL = app.config["WA_URL"]
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
    </div>"""
    return shell("التواصل", html, _load_count())

@app.get("/health")
def health():
    return {"status":"ok"}, 200

# ===== تسجيل الـBlueprint لصفحة CBT =====
from cbt import cbt_bp
app.register_blueprint(cbt_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
