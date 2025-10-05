# app.py — عربي سايكو (نسخة مُوسَّعة وجذّابة)
import os, importlib, sqlite3, secrets
from pathlib import Path
from datetime import date, timedelta
from flask import Flask, render_template_string, request, make_response, abort

app = Flask(__name__)

# ================= إعدادات عامة =================
BRAND_NAME   = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO_URL     = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
WHATS_NUM    = os.environ.get("WHATS_NUM", "966530565696")   # 0530565696 -> 966530565696
TELEGRAM_URL = os.environ.get("TELEGRAM_URL", "https://t.me/ArabiPsychoBot")
STATS_KEY    = os.environ.get("STATS_KEY", "arabipsycho")

def wa_link(msg: str) -> str:
    from urllib.parse import quote
    return f"https://wa.me/{WHATS_NUM}?text={quote(msg)}"

BOOK_PSY = wa_link("مرحبًا، أرغب بحجز جلسة مع الأخصائي النفسي عبر عربي سايكو.")
BOOK_DOC = wa_link("مرحبًا، أرغب بحجز جلسة مع الطبيب النفسي عبر عربي سايكو.")
BOOK_SOC = wa_link("مرحبًا، أرغب بحجز جلسة مع الأخصائي الاجتماعي عبر عربي سايكو.")
WA_QUICK = wa_link("تواصل من خلال عربي سايكو.")

# ================= عدّاد الزوّار (SQLite بسيط) =================
DB_PATH = Path("visitors.db")

def _db():
    c = sqlite3.connect(DB_PATH)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("CREATE TABLE IF NOT EXISTS counters(id INTEGER PRIMARY KEY CHECK(id=1), total INTEGER NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS daily(day TEXT PRIMARY KEY, total INTEGER NOT NULL)")
    if not c.execute("SELECT 1 FROM counters WHERE id=1").fetchone():
        c.execute("INSERT INTO counters(id,total) VALUES(1,0)")
        c.commit()
    return c

def _today(): return date.today().isoformat()

def inc_visitors():
    if request.cookies.get("VSTR"): return None
    c=_db(); c.execute("UPDATE counters SET total=total+1 WHERE id=1")
    d=_today()
    if c.execute("SELECT 1 FROM daily WHERE day=?",(d,)).fetchone():
        c.execute("UPDATE daily SET total=total+1 WHERE day=?",(d,))
    else:
        c.execute("INSERT INTO daily(day,total) VALUES(?,1)",(d,))
    c.commit(); c.close()
    return secrets.token_hex(16)

def total_visitors():
    c=_db(); n=c.execute("SELECT total FROM counters WHERE id=1").fetchone()[0]; c.close(); return n

def last30():
    c=_db()
    days=[(date.today()-timedelta(days=i)).isoformat() for i in range(29,-1,-1)]
    got=dict(c.execute("SELECT day,total FROM daily WHERE day IN ({})".format(",".join("?"*len(days))), tuple(days)).fetchall() or [])
    c.close(); return [(d, got.get(d,0)) for d in days]

