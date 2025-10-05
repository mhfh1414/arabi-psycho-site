# app.py — عربي سايكو (نسخة خدمية): الرئيسية + دراسة الحالة + DSM + CBT + إدمان + حجز + تواصل
import os, importlib, sqlite3
from pathlib import Path
from datetime import date, timedelta
from flask import Flask, render_template_string, request, make_response

app = Flask(__name__)

# إعدادات عامة
BRAND_NAME = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO_URL   = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
WHATS_NUM  = os.environ.get("WHATS_NUM", "966530565696")
TELEGRAM_URL = os.environ.get("TELEGRAM_URL", "https://t.me/ArabiPsychoBot")

def walink(msg):
    from urllib.parse import quote
    return f"https://wa.me/{WHATS_NUM}?text={quote(msg)}"

BOOK_PSY = walink("مرحبًا، أرغب بحجز جلسة مع الأخصائي النفسي عبر عربي سايكو.")
BOOK_DOC = walink("مرحبًا، أرغب بحجز جلسة مع الطبيب النفسي عبر عربي سايكو.")
BOOK_SOC = walink("مرحبًا، أرغب بحجز جلسة مع الأخصائي الاجتماعي عبر عربي سايكو.")

# عدّاد بسيط
DB = Path("visitors.db")
def _db():
    c = sqlite3.connect(DB)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("CREATE TABLE IF NOT EXISTS counters(id INTEGER PRIMARY KEY CHECK(id=1), total INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS daily(day TEXT PRIMARY KEY,total INTEGER)")
    if not c.execute("SELECT 1 FROM counters WHERE id=1").fetchone():
        c.execute("INSERT INTO counters(id,total) VALUES(1,0)")
        c.commit()
    return c
def inc():
    if request.cookies.get("VSTR"): return None
    c=_db(); c.execute("UPDATE counters SET total=total+1 WHERE id=1")
    d=date.today().isoformat()
    if c.execute("SELECT 1 FROM daily WHERE day=?",(d,)).fetchone():
        c.execute("UPDATE daily SET total=total+1 WHERE day=?",(d,))
    else:
        c.execute("INSERT INTO daily(day,total) VALUES(?,1)",(d,))
    c.commit(); c.close()
    import secrets; return secrets.token_hex(12)
def total():
    c=_db(); n=c.execute("SELECT total FROM counters WHERE id=1").fetchone()[0]; c.close(); return n

BASE = f"""
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<link rel="icon" href="{LOGO_URL}">
<style>
:root{{--p:#4B0082;--g:#FFD700;--bg:#faf7e6}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif}}
.top{{position:sticky;top:0;background:var(--p);color:#fff;display:flex;align-items:center;gap:10px;padding:10px 14px}}
.top img{{width:42px;height:42px;border-radius:50%}}
.top a{{color:#fff;text-decoration:none;margin:0 6px;font-weight:700}}
.layout{{max-width:1200px;margin:18px auto;padding:0 12px;display:grid;gap:16px;grid-template-columns:290px 1fr}}
.side,.card{{background:#fff;border:1px solid #eee;border-radius:16px;box-shadow:0 10px 24px rgba(0,0,0,.06)}}
.side{{padding:16px}}.card{{padding:20px}}
.navlink{{display:block;padding:10px;border-radius:12px;border:1px solid #eee;margin-bottom:8px;color:#222;text-decoration:none}}
.navlink:hover{{background:#fafafa}}.navlink.primary{{background:var(--p);color:#fff;border-color:var(--p)}}
.btn{{display:inline-block;padding:10px 14px;border-radius:12px;text-decoration:none;font-weight:700;background:var(--p);color:#fff;text-align:center}}
.btn.alt{{background:#5b22a6}}.btn.gold{{background:var(--g);color:#4B0082}}
.btn.wa{{background:#25D366}}.btn.tg{{background:#229ED9}}
.grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}}
.grid-sm{{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(170px,1fr))}}
label.chk{{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:10px}}
input[type=number]{{width:100%;padding:10px;border:1px solid #ddd;border-radius:10px}}
.hero{{background:linear-gradient(160deg,rgba(75,0,130,.96),rgba(75,0,130,.86));color:#fff}}
.hero .in{{max-width:1100px;margin:0 auto;padding:40px 14px}}
.service{{border:1px dashed #eee;padding:12px;border-radius:12px}}
.footer{{text-align:center;color:#fff;background:var(--p);padding:12px;margin-top:24px}}
</style>
"""

