# app.py — عربي سايكو (إصدار موسّع): دراسة حالة مطوّرة + حجز جلسات + عبارات داعمة + إحصاءات
import os, importlib, sqlite3, secrets
from pathlib import Path
from datetime import date, timedelta
from flask import Flask, render_template_string, request, make_response, abort

app = Flask(__name__)

# ===== إعدادات عامة =====
BRAND_NAME   = os.environ.get("BRAND_NAME", "عربي سايكو")
WHATS_NUM    = os.environ.get("WHATS_NUM", "966530565696")   # 0530565696 -> بصيغة دولية
LOGO_URL     = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
TELEGRAM_URL = os.environ.get("TELEGRAM_URL", "https://t.me/ArabiPsychoBot")
STATS_KEY    = os.environ.get("STATS_KEY", "arabipsycho")

def wa_link(preset: str) -> str:
    from urllib.parse import quote
    return f"https://wa.me/{WHATS_NUM}?text={quote(preset)}"

BOOK_TEXT = "مرحبًا، أودّ حجز جلسة عبر عربي سايكو."

BOOKINGS = {
    "psy": wa_link(BOOK_TEXT + " مع الأخصائي النفسي."),
    "doc": wa_link(BOOK_TEXT + " مع الطبيب النفسي."),
    "soc": wa_link(BOOK_TEXT + " مع الأخصائي الاجتماعي.")
}

# ===== عدّاد الزوّار (SQLite بسيط) =====
DB_PATH = Path("visitors.db")
def _db():
    c = sqlite3.connect(DB_PATH)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("CREATE TABLE IF NOT EXISTS counters (id INTEGER PRIMARY KEY CHECK(id=1), total INTEGER NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS daily (day TEXT PRIMARY KEY, total INTEGER NOT NULL)")
    if c.execute("SELECT 1 FROM counters WHERE id=1").fetchone() is None:
        c.execute("INSERT INTO counters (id,total) VALUES (1,0)")
        c.commit()
    return c
def _today(): return date.today().isoformat()
def inc_visitors():
    if request.cookies.get("VSTR"): return None
    c=_db(); c.execute("UPDATE counters SET total=total+1 WHERE id=1")
    day=_today()
    row=c.execute("SELECT total FROM daily WHERE day=?",(day,)).fetchone()
    if row: c.execute("UPDATE daily SET total=total+1 WHERE day=?",(day,))
    else:   c.execute("INSERT INTO daily(day,total) VALUES(?,1)",(day,))
    c.commit(); c.close()
    import secrets as _s
    return _s.token_hex(16)
def total_visitors():
    c=_db(); n=c.execute("SELECT total FROM counters WHERE id=1").fetchone()[0]; c.close(); return n
def last30():
    c=_db()
    days=[(date.today()-timedelta(days=i)).isoformat() for i in range(29,-1,-1)]
    got=dict(c.execute("SELECT day,total FROM daily WHERE day IN ({})".format(",".join("?"*len(days))), tuple(days)).fetchall() or [])
    c.close(); return [(d, got.get(d,0)) for d in days]

# ===== تنسيق عام =====
BASE_HEAD = f"""
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="icon" href="{LOGO_URL}">
<style>
:root{{ --purple:#4B0082; --gold:#FFD700; --bg:#faf7e6 }}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif}}
.topbar{{position:sticky;top:0;background:var(--purple);color:#fff;padding:10px 14px;display:flex;gap:10px;align-items:center}}
.topbar img{{width:42px;height:42px;border-radius:50%}}
.toplinks a{{color:#fff;margin:0 6px;font-weight:700;text-decoration:none}}
.layout{{max-width:1250px;margin:20px auto;display:grid;gap:18px;grid-template-columns:290px 1fr;padding:0 12px}}
.sidebar,.card{{background:#fff;border:1px solid #eee;border-radius:16px;box-shadow:0 10px 24px rgba(0,0,0,.06)}}
.sidebar{{padding:16px}} .card{{padding:20px}}
.navlink{{display:block;padding:10px 12px;border-radius:12px;color:#222;border:1px solid #f0f0f0;margin-bottom:8px;text-decoration:none}}
.navlink:hover{{background:#fafafa}} .navlink.primary{{background:var(--purple);color:#fff;border-color:var(--purple)}}
.btn{{display:inline-block;background:var(--purple);color:#fff;padding:10px 14px;border-radius:12px;font-weight:700;text-decoration:none;text-align:center}}
.btn.alt{{background:#5b22a6}} .btn.gold{{background:var(--gold);color:#4B0082}}
.btn.whatsapp{{background:#25D366}} .btn.tg{{background:#229ED9}}
.grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
.grid-sm{{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}}
label.chk{{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:10px}}
input[type=number]{{width:100%;padding:10px;border:1px solid #ddd;border-radius:10px}}
.hero{{background:linear-gradient(160deg, rgba(75,0,130,.96), rgba(75,0,130,.85));color:#fff}}
.hero .inner{{max-width:1000px;margin:0 auto;padding:42px 14px}}
.footer{{text-align:center;color:#fff;margin-top:24px;padding:14px;background:var(--purple)}}
.note{{background:#fff7d1;border:1px dashed #e5c100;padding:8px 12px;border-radius:10px}}
blockquote.q{{border-right:4px solid var(--gold);padding:8px 12px;background:#fff;border-radius:10px}}
.table{{width:100%;border-collapse:collapse}} .table th,.table td{{padding:8px;border-bottom:1px solid #eee;text-align:center}}
</style>
"""