# ================= ستايل عام =================
BASE_HEAD = f"""
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="icon" href="{LOGO_URL}">
<style>
:root{{ --p:#4B0082; --g:#FFD700; --bg:#faf7e6; --ink:#2d1b4e }}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif;color:#222}}
a{{text-decoration:none}}

.topbar{{position:sticky;top:0;z-index:20;background:var(--p);color:#fff;display:flex;gap:10px;align-items:center;padding:10px 14px;box-shadow:0 6px 20px rgba(0,0,0,.2)}}
.topbar img{{width:44px;height:44px;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
.toplinks a{{color:#fff;margin:0 6px;font-weight:700;opacity:.95}} .toplinks a:hover{{opacity:1}}

.layout{{max-width:1280px;margin:20px auto;padding:0 12px;display:grid;gap:18px;grid-template-columns:300px 1fr}}
.sidebar,.card{{background:#fff;border:1px solid #eee;border-radius:16px;box-shadow:0 10px 26px rgba(0,0,0,.07)}}
.sidebar{{padding:16px}} .card{{padding:20px}}

.navlink{{display:block;padding:10px 12px;border-radius:12px;border:1px solid #f0f0f0;margin-bottom:8px;color:#222}}
.navlink:hover{{background:#fafafa}} .navlink.primary{{background:var(--p);color:#fff;border-color:var(--p)}}

.btn{{display:inline-block;padding:10px 14px;border-radius:12px;font-weight:800;text-align:center}}
.btn.p{{background:var(--p);color:#fff}} .btn.alt{{background:#5b22a6;color:#fff}} .btn.g{{background:var(--g);color:var(--p)}}
.btn.wa{{background:#25D366;color:#fff}} .btn.tg{{background:#229ED9;color:#fff}}

.grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
.grid-sm{{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}}

label.chk{{display:block;background:#fbfbfb;border:1px solid #eee;border-radius:10px;padding:10px}}
input[type=text],input[type=number],select,textarea{{width:100%;padding:10px;border:1px solid #ddd;border-radius:10px}}
small.muted{{opacity:.85}}

.hero{{background:linear-gradient(150deg, rgba(75,0,130,.95), rgba(75,0,130,.85)), url('https://images.unsplash.com/photo-1518199266791-5375a83190b7?q=80&w=1600&auto=format') center/cover no-repeat; color:#fff}}
.hero .in{{max-width:1100px;margin:0 auto;padding:54px 14px}}
.hero h1{{margin:.2rem 0 1rem}} .hero p{{opacity:.98;line-height:1.9}}

.section-title{{margin:14px 0 8px;color:var(--p);font-weight:900}}
.note{{background:#fff7d1;border:1px dashed #e5c100;padding:8px 12px;border-radius:10px}}

.footer{{text-align:center;margin-top:24px;background:var(--p);color:#fff;padding:12px}}
blockquote.q{{border-right:4px solid var(--g);background:#fff;padding:10px 12px;border-radius:12px}}

.kpi{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:10px}}
.kpi .tile{{background:#fff;border:1px solid #eee;border-radius:12px;padding:12px;text-align:center}}
.kpi .tile b{{font-size:1.6rem;color:var(--p)}}
.divider{{height:1px;background:#eee;margin:12px 0}}
</style>
"""

def shell(content_html: str, title: str):
    tpl = """
    <!doctype html><html lang="ar" dir="rtl"><head><title>{{t}}</title>""" + BASE_HEAD + """
    </head><body>
      <header class="topbar">
        <img src='""" + LOGO_URL + """' alt="logo"><b>""" + BRAND_NAME + """</b>
        <div class="toplinks" style="margin-right:auto">
          <a href="/">الرئيسية</a><a href="/case">دراسة الحالة</a><a href="/dsm">DSM</a>
          <a href="/cbt">CBT</a><a href="/addiction">إدمان</a><a href="/contact">تواصل</a>
        </div>
      </header>

      <div class="layout">
        <aside class="sidebar">
          <div class="section-title">القائمة</div>
          <a class="navlink primary" href="/case">📝 ابدأ دراسة الحالة</a>
          <a class="navlink" href="/dsm">📘 مرجع DSM شامل</a>
          <a class="navlink" href="/cbt">🧠 تمارين CBT</a>
          <a class="navlink" href="/addiction">🚭 برنامج الإدمان</a>
          <div class="divider"></div>
          <div class="section-title">التواصل والحجز</div>
          <div class="grid-sm">
            <a class="btn tg" href='""" + TELEGRAM_URL + """' target="_blank">بوت تيليجرام</a>
            <a class="btn wa" href='""" + WA_QUICK + """' target="_blank">واتساب سريع</a>
          </div>
          <a class="btn g"  style="margin-top:10px;display:block" href='""" + BOOK_PSY + """' target="_blank">احجز مع الأخصائي النفسي</a>
          <a class="btn alt" style="margin-top:8px;display:block" href='""" + BOOK_DOC + """' target="_blank">احجز مع الطبيب النفسي</a>
          <a class="btn p"  style="margin-top:8px;display:block" href='""" + BOOK_SOC + """' target="_blank">احجز مع الأخصائي الاجتماعي</a>

          <div class="divider"></div>
          <blockquote class="q">نراك، ونحترم قصّتك. خطوة صغيرة اليوم تغيّر اتجاه الطريق كله.</blockquote>
        </aside>

        <main class="card">{{ c|safe }}</main>
      </div>

      <footer class="footer"><small>© """ + BRAND_NAME + """ — 👥 الزوار: {{v}}</small></footer>
    </body></html>"""
    token = inc_visitors()
    html  = render_template_string(tpl, t=title, c=content_html, v=total_visitors())
    resp  = make_response(html)
    if token: resp.set_cookie("VSTR", token, max_age=60*60*24*365, samesite="Lax")
    return resp