def shell(content, title):
    tpl = """
    <!doctype html><html lang="ar" dir="rtl"><head><title>{{t}}</title>""" + BASE + """
    </head><body>
      <header class="top">
        <img src='""" + LOGO_URL + """' alt="logo"><b>""" + BRAND_NAME + """</b>
        <div style="margin-right:auto">
          <a href="/">الرئيسية</a><a href="/case">دراسة الحالة</a><a href="/dsm">DSM</a>
          <a href="/cbt">CBT</a><a href="/addiction">إدمان</a><a href="/contact">تواصل</a>
        </div>
      </header>

      <div class="layout">
        <aside class="side">
          <a class="navlink primary" href="/case">📝 ابدأ دراسة الحالة</a>
          <a class="navlink" href="/cbt">🧠 تمارين CBT وخطط</a>
          <a class="navlink" href="/addiction">🚭 برنامج الإدمان</a>
          <div class="grid-sm" style="margin-top:8px">
            <a class="btn tg" href='""" + TELEGRAM_URL + """' target="_blank">تيليجرام</a>
            <a class="btn wa" href='""" + walink("تواصل من خلال عربي سايكو.") + """' target="_blank">واتساب</a>
          </div>
          <hr style="margin:12px 0;border:none;border-top:1px solid #eee">
          <a class="btn gold" style="width:100%;margin-bottom:8px" href='""" + BOOK_PSY + """' target="_blank">احجز مع الأخصائي النفسي</a>
          <a class="btn alt"  style="width:100%;margin-bottom:8px" href='""" + BOOK_DOC + """' target="_blank">احجز مع الطبيب النفسي</a>
          <a class="btn"     style="width:100%"                    href='""" + BOOK_SOC + """' target="_blank">احجز مع الأخصائي الاجتماعي</a>
        </aside>
        <main class="card">{{c|safe}}</main>
      </div>

      <footer class="footer"><small>© """ + BRAND_NAME + """ — الزوار: {{v}}</small></footer>
    </body></html>"""
    tok = inc()
    html = render_template_string(tpl, t=title, c=content, v=total())
    resp = make_response(html)
    if tok: resp.set_cookie("VSTR", tok, max_age=60*60*24*365, samesite="Lax")
    return resp

# الرئيسية مع “خدمات”
@app.get("/")
def home():
    content = f"""
    <section class="hero"><div class="in">
      <h2>علاج نفسي افتراضي — خدمات تساعدك خطوة بخطوة</h2>
      <p>ابدأ بتعبئة دراسة الحالة ثم اطّلع على الترشيحات وتمارين CBT وخطة الإدمان، واحجز جلستك بسهولة.</p>
      <div class="grid">
        <div class="service"><h3>📝 دراسة الحالة</h3><p>نموذج موسّع يجمع الأعراض والعوامل ليساعدك على فهم الصورة.</p><a class="btn gold" href="/case">ابدأ الآن</a></div>
        <div class="service"><h3>🧠 CBT فعّال</h3><p>تمارين جاهزة: تحدّي الأفكار، تنشيط سلوكي، تعرّض تدريجي، بومودورو، والمزيد.</p><a class="btn" href="/cbt">افتح التمارين</a></div>
        <div class="service"><h3>🚭 علاج الإدمان</h3><p>مراحل واضحة: إزالة السُمّية، التأهيل، منع الانتكاسة + خطة شخصية قابلة للحفظ.</p><a class="btn alt" href="/addiction">ابدأ البرنامج</a></div>
        <div class="service"><h3>📞 احجز جلسة</h3><p>اختر النوع المناسب: أخصائي نفسي، طبيب نفسي، أخصائي اجتماعي.</p>
          <div class="grid-sm">
            <a class="btn gold" href="{BOOK_PSY}" target="_blank">أخصائي نفسي</a>
            <a class="btn alt"  href="{BOOK_DOC}" target="_blank">طبيب نفسي</a>
            <a class="btn"     href="{BOOK_SOC}" target="_blank">أخصائي اجتماعي</a>
          </div>
        </div>
      </div>
    </div></section>
    """
    return shell(content, "الرئيسية — عربي سايكو")