def shell(content_html: str, title: str):
    tpl = """
    <!doctype html><html lang="ar" dir="rtl"><head>
      <title>{{title}}</title>""" + BASE_HEAD + """
    </head><body>
      <header class="topbar">
        <img src='""" + LOGO_URL + """' alt="logo"><b>""" + BRAND_NAME + """</b>
        <div class="toplinks">
          <a href="/">الرئيسية</a><a href="/case">دراسة الحالة</a><a href="/dsm">DSM</a>
          <a href="/cbt">CBT</a><a href="/addiction">إدمان</a><a href="/contact">تواصل</a>
        </div>
      </header>

      <div class="layout">
        <aside class="sidebar">
          <a class="navlink primary" href="/case">📝 ابدأ دراسة الحالة</a>
          <a class="navlink" href="/dsm">📘 مرجع DSM شامل</a>
          <a class="navlink" href="/cbt">🧠 تمارين CBT فعّالة</a>
          <a class="navlink" href="/addiction">🚭 برنامج علاج الإدمان</a>
          <div class="grid-sm" style="margin-top:10px">
            <a class="btn tg" href='""" + TELEGRAM_URL + """' target="_blank">تيليجرام</a>
            <a class="btn whatsapp" href='""" + wa_link("مرحبًا، تواصل من خلال عربي سايكو.") + """' target="_blank">واتساب</a>
          </div>
          <div style="margin-top:14px">
            <a class="btn gold" style="width:100%;margin-bottom:8px" href='""" + BOOKINGS["psy"] + """' target="_blank">احجز جلسة مع الأخصائي النفسي</a>
            <a class="btn alt"  style="width:100%;margin-bottom:8px" href='""" + BOOKINGS["doc"] + """' target="_blank">احجز مع الطبيب النفسي</a>
            <a class="btn"       style="width:100%"                  href='""" + BOOKINGS["soc"] + """' target="_blank">احجز مع الأخصائي الاجتماعي</a>
          </div>
          <hr style="margin:16px 0;border:none;border-top:1px solid #eee">
          <blockquote class="q">
            أنت أثمن من ألمك. خطوة اليوم — ولو صغيرة — تغيّر اتجاه الطريق كله.
          </blockquote>
        </aside>
        <main class="card">{{ content|safe }}</main>
      </div>

      <footer class="footer"><small>© """ + BRAND_NAME + """ — 👥 عدد الزوار: {{visitors}}</small></footer>
    </body></html>"""
    token = inc_visitors()
    html = render_template_string(tpl, title=title, content=content_html, visitors=total_visitors())
    resp = make_response(html)
    if token: resp.set_cookie("VSTR", token, max_age=60*60*24*365, samesite="Lax")
    return resp

# ===== الرئيسية بعبارات داعمة =====
@app.get("/")
def home():
    hero = """
    <section class="hero"><div class="inner">
      <h2>علاج نفسي افتراضي — بخطوات عملية تحترم تجربتك</h2>
      <p>ابدأ بدراسة الحالة الموسّعة، ثم استعرض الترشيحات، وطبّق تمارين CBT، واحجز جلستك عند الحاجة.</p>
      <div class="grid-sm">
        <a class="btn gold" href="/case">ابدأ الآن</a>
        <a class="btn alt" href="/dsm">استعرض DSM</a>
        <a class="btn tg" href='""" + TELEGRAM_URL + """' target="_blank">تيليجرام</a>
        <a class="btn whatsapp" href='""" + wa_link("مرحبًا، أحتاج مساعدة عبر عربي سايكو.") + """' target="_blank">واتساب</a>
      </div>
    </div></section>
    """
    return shell(hero, f"{BRAND_NAME} — الرئيسية")