# ================= الرئيسية =================
@app.get("/")
def home():
    content = f"""
    <section class="hero"><div class="in">
      <h1>علاج نفسي افتراضي بتصميم عربي أنيق</h1>
      <p>ابدأ بدراسة حالة موسّعة، شاهد الترشيحات، طبّق تمارين CBT، واتّبع برنامجًا عمليًا لدعم التعافي.</p>
      <div class="grid">
        <div style="background:#fff;border-radius:14px;padding:14px">
          <h3>📝 دراسة الحالة</h3>
          <p>نموذج شامل للأعراض والعوامل—من المزاج والقلق حتى النوم والشخصية.</p>
          <a class="btn g" href="/case">ابدأ الآن</a>
        </div>
        <div style="background:#fff;border-radius:14px;padding:14px">
          <h3>🧠 CBT فعّال</h3>
          <p>تمارين واضحة: تنشيط سلوكي، تحدّي الأفكار، تعرّض تدريجي، بومودورو، تأريض.</p>
          <a class="btn p" href="/cbt">افتح التمارين</a>
        </div>
        <div style="background:#fff;border-radius:14px;padding:14px">
          <h3>🚭 برنامج الإدمان</h3>
          <p>مراحل: إزالة سمّية، تأهيل، منع انتكاسة—مع خطط قابلة للحفظ.</p>
          <a class="btn alt" href="/addiction">ابدأ البرنامج</a>
        </div>
        <div style="background:#fff;border-radius:14px;padding:14px">
          <h3>📞 احجز جلسة</h3>
          <p>أخصائي نفسي • طبيب نفسي • أخصائي اجتماعي</p>
          <div class="grid-sm">
            <a class="btn g" href="{BOOK_PSY}" target="_blank">أخصائي نفسي</a>
            <a class="btn alt" href="{BOOK_DOC}" target="_blank">طبيب نفسي</a>
            <a class="btn p" href="{BOOK_SOC}" target="_blank">أخصائي اجتماعي</a>
          </div>
        </div>
      </div>
      <div class="kpi">
        <div class="tile"><small class="muted">جلسات مُجدولة</small><br><b>جاهز</b></div>
        <div class="tile"><small class="muted">تمارين CBT</small><br><b>فعّالة</b></div>
        <div class="tile"><small class="muted">تصميم</small><br><b>ملفت</b></div>
      </div>
    </div></section>
    """
    return shell(content, f"{BRAND_NAME} — الرئيسية")

# ================= DSM/CBT/إدمان =================
@app.get("/dsm")
def dsm_page():
    try:
        DSM = importlib.import_module("DSM")
        html = DSM.main() if hasattr(DSM,"main") else "<p>DSM غير متاح.</p>"
    except Exception as e:
        html = f"<p>تعذّر تحميل DSM: {e}</p>"
    return shell(html, "DSM — مرجع")

@app.get("/cbt")
def cbt_page():
    try:
        CBT = importlib.import_module("CBT")
        html = CBT.main() if hasattr(CBT,"main") else "<p>CBT غير متاح.</p>"
    except Exception as e:
        html = f"<p>تعذّر تحميل CBT: {e}</p>"
    return shell(html, "CBT — تمارين وخطط")

