# app.py — عربي سايكو: قائمة جانبية + علاج نفسي افتراضي + دراسة حالة + DSM/CBT/إدمان + تواصل
import os, importlib, sqlite3, secrets
from pathlib import Path
from datetime import date, timedelta
from flask import Flask, render_template_string, request, make_response, abort

app = Flask(__name__)

# إعدادات
BRAND_NAME   = os.environ.get("BRAND_NAME", "عربي سايكو")
WHATS_NUM    = os.environ.get("WHATS_NUM", "966530565696")  # 0530565696 -> 966530565696
WHATSAPP_URL = os.environ.get("WHATSAPP_URL", f"https://wa.me/{WHATS_NUM}?text=%D8%A3%D8%B1%D9%8A%D8%AF%20%D8%A7%D9%84%D8%AA%D9%88%D8%A7%D8%B5%D9%84%20%D9%85%D8%B9%20%D8%B9%D8%B1%D8%A8%D9%8A%20%D8%B3%D8%A7%D9%8A%D9%83%D9%88")
TELEGRAM_URL = os.environ.get("TELEGRAM_URL", "https://t.me/ArabiPsychoBot")
LOGO_URL     = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
STATS_KEY    = os.environ.get("STATS_KEY", "arabipsycho")

# عدّاد الزوّار (SQLite)
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
    return secrets.token_hex(16)
def total_visitors():
    c=_db(); n=c.execute("SELECT total FROM counters WHERE id=1").fetchone()[0]; c.close(); return n
def last30():
    c=_db()
    days=[(date.today()-timedelta(days=i)).isoformat() for i in range(29,-1,-1)]
    got=dict(c.execute("SELECT day,total FROM daily WHERE day IN ({})".format(",".join("?"*len(days))), tuple(days)).fetchall() or [])
    c.close()
    return [(d, got.get(d,0)) for d in days]

# CSS/رأس
BASE_HEAD = f"""
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="icon" href="{LOGO_URL}">
<style>
:root{{ --purple:#4B0082; --gold:#FFD700; --bg:#faf7e6 }}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif}}
.topbar{{position:sticky;top:0;background:var(--purple);color:#fff;padding:10px 14px;display:flex;gap:10px;align-items:center}}
.topbar img{{width:42px;height:42px;border-radius:50%}}
.toplinks a{{color:#fff;margin:0 6px;font-weight:700;text-decoration:none}}
.layout{{max-width:1250px;margin:20px auto;display:grid;gap:18px;grid-template-columns:280px 1fr;padding:0 12px}}
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
          <a class="navlink primary" href="/case">📝 دراسة الحالة</a>
          <a class="navlink" href="/dsm">📘 مرجع DSM شامل</a>
          <a class="navlink" href="/cbt">🧠 خطط CBT</a>
          <a class="navlink" href="/addiction">🚭 برنامج الإدمان</a>
          <div class="grid-sm" style="margin-top:10px">
            <a class="btn tg" href='""" + TELEGRAM_URL + """' target="_blank">تيليجرام</a>
            <a class="btn whatsapp" href='""" + WHATSAPP_URL + """' target="_blank">واتساب</a>
          </div>
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

# الرئيسية
@app.get("/")
def home():
    hero = """
    <section class="hero"><div class="inner">
      <h2>علاج نفسي افتراضي — بخطوات واضحة وواجهة أنيقة</h2>
      <p>ابدأ بدراسة الحالة، ثم استعرض ترشيحات DSM، وطبّق أدوات CBT وخطة دعم الإدمان متى احتجت.</p>
      <div class="grid-sm"><a class="btn gold" href="/case">ابدأ الآن</a><a class="btn alt" href="/dsm">استعرض DSM</a></div>
    </div></section>
    """
    return shell(hero, f"{BRAND_NAME} — الرئيسية")

# DSM/CBT/إدمان
@app.get("/dsm")
def dsm_page():
    try:
        DSM = importlib.import_module("DSM"); html = DSM.main() if hasattr(DSM,"main") else "<p>DSM غير متاح.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل DSM: {e}</p>"
    return shell(html, "DSM — مرجع")

@app.get("/cbt")
def cbt_page():
    try:
        CBT = importlib.import_module("CBT"); html = CBT.main() if hasattr(CBT,"main") else "<p>CBT غير متاح.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل CBT: {e}</p>"
    return shell(html, "CBT — خطط علاجية")

@app.get("/addiction")
def addiction_page():
    try:
        ADD = importlib.import_module("Addiction"); html = ADD.main() if hasattr(ADD,"main") else "<p>صفحة الإدمان غير متاحة.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل الإدمان: {e}</p>"
    return shell(html, "برنامج علاج الإدمان")

# دراسة الحالة (نموذج موسع)
FORM_HTML = """
<h1>📝 دراسة الحالة</h1>
<p class="note">دون ما تشعر به بهدوء… وسنرتّب الصورة بشكل أوضح.</p>