# ===== صفحات DSM/CBT/إدمان (من الملفات الخارجية) =====
@app.get("/dsm")
def dsm_page():
    try:
        DSM = importlib.import_module("DSM")
        html = DSM.main() if hasattr(DSM, "main") else "<p>DSM غير متاح.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل DSM: {e}</p>"
    return shell(html, "DSM — مرجع")

@app.get("/cbt")
def cbt_page():
    try:
        CBT = importlib.import_module("CBT")
        html = CBT.main() if hasattr(CBT, "main") else "<p>CBT غير متاح.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل CBT: {e}</p>"
    return shell(html, "CBT — خطط علاجية")

@app.get("/addiction")
def addiction_page():
    try:
        ADD = importlib.import_module("Addiction")
        html = ADD.main() if hasattr(ADD, "main") else "<p>صفحة الإدمان غير متاحة.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل الإدمان: {e}</p>"
    return shell(html, "برنامج علاج الإدمان")

# ===== دراسة الحالة (نموذج موسّع جدًا) =====
FORM_HTML = """
<h1>📝 دراسة الحالة</h1>
<p class="note">نقدّر مشاعرك وتجربتك. اكتب ما يناسبك واختر ما ينطبق عليك.</p>

<form id="caseForm" method="post" action="/case">
  <h3>المزاج والاكتئاب</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="low_mood"> مزاج منخفض معظم اليوم</label>
    <label class="chk"><input type="checkbox" name="anhedonia"> فقدان الاهتمام/المتعة</label>
    <label class="chk"><input type="checkbox" name="guilt"> شعور بالذنب/قيمة ذاتية منخفضة</label>
    <label class="chk"><input type="checkbox" name="sleep_issue"> اضطراب نوم</label>
    <label class="chk"><input type="checkbox" name="appetite_change"> تغيّر شهية/وزن</label>
    <label class="chk"><input type="checkbox" name="fatigue"> إرهاق/خمول</label>
    <label class="chk"><input type="checkbox" name="slow_psychomotor"> بطء/تهدّج نفسي حركي</label>
    <label class="chk"><input type="checkbox" name="concentration"> ضعف تركيز</label>
    <label class="chk"><input type="checkbox" name="suicidal"> أفكار إيذاء/انتحار</label>
  </div>

  <h3>القلق والرهاب/الهلع/الوسواس/الصدمة</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="worry"> قلق مفرط مستمر</label>
    <label class="chk"><input type="checkbox" name="tension"> توتر جسدي/شدّ عضلي</label>
    <label class="chk"><input type="checkbox" name="restlessness"> تململ/على أعصابي</label>
    <label class="chk"><input type="checkbox" name="panic_attacks"> نوبات هلع مفاجئة</label>
    <label class="chk"><input type="checkbox" name="panic_avoidance"> تجنّب خوفًا من النوبات</label>
    <label class="chk"><input type="checkbox" name="social_avoid"> تجنّب اجتماعي</label>
    <label class="chk"><input type="checkbox" name="fear_judgment"> خوف من تقييم الآخرين</label>
    <label class="chk"><input type="checkbox" name="obsessions"> أفكار ملحّة مزعجة</label>
    <label class="chk"><input type="checkbox" name="compulsions"> أفعال قهرية لتخفيف القلق</label>
    <label class="chk"><input type="checkbox" name="trauma_event"> حدث/تعرض صادمي</label>
    <label class="chk"><input type="checkbox" name="flashbacks"> فلاشباك/استرجاع</label>
    <label class="chk"><input type="checkbox" name="nightmares"> كوابيس مرتبطة بالحدث</label>
    <label class="chk"><input type="checkbox" name="hypervigilance"> يقظة مفرطة</label>
    <label class="chk"><input type="checkbox" name="trauma_avoid"> تجنّب مذكّرات الحدث</label>
  </div>

  <h3>ثنائي القطب/الذهان</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="elevated_mood"> مزاج مرتفع/مبالغ</label>
    <label class="chk"><input type="checkbox" name="grandiosity"> شعور بالعظمة</label>
    <label class="chk"><input type="checkbox" name="decreased_sleep_need"> قلة الحاجة للنوم</label>
    <label class="chk"><input type="checkbox" name="pressured_speech"> كلام متسارع</label>
    <label class="chk"><input type="checkbox" name="impulsivity"> اندفاع/مخاطر</label>
    <label class="chk"><input type="checkbox" name="hallucinations"> هلوسات</label>
    <label class="chk"><input type="checkbox" name="delusions"> أوهام ثابتة</label>
    <label class="chk"><input type="checkbox" name="disorganized_speech"> اضطراب كلام/تفكير</label>
    <label class="chk"><input type="checkbox" name="functional_decline"> تدهور وظيفي/دراسي/اجتماعي</label>
  </div>

  <h3>الانتباه والعصبية النمائية</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="inattention"> عدم انتباه/نسيان</label>
    <label class="chk"><input type="checkbox" name="hyperactivity"> فرط حركة/تململ</label>
    <label class="chk"><input type="checkbox" name="impulsivity"> اندفاعية</label>
    <label class="chk"><input type="checkbox" name="since_childhood"> الأعراض منذ الطفولة</label>
    <label class="chk"><input type="checkbox" name="functional_impair"> تأثير وظيفي واضح</label>
    <label class="chk"><input type="checkbox" name="autism_social"> صعوبات تواصل اجتماعي</label>
    <label class="chk"><input type="checkbox" name="autism_rigid"> اهتمام/سلوك نمطي أو جامد</label>
  </div>

  <h3>الأكل والنوم/الجسد</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="restriction"> تقييد الأكل/خوف من الوزن</label>
    <label class="chk"><input type="checkbox" name="underweight"> نقص وزن ملحوظ</label>
    <label class="chk"><input type="checkbox" name="body_image_distort"> تشوّه صورة الجسد</label>
    <label class="chk"><input type="checkbox" name="binges"> نوبات أكل كبيرة</label>
    <label class="chk"><input type="checkbox" name="compensatory"> تعويض (تقيؤ/مليّن/صيام)</label>
    <label class="chk"><input type="checkbox" name="insomnia"> أرق مستمر</label>
    <label class="chk"><input type="checkbox" name="somatic_pain"> آلام جسدية متكررة دون سبب واضح</label>
  </div>

  <h3>التعاطي</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="craving"> اشتهاء شديد</label>
    <label class="chk"><input type="checkbox" name="tolerance"> تحمّل/زيادة الجرعة</label>
    <label class="chk"><input type="checkbox" name="withdrawal"> أعراض انسحاب</label>
    <label class="chk"><input type="checkbox" name="use_despite_harm"> استخدام رغم الضرر</label>
  </div>

  <h3>تقدير الشدة (0–10)</h3>
  <div class="grid-sm"><label>الشدّة العامة:
    <input type="number" name="distress" min="0" max="10" value="5"></label>
  </div>

  <div class="grid-sm" style="margin-top:10px">
    <button class="btn" type="submit">اعرض الترشيح</button>
    <button class="btn alt" type="button" onclick="window.print()">طباعة</button>
  </div>
</form>
"""