@app.get("/addiction")
def addiction_page():
    try:
        ADD = importlib.import_module("Addiction")
        html = ADD.main() if hasattr(ADD,"main") else "<p>صفحة الإدمان غير متاحة.</p>"
    except Exception as e:
        html = f"<p>تعذّر تحميل الإدمان: {e}</p>"
    return shell(html, "برنامج علاج الإدمان")

# ================= دراسة الحالة (موسّعة جدًا) =================
FORM_HTML = """
<h1>📝 دراسة الحالة — نموذج موسّع</h1>
<p class="note">نقدّر مشاعرك وتجربتك. اختر ما ينطبق عليك بهدوء، ويمكنك حفظ النتائج.</p>

<form id="caseForm" method="post" action="/case">
  <!-- المزاج والاكتئاب -->
  <div class="section-title">المزاج والاكتئاب</div>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="low_mood"> مزاج منخفض معظم اليوم</label>
    <label class="chk"><input type="checkbox" name="anhedonia"> فقدان الاهتمام/المتعة</label>
    <label class="chk"><input type="checkbox" name="guilt"> ذنب/قيمة ذاتية منخفضة</label>
    <label class="chk"><input type="checkbox" name="sleep_issue"> اضطراب نوم</label>
    <label class="chk"><input type="checkbox" name="appetite_change"> تغيّر شهية/وزن</label>
    <label class="chk"><input type="checkbox" name="fatigue"> إرهاق/خمول</label>
    <label class="chk"><input type="checkbox" name="slow_psychomotor"> بطء/تهدّج نفسي حركي</label>
    <label class="chk"><input type="checkbox" name="concentration"> ضعف تركيز</label>
    <label class="chk"><input type="checkbox" name="suicidal"> أفكار إيذاء/انتحار (خطر)</label>
  </div>

  <!-- القلق/الوسواس/الصدمة/الهلع -->
  <div class="section-title">القلق والرهاب/الهلع/الوسواس/الصدمة</div>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="worry"> قلق مفرط مستمر</label>
    <label class="chk"><input type="checkbox" name="tension"> توتر جسدي/شدّ عضلي</label>
    <label class="chk"><input type="checkbox" name="restlessness"> تململ/يقظة زائدة</label>
    <label class="chk"><input type="checkbox" name="panic_attacks"> نوبات هلع</label>
    <label class="chk"><input type="checkbox" name="panic_avoidance"> تجنّب خوفًا من النوبات</label>
    <label class="chk"><input type="checkbox" name="social_avoid"> تجنّب اجتماعي</label>
    <label class="chk"><input type="checkbox" name="fear_judgment"> خوف من تقييم الآخرين</label>
    <label class="chk"><input type="checkbox" name="obsessions"> أفكار ملحّة</label>
    <label class="chk"><input type="checkbox" name="compulsions"> أفعال قهرية</label>
    <label class="chk"><input type="checkbox" name="trauma_event"> تعرّض لحدث صادمي</label>
    <label class="chk"><input type="checkbox" name="flashbacks"> فلاشباك/استرجاع</label>
    <label class="chk"><input type="checkbox" name="nightmares"> كوابيس مرتبطة بالحدث</label>
    <label class="chk"><input type="checkbox" name="hypervigilance"> يقظة مفرطة/حساسية</label>
    <label class="chk"><input type="checkbox" name="trauma_avoid"> تجنّب مذكّرات الحدث</label>
  </div>

  <!-- ثنائي القطب/الذهان -->
  <div class="section-title">ثنائي القطب/الذهان</div>
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

  <!-- عصبية نمائية/انتباه/توحد -->
  <div class="section-title">العصبية النمائية والانتباه</div>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="inattention"> عدم انتباه/نسيان</label>
    <label class="chk"><input type="checkbox" name="hyperactivity"> فرط حركة/تململ</label>
    <label class="chk"><input type="checkbox" name="impulsivity_symp"> اندفاعية</label>
    <label class="chk"><input type="checkbox" name="since_childhood"> الأعراض منذ الطفولة</label>
    <label class="chk"><input type="checkbox" name="functional_impair"> تأثير وظيفي واضح</label>
    <label class="chk"><input type="checkbox" name="autism_social"> صعوبات تواصل اجتماعي</label>
    <label class="chk"><input type="checkbox" name="autism_rigid"> سلوك/اهتمام نمطي أو جامد</label>
  </div>

  <!-- الأكل والنوم/الجسد -->
  <div class="section-title">الأكل والنوم/الجسد</div>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="restriction"> تقييد الأكل/خوف من الوزن</label>
    <label class="chk"><input type="checkbox" name="underweight"> نقص وزن ملحوظ</label>
    <label class="chk"><input type="checkbox" name="body_image_distort"> تشوّه صورة الجسد</label>
    <label class="chk"><input type="checkbox" name="binges"> نوبات أكل كبيرة</label>
    <label class="chk"><input type="checkbox" name="compensatory"> تعويض (تقيؤ/مليّن/صيام)</label>
    <label class="chk"><input type="checkbox" name="insomnia"> أرق مستمر</label>
    <label class="chk"><input type="checkbox" name="somatic_pain"> آلام جسدية دون سبب واضح</label>
  </div>

  <!-- اضطرابات الشخصية (A/B/C) -->
  <div class="section-title">اضطرابات الشخصية — مؤشرات عامة</div>
  <div class="grid">
    <!-- عنقودية A -->
    <label class="chk"><input type="checkbox" name="paranoid_traits"> شكّ دائم/تأويل عدائي (زورانية)</label>
    <label class="chk"><input type="checkbox" name="schizoid_traits"> انعزال وبرود عاطفي (انعزالية)</label>
    <label class="chk"><input type="checkbox" name="schizotypal_traits"> غرابة إدراك/تفكير وسلوك (فصامية نمط)</label>
    <!-- عنقودية B -->
    <label class="chk"><input type="checkbox" name="borderline_traits"> اندفاع/تقلّب حاد/خوف هجر (حدّية)</label>
    <label class="chk"><input type="checkbox" name="narcissistic_traits"> تعاظم ذات/حاجة إعجاب/تعاطف منخفض</label>
    <label class="chk"><input type="checkbox" name="histrionic_traits"> بحث عن الانتباه/تعبير عاطفي درامي</label>
    <label class="chk"><input type="checkbox" name="antisocial_traits"> انتهاك حقوق/اندفاع وعدوانية</label>
    <!-- عنقودية C -->
    <label class="chk"><input type="checkbox" name="avoidant_traits"> خجل شديد/تجنّب خوفًا من الرفض</label>
    <label class="chk"><input type="checkbox" name="dependent_traits"> حاجة دعم مفرطة/صعوبة اتخاذ قرار</label>
    <label class="chk"><input type="checkbox" name="ocpd_traits"> كمالية/صرامة/قواعدية مفرطة</label>
  </div>

  <!-- التعاطي -->
  <div class="section-title">التعاطي</div>
  <div class="grid">
    <label class="chk"><input type="checkbox" name="craving"> اشتهاء شديد</label>
    <label class="chk"><input type="checkbox" name="tolerance"> تحمّل/زيادة الجرعة</label>
    <label class="chk"><input type="checkbox" name="withdrawal"> أعراض انسحاب</label>
    <label class="chk"><input type="checkbox" name="use_despite_harm"> استمرار رغم الضرر</label>
    <label class="chk"><input type="checkbox" name="alcohol"> كحول</label>
    <label class="chk"><input type="checkbox" name="opioid"> أفيونات</label>
    <label class="chk"><input type="checkbox" name="stimulant"> منبهات</label>
    <label class="chk"><input type="checkbox" name="cannabis"> قنّب</label>
    <label class="chk"><input type="checkbox" name="sedative"> مهدئات/بنزوديازيبين</label>
  </div>

  <!-- عوامل إضافية -->
  <div class="section-title">العوامل العامة</div>
  <div class="grid">
    <label>المدّة:<br>
      <select name="duration">
        <option value="lt2w">أقل من أسبوعين</option>
        <option value="2to4w">2–4 أسابيع</option>
        <option value="1to6m">1–6 أشهر</option>
        <option value="gt6m">أكثر من 6 أشهر</option>
      </select>
    </label>
    <label>شدة عامة (0–10):<br><input type="number" min="0" max="10" name="distress" value="5"></label>
    <label>بدايات/عمر الظهور:<br><input type="text" name="onset"></label>
    <label>ضغوط/أحداث مؤثرة:<br><input type="text" name="stressors" placeholder="مثال: فقد/خلاف/دراسة/عمل..."></label>
  </div>

  <div class="grid-sm" style="margin-top:10px">
    <button class="btn p" type="submit">اعرض الترشيحات</button>
    <button class="btn alt" type="button" onclick="window.print()">طباعة</button>
    <button class="btn g" type="button" onclick="saveJSON()">حفظ JSON</button>
    <button class="btn" type="button" onclick="clearForm()">مسح</button>
  </div>
</form>

<script>
const KEY='arpsy_case_form_v2';
function toObj(form){
  const data={};
  new FormData(form).forEach((v,k)=>data[k]=v);
  form.querySelectorAll('input[type=checkbox]').forEach(cb=>data[cb.name]=cb.checked);
  return data;
}
function fromObj(form, data){
  if(!data) return;
  Object.keys(data).forEach(k=>{
    const el=form.querySelector(`[name="${k}"]`);
    if(!el) return;
    if(el.type==='checkbox') el.checked=!!data[k]; else el.value=data[k];
  });
}
function saveDraft(){ localStorage.setItem(KEY, JSON.stringify(toObj(document.getElementById('caseForm')))); }
function loadDraft(){ const s=localStorage.getItem(KEY); if(s) fromObj(document.getElementById('caseForm'), JSON.parse(s)); }
function clearForm(){ localStorage.removeItem(KEY); document.getElementById('caseForm').reset(); }
function saveJSON(){
  const blob=new Blob([JSON.stringify(toObj(document.getElementById('caseForm')),null,2)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='case_form.json'; a.click(); URL.revokeObjectURL(a.href);
}
document.getElementById('caseForm').addEventListener('change', saveDraft);
window.addEventListener('DOMContentLoaded', loadDraft);
</script>
"""