# DSM (يقرأ من DSM.py)
@app.get("/dsm")
def dsm():
    try:
        DSM = importlib.import_module("DSM")
        html = DSM.main() if hasattr(DSM,"main") else "<p>DSM غير متاح.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل DSM: {e}</p>"
    return shell(html, "DSM — مرجع")

# CBT (يقرأ من CBT.py)
@app.get("/cbt")
def cbt():
    try:
        CBT = importlib.import_module("CBT")
        html = CBT.main() if hasattr(CBT,"main") else "<p>CBT غير متاح.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل CBT: {e}</p>"
    return shell(html, "CBT — خطط وتمارين")

# الإدمان (من Addiction.py)
@app.get("/addiction")
def addiction():
    try:
        ADD = importlib.import_module("Addiction")
        html = ADD.main() if hasattr(ADD,"main") else "<p>صفحة الإدمان غير متاحة.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل الإدمان: {e}</p>"
    return shell(html, "برنامج علاج الإدمان")

# دراسة الحالة (النموذج كما في نسختك الموسعة – تركته كما هو لديك حتى لا يطول)
FORM = """
<h1>دراسة الحالة</h1>
<p>اختر ما ينطبق عليك. يمكنك الطباعة أو مشاركة النتائج مع المختص.</p>
<style>.grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}label.chk{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:10px}.btn{margin-top:10px}</style>
<form method="post">
  <h3>المزاج والاكتئاب</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="low_mood"> مزاج منخفض</label>
    <label class="chk"><input type="checkbox" name="anhedonia"> فقدان المتعة</label>
    <label class="chk"><input type="checkbox" name="sleep_issue"> اضطراب نوم</label>
    <label class="chk"><input type="checkbox" name="appetite_change"> تغيّر شهية</label>
    <label class="chk"><input type="checkbox" name="fatigue"> إرهاق</label>
    <label class="chk"><input type="checkbox" name="guilt"> شعور بالذنب/قيمة منخفضة</label>
    <label class="chk"><input type="checkbox" name="concentration"> ضعف تركيز</label>
  </div>

  <h3>القلق/الهلع/الوسواس/الصدمة</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="worry"> قلق مستمر</label>
    <label class="chk"><input type="checkbox" name="panic_attacks"> نوبات هلع</label>
    <label class="chk"><input type="checkbox" name="social_avoid"> تجنّب اجتماعي</label>
    <label class="chk"><input type="checkbox" name="obsessions"> أفكار ملحّة</label>
    <label class="chk"><input type="checkbox" name="compulsions"> أفعال قهرية</label>
    <label class="chk"><input type="checkbox" name="trauma_event"> حدث صادمي</label>
    <label class="chk"><input type="checkbox" name="flashbacks"> فلاشباك</label>
  </div>

  <h3>ثنائي القطب/ذهان</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="elevated_mood"> مزاج مرتفع</label>
    <label class="chk"><input type="checkbox" name="grandiosity"> شعور بالعظمة</label>
    <label class="chk"><input type="checkbox" name="hallucinations"> هلوسات</label>
    <label class="chk"><input type="checkbox" name="delusions"> أوهام</label>
    <label class="chk"><input type="checkbox" name="functional_decline"> تدهور وظيفي</label>
  </div>

  <h3>انتباه/تعاطي</h3>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="inattention"> عدم انتباه</label>
    <label class="chk"><input type="checkbox" name="hyperactivity"> فرط حركة</label>
    <label class="chk"><input type="checkbox" name="craving"> اشتهاء</label>
    <label class="chk"><input type="checkbox" name="tolerance"> تحمّل</label>
    <label class="chk"><input type="checkbox" name="withdrawal"> انسحاب</label>
  </div>

  <label>الشدّة (0–10): <input type="number" name="distress" min="0" max="10" value="5"></label><br>
  <button class="btn gold" type="submit">اعرض الترشيح</button>
  <button class="btn alt" type="button" onclick="window.print()">طباعة</button>
</form>
"""

