# app.py — عربي سايكو: رئيسية + دراسة حالة شاملة + DSM/CBT/إدمان + تواصل + نموذج حجز داخلي
import os, importlib, urllib.parse
from flask import Flask, request, redirect
try:
    import requests  # لإرسال رسالة إلى تيليجرام (اختياري)
except Exception:
    requests = None

app = Flask(__name__)

# ===== إعدادات عامة =====
BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO  = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")

# قنوات عامة
TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696?text=%D8%B9%D8%B1%D8%A8%D9%8A%20%D8%B3%D8%A7%D9%8A%D9%83%D9%88")

# أرقام الحجز (واتساب)
PSYCHO_WA = os.environ.get("PSYCHOLOGIST_WA", "https://wa.me/966530565696")
PSYCH_WA  = os.environ.get("PSYCHIATRIST_WA", "https://wa.me/966530565696")
SOCIAL_WA = os.environ.get("SOCIAL_WORKER_WA", "https://wa.me/966530565696")

# تيليجرام اختياري لإشعار البوت
TG_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # مثال: 123456:AA...
TG_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID")    # آيدي القناة/المجموعة/الحساب

# ===== إطار صفحات بدون Jinja =====
def shell(title: str, content: str) -> str:
    return f"""<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<style>
:root{{--p:#4B0082;--g:#FFD700;--bg:#faf7e6}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif;color:#222}}
.top{{display:flex;align-items:center;gap:10px;background:var(--p);color:#fff;padding:10px 14px}}
.top img{{width:42px;height:42px;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
.brand{{font-weight:800}}
.nav a{{color:#fff;text-decoration:none;margin:0 8px;font-weight:700;opacity:.95}}
.wrap{{max-width:1100px;margin:28px auto;padding:20px;background:#fff;border:1px solid #eee;border-radius:16px;box-shadow:0 10px 24px rgba(0,0,0,.06)}}
.btn{{display:inline-block;background:var(--p);color:#fff;text-decoration:none;padding:10px 14px;border-radius:12px;font-weight:800}}
.btn.alt{{background:#5b22a6}} .btn.gold{{background:var(--g);color:var(--p)}} .btn.wa{{background:#25D366}} .btn.tg{{background:#229ED9}}
.grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
.tile{{background:#fff;border:1px solid #eee;border-radius:12px;padding:12px}}
label.chk{{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:8px}}
.note{{background:#fff7d1;border:1px dashed #e5c100;border-radius:10px;padding:8px 12px;margin-bottom:10px}}
input,select,textarea{{width:100%;border:1px solid #ddd;border-radius:10px;padding:10px}}
.footer{{text-align:center;color:#fff;margin-top:24px;padding:14px;background:var(--p)}}
.small{{font-size:.92rem;opacity:.85}}
</style></head><body>
<header class="top">
  <img src="{LOGO}" alt="شعار"/><div class="brand">{BRAND}</div>
  <nav class="nav" style="margin-right:auto">
    <a href="/">الرئيسية</a><a href="/case">دراسة الحالة</a><a href="/dsm">DSM</a>
    <a href="/cbt">CBT</a><a href="/addiction">إدمان</a><a href="/book">احجز موعد</a><a href="/contact">تواصل</a>
  </nav>
</header>
<main class="wrap">{content}</main>
<footer class="footer"><small>© جميع الحقوق محفوظة لـ {BRAND}</small></footer>
</body></html>"""

# ===== الرئيسية =====
@app.get("/")
def home():
    content = f"""
    <div class="grid">
      <div class="tile">
        <h2>علاج نفسي افتراضي</h2>
        <p>منصّة منظَّمة تساعدك على فهم أعراضك وبناء خطة أولية محترمة لخصوصيتك.</p>
        <a class="btn gold" href="/case">📝 ابدأ دراسة الحالة</a>
      </div>
      <div class="tile"><h3>مرجع DSM</h3><p>قوائم منظّمة للاضطرابات الشائعة.</p><a class="btn alt" href="/dsm">📘 فتح DSM</a></div>
      <div class="tile"><h3>CBT</h3><p>أدوات عملية: تنشيط سلوكي، سجل أفكار، ERP، تعرّض اجتماعي، نوم…</p><a class="btn" href="/cbt">🧠 افتح CBT</a></div>
      <div class="tile"><h3>برنامج الإدمان</h3><p>اختيار المادة ثم خطة Detox → Rehab → Relapse.</p><a class="btn" href="/addiction">🚭 افتح الإدمان</a></div>
      <div class="tile">
        <h3>احجز موعد الآن</h3>
        <p>اختر نوع المختص وأرسل بياناتك بسهولة.</p>
        <a class="btn gold" href="/book">📅 نموذج الحجز</a>
      </div>
      <div class="tile">
        <h3>تواصل سريع</h3>
        <a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">✈️ تيليجرام</a>
        <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">🟢 واتساب عام</a>
      </div>
    </div>
    """
    return shell("عربي سايكو — الرئيسية", content)

