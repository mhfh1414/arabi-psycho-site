# -*- coding: utf-8 -*-
# app.py — Arabi Psycho (Main App, + Case/DSM/Booking/Addiction/Contact)
# يعمل مع cbt.py (ستجده بالأسفل). شغّل:  python app.py

import os, json, tempfile, urllib.parse
from datetime import datetime
from typing import Optional, Tuple, List
from flask import Flask, request, redirect, jsonify

# ========== إعداد التطبيق ==========
app = Flask(__name__)

# إعدادات عامة (يمكنك تغييرها بمتغيّرات البيئة)
BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO  = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696?text=%D8%B9%D8%B1%D8%A8%D9%8A%20%D8%B3%D8%A7%D9%8A%D9%83%D9%88")

PSYCHO_WA = os.environ.get("PSYCHOLOGIST_WA", "https://wa.me/966530565696")
PSYCH_WA  = os.environ.get("PSYCHIATRIST_WA", "https://wa.me/966530565696")
SOCIAL_WA = os.environ.get("SOCIAL_WORKER_WA", "https://wa.me/966530565696")

# ========= عدّاد الزوار (آمن) =========
COUNTER_FILE = "visitors.json"

def _atomic_write(path: str, data: dict):
    fd, tmp = tempfile.mkstemp(prefix="vis_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        try:
            if os.path.exists(tmp): os.remove(tmp)
        except Exception:
            pass

def _load_count() -> int:
    try:
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            return int(json.load(f).get("count", 0))
    except Exception:
        return 0

def _save_count(n: int):
    try:
        _atomic_write(COUNTER_FILE, {"count": int(n)})
    except Exception:
        pass

def bump_visitors() -> int:
    n = _load_count() + 1
    _save_count(n)
    return n

# ========= إطار الصفحات (Shell) =========
CACHE_BUST = os.environ.get("CACHE_BUST", datetime.utcnow().strftime("%Y%m%d%H%M%S"))

def shell(title: str, content: str, visitors: Optional[int] = None) -> str:
    visitors_html = f"<div class='small' style='margin-top:12px'>👀 عدد الزوّار: <b>{visitors}</b></div>" if visitors is not None else ""
    return f"""<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>
<meta http-equiv="Pragma" content="no-cache"/><meta http-equiv="Expires" content="0"/>
<link rel="icon" href="{LOGO}"/>
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
.btn{{display:inline-block;background:var(--p);color:#fff;text-decoration:none;padding:11px 16px;border-radius:12px;font-weight:800;cursor:pointer}}
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
  .print-only {{ display:initial !重要; }}
  body {{ background:#fff; font-size:18px; line-height:1.8; }}
  .content {{ padding:0 !important; }}
  .card {{ box-shadow:none; border:none; padding:0; }}
  h1{{font-size:26px}} h2{{font-size:22px}} h3{{font-size:18px}}
  ul{{padding-inline-start:20px}}
}}
</style></head><body>
<script>window.__BUILD__='{CACHE_BUST}';</script>
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
    {visitors_html}
  </aside>
  <main class="content">{content}</main>
</div>
<div class="footer"><small>© جميع الحقوق محفوظة لـ {BRAND}</small></div>
</body></html>"""

# ========= الرئيسية =========
@app.get("/")
def home():
    v = bump_visitors()
    content = f"""
    <div class="card" style="margin-bottom:14px">
      <h1>مرحبًا بك في {BRAND}</h1>
      <div class="small">مساحتك الهادئة لفهم الأعراض وبناء خطة عملية محترمة لخصوصيتك.</div>
    </div>
    <div class="grid">
      <div class="tile"><h3>📝 دراسة الحالة</h3><p class="small">قسّم الأعراض بدقة؛ ترتبط بالـ CBT وبرنامج الإدمان والحجز.</p><a class="btn gold" href="/case">ابدأ الآن</a></div>
      <div class="tile"><h3>📘 مرجع DSM</h3><p class="small">ملخّص منظّم للمحاور الكبرى.</p><a class="btn alt" href="/dsm">فتح DSM</a></div>
      <div class="tile"><h3>🧠 CBT</h3><p class="small">خطط جاهزة + مولّد جدول 7/10/14 يوم.</p><a class="btn" href="/cbt">افتح CBT</a></div>
      <div class="tile"><h3>🚭 برنامج الإدمان</h3><p class="small">Detox → Rehab → Aftercare → منع الانتكاس.</p><a class="btn" href="/addiction">افتح الإدمان</a></div>
      <div class="tile"><h3>📅 احجز موعدًا</h3><p class="small">الأخصائي النفسي / الطبيب النفسي / الأخصائي الاجتماعي.</p><a class="btn gold" href="/book">نموذج الحجز</a></div>
      <div class="tile"><h3>تواصل سريع</h3><a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">تيليجرام</a> <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">واتساب</a></div>
    </div>"""
    return shell("الرئيسية — عربي سايكو", content, v)

# ========= DSM =========
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

# ========= نموذج الحجز =========
BOOK_FORM = """
<div class="card">
  <h1>📅 احجز موعدك</h1>
  <div class="note">«موعدٌ واحد قد يغيّر مسار أسبوعك.»</div>
  <form method="post" action="/book" novalidate onsubmit="return validateBook()">
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
    <div class="row"><button class="btn gold" type="submit">إرسال عبر واتساب</button><a class="btn alt" href="/">رجوع</a></div>
  </form>
  <script>
    function validateBook(){
      const phone=document.querySelector('[name="phone"]');
      if(!/^\\d{{9,15}}$/.test(phone.value||'')){ alert('الرجاء إدخال رقم صحيح (9–15 رقم).'); return false; }
      return true;
    }
  </script>
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

# ========= دراسة الحالة =========
def c(data,*keys):  # مساعد العدّ
    return sum(1 for k in keys if data.get(k) is not None)

FORM_HTML = r"""
<div class="card">
  <h1>📝 دراسة الحالة</h1>
  <div class="small">قسّم الأعراض بدقة؛ ستظهر ترشيحات أولية وروابط لأدوات CBT والحجز. <b>اختياراتك تُحفظ تلقائيًا</b>.</div>

  <form method="post" action="/case" oninput="persistCase()">
    <div class="grid">
      <div class="tile"><h3>المزاج العام</h3>
        <label class="chk"><input type="checkbox" name="low_mood"> مزاج منخفض معظم اليوم</label>
        <label class="chk"><input type="checkbox" name="anhedonia"> فقدان المتعة</label>
        <label class="chk"><input type="checkbox" name="fatigue"> إرهاق/انخفاض طاقة</label>
        <label class="chk"><input type="checkbox" name="sleep_issue"> نوم مضطرب</label>
        <label class="chk"><input type="checkbox" name="appetite_change"> تغيّر الشهية/الوزن</label>
        <label class="chk"><input type="checkbox" name="pain_chronic"> ألم مزمن/توتر جسدي عام</label>
      </div>

      <div class="tile"><h3>اكتئاب — إضافية</h3>
        <label class="chk"><input type="checkbox" name="psychomotor"> تباطؤ/انفعال حركي</label>
        <label class="chk"><input type="checkbox" name="worthlessness"> ذنب/عدم القيمة</label>
        <label class="chk"><input type="checkbox" name="poor_concentration"> تركيز ضعيف/تردّد</label>
        <label class="chk"><input type="checkbox" name="suicidal"> أفكار إيذاء/انتحار</label>
        <label class="chk"><input type="checkbox" name="dep_2w"> استمرار ≥ أسبوعين</label>
        <label class="chk"><input type="checkbox" name="dep_function"> تأثير على الدراسة/العمل/العلاقات</label>
      </div>

      <div class="tile"><h3>قلق/هلع/اجتماعي</h3>
        <label class="chk"><input type="checkbox" name="worry"> قلق مفرط</label>
        <label class="chk"><input type="checkbox" name="tension"> توتر جسدي</label>
        <label class="chk"><input type="checkbox" name="restlessness"> عصبية/أرق</label>
        <label class="chk"><input type="checkbox" name="panic_attacks"> نوبات هلع</label>
        <label class="chk"><input type="checkbox" name="social_fear"> خوف من تقييم اجتماعي</label>
        <label class="chk"><input type="checkbox" name="phobia_specific"> رُهاب محدد</label>
      </div>

      <div class="tile"><h3>وسواس/صدمات</h3>
        <label class="chk"><input type="checkbox" name="obsessions"> أفكار مُلِحّة</label>
        <label class="chk"><input type="checkbox" name="compulsions"> أفعال قهرية</label>
        <label class="chk"><input type="checkbox" name="flashbacks"> استرجاعات/كوابيس</label>
        <label class="chk"><input type="checkbox" name="hypervigilance"> يقظة مفرطة</label>
        <label class="chk"><input type="checkbox" name="avoidance"> تجنّب ملحوظ</label>
      </div>

      <div class="tile"><h3>ذهانية/طيف الفصام</h3>
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

      <div class="tile"><h3>ثنائي القطب (هوس)</h3>
        <label class="chk"><input type="checkbox" name="elevated_mood"> مزاج مرتفع/متهوّر</label>
        <label class="chk"><input type="checkbox" name="decreased_sleep_need"> قلة الحاجة للنوم</label>
        <label class="chk"><input type="checkbox" name="grandiosity"> شعور بالعظمة</label>
        <label class="chk"><input type="checkbox" name="racing_thoughts"> أفكار متسارعة</label>
        <label class="chk"><input type="checkbox" name="pressured_speech"> كلام ضاغط</label>
        <label class="chk"><input type="checkbox" name="risky_behavior"> سلوك محفوف بالمخاطر/صرف زائد</label>
        <label class="chk"><input type="checkbox" name="mania_ge_7d"> استمرار ≥ 7 أيام</label>
        <label class="chk"><input type="checkbox" name="mania_hospital"> احتاج دخول/تدخل طبي</label>
      </div>

      <div class="tile"><h3>نوم/أكل/انتباه</h3>
        <label class="chk"><input type="checkbox" name="insomnia"> أرق مستمر</label>
        <label class="chk"><input type="checkbox" name="hypersomnia"> نوم زائد</label>
        <label class="chk"><input type="checkbox" name="binge_eating"> أكل شره</label>
        <label class="chk"><input type="checkbox" name="restrict_eating"> تقييد في الأكل</label>
        <label class="chk"><input type="checkbox" name="adhd_inattention"> تشتت/نسيان</label>
        <label class="chk"><input type="checkbox" name="adhd_hyper"> فرط حركة/اندفاع</label>
      </div>

      <div class="tile"><h3>مواد</h3>
        <label class="chk"><input type="checkbox" name="craving"> اشتهاء</label>
        <label class="chk"><input type="checkbox" name="withdrawal"> انسحاب</label>
        <label class="chk"><input type="checkbox" name="use_harm"> استخدام رغم الضرر</label>
      </div>
    </div>

    <div class="tile" style="margin-top:10px"><label>ملاحظاتك<textarea name="notes" rows="4" placeholder="أي تفاصيل إضافية مهمة لك" oninput="persistCase()"></textarea></label></div>
    <button class="btn gold" type="submit">عرض الترشيحات</button>
  </form>

  <script>
    const KEY='case_state';
    function persistCase(){
      const form=document.querySelector('form[action="/case"]');
      const data={};
      form.querySelectorAll('input[type=checkbox]').forEach(ch=>{ if(ch.checked) data[ch.name]=true; });
      data.notes=form.querySelector('[name=notes]')?.value||'';
      localStorage.setItem(KEY, JSON.stringify(data));
    }
    (function restore(){
      try{
        const data=JSON.parse(localStorage.getItem(KEY)||'{}');
        Object.keys(data).forEach(k=>{
          const el=document.querySelector('[name="'+k+'"]');
          if(el && el.type==='checkbox') el.checked=true;
        });
        if(data.notes){ const n=document.querySelector('[name=notes]'); if(n) n.value=data.notes; }
      }catch(e){}
    })();
  </script>
</div>
"""

def build_recommendations(data: dict) -> Tuple[List[Tuple[str,str,int]], List[str], List[str]]:
    picks, go_cbt, go_add = [], [], []

    dep_core = c(data,"low_mood","anhedonia")
    dep_more = c(data,"fatigue","sleep_issue","appetite_change","psychomotor","worthlessness","poor_concentration","suicidal","pain_chronic")
    dep_total = dep_core + dep_more
    dep_2w = bool(data.get("dep_2w")); dep_fx = bool(data.get("dep_function"))
    if dep_total >= 5 and dep_2w and dep_core >= 1:
        picks.append(("نوبة اكتئابية جسيمة (MDD)", "≥5 أعراض لمدة ≥ أسبوعين مع تأثير وظيفي", 90 if dep_fx else 80))
        go_cbt += ["BA — تنشيط سلوكي","TR — سجل أفكار","SH — نظافة النوم","PS — حل المشكلات"]
    elif dep_total >= 3 and dep_2w:
        picks.append(("نوبة اكتئابية خفيفة/متوسطة", "مجموعة أعراض مستمرة أسبوعين", 70))
        go_cbt += ["BA — تنشيط سلوكي","TR — سجل أفكار","مراقبة مزاج"]
    elif dep_core >= 1 and dep_total >= 2:
        picks.append(("مزاج منخفض/فتور", "كتلة أعراض مزاجية جزئية", 55))
        go_cbt += ["BA — تنشيط سلوكي","روتين يومي لطيف"]

    if data.get("suicidal"):
        picks.append(("تنبيه أمان", "وجود أفكار إيذاء/انتحار — فضّل تواصلًا فوريًا مع مختص", 99))

    if c(data,"worry","tension","restlessness") >= 2:
        picks.append(("قلق معمّم", "قلق مفرط مع توتر/أرق", 75)); go_cbt += ["WT — وقت القلق","MB — يقظة","PS — حل المشكلات"]
    if data.get("panic_attacks"):
        picks.append(("نوبات هلع", "نوبات مفاجئة مع خوف من التكرار", 70)); go_cbt += ["IE — تعرّض داخلي","SA — إيقاف سلوكيات آمنة"]
    if data.get("social_fear") or data.get("phobia_specific"):
        picks.append(("قلق اجتماعي/رُهاب", "خشية تقييم أو موقف محدد مع تجنّب", 70)); go_cbt += ["GE — تعرّض اجتماعي","SS — مهارات اجتماعية","TR — سجل أفكار"]

    if data.get("obsessions") and data.get("compulsions"):
        picks.append(("وسواس قهري (OCD)", "وساوس + أفعال قهرية", 80)); go_cbt += ["ERP — وسواس","SA — إيقاف سلوكيات آمنة"]
    if c(data,"flashbacks","hypervigilance","avoidance") >= 2:
        picks.append(("آثار صدمة (PTSD/ASD)", "استرجاعات/يقظة/تجنّب", 70)); go_cbt += ["PTSD — تأريض/تنظيم","MB — يقظة"]

    if c(data,"insomnia","hypersomnia") >= 1:
        go_cbt += ["SH — نظافة النوم"]
    if c(data,"binge_eating","restrict_eating") >= 1:
        picks.append(("مخاوف الأكل", "نمط شره/تقييد", 55)); go_cbt += ["PS — حل المشكلات","MB — يقظة"]
    if c(data,"adhd_inattention","adhd_hyper") >= 2:
        picks.append(("سمات ADHD", "تشتّت واندفاعية مؤثرة", 60)); go_cbt += ["PS — حل المشكلات","روتين يومي"]

    if c(data,"craving","withdrawal","use_harm") >= 2:
        picks.append(("تعاطي مواد", "اشتهاء/انسحاب/استمرار رغم الضرر", 80)); go_cbt += ["RP — منع الانتكاس","PS — حل المشكلات"]
        go_add.append("برنامج الإدمان")

    pc = c(data,"hallucinations","delusions","disorganized_speech","negative_symptoms","catatonia")
    dur_lt_1m  = bool(data.get("duration_lt_1m"))
    dur_ge_1m  = bool(data.get("duration_ge_1m"))
    dur_ge_6m  = bool(data.get("duration_ge_6m"))
    decline    = bool(data.get("decline_function"))
    if pc >= 2 and (dur_ge_6m or (dur_ge_1m and decline)):
        picks.append(("فصام", "ذهانية أساسية مع استمرار/تدهور وظيفي", 85)); go_cbt += ["تثقيف + مهارات التعامل","SH — نظافة النوم","دعم أسري"]
    elif pc >= 2 and (dep_total >= 3):
        picks.append(("فصامي وجداني", "ذهانية مع كتلة مزاجية واضحة", 75))
    elif pc >= 2 and dur_lt_1m:
        picks.append(("اضطراب ذهاني وجيز", "ذهانية قصيرة المدة", 65))
    elif data.get("delusions") and pc == 1 and dur_ge_1m and not decline:
        picks.append(("اضطراب وهامي", "أوهام ثابتة مع أداء وظيفي مقبول", 60))

    go_cbt = sorted(set(go_cbt))
    return picks, go_cbt, go_add

def render_results(picks, go_cbt, go_add, notes):
    items_li = "".join([f"<li><b>{t}</b> — {w} <span class='small'>(درجة: {s:.0f})</span></li>" for (t,w,s) in picks]) or "<li>لا توجد مؤشرات كافية.</li>"
    cbt_badges = "".join([f"<span class='badge2'>🔧 {x}</span>" for x in go_cbt])
    add_badge  = "<span class='badge2'>🚭 برنامج الإدمان مُقترح</span>" if go_add else ""
    header = f"""
    <div class='header-result'>
      <img src='{LOGO}' alt='logo' onerror="this.style.display='none'">
      <div><div style='font-weight:900;font-size:22px'>{BRAND}</div>
      <div class='small'>نتيجة دراسة الحالة — تلخيص أولي جاهز للطباعة والمشاركة</div></div>
    </div>"""
    summary = f"""
    <div class='summary-cards'>
      <div class='scard'><b>الترشيحات</b><br/><span class='small'>{len(picks)} نتيجة</span></div>
      <div class='scard'><b>CBT المقترح</b><br/>{(cbt_badges or "<span class='small'>—</span>")}</div>
      <div class='scard'><b>الإدمان</b><br/>{(add_badge or "<span class='small'>—</span>")}</div>
    </div>"""
    note_html = f"<div class='tile' style='margin-top:10px'><b>ملاحظاتك:</b><br/>{notes}</div>" if notes else ""
    actions = f"""
    <div class='row screen-only' style='margin-top:12px'>
      <button class='btn alt' onclick='window.print()'>🖨️ طباعة</button>
      <button class='btn' onclick='saveJSON()'>💾 تنزيل JSON</button>
      <a class='btn wa' id='share-wa' target='_blank' rel='noopener'>🟢 مشاركة واتساب</a>
      <a class='btn tg' id='share-tg' target='_blank' rel='noopener'>✈️ مشاركة تيليجرام</a>
      <a class='btn gold' href='/book'>📅 حجز سريع</a>
      <a class='btn' href='/cbt'>🧠 فتح CBT</a>
    </div>
    <div class='print-only small' style='margin-top:8px'>تم إنشاء هذا الملخّص بواسطة <b>{BRAND}</b> — {TG_URL}</div>
    <script>
      function buildShareText(){{
        const items=[...document.querySelectorAll('#diag-items li')].map(li=>'- '+li.innerText).join('\\n');
        const notes={json.dumps(notes or "")!r};
        let msg='نتيجة دراسة الحالة — {BRAND}\\n\\n'+items;
        if(notes) msg+='\\n\\nملاحظات: '+notes;
        msg += '\\n' + location.origin + '/case';
        return msg;
      }}
      function saveJSON(){{
        const data={{items:[...document.querySelectorAll('#diag-items li')].map(li=>li.innerText),
                     cbt:[...document.querySelectorAll('.badge2')].map(b=>b.innerText),
                     notes:{json.dumps(notes or "")!r},
                     created_at:new Date().toISOString(), build: window.__BUILD__}};
        const a=document.createElement('a');
        a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}}));
        a.download='case_result.json'; a.click(); URL.revokeObjectURL(a.href);
      }}
      const text=encodeURIComponent(buildShareText());
      document.getElementById('share-wa').href='{WA_URL.split("?")[0]}'+'?text='+text;
      document.getElementById('share-tg').href='https://t.me/share/url?url='+encodeURIComponent(location.origin+'/case')+'&text='+text;
    </script>"""
    return f"""
    <div class='card'>
      {header}{summary}
      <h2 style='margin-top:12px'>📌 الترشيحات</h2>
      <ol id='diag-items' style='line-height:1.95; padding-inline-start: 20px'>{items_li}</ol>
      <h3>🔧 أدوات CBT المقترحة</h3>
      <div>{cbt_badges or "<span class='small'>لا توجد أدوات محددة</span>"}</div>
      <h3 style='margin-top:10px'>🚭 الإدمان</h3>
      <div>{add_badge or "<span class='small'>لا مؤشرات</span>"}</div>
      {note_html}{actions}
    </div>"""

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell("دراسة الحالة", FORM_HTML, _load_count())
    data  = {k: v for k, v in request.form.items()}
    picks, go_cbt, go_add = build_recommendations(data)
    notes = (request.form.get("notes") or "").strip()
    return shell("نتيجة الترشيح", render_results(picks, go_cbt, go_add, notes), _load_count())

# ========= تواصل =========
@app.get("/contact")
def contact():
    html = f"""
    <div class='card'>
      <h1>📞 التواصل</h1>
      <div class='grid'>
        <div class='tile'><h3>قنوات عامة</h3>
          <a class='btn tg' href='{TG_URL}' target='_blank' rel='noopener'>تيليجرام عربي سايكو</a>
          <a class='btn wa' href='{WA_URL}' target='_blank' rel='noopener'>واتساب</a>
        </div>
        <div class='tile'><h3>حجز سريع</h3><a class='btn gold' href='/book'>📅 افتح نموذج الحجز</a></div>
      </div>
    </div>"""
    return shell("التواصل", html, _load_count())

# ========= API/Health/404 =========
@app.get("/api/health")
def api_health():
    return jsonify({"ok": True, "brand": BRAND, "build": CACHE_BUST}), 200

@app.get("/health")
def health():
    return {"status":"ok","brand":BRAND,"build":CACHE_BUST}, 200

# ========= رؤوس أمان =========
@app.after_request
def add_headers(resp):
    # السماح بالـ inline scripts (لجداول CBT ونتائج دراسة الحالة)
    csp = (
        "default-src 'self' data: blob: https://t.me https://wa.me https://api.whatsapp.com; "
        "script-src 'self' 'unsafe-inline' data: blob: https://t.me https://wa.me https://api.whatsapp.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob: *; "
        "connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors *"
    )
    resp.headers['Content-Security-Policy'] = csp
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    resp.headers['Permissions-Policy'] = 'geolocation=()'
    return resp

# ========= ربط صفحة CBT من الملف المنفصل =========
from cbt import register_cbt   # <-- يتطلب وجود cbt.py بجانب هذا الملف
register_cbt(app, shell, BRAND, LOGO, TG_URL, WA_URL)

# ========= تشغيل =========
if __name__ == "__main__":
    # للتشغيل: python app.py
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