RESULT_HTML = """
<h1>📌 ترشيحات أولية</h1>
<ul style="line-height:1.9">{items}</ul>

<h3>🎯 اقتراحات علاج نفسي افتراضي (CBT)</h3>
<ul style="line-height:1.9">{cbt}</ul>

<div class="grid-sm" style="margin:10px 0">
  <a class="btn gold" href="{book_psy}" target="_blank">احجز جلسة مع الأخصائي النفسي</a>
  <a class="btn alt"  href="{book_doc}" target="_blank">احجز مع الطبيب النفسي</a>
  <a class="btn"      href="{book_soc}" target="_blank">احجز مع الأخصائي الاجتماعي</a>
  <a class="btn tg"   href="{tg}" target="_blank">تيليجرام</a>
  <a class="btn whatsapp" href="{wa}" target="_blank">واتساب</a>
</div>

<blockquote class="q">نراك، ونحترم قصتك. كل خطوة وعي هي رعاية لنفسك، وأنت تستحق ذلك.</blockquote>
"""

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell(FORM_HTML, "دراسة الحالة")

    data = {k:v for k,v in request.form.items()}
    # التشخيص (من DSM.py)
    try:
        DSM = importlib.import_module("DSM")
        picks = DSM.diagnose(data) if hasattr(DSM,"diagnose") else [("تعذر الترشيح","DSM.diagnose غير متوفر",0.0)]
    except Exception as e:
        picks = [("خطأ", str(e), 0.0)]

    items = "".join([f"<li><b>{n}</b> — {w} <small>(Score: {s:.0f})</small></li>" for n,w,s in picks])

    # توصيات CBT ذكية مبسطة حسب الأعراض المختارة
    def f(k): return data.get(k) in ("on","true","True","1")
    tips = []
    if f("worry") or f("panic_attacks") or f("social_avoid"):
        tips.append("قلق/هلع: قياس اليوم (0–10)، تحدّي الأفكار، تعرّض تدريجي + تنفّس 4-4-6، ومنع الأمان الزائف.")
    if f("low_mood") or f("anhedonia"):
        tips.append("اكتئاب: تنشيط سلوكي — 3 أنشطة يوميًا (ممتع/مفيد/قريب من القيم) + مراجعة الأفكار اليائسة.")
    if f("obsessions") or f("compulsions"):
        tips.append("OCD: ERP تدريجي (قائمة 10 محفزات) مع <b>منع الاستجابة</b> ووقت قلق محدّد.")
    if f("trauma_event") and (f("flashbacks") or f("nightmares")):
        tips.append("PTSD: تأريض 5-4-3-2-1، تنظيم نوم وأكل، تعرّض تدريجي للذكريات بأمان وكتابة سرد.")
    if f("inattention") or f("hyperactivity"):
        tips.append("ADHD: بومودورو 25–5، ثلاث أولويات لليوم، مؤقّت مرئي وبيئة قليلة المشتتات.")
    if f("restriction") or f("binges"):
        tips.append("اضطرابات الأكل: جدول وجبات ثابت 3+2، منع التعويض، وتمارين صورة الجسد أمام المرآة تدريجيًا.")
    if f("craving") or f("use_despite_harm") or f("withdrawal"):
        tips.append("تعاطي: خطة إشارات إنذار + بدائل فورية + تواصل داعم؛ ويمكن مراجعة صفحة الإدمان.")

    if not tips:
        tips.append("ابدأ بدفتر يومي: موقف → فكرة → شعور → سلوك؛ وجرّب أنشطة قصيرة ممتعة لرفع الطاقة.")

    cbt_html = "".join([f"<li>{t}</li>" for t in tips])

    html = RESULT_HTML.format(
        items=items, cbt=cbt_html,
        book_psy=BOOKINGS["psy"], book_doc=BOOKINGS["doc"], book_soc=BOOKINGS["soc"],
        tg=TELEGRAM_URL, wa=wa_link("مرحبًا، أحتاج حجز/استفسار عبر عربي سايكو.")
    )
    return shell(html, "نتيجة الترشيح")