# ===== صفحات DSM/CBT/إدمان من ملفاتها =====
@app.get("/dsm")
def dsm():
    try:
        DSM = importlib.import_module("DSM")
        html = DSM.main() if hasattr(DSM, "main") else "<p>مرجع DSM غير متوفر.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل DSM: {e}</p>"
    return shell("DSM — مرجع", html)

@app.get("/cbt")
def cbt():
    try:
        CBT = importlib.import_module("CBT")
        html = CBT.main() if hasattr(CBT, "main") else "<p>CBT غير متوفر.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل CBT: {e}</p>"
    return shell("CBT — خطط وتمارين", html)

@app.get("/addiction")
def addiction():
    try:
        ADD = importlib.import_module("Addiction")
        html = ADD.main() if hasattr(ADD, "main") else "<p>صفحة الإدمان غير متوفرة.</p>"
    except Exception as e:
        html = f"<p>تعذر تحميل صفحة الإدمان: {e}</p>"
    return shell("علاج الإدمان", html)

# ===== نموذج حجز داخلي =====
BOOK_FORM = """
<h1>📅 حجز موعد</h1>
<p class="small">املأ البيانات التالية، وسيتم إرسالها مباشرةً إلى فريق {brand} عبر واتساب، مع خيار إشعار تيليجرام.</p>
<form method="post" action="/book">
  <div class="grid">
    <div class="tile"><label>الاسم الكامل<input name="name" required></label></div>
    <div class="tile"><label>العمر<input name="age" type="number" min="5" max="120"></label></div>
    <div class="tile">
      <label>نوع الموعد
        <select name="type" required>
          <option value="الأخصائي النفسي">الأخصائي النفسي</option>
          <option value="الطبيب النفسي">الطبيب النفسي</option>
          <option value="الأخصائي الاجتماعي">الأخصائي الاجتماعي</option>
        </select>
      </label>
    </div>
    <div class="tile">
      <label>أفضل وسيلة تواصل
        <select name="channel" required>
          <option value="واتساب">واتساب</option>
          <option value="اتصال">اتصال</option>
          <option value="تيليجرام">تيليجرام</option>
        </select>
      </label>
    </div>
    <div class="tile"><label>رقم التواصل (مطلوب)<input name="phone" required placeholder="9665xxxxxxxx"></label></div>
    <div class="tile"><label>أفضل وقت للتواصل<input name="best_time" placeholder="مثال: مساءً 7-9"></label></div>
  </div>
  <div class="tile" style="margin-top:10px">
    <label>نبذة عن المشكلة/الهدف العلاجي
      <textarea name="summary" rows="5" placeholder="اكتب بإيجاز الأعراض أو الهدف من الجلسة"></textarea>
    </label>
  </div>
  <button class="btn gold" type="submit">إرسال الطلب</button>
  <a class="btn out" href="/">إلغاء</a>
</form>
""".replace("{brand}", BRAND)

def _telegram_notify(text: str):
    """يرسل إشعار تيليجرام إذا تم ضبط مفاتيح البوت"""
    if not (TG_BOT_TOKEN and TG_CHAT_ID and requests):
        return False, "telegram_not_configured"
    try:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        resp = requests.post(url, data={"chat_id": TG_CHAT_ID, "text": text})
        return resp.ok, f"telegram_status_{resp.status_code}"
    except Exception as e:
        return False, f"telegram_error_{e}"

@app.route("/book", methods=["GET","POST"])
def book():
    if request.method == "GET":
        return shell("حجز موعد", BOOK_FORM)

    # اجمع البيانات
    f = request.form
    name       = (f.get("name") or "").strip()
    age        = (f.get("age") or "").strip()
    typ        = (f.get("type") or "").strip()
    channel    = (f.get("channel") or "").strip()
    phone      = (f.get("phone") or "").strip()
    best_time  = (f.get("best_time") or "").strip()
    summary    = (f.get("summary") or "").strip()

    # كوّن نص الرسالة
    msg = (
        "طلب حجز جديد — عربي سايكو\n"
        f"👤 الاسم: {name}\n"
        f"🎯 نوع الموعد: {typ}\n"
        f"📞 وسيلة التواصل: {channel}\n"
        f"📱 الرقم: {phone}\n"
        f"⏰ أفضل وقت: {best_time}\n"
        f"📝 نبذة: {summary}\n"
        "— تم الإرسال من نموذج الحجز بالموقع."
    )

    # إشعار تيليجرام (اختياري)
    _telegram_notify(msg)

    # إرسال إلى واتساب بالرسالة المعبأة ثم إعادة توجيه الزائر
    encoded = urllib.parse.quote_plus(msg)
    if "الطبيب" in typ:
        wa_base = PSYCH_WA
    elif "الاجتماعي" in typ:
        wa_base = SOCIAL_WA
    else:
        wa_base = PSYCHO_WA

    # إذا كان الرابط لا يحتوي ?text أضف المعامل
    wa_link = wa_base + ("&" if "?" in wa_base else "?") + f"text={encoded}"
    return redirect(wa_link, code=302)