RESULT_HTML = """
<h1>📌 ترشيحات أولية</h1>
<ul style="line-height:1.9">{items}</ul>

<h3>🎯 اقتراحات CBT فورية</h3>
<ul style="line-height:1.9">{cbt}</ul>

{flags}

<div class="grid-sm" style="margin:12px 0">
  <a class="btn g" href="{book_psy}" target="_blank">احجز مع الأخصائي النفسي</a>
  <a class="btn alt" href="{book_doc}" target="_blank">احجز مع الطبيب النفسي</a>
  <a class="btn p" href="{book_soc}" target="_blank">احجز مع الأخصائي الاجتماعي</a>
</div>

<blockquote class="q">نثق بقدرتك على التحسّن. خطوة اليوم — ولو صغيرة — تصنع فارقًا كبيرًا.</blockquote>
"""

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell(FORM_HTML, "دراسة الحالة")
    data = {k:v for k,v in request.form.items()}

    # تشخيص مبدئي (عن طريق DSM.py إن وُجد)
    try:
        DSM = importlib.import_module("DSM")
        picks = DSM.diagnose(data) if hasattr(DSM,"diagnose") else [("تعذر الترشيح","DSM.diagnose غير متوفر",0.0)]
    except Exception as e:
        picks = [("خطأ", str(e), 0.0)]

    items = "".join([f"<li><b>{n}</b> — {w} <small>(Score: {s:.0f})</small></li>" for n,w,s in picks])

    # نصائح CBT حسب الأعراض
    f=lambda k: data.get(k) in ("on","true","True","1")
    tips=[]
    if f("worry") or f("social_avoid") or f("panic_attacks"):
        tips.append("قلق/هلع: قياس يومي (0–10) + تنفّس 4-4-6 + تعرّض تدريجي مع منع الأمان الزائف.")
    if f("low_mood") or f("anhedonia"):
        tips.append("اكتئاب: تنشيط سلوكي — 3 أنشطة (ممتع/مفيد/قيمة) يوميًا + مراجعة الأفكار اليائسة.")
    if f("obsessions") or f("compulsions"):
        tips.append("OCD: ERP تدريجي بقائمة 10 محفزات مع <b>منع الاستجابة</b> ووقت قلق محدّد.")
    if f("trauma_event") and (f("flashbacks") or f("nightmares")):
        tips.append("PTSD: تأريض 5–4–3–2–1 وتنظيم نوم/أكل، وتعريض سردي آمن تدريجيًا.")
    if f("inattention") or f("hyperactivity") or f("impulsivity_symp"):
        tips.append("ADHD: بومودورو 25–5 + 3 أولويات صباحية + مؤقّت مرئي وبيئة قليلة المشتتات.")
    if f("restriction") or f("binges") or f("body_image_distort"):
        tips.append("اضطرابات الأكل: جدول وجبات 3+2، منع التعويض، وتمارين صورة الجسد تدريجيًا.")
    if f("craving") or f("withdrawal") or f("use_despite_harm"):
        tips.append("تعاطي: إنذار مبكر + بدائل سريعة + تواصل داعم، وراجع برنامج الإدمان.")

    if not tips:
        tips.append("ابدأ بدفتر ABC (موقف→فكرة→شعور→سلوك) لمدة 3 أيام ولاحظ أكثر 3 أفكار تكرارًا.")

    cbt_html = "".join([f"<li>{t}</li>" for t in tips])

    # إشارات تنبيه/سلامة
    flags_txt = ""
    red = []
    if data.get("suicidal") in ("on","true","True","1"):
        red.append("⚠️ وجود أفكار إيذاء/انتحار — يُرجى التواصل فورًا مع مختص أو جهة مساعدة طارئة في بلدك.")
    if data.get("hallucinations") in ("on","true","True","1") or data.get("delusions") in ("on","true","True","1"):
        red.append("⚠️ أعراض ذهانية ظاهرة — يُستحسن تقييم طبي سريع.")
    if red:
        flags_txt = "<h3>تنبيه</h3><ul>" + "".join([f"<li>{x}</li>" for x in red]) + "</ul>"

    html = RESULT_HTML.format(
        items=items, cbt=cbt_html, flags=flags_txt,
        book_psy=BOOK_PSY, book_doc=BOOK_DOC, book_soc=BOOK_SOC
    )
    return shell(html, "نتيجة الترشيح")