RESULT = """
<h1>نتيجة أولية</h1>
<ul>{items}</ul>
<h3>اقتراحات فورية (CBT)</h3>
<ul>{tips}</ul>
<div class="grid-sm" style="margin-top:10px">
  <a class="btn gold" href='""" + BOOK_PSY + """' target="_blank">احجز مع الأخصائي النفسي</a>
  <a class="btn alt"  href='""" + BOOK_DOC + """' target="_blank">احجز مع الطبيب النفسي</a>
  <a class="btn"     href='""" + BOOK_SOC + """' target="_blank">احجز مع الأخصائي الاجتماعي</a>
</div>
"""

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell(FORM, "دراسة الحالة")

    data = {k:v for k,v in request.form.items()}
    # ترشيح من DSM.py إن وُجد
    try:
        DSM = importlib.import_module("DSM")
        picks = DSM.diagnose(data) if hasattr(DSM,"diagnose") else [("تعذر الترشيح","DSM.diagnose غير متوفر",0.0)]
    except Exception as e:
        picks = [("خطأ", str(e), 0.0)]
    items = "".join([f"<li><b>{n}</b> — {w} <small>({s:.0f})</small></li>" for n,w,s in picks])

    # نصائح قصيرة حسب الأعراض
    f=lambda k: data.get(k)=="on"
    tips=[]
    if f("worry") or f("panic_attacks"): tips.append("تنفّس 4-4-6 + تعرّض تدريجي ومنع سلوكيات الأمان.")
    if f("low_mood") or f("anhedonia"): tips.append("تنشيط سلوكي: 3 أنشطة (ممتع/مفيد/قيمة) يوميًا.")
    if f("obsessions") or f("compulsions"): tips.append("ERP: قائمة محفزات مع منع الاستجابة + وقت قلق محدد.")
    if f("inattention") or f("hyperactivity"): tips.append("بومودورو 25/5 + ثلاث أولويات صباحية + مؤقّت مرئي.")
    if f("craving") or f("withdrawal"): tips.append("خطة إشارات الإنذار + بدائل فورية + تواصل داعم.")
    if not tips: tips.append("ابدأ بدفتر أفكار (موقف→فكرة→شعور→سلوك) ليومين وراجع ما تلاحظه.")
    tips_html="".join([f"<li>{t}</li>" for t in tips])

    return shell(RESULT.format(items=items, tips=tips_html), "نتيجة الترشيح")

@app.get("/contact")
def contact():
    content = f"""
    <h1>التواصل والحجز</h1>
    <div class="grid-sm">
      <a class="btn gold" href="{BOOK_PSY}" target="_blank">أخصائي نفسي</a>
      <a class="btn alt"  href="{BOOK_DOC}" target="_blank">طبيب نفسي</a>
      <a class="btn"     href="{BOOK_SOC}" target="_blank">أخصائي اجتماعي</a>
      <a class="btn tg"  href="{TELEGRAM_URL}" target="_blank">بوت تيليجرام</a>
      <a class="btn wa"  href="{walink('تواصل من خلال عربي سايكو.')}" target="_blank">واتساب</a>
    </div>
    """
    return shell(content, "التواصل")

@app.get("/health")
def health(): return {"ok": True, "visitors": total()}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