# ===== تواصل عام =====
@app.get("/contact")
def contact():
    html = f"""
    <h1>📞 التواصل</h1>
    <div class="grid">
      <div class="tile">
        <h3>قنوات عامة</h3>
        <a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">✈️ تيليجرام</a>
        <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">🟢 واتساب</a>
      </div>
      <div class="tile">
        <h3>حجز سريع</h3>
        <a class="btn gold" href="/book">📅 افتح نموذج الحجز</a>
      </div>
    </div>
    """
    return shell("التواصل", html)

# ===== دراسة الحالة (مختصرة هنا – تبقى موسعة لديك) =====
def score_true(data, keys): return sum(1 for k in keys if data.get(k) is not None)

FORM_HTML = """
<h1>📝 دراسة الحالة</h1>
<div class="note">يساعدك هذا القسم على ترتيب الأعراض لتوجيه الخطة الأولية.</div>
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
      <label class="chk"><input type="checkbox" name="obsessions"> أفكار ملحّة</label>
      <label class="chk"><input type="checkbox" name="compulsions"> أفعال قهرية</label>
      <label class="chk"><input type="checkbox" name="flashbacks"> استرجاعات</label>
      <label class="chk"><input type="checkbox" name="hypervigilance"> يقظة مفرطة</label>
    </div>
    <div class="tile"><h3>مواد</h3>
      <label class="chk"><input type="checkbox" name="craving"> اشتهاء</label>
      <label class="chk"><input type="checkbox" name="withdrawal"> انسحاب</label>
      <label class="chk"><input type="checkbox" name="use_harm"> استخدام رغم الضرر</label>
    </div>
  </div>
  <div class="tile" style="margin-top:10px">
    <label>ملاحظاتك<textarea name="notes" rows="4"></textarea></label>
  </div>
  <button class="btn gold" type="submit">عرض الترشيحات</button>
</form>
"""

def build_recommendations(data):
    picks, go_cbt, go_add = [], [], []
    dep = score_true(data, ["low_mood","anhedonia","fatigue","sleep_issue","appetite_change"])
    if dep >= 3:
        picks.append(("اضطراب اكتئابي", "عدة أعراض أساسية للمزاج", min(100, dep*15)))
        go_cbt += ["تنشيط سلوكي","سجل الأفكار","نظافة النوم"]
    anx = score_true(data, ["worry","tension"])
    if anx >= 2: 
        picks.append(("قلق معمم", "قلق وتوتر", 75)); go_cbt += ["تنفس 4-4-6","تعرّض تدريجي"]
    if data.get("panic_attacks"): 
        picks.append(("نوبات هلع", "نوبات مفاجئة", 70)); go_cbt += ["تعرّض داخلي + منع الأمان"]
    if data.get("social_fear"):
        picks.append(("قلق اجتماعي", "خشية تقييم الآخرين", 70)); go_cbt += ["واجبات اجتماعية تصاعدية"]
    if data.get("obsessions") and data.get("compulsions"):
        picks.append(("وسواس قهري", "وساوس مع أفعال قهرية", 80)); go_cbt += ["ERP"]
    if score_true(data, ["flashbacks","hypervigilance"]) >= 2:
        picks.append(("آثار صدمة", "استرجاعات ويقظة", 70)); go_cbt += ["تأريض 5-4-3-2-1"]
    if score_true(data, ["craving","withdrawal","use_harm"]) >= 2:
        picks.append(("تعاطي مواد", "اشتهاء/انسحاب/ضرر", 80)); go_add += ["generic"]
    return picks, sorted(set(go_cbt)), sorted(set(go_add))

def render_results(picks, go_cbt, go_add, notes):
    items = "".join([f"<li><b>{t}</b> — {w} <small>(درجة: {s:.0f})</small></li>" for (t,w,s) in picks]) or "<li>لا توجد مؤشرات كافية.</li>"
    cbt_block = ("<h3>🔧 أدوات CBT المقترحة</h3><ul>" + "".join(f"<li>{x}</li>" for x in go_cbt) +
                 "</ul><a class='btn' href='/cbt'>انتقل إلى CBT</a>") if go_cbt else ""
    add_block = "<h3>🚭 برنامج الإدمان</h3><a class='btn alt' href='/addiction'>افتح برنامج الإدمان</a>" if go_add else ""
    note_html = f"<h3>ملاحظاتك</h3><div class='tile'>{notes}</div>" if notes else ""
    booking = "<h3>📅 احجز جلسة الآن</h3><a class='btn gold' href='/book'>نموذج الحجز</a>"
    return "<h1>📌 ترشيحات أولية</h1><ul style='line-height:1.9'>" + items + "</ul>" + cbt_block + add_block + note_html + booking

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET": return shell("دراسة الحالة", FORM_HTML)
    data = {k: v for k, v in request.form.items()}
    picks, go_cbt, go_add = build_recommendations(data)
    notes = (request.form.get("notes") or "").strip()
    return shell("نتيجة الترشيح", render_results(picks, go_cbt, go_add, notes))

# صحة الخدمة
@app.get("/health")
def health():
    return {"status":"ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