# ================= تواصل =================
@app.get("/contact")
def contact():
    html = f"""
    <h1>📞 التواصل والحجز</h1>
    <div class="grid-sm">
      <a class="btn g"  href="{BOOK_PSY}" target="_blank">احجز مع الأخصائي النفسي</a>
      <a class="btn alt" href="{BOOK_DOC}" target="_blank">احجز مع الطبيب النفسي</a>
      <a class="btn p"  href="{BOOK_SOC}" target="_blank">احجز مع الأخصائي الاجتماعي</a>
      <a class="btn tg" href="{TELEGRAM_URL}" target="_blank">بوت تيليجرام</a>
      <a class="btn wa" href="{WA_QUICK}" target="_blank">واتساب سريع</a>
    </div>
    <p class="note" style="margin-top:12px">نُقدّر قصتك. تواصل معنا متى ما احتجت—سنكون معك خطوة بخطوة.</p>
    """
    return shell(html, "التواصل")

# ================= إحصاءات =================
@app.get("/stats")
def stats():
    if request.args.get("key","") != STATS_KEY: abort(401)
    rows = "".join([f"<tr><td>{d}</td><td>{n}</td></tr>" for d,n in last30()])
    html = f"""
    <h1>📈 إحصاءات الزوّار</h1>
    <p>الإجمالي: <b>{total_visitors()}</b></p>
    <table class="table"><thead><tr><th>اليوم</th><th>زيارات</th></tr></thead><tbody>{rows}</tbody></table>
    """
    return shell(html, "إحصاءات الزوار")

@app.errorhandler(401)
def unauth(_): return shell("<h3>غير مصرّح</h3>", "401"), 401

@app.get("/health")
def health(): return {"status":"ok"}, 200

# ================= تشغيل محلي =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