# ===== تواصل =====
@app.get("/contact")
def contact():
    html = f"""
    <h1>📞 تواصل معنا</h1>
    <div class="grid-sm">
      <a class="btn gold" href="{BOOKINGS['psy']}" target="_blank">احجز مع الأخصائي النفسي</a>
      <a class="btn alt"  href="{BOOKINGS['doc']}" target="_blank">احجز مع الطبيب النفسي</a>
      <a class="btn"      href="{BOOKINGS['soc']}" target="_blank">احجز مع الأخصائي الاجتماعي</a>
      <a class="btn tg"  href="{TELEGRAM_URL}" target="_blank">تيليجرام</a>
      <a class="btn whatsapp" href="{wa_link('تواصل عبر عربي سايكو')}" target="_blank">واتساب</a>
    </div>
    <p style="margin-top:12px" class="note">نثق بقدرتك على التحسّن. سنسير معك خطوة بخطوة.</p>
    """
    return shell(html, "التواصل")

# ===== إحصاءات الزوّار =====
@app.get("/stats")
def stats():
    if request.args.get("key","") != STATS_KEY: abort(401)
    rows = "".join([f"<tr><td>{d}</td><td>{n}</td></tr>" for d,n in last30()])
    html = f"""
    <h1>📈 الزوّار</h1>
    <p>الإجمالي: <b>{total_visitors()}</b></p>
    <table class="table"><thead><tr><th>اليوم</th><th>زيارات</th></tr></thead><tbody>{rows}</tbody></table>
    """
    return shell(html, "إحصاءات")

@app.errorhandler(401)
def unauth(_): return shell("<h3>غير مصرّح</h3>", "401"), 401

@app.get("/health")
def health(): return {"status":"ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