<form id="caseForm" method="post" action="/case">
  <h3>المزاج والاكتئاب</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="low_mood"> مزاج منخفض</label>
    <label class="chk"><input type="checkbox" name="anhedonia"> فقدان المتعة</label>
    <label class="chk"><input type="checkbox" name="guilt"> شعور بالذنب/قيمة ذاتية منخفضة</label>
    <label class="chk"><input type="checkbox" name="sleep_issue"> صعوبات نوم</label>
    <label class="chk"><input type="checkbox" name="appetite_change"> تغيّر شهية/وزن</label>
    <label class="chk"><input type="checkbox" name="fatigue"> إرهاق/خمول</label>
    <label class="chk"><input type="checkbox" name="slow_psychomotor"> بطء/تهدّج نفسي حركي</label>
    <label class="chk"><input type="checkbox" name="concentration"> ضعف تركيز</label>
    <label class="chk"><input type="checkbox" name="suicidal"> أفكار انتحارية</label>
  </div>

  <h3>القلق والرهاب/الهلع/الوسواس/الصدمة</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="worry"> قلق مفرط مستمر (أغلب الأيام 6 أشهر+)</label>
    <label class="chk"><input type="checkbox" name="tension"> توتر جسدي/توتر عضلي</label>
    <label class="chk"><input type="checkbox" name="restlessness"> تململ/على أعصابي</label>
    <label class="chk"><input type="checkbox" name="panic_attacks"> نوبات هلع مفاجئة</label>
    <label class="chk"><input type="checkbox" name="panic_avoidance"> تجنّب أماكن خوفًا من النوبات</label>
    <label class="chk"><input type="checkbox" name="social_avoid"> تجنّب اجتماعي/خوف تقييم</label>
    <label class="chk"><input type="checkbox" name="obsessions"> أفكار ملحّة مزعجة</label>
    <label class="chk"><input type="checkbox" name="compulsions"> أفعال قهرية لتخفيف التوتر</label>
    <label class="chk"><input type="checkbox" name="trauma_event"> حدث/تعرض صادمي</label>
    <label class="chk"><input type="checkbox" name="flashbacks"> فلاشباك/استرجاع</label>
    <label class="chk"><input type="checkbox" name="nightmares"> كوابيس مرتبطة بالحدث</label>
    <label class="chk"><input type="checkbox" name="hypervigilance"> يقظة مفرطة/حساسية مفرطة</label>
    <label class="chk"><input type="checkbox" name="trauma_avoid"> تجنّب مذكّرات الحدث</label>
  </div>

  <h3>ثنائي القطب/الذهان</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="elevated_mood"> مزاج مرتفع/مبالغ</label>
    <label class="chk"><input type="checkbox" name="grandiosity"> شعور بالعظمة</label>
    <label class="chk"><input type="checkbox" name="decreased_sleep_need"> قلة الحاجة للنوم</label>
    <label class="chk"><input type="checkbox" name="pressured_speech"> كلام متسارع</label>
    <label class="chk"><input type="checkbox" name="impulsivity"> اندفاع/مخاطر (صرف/سفر/جنس)</label>
    <label class="chk"><input type="checkbox" name="hallucinations"> هلوسات</label>
    <label class="chk"><input type="checkbox" name="delusions"> أوهام ثابتة</label>
    <label class="chk"><input type="checkbox" name="disorganized_speech"> اضطراب كلام/تفكير</label>
    <label class="chk"><input type="checkbox" name="functional_decline"> تدهور وظيفي/اجتماعي</label>
  </div>

  <h3>انتباه/أكل/تعاطي</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="inattention"> عدم انتباه/نسيان</label>
    <label class="chk"><input type="checkbox" name="hyperactivity"> فرط حركة/تململ</label>
    <label class="chk"><input type="checkbox" name="since_childhood"> منذ الطفولة</label>
    <label class="chk"><input type="checkbox" name="functional_impair"> تأثير وظيفي واضح</label>

    <label class="chk"><input type="checkbox" name="restriction"> تقييد الأكل/خوف سمنة</label>
    <label class="chk"><input type="checkbox" name="underweight"> نقص وزن ملحوظ</label>
    <label class="chk"><input type="checkbox" name="body_image_distort"> تشوّه صورة الجسد</label>
    <label class="chk"><input type="checkbox" name="binges"> نوبات أكل كبيرة</label>
    <label class="chk"><input type="checkbox" name="compensatory"> تقيّؤ/مُليّن/صيام تعويضي</label>

    <label class="chk"><input type="checkbox" name="craving"> اشتهاء شديد للمواد</label>
    <label class="chk"><input type="checkbox" name="tolerance"> تحمّل/زيادة الجرعة</label>
    <label class="chk"><input type="checkbox" name="withdrawal"> أعراض انسحاب</label>
    <label class="chk"><input type="checkbox" name="use_despite_harm"> استخدام رغم الأذى</label>
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
<div class="grid-sm"><button onclick="window.print()" class="btn">طباعة</button></div>
"""

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell(FORM_HTML, "دراسة الحالة")
    data = {k:v for k,v in request.form.items()}
    try:
        DSM = importlib.import_module("DSM")
        picks = DSM.diagnose(data) if hasattr(DSM,"diagnose") else [("تعذر الترشيح","DSM.diagnose غير متوفر",0.0)]
    except Exception as e:
        picks = [("خطأ", str(e), 0.0)]
    items = "".join([f"<li><b>{n}</b> — {w} <small>(Score: {s:.0f})</small></li>" for n,w,s in picks])
    return shell(RESULT_HTML.format(items=items), "نتيجة الترشيح")

# تواصل + إحصاءات بسيطة
@app.get("/contact")
def contact():
    html = f"""
    <h1>📞 تواصل معنا</h1>
    <div class="grid-sm">
      <a class="btn tg" href="{TELEGRAM_URL}" target="_blank">تيليجرام</a>
      <a class="btn whatsapp" href="{WHATSAPP_URL}" target="_blank">واتساب</a>
    </div>
    """
    return shell(html, "التواصل")

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
