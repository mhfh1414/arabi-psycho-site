 # -*- coding: utf-8 -*-
"""
عربي سايكو — ملف واحد (Purple × Gold, Black Border)
v8.1 production / single-file Flask

الصفحات:
    /            الرئيسية
    /case        دراسة الحالة (DSM-style + إدمان)
    /cbt         العلاج السلوكي المعرفي + مولّد الجداول
    /tests       اختبارات سريعة (قلق / اكتئاب / ثقة / غضب / إدمان)
    /pharm       دليل الأدوية النفسية (تثقيف فقط)
    /health      Ping جاهزية

⚠ مهم:
- هذا مو تشخيص طبي، ولا وصفة دواء.
- لا تبدأ/توقف دواء بدون إشراف طبي/صيدلي مختص.
- أي أفكار انتحار/إيذاء = طارئ. لازم دعم بشري مباشر الآن مو بعدين.
"""

import os, json
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# ======================== إعدادات عامة ========================

BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO  = os.environ.get(
    "LOGO_URL",
    "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg"
)

TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696")
WA_BASE = WA_URL.split("?")[0]

PSYCHO_WA = os.environ.get("PSYCHOLOGIST_WA", "https://wa.me/966530565696")
PSYCH_WA  = os.environ.get("PSYCHIATRIST_WA", "https://wa.me/966530565696")
SOCIAL_WA = os.environ.get("SOCIAL_WORKER_WA", "https://wa.me/966530565696")

CACHE_BUST = os.environ.get("CACHE_BUST", datetime.utcnow().strftime("%Y%m%d%H%M%S"))
SLOGAN = "«نراك بعين الاحترام، ونسير معك بخطوات عملية.»"


# ================== القسم العام للصفحة /consult ==================
CONSULTATIONS_FILE = "consultations.json"
CONSULT_PAGE_HTML = ""
# shell(...)
<!doctype html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>الاستشارات النفسية - عربي سايكو</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #f5f3ff;
            margin: 0;
            padding: 0;
            direction: rtl;
            text-align: right;
        }
        .page {
            max-width: 720px;
            margin: 24px auto;
            background: #ffffff;
            border-radius: 16px;
            border: 2px solid #4b0082;
            box-shadow: 0 8px 20px rgba(0,0,0,0.06);
            padding: 24px 20px 28px;
        }
        h1 {
            margin-top: 0;
            font-size: 1.5rem;
            color: #4b0082;
        }
        p.lead {
            margin-top: 4px;
            margin-bottom: 16px;
            color: #444;
            font-size: 0.95rem;
        }
        .alert {
            padding: 10px 12px;
            border-radius: 10px;
            margin-bottom: 14px;
            font-size: 0.9rem;
        }
        .alert-ok {
            background: #ecfdf3;
            border: 1px solid #16a34a;
            color: #166534;
        }
        .alert-note {
            background: #eff6ff;
            border: 1px solid #3b82f6;
            color: #1d4ed8;
        }
        label {
            display: block;
            margin-bottom: 6px;
            font-size: 0.9rem;
            font-weight: 600;
            color: #111827;
        }
        input[type="text"],
        input[type="email"],
        input[type="number"],
        select,
        textarea {
            width: 100%;
            box-sizing: border-box;
            padding: 8px 10px;
            border-radius: 10px;
            border: 1px solid #d4d4d8;
            margin-bottom: 12px;
            font-size: 0.9rem;
        }
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        .hint {
            font-size: 0.8rem;
            color: #6b7280;
            margin-top: -6px;
            margin-bottom: 10px;
        }
        .row {
            display: flex;
            gap: 10px;
        }
        .row > div {
            flex: 1;
        }
        .checkbox-line {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
            font-size: 0.85rem;
        }
        .checkbox-line input {
            width: 16px;
            height: 16px;
        }
        button {
            width: 100%;
            padding: 10px 14px;
            border-radius: 999px;
            border: none;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            background: linear-gradient(135deg, #4b0082, #facc15);
            color: white;
        }
        button:active {
            transform: translateY(1px);
        }
        .footer-note {
            margin-top: 14px;
            font-size: 0.78rem;
            color: #6b7280;
            text-align: center;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="page">
        <h1>طلب استشارة نفسية</h1>
        <p class="lead">
            أرسل استشارتك بشكل سري، وسيتم الاطلاع عليها من قبل مختص نفسي.  
            هذه الخدمة للتوجيه النفسي العام وليست بديلاً عن مراجعة الطبيب أو الطوارئ في الحالات الحرجة.
        </p>

        <div class="alert alert-note">
            ⚠️ إذا كانت لديك أفكار انتحار أو نية لإيذاء نفسك أو الآخرين: هذه حالة طارئة،  
            تواصل فورًا مع الطوارئ أو أقرب مستشفى ولا تنتظر الرد على الاستشارة.
        </div>

        {% if success_message %}
        <div class="alert alert-ok">
            {{ success_message }}
        </div>
        {% endif %}

        <form method="post" action="/consult">
            <div class="row">
                <div>
                    <label for="name">الاسم (اختياري)</label>
                    <input id="name" name="name" type="text" placeholder="يمكنك كتابة اسم مستعار">
                </div>
                <div>
                    <label for="age">العمر</label>
                    <input id="age" name="age" type="number" min="8" max="100" placeholder="مثال: 28">
                </div>
            </div>

            <label for="gender">الجنس</label>
            <select id="gender" name="gender">
                <option value="">اختر...</option>
                <option value="ذكر">ذكر</option>
                <option value="أنثى">أنثى</option>
                <option value="أفضل عدم التحديد">أفضل عدم التحديد</option>
            </select>

            <label for="contact">وسيلة التواصل (واتساب أو إيميل)</label>
            <input id="contact" name="contact" type="text" placeholder="مثال: 05XXXXXXXX أو name@email.com">
            <div class="hint">تُستخدم فقط للرد على استشارتك، ولن تُشارك مع أي جهة أخرى.</div>

            <label for="topic">موضوع الاستشارة</label>
            <select id="topic" name="topic">
                <option value="">اختر أقرب موضوع</option>
                <option value="قلق وتوتر">قلق وتوتر</option>
                <option value="اكتئاب وحزن">اكتئاب وحزن</option>
                <option value="مشكلات زوجية / أسرية">مشكلات زوجية / أسرية</option>
                <option value="تربية الأبناء">تربية الأبناء</option>
                <option value="إدمان مواد / سلوكيات">إدمان مواد / سلوكيات</option>
                <option value="ثقة بالنفس / تقدير ذات">ثقة بالنفس / تقدير ذات</option>
                <option value="أعراض ذهانية / غريبة">أعراض ذهانية / غريبة</option>
                <option value="شيء آخر">شيء آخر</option>
            </select>

            <label for="message">وصف مشكلتك بالتفصيل</label>
            <textarea id="message" name="message" placeholder="اكتب ما تعاني منه، منذ متى، وما الذي يزيد الأعراض أو يخففها..."></textarea>

            <div class="checkbox-line">
                <input id="consent" name="consent" type="checkbox" value="yes" required>
                <label for="consent">أوافق أن هذه الاستشارة للتوجيه النفسي العام وليست تشخيصًا طبيًا أو وصفًا دوائيًا.</label>
            </div>

            <button type="submit">إرسال الاستشارة</button>

            <div class="footer-note">
                🛡️ خصوصيتك أولوية. يتم التعامل مع الاستشارات بسرية قدر الإمكان،  
                لكن لا تُرسل معلومات هوية حساسة جدًا (مثل أرقام هويات، حسابات بنكية، إلخ).
            </div>
        </form>
    </div>
</body>
</html>
"""

def save_consultation(data: dict):
    """حفظ الاستشارة في ملف JSON بسيط."""
    try:
        with open(CONSULTATIONS_FILE, "r", encoding="utf-8") as f:
            all_data = json.load(f)
            if not isinstance(all_data, list):
                all_data = []
    except Exception:
        all_data = []

    all_data.append(data)

    with open(CONSULTATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

@app.route("/consult", methods=["GET", "POST"])
def consult_page():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        contact = request.form.get("contact", "").strip()
        topic = request.form.get("topic", "").strip()
        message = request.form.get("message", "").strip()
        consent = True if request.form.get("consent") == "yes" else False

        # بيانات للاستشارة
        consult_data = {
            "name": name or "بدون اسم",
            "age": age,
            "gender": gender,
            "contact": contact,
            "topic": topic,
            "message": message,
            "consent": consent,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        # حفظ في ملف JSON
        save_consultation(consult_data)

        success_message = "🌿 تم استلام استشارتك بنجاح. سيتم الاطلاع عليها والرد عليك قدر المستطاع في أقرب وقت."
        return render_template_string(CONSULT_PAGE_HTML, success_message=success_message)

    # GET
    return render_template_string(CONSULT_PAGE_HTML, success_message=None)

# ================== نهاية قسم الاستشارات ==================

def shell(title, content, active="home"):
    base_html = r"""
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>[[TITLE]]</title>
<link rel="icon" href="[[LOGO]]"/>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>
<meta http-equiv="Pragma" content="no-cache"/>
<meta http-equiv="Expires" content="0"/>

<style>
:root{
  --p:#4B0082;
  --p-dark:#3a0d72;
  --g:#FFD700;
  --bg:#f8f6ff;
  --ink:#2b1a4c;
  --line:#000000;
  --soft-shadow:0 10px 24px rgba(0,0,0,.06);
  --radius-xl:16px;
  --radius-md:12px;
  --radius-sm:10px;
  --card-border:#eee;
  --section-bg:#fff;
  --note-bg:#fff7d1;
  --note-border:#e5c100;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  background:var(--bg);
  font-family:"Tajawal","Segoe UI",system-ui,sans-serif;
  color:var(--ink);
  font-size:16.5px;
  line-height:1.7;
  direction:rtl;
  text-align:right;
}
.layout{
  display:grid;
  grid-template-columns:300px 1fr;
  min-height:100vh;
  border-left:1px solid var(--line);
}
.side{
  background:linear-gradient(180deg,var(--p),var(--p-dark));
  color:#fff;
  padding:18px;
  position:sticky;
  top:0;
  height:100vh;
  display:flex;
  flex-direction:column;
  border-left:1px solid #000;
  border-right:1px solid #000;
}
.logo{
  display:flex;
  align-items:center;
  gap:10px;
  margin-bottom:18px;
  border:1px solid rgba(0,0,0,.4);
  background:rgba(0,0,0,.15);
  border-radius:var(--radius-md);
  padding:10px;
  box-shadow:0 4px 12px rgba(0,0,0,.4);
}
.logo img{
  width:52px;
  height:52px;
  border-radius:14px;
  box-shadow:0 2px 8px rgba(0,0,0,.6);
  background:#fff;
  object-fit:cover;
  border:2px solid var(--g);
}
.brand{
  font-weight:900;
  letter-spacing:.3px;
  font-size:22px;
  line-height:1.3;
  color:#fff;
  text-shadow:0 2px 4px rgba(0,0,0,.7);
}
.brand-handle{
  font-size:.8rem;
  font-weight:700;
  color:var(--g);
  background:rgba(0,0,0,.35);
  display:inline-block;
  padding:2px 8px;
  border-radius:999px;
  border:1px solid #000;
  box-shadow:0 2px 4px rgba(0,0,0,.7);
}
.side-slogan{
  font-size:.9rem;
  font-weight:500;
  color:#fff;
  margin-top:6px;
  line-height:1.6;
  text-shadow:0 2px 4px rgba(0,0,0,.6);
}
.badge{
  display:inline-block;
  background:var(--g);
  color:#4b0082;
  border-radius:999px;
  padding:2px 10px;
  font-weight:900;
  font-size:.8rem;
  margin-top:8px;
  border:1px solid #000;
  box-shadow:0 2px 4px rgba(0,0,0,.6);
}
.nav{
  margin-top:20px;
  padding-top:12px;
  border-top:1px solid rgba(255,255,255,.4);
  border-bottom:1px solid rgba(0,0,0,.8);
}
.nav a{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  color:#fff;
  text-decoration:none;
  background:rgba(0,0,0,.25);
  border-radius:var(--radius-md);
  margin:6px 0;
  padding:10px 12px;
  font-weight:700;
  opacity:.9;
  border:1px solid #000;
  box-shadow:0 4px 12px rgba(0,0,0,.6);
  font-size:15px;
  line-height:1.4;
}
.nav a small{
  font-size:.7rem;
  color:var(--g);
  font-weight:800;
}
.nav a.active{
  background:rgba(255,215,0,.15);
  outline:2px solid var(--g);
  color:#fff;
}
.nav a:hover{
  opacity:1;
  background:rgba(0,0,0,.4);
}
.ref-box{
  margin-top:auto;
  background:rgba(0,0,0,.2);
  border:1px solid #000;
  border-radius:var(--radius-md);
  box-shadow:0 4px 12px rgba(0,0,0,.6);
  padding:12px;
  font-size:.9rem;
  line-height:1.6;
  color:#fff;
}
.ref-box h4{
  margin:0 0 8px;
  color:var(--g);
  font-size:1rem;
  font-weight:800;
  text-shadow:0 2px 4px rgba(0,0,0,.8);
  display:flex;
  align-items:center;
  gap:6px;
}
.ref-links{
  display:flex;
  flex-direction:column;
  gap:8px;
}
.ref-links a{
  display:block;
  background:#000;
  border-radius:var(--radius-md);
  text-decoration:none;
  font-weight:800;
  border:1px solid var(--g);
  box-shadow:0 4px 10px rgba(0,0,0,.7);
  padding:8px 10px;
  font-size:.8rem;
  line-height:1.5;
  color:#fff;
}
.ref-links a span{
  display:block;
  color:var(--g);
  font-size:.7rem;
  font-weight:700;
}
.content{
  padding:26px;
  background:var(--bg);
  border-right:1px solid var(--line);
}
.card{
  background:var(--section-bg);
  border:2px solid #000;
  border-radius:var(--radius-xl);
  padding:22px;
  box-shadow:var(--soft-shadow);
  position:relative;
}
.card + .card{
  margin-top:18px;
}
.grid{
  display:grid;
  gap:14px;
  grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
}
.tile{
  background:#fff;
  border:2px solid #000;
  border-radius:var(--radius-md);
  padding:14px;
  box-shadow:0 6px 12px rgba(0,0,0,.04);
  position:relative;
}
.tile h3{
  margin-top:0;
}
h1{
  font-weight:900;
  font-size:28px;
  line-height:1.4;
  color:var(--p);
  text-shadow:0 2px 4px rgba(0,0,0,.06);
  margin-top:0;
}
h2{
  font-weight:800;
  margin:.2rem 0 .6rem;
  font-size:20px;
  color:var(--p);
}
h3{
  font-weight:800;
  margin:.2rem 0 .6rem;
  font-size:17px;
  color:var(--p);
}
.small{
  font-size:.95rem;
  opacity:.9;
  line-height:1.7;
  color:var(--ink);
}
.note{
  background:var(--note-bg);
  border:2px dashed var(--note-border);
  border-radius:var(--radius-md);
  padding:10px 12px;
  margin:10px 0;
  font-size:.9rem;
  line-height:1.6;
  font-weight:600;
  color:#5c4a00;
  box-shadow:0 4px 10px rgba(0,0,0,.05);
}
.btn{
  display:inline-block;
  background:var(--p);
  color:#fff;
  text-decoration:none;
  padding:11px 16px;
  border-radius:var(--radius-md);
  font-weight:800;
  cursor:pointer;
  border:2px solid #000;
  box-shadow:0 4px 12px rgba(0,0,0,.25);
  font-size:.9rem;
  line-height:1.4;
  min-width:fit-content;
  text-align:center;
}
.btn.alt{
  background:#5b22a6;
}
.btn.gold{
  background:var(--g);
  color:#4b0082;
}
.btn.wa{
  background:#25D366;
}
.btn.tg{
  background:#229ED9;
}
.row{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  align-items:flex-start;
}
.badge2{
  display:inline-block;
  border:2px solid #000;
  background:#fafafa;
  padding:6px 10px;
  border-radius:999px;
  margin:4px 4px 0 0;
  font-weight:700;
  font-size:.8rem;
  line-height:1.4;
  color:#222;
  box-shadow:0 4px 10px rgba(0,0,0,.04);
}
.badge2.plan{
  cursor:pointer;
  user-select:none;
  border:2px solid var(--g);
  background:#fffdf2;
  color:#000;
  box-shadow:0 4px 10px rgba(255,215,0,.35);
}
.table{
  width:100%;
  border-collapse:collapse;
  font-size:.9rem;
}
.table th,
.table td{
  border:1px solid #000;
  padding:8px;
  text-align:center;
  vertical-align:top;
  line-height:1.5;
  min-width:60px;
  background:#fff;
}
.table thead th{
  background:#fafafa;
  font-weight:700;
  color:#2b1a4c;
}
.header-result{
  display:flex;
  align-items:center;
  gap:12px;
  margin-bottom:10px;
  flex-wrap:wrap;
  border-bottom:2px solid var(--line);
  padding-bottom:10px;
}
.header-result img{
  width:48px;
  height:48px;
  border-radius:12px;
  background:#fff;
  border:2px solid var(--g);
  box-shadow:0 4px 12px rgba(0,0,0,.4);
  object-fit:cover;
}
.header-brand-wrap{
  display:flex;
  flex-direction:column;
  gap:2px;
  line-height:1.4;
}
.header-brand-title{
  font-weight:900;
  font-size:22px;
  color:var(--p);
  text-shadow:0 2px 4px rgba(0,0,0,.06);
}
.header-brand-sub{
  font-size:.8rem;
  color:#444;
  font-weight:600;
}
.divider{
  width:100%;
  border-top:2px solid var(--line);
  margin:12px 0;
}
label.badge2 input[type=checkbox]{
  margin-left:6px;
  transform:scale(1.2);
}
input, select, textarea{
  width:100%;
  border:2px solid #000;
  border-radius:var(--radius-md);
  padding:10px;
  font-family:inherit;
  font-size:1rem;
  line-height:1.5;
  color:#000;
  background:#fff;
  box-shadow:0 4px 10px rgba(0,0,0,.03);
}
#err{
  position:fixed;
  inset:10px 10px auto 10px;
  background:#fff5f5;
  border:2px solid #ff4d4d;
  color:#7a1f1f;
  border-radius:var(--radius-md);
  padding:10px;
  z-index:9999;
  display:none;
  font-size:.8rem;
  line-height:1.5;
  box-shadow:0 8px 18px rgba(0,0,0,.2);
}
.footer{
  color:#fff;
  background:var(--p-dark);
  text-align:center;
  padding:16px;
  border-top:2px solid #000;
  border-bottom:2px solid #000;
  font-size:.8rem;
  font-weight:600;
  text-shadow:0 2px 4px rgba(0,0,0,.7);
}
@media print {
  @page { size: A4; margin: 16mm 14mm; }
  .side,
  .footer,
  .screen-only,
  #err { display:none !important; }
  body {
    background:#fff;
    font-size:18px;
    line-height:1.8;
  }
  .layout{
    grid-template-columns:1fr;
    border:none;
  }
  .content{
    padding:0 !important;
    background:#fff;
    border:none;
  }
  .card{
    box-shadow:none;
    border:2px solid #000;
    border-radius:0;
    padding:0;
  }
  h1{font-size:26px}
  h2{font-size:22px}
  h3{font-size:18px}
  .table th,
  .table td{
    font-size:.8rem;
    padding:4px;
  }
}
</style>

<script>
window.__BUILD__="[[BUILD]]";
window.addEventListener('error', function(e){
  var box=document.getElementById('err');
  if(!box) return;
  box.style.display='block';
  box.textContent='JS Error: '+(e.message||'')+' @ '+(e.filename||'')+':'+(e.lineno||'');
});
</script>
</head>

<body>

<div id="err"></div>

<div class="layout">
  <aside class="side">
    <div class="logo">
      <img src="[[LOGO]]" alt="شعار" onerror="this.style.display='none'">
      <div>
        <div class="brand">[[BRAND]]</div>
        <div class="brand-handle">@ArabiPsycho</div>
        <div class="side-slogan">[[SLOGAN]]</div>
        <div class="badge">بنفسجي × ذهبي</div>
      </div>
    </div>

    <nav class="nav">
      <a href="/" class="[[A_HOME]]">
        <span>🏠 الرئيسية</span>
        <small>الصفحة الأولى</small>
      </a>
      <a href="/case" class="[[A_CASE]]">
        <span>📝 دراسة الحالة</span>
        <small>أعراضك وتشخيص مبدئي</small>
      </a>
      <a href="/cbt" class="[[A_CBT]]">
        <span>🧠 CBT</span>
        <small>خطط / جدول يومي</small>
      </a>
      <a href="/tests" class="[[A_TESTS]]">
        <span>📊 اختبارات سريعة</span>
        <small>قلق / اكتئاب / ثقة</small>
      </a>
      <a href="/pharm" class="[[A_PHARM]]">
        <span>💊 دليل الأدوية</span>
        <small>ليش ينصرف؟ التحذيرات؟</small>
      </a>
    </nav>

    <div class="ref-box">
      <h4>📞 دعم مباشر الآن</h4>
      <div class="ref-links">
        <a href="[[PSYCHO_WA]]" target="_blank" rel="noopener">
          👨‍🎓 أخصائي نفسي
          <span>خطة سلوكية/معرفية</span>
        </a>
        <a href="[[PSYCH_WA]]" target="_blank" rel="noopener">
          👨‍⚕️ طبيب نفسي
          <span>تشخيص طبي / أدوية</span>
        </a>
        <a href="[[SOCIAL_WA]]" target="_blank" rel="noopener">
          🤝 أخصائي اجتماعي
          <span>دعم أسري / مواقف حياتية</span>
        </a>
      </div>
    </div>

  </aside>

  <main class="content">
    [[CONTENT]]
  </main>
</div>

<div class="footer">
  <div>© جميع الحقوق محفوظة لـ [[BRAND]] — [[SLOGAN]]</div>
  <div style="margin-top:6px;font-size:.7rem;color:var(--g);">
    تيليجرام الدعم: [[TG_URL]] · واتساب: [[WA_URL]]
  </div>
  <div style="margin-top:4px;font-size:.7rem;">
    الإصدار البنفسجي × الذهبي — BUILD [[BUILD]]
  </div>
</div>

</body>
</html>
"""
    return (
        base_html
        .replace("[[TITLE]]", title)
        .replace("[[LOGO]]", LOGO)
        .replace("[[BRAND]]", BRAND)
        .replace("[[TG_URL]]", TG_URL)
        .replace("[[WA_URL]]", WA_URL)
        .replace("[[SLOGAN]]", SLOGAN)
        .replace("[[BUILD]]", CACHE_BUST)
        .replace("[[PSYCHO_WA]]", PSYCHO_WA)
        .replace("[[PSYCH_WA]]", PSYCH_WA)
        .replace("[[SOCIAL_WA]]", SOCIAL_WA)
        .replace("[[A_HOME]]", "active" if active=="home" else "")
        .replace("[[A_CASE]]", "active" if active=="case" else "")
        .replace("[[A_CBT]]", "active" if active=="cbt" else "")
        .replace("[[A_TESTS]]", "active" if active=="tests" else "")
        .replace("[[A_PHARM]]", "active" if active=="pharm" else "")
        .replace("[[CONTENT]]", content)
    )


# ======================== منطق دراسة الحالة ========================

def _cnt(flags, *keys):
    return sum(1 for k in keys if flags.get(k))

def preliminary_picks(flags):
    picks = []

    dep_core = _cnt(flags, "low_mood", "anhedonia")
    dep_more = _cnt(flags,
        "fatigue", "sleep_issue", "appetite_change",
        "worthlessness", "poor_concentration",
        "psychomotor", "hopeless", "somatic_pain"
    )
    if dep_core >= 1 and dep_more >= 2:
        picks.append((
            "كتلة اكتئابية / مزاج منخفض",
            "أعراض مزاجية متعددة (طاقة/نوم/تركيز/ذنب..) قد تؤثر على حياتك اليومية",
            "درجة 70"
        ))

    if _cnt(flags, "worry", "tension", "restlessness", "irritability",
             "mind_blank", "sleep_anxiety", "concentration_anxiety") >= 3:
        picks.append((
            "قلق معمّم / توتر مستمر",
            "قلق زائد صعب التحكم مع توتر جسدي أو صعوبة نوم أو تشوش التركيز",
            "درجة 65"
        ))

    if flags.get("panic_attacks") or flags.get("panic_fear"):
        picks.append((
            "نوبات هلع",
            "نوبات مفاجئة قوية مع خوف من تكرارها أو تجنّب أماكن",
            "درجة 70"
        ))
    if flags.get("agoraphobia") or flags.get("specific_phobia"):
        picks.append((
            "رُهاب/رهبة مواقف",
            "خوف محدد (أماكن/مواقف/أشياء) مع تجنّب وطلب أمان",
            "درجة 65"
        ))
    if flags.get("social_fear"):
        picks.append((
            "قلق اجتماعي",
            "خشية التقييم من الآخرين/الإحراج مع تجنّب المواقف الاجتماعية",
            "درجة 65"
        ))

    if flags.get("obsessions") and flags.get("compulsions"):
        picks.append((
            "وسواس قهري (OCD)",
            "وساوس ملحّة + أفعال قهرية (غسل/تفقد/ترتيب/طمأنة...)",
            "درجة 80"
        ))

    if _cnt(flags, "flashbacks", "hypervigilance", "startle",
             "numbing", "trauma_avoid", "guilt_trauma") >= 2:
        picks.append((
            "آثار صدمة / يقظة مفرطة",
            "استرجاعات/كوابيس/توتر شديد/تجنّب مرتبط بحدث مؤلم",
            "درجة 70"
        ))

    if _cnt(flags, "insomnia", "hypersomnia", "nightmares", "irregular_sleep") >= 1:
        picks.append((
            "صعوبات نوم",
            "مشاكل بدء/استمرار النوم أو نوم زائد/كوابيس",
            "درجة 55"
        ))

    if _cnt(flags, "adhd_inattention", "adhd_hyper", "disorganization", "time_blindness") >= 2:
        picks.append((
            "سمات تشتت/اندفاع (ADHD سمات)",
            "تشتت/نسيان/اندفاع/ضعف التنظيم ممكن يأثر على العمل أو الدراسة",
            "درجة 60"
        ))

    if _cnt(flags, "elevated_mood", "decreased_sleep_need", "grandiosity",
             "racing_thoughts", "pressured_speech", "risk_spending") >= 3:
        picks.append((
            "سمات مزاج مرتفع / اندفاع عالي",
            "طاقة عالية جدًا + نوم قليل + سلوك متهور ممكن يشير لسمات هوس/ثنائي القطب",
            "درجة 70"
        ))

    if _cnt(flags, "hallucinations", "delusions",
             "disorganized_speech", "negative_symptoms",
             "catatonia") >= 2 and flags.get("decline_function"):
        picks.append((
            "سمات ذهانية / فصامية",
            "وجود هلوسات/أوهام/تفكك تفكير مع تأثير واضح على الأداء اليومي",
            "درجة 80"
        ))

    if _cnt(flags, "binge_eating", "restrict_eating", "body_image", "purging") >= 2:
        picks.append((
            "صعوبات أكل/صورة الجسد",
            "نوبات أكل أو تقييد أو قلق عالي حول الجسم/الوزن",
            "درجة 60"
        ))

    if _cnt(flags, "craving", "withdrawal", "use_harm",
             "loss_control", "relapse_history") >= 2:
        picks.append((
            "تعاطي مواد / سلوك إدماني",
            "اشتهاء قوي، انسحاب، أو استمرار رغم الضرر",
            "درجة 80"
        ))

    if _cnt(flags, "emotion_instability", "impulsivity", "anger_issues",
             "perfectionism", "dependence", "social_withdrawal") >= 3:
        picks.append((
            "تنظيم عاطفي / غضب / علاقات",
            "تقلب عاطفي، اندفاع، انفجارات غضب أو تمسك زائد يضغط العلاقات",
            "درجة 60"
        ))

    if flags.get("self_conf_low"):
        picks.append((
            "ثقة بالنفس منخفضة",
            "نظرة ذاتية سلبية / تردد عالي / إحساس بعدم الكفاية",
            "درجة 50"
        ))

    if _cnt(flags, "asd_social", "sensory", "rigidity") >= 2:
        picks.append((
            "سمات تواصل/حسّية (طيف توحد)",
            "صعوبة قراءة الإشارات الاجتماعية، حساسية حسّية، أو تمسّك روتيني عالي",
            "درجة 55"
        ))

    if flags.get("suicidal"):
        picks.insert(0, (
            "تنبيه أمان",
            "وجود أفكار إيذاء أو انتحار — نوصي بالتواصل الفوري مع مختص أو دعم طارئ.",
            "درجة 99"
        ))

    return picks


def suggest_plans(flags):
    sug = []

    dep_core = _cnt(flags, "low_mood", "anhedonia")
    dep_more = _cnt(flags,
        "fatigue", "sleep_issue", "appetite_change",
        "worthlessness", "poor_concentration",
        "psychomotor", "hopeless", "somatic_pain"
    )
    if dep_core >= 1 and dep_more >= 2:
        sug += ["ba", "thought_record", "sleep_hygiene", "problem_solving"]

    if _cnt(flags, "worry", "tension", "restlessness", "irritability",
             "mind_blank", "sleep_anxiety", "concentration_anxiety") >= 3:
        sug += ["worry_time", "mindfulness", "problem_solving"]

    if flags.get("panic_attacks") or flags.get("panic_fear"):
        sug += ["interoceptive_exposure", "safety_behaviors"]

    if flags.get("agoraphobia") or flags.get("specific_phobia"):
        sug += ["graded_exposure"]

    if flags.get("social_fear"):
        sug += ["graded_exposure", "social_skills", "thought_record", "self_confidence"]

    if flags.get("obsessions") and flags.get("compulsions"):
        sug += ["ocd_erp", "safety_behaviors", "mindfulness"]

    if _cnt(flags, "flashbacks", "hypervigilance", "startle",
             "numbing", "trauma_avoid", "guilt_trauma") >= 2:
        sug += ["ptsd_grounding", "mindfulness", "sleep_hygiene"]

    if _cnt(flags, "insomnia", "hypersomnia", "nightmares", "irregular_sleep") >= 1:
        sug += ["sleep_hygiene", "mindfulness"]

    if _cnt(flags, "adhd_inattention", "adhd_hyper", "disorganization", "time_blindness") >= 2:
        sug += ["problem_solving", "ba"]

    if _cnt(flags, "elevated_mood", "decreased_sleep_need", "grandiosity",
             "racing_thoughts", "pressured_speech", "risk_spending") >= 3:
        sug += ["bipolar_routine", "sleep_hygiene"]

    if _cnt(flags, "craving", "withdrawal", "use_harm",
             "loss_control", "relapse_history") >= 2:
        sug += ["relapse_prevention", "problem_solving", "mindfulness"]

    if _cnt(flags, "emotion_instability", "impulsivity", "anger_issues",
             "perfectionism", "dependence", "social_withdrawal") >= 2:
        sug += ["anger_management", "mindfulness", "problem_solving", "self_confidence"]

    if _cnt(flags, "asd_social", "sensory", "rigidity") >= 2:
        sug += ["social_skills", "self_confidence", "problem_solving"]

    final = []
    seen = set()
    for k in sug:
        if k not in seen:
            seen.add(k)
            final.append(k)
    return final[:10]


def build_case_result_html(picks, plan_keys):
    PLAN_TITLES = {
        "ba": "BA — تنشيط سلوكي",
        "thought_record": "TR — سجل أفكار",
        "sleep_hygiene": "SH — نظافة النوم",
        "interoceptive_exposure": "IE — تعرّض داخلي (هلع)",
        "graded_exposure": "GE — تعرّض تدرّجي (رهاب/اجتماعي)",
        "ocd_erp": "ERP — وسواس قهري",
        "ptsd_grounding": "PTSD — تأريض/تنظيم",
        "problem_solving": "PS — حلّ المشكلات",
        "worry_time": "WT — وقت القلق",
        "mindfulness": "MB — يقظة ذهنية",
        "behavioral_experiments": "BE — تجارب سلوكية",
        "safety_behaviors": "SA — إيقاف طمأنة قهرية",
        "bipolar_routine": "IPSRT — روتين ثنائي القطب",
        "relapse_prevention": "RP — منع الانتكاس (إدمان)",
        "social_skills": "SS — مهارات اجتماعية",
        "anger_management": "AM — إدارة الغضب",
        "self_confidence": "SC — تعزيز الثقة"
    }

    if picks:
        lis = "".join([
            f"<li><b>{t}</b> — {desc} <span class='small'>({score})</span></li>"
            for (t, desc, score) in picks
        ])
    else:
        lis = "<li>لا توجد مؤشرات كافية حالياً. استمر بالملاحظة الذاتية 👀</li>"

    if plan_keys:
        cbt_badges = "".join([
            f"<span class='badge2 plan' data-key='{k}'>🔧 {PLAN_TITLES.get(k,k)}</span>"
            for k in plan_keys
        ])
    else:
        cbt_badges = "<span class='small'>لا توجد توصيات محددة الآن.</span>"

    js_block = f"""
<script>
  function saveJSON(){{
    const data={{
      items:[...document.querySelectorAll('#diag-items li')].map(li=>li.innerText),
      cbt:[...document.querySelectorAll('.badge2.plan')].map(b=>b.dataset.key),
      created_at:new Date().toISOString(),
      build: window.__BUILD__
    }};
    const a=document.createElement('a');
    a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}}));
    a.download='case_result.json';
    a.click();
    URL.revokeObjectURL(a.href);
  }}

  function buildShare(){{
    const items=[...document.querySelectorAll('#diag-items li')].map(li=>'- '+li.innerText).join('\\n');
    const msg='نتيجة دراسة الحالة — {BRAND}\\n\\n'+items+'\\n'+location.origin+'/case';
    const text=encodeURIComponent(msg);
    document.getElementById('share-wa').href='{WA_BASE}'+'?text='+text;
    document.getElementById('share-tg').href='https://t.me/share/url?url='+encodeURIComponent(location.origin+'/case')+'&text='+text;
  }}

  function openCBTWithSuggestions(keys){{
    try {{
      localStorage.setItem('cbt_suggested', JSON.stringify(keys||[]));
    }} catch(e){{}}
    const qp = (keys && keys.length) ? ('?suggest='+encodeURIComponent(keys.join(','))) : '';
    location.href = '/cbt'+qp;
  }}

  buildShare();
</script>
"""

    praise_line = (
        "أحسنت 👏 — كل خطوة وعي تقرّبك من التعافي. "
        "هذه ليست تشخيص نهائي طبي، لكنها خريطة أولية تساعدك تبني خطة سلوكية محترمة."
    )

    return f"""
<div class="card">
  <div class="header-result">
    <img src="{LOGO}" alt="logo" onerror="this.style.display='none'">
    <div class="header-brand-wrap">
      <div class="header-brand-title">{BRAND}</div>
      <div class="header-brand-sub">نتيجة دراسة الحالة — ملخص جاهز للطباعة والمشاركة</div>
    </div>
  </div>

  <div class="note">{praise_line}</div>

  <h2>📌 الترشيحات المبدئية</h2>
  <ol id="diag-items" style="line-height:1.95; padding-inline-start:20px">{lis}</ol>

  <div class="divider"></div>

  <h3>🔧 أدوات CBT المقترحة حسب حالتك</h3>
  <div>{cbt_badges}</div>

  <div class="divider"></div>

  <h3>🚀 ماذا بعد؟</h3>
  <div class="small">
    1. اطبع أو خزّن هذه النتائج.<br/>
    2. اضغط "فتح CBT" لتوليد جدول 7 / 10 / 14 يوم بخطوات يومية واضحة.<br/>
    3. إذا حسّيت أنك تحتاج دعم بشري مباشر: تواصل من الأزرار تحت.
  </div>

  <div class="row screen-only" style="margin-top:14px">
    <button class="btn alt" onclick="window.print()">🖨️ طباعة</button>
    <button class="btn" onclick="saveJSON()">💾 تنزيل JSON</button>
    <a class="btn wa" id="share-wa" target="_blank" rel="noopener">🟢 مشاركة واتساب</a>
    <a class="btn tg" id="share-tg" target="_blank" rel="noopener">✈️ مشاركة تيليجرام</a>
    <a class="btn gold" onclick='openCBTWithSuggestions({json.dumps(plan_keys)})'>🧠 فتح CBT (مخصّص لحالتك)</a>
  </div>

  <div class="row screen-only" style="margin-top:16px">
    <a class="btn" href="{PSYCHO_WA}" target="_blank" rel="noopener">👨‍🎓 أخصائي نفسي الآن</a>
    <a class="btn" href="{PSYCH_WA}"  target="_blank" rel="noopener">👨‍⚕️ طبيب نفسي</a>
    <a class="btn" href="{SOCIAL_WA}" target="_blank" rel="noopener">🤝 أخصائي اجتماعي</a>
  </div>

  {js_block}
</div>
"""


# ======================== الصفحة الرئيسية ========================

@app.get("/")
def home():
    content = f"""
<div class="card" style="margin-bottom:18px;">
  <h1>مرحبًا بك في {BRAND}</h1>
  <div class="small">
    هذه مساحة آمنة تساعدك تحلل وضعك بصراحة، بدون حُكم.
    <br/><br/>
    1) 📝 قيّم نفسك في «دراسة الحالة»<br/>
    2) 🧠 نبني لك خطة CBT يومية (7 / 10 / 14 يوم)<br/>
    3) 📊 لو تبغى قياس سريع: «اختبارات نفسية»<br/>
    4) 💊 تشوف أدوية الطب النفسي؟ قسم «دليل الأدوية»<br/>
    5) 🤝 تحتاج إنسان الآن؟ زر واحد يوصلك باختصاصي.
  </div>
  <div class="note">
    "نحن نحترمك. ألمك حقيقي. وبدل ما نقول 'شد حيلك' نعطيك خطة."
  </div>
</div>

<div class="grid">

  <div class="tile">
    <h3>📝 دراسة الحالة (DSM + الإدمان)</h3>
    <p class="small">
      أكثر من 70 عرض (مزاج، قلق، وسواس، صدمة، نوم، تركيز، ثقة، غضب، تعاطي مواد...).
      <br/>بعدها يطلع لك ملخص + توصيات CBT + زر تواصل مع مختص.
    </p>
    <a class="btn gold" href="/case">ابدأ الآن</a>
  </div>

  <div class="tile">
    <h3>🧠 CBT العلاج السلوكي المعرفي</h3>
    <p class="small">
      17 خطة واضحة (تنشيط سلوكي، إدارة الغضب، ثقة بالنفس، نوم، هلع، وسواس...).
      <br/>نولّد لك جدول أيام قابل للطباعة والمشاركة.
    </p>
    <a class="btn" href="/cbt">افتح CBT</a>
  </div>

  <div class="tile">
    <h3>📊 الاختبارات النفسية السريعة</h3>
    <p class="small">
      قلق؟ اكتئاب؟ غضب؟ اندفاع؟ ثقتك بنفسك؟<br/>
      10 أسئلة وتحصل على درجة فورية + ملاحظات.
    </p>
    <a class="btn alt" href="/tests">جرّب اختبار</a>
  </div>

  <div class="tile">
    <h3>💊 دليل الأدوية النفسية</h3>
    <p class="small">
      مضادات اكتئاب، مثبت مزاج، مضاد ذهان، مهدّئات، أدوية الإدمان...
      <br/>ليش يوصفه الدكتور؟ آثار جانبية؟ متى طوارئ؟
    </p>
    <a class="btn" href="/pharm">استعرض الأدوية</a>
  </div>

  <div class="tile">
    <h3>📞 تواصل سريع</h3>
    <p class="small">
      تحتاج تتكلم مع بشر حقيقي؟ نوصلك مباشرة.
    </p>
    <div class="row">
      <a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">✈️ تيليجرام</a>
      <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">🟢 واتساب</a>
    </div>
  </div>

</div>
"""
    return shell("الرئيسية — " + BRAND, content, "home")


# ======================== /case ========================

CASE_FORM_HTML = r"""
<div class="card">
  <h1>📝 دراسة الحالة — (DSM + الإدمان مدمج)</h1>
  <div class="small">
    اختر الأعراض اللي تحس إنها <b>عندك فعلاً</b> بالفترة الحالية.
    بعدها اضغط «عرض النتيجة».
    <br/>مهم: هذا مو تشخيص طبي نهائي. هذا مسار مبدئي يساعدك تبني خطة سلوكية محترمة.
  </div>
  <div class="note">
    ⚠ خصوصيتك: يتم حفظ اختياراتك محليًا في جهازك (localStorage) وليس في السيرفر.
  </div>

  <form method="post" action="/case" oninput="persistCase()">

    <h2>1) معلومات أساسية</h2>
    <div class="grid">
      <div class="tile">
        <label>العمر
          <input name="age" type="number" min="5" max="120" placeholder="28">
        </label>
      </div>
      <div class="tile">
        <label>الحالة الاجتماعية
          <select name="marital">
            <option value="">—</option>
            <option>أعزب/عزباء</option>
            <option>متزوج/ة</option>
            <option>منفصل/ة</option>
            <option>مطلق/ة</option>
            <option>أرمل/أرملة</option>
          </select>
        </label>
      </div>
      <div class="tile">
        <label>العمل / الدراسة
          <input name="work" placeholder="طالب / موظف / باحث عن عمل / غير ذلك">
        </label>
      </div>
    </div>

    <div class="divider"></div>

    <h2>2) الأعراض الحالية (اختر ما ينطبق فعلاً)</h2>

    <div class="grid">

      <div class="tile">
        <h3>🟣 المزاج / الاكتئاب</h3>
        <label class="badge2"><input type="checkbox" name="low_mood"> مزاج منخفض أكثر اليوم</label>
        <label class="badge2"><input type="checkbox" name="anhedonia"> فقدان المتعة بالأشياء</label>
        <label class="badge2"><input type="checkbox" name="hopeless"> إحساس بالتشاؤم / اليأس</label>
        <label class="badge2"><input type="checkbox" name="fatigue"> إرهاق / طاقة منخفضة</label>
        <label class="badge2"><input type="checkbox" name="sleep_issue"> نوم مضطرب أو متقطع</label>
        <label class="badge2"><input type="checkbox" name="appetite_change"> تغيّر واضح بالشّهية / الوزن</label>
        <label class="badge2"><input type="checkbox" name="somatic_pain"> آلام جسدية مرتبطة بالمزاج</label>
        <label class="badge2"><input type="checkbox" name="worthlessness"> شعور بالذنب / عدم القيمة</label>
        <label class="badge2"><input type="checkbox" name="poor_concentration"> تركيز ضعيف / بطء تفكير</label>
        <label class="badge2"><input type="checkbox" name="psychomotor"> تباطؤ أو تهيّج حركي</label>
        <label class="badge2"><input type="checkbox" name="suicidal"> أفكار إيذاء أو انتحار</label>
      </div>

      <div class="tile">
        <h3>🟣 القلق / الهلع / الرهاب</h3>
        <label class="badge2"><input type="checkbox" name="worry"> قلق زائد صعب السيطرة</label>
        <label class="badge2"><input type="checkbox" name="tension"> توتر عضلي / شد جسدي</label>
        <label class="badge2"><input type="checkbox" name="restlessness"> تململ / أرق / عصبية</label>
        <label class="badge2"><input type="checkbox" name="irritability"> سرعة انفعال / عصبية سريعة</label>
        <label class="badge2"><input type="checkbox" name="mind_blank"> فراغ ذهني تحت الضغط</label>
        <label class="badge2"><input type="checkbox" name="sleep_anxiety"> صعوبة نوم بسبب القلق</label>
        <label class="badge2"><input type="checkbox" name="concentration_anxiety"> تشوش تركيز مع القلق</label>
        <label class="badge2"><input type="checkbox" name="panic_attacks"> نوبات هلع متكررة</label>
        <label class="badge2"><input type="checkbox" name="panic_fear"> خوف من تكرار نوبة هلع</label>
        <label class="badge2"><input type="checkbox" name="agoraphobia"> رهبة الأماكن المزدحمة / المفتوحة</label>
        <label class="badge2"><input type="checkbox" name="specific_phobia"> رُهاب محدد (حيوان/قيادة/طيران..)</label>
        <label class="badge2"><input type="checkbox" name="social_fear"> خوف من تقييم الآخرين / إحراج اجتماعي</label>
        <label class="badge2"><input type="checkbox" name="avoidance"> تجنّب مواقف خوفًا من الأعراض</label>
        <label class="badge2"><input type="checkbox" name="safety_behaviors"> أحتاج طمأنة أو مرافقة عشان أهدى</label>
      </div>

      <div class="tile">
        <h3>🟣 وسواس قهري (OCD)</h3>
        <label class="badge2"><input type="checkbox" name="obsessions"> أفكار/صور مُلِحّة ما أقدر أوقفها</label>
        <label class="badge2"><input type="checkbox" name="compulsions"> أفعال قهرية (غسل/تفقد/ترتيب...)</label>
        <label class="badge2"><input type="checkbox" name="contamination"> هوس تلوّث / غسل مفرط</label>
        <label class="badge2"><input type="checkbox" name="checking"> تفقد الأبواب/القفل/الأشياء كثير</label>
        <label class="badge2"><input type="checkbox" name="ordering"> لازم ترتيب/تماثل كامل</label>
        <label class="badge2"><input type="checkbox" name="harm_obs"> وساوس أذى (أخاف أضر نفسي/غيري)</label>
        <label class="badge2"><input type="checkbox" name="scrupulosity"> تدقيق ديني/أخلاقي قهري</label>
      </div>

      <div class="tile">
        <h3>🟣 الصدمة / ما بعد الصدمة</h3>
        <label class="badge2"><input type="checkbox" name="flashbacks"> استرجاعات / كوابيس عن حدث صعب</label>
        <label class="badge2"><input type="checkbox" name="hypervigilance"> يقظة مفرطة / دائمًا على أهبة الاستعداد</label>
        <label class="badge2"><input type="checkbox" name="startle"> فزع مفرط من الأصوات/المفاجآت</label>
        <label class="badge2"><input type="checkbox" name="numbing"> خدر عاطفي / كأني مو موجود</label>
        <label class="badge2"><input type="checkbox" name="trauma_avoid"> أتجنب أي تذكير بالحدث (أماكن/كلام)</label>
        <label class="badge2"><input type="checkbox" name="guilt_trauma"> شعور بالذنب تجاه الحدث</label>
      </div>

      <div class="tile">
        <h3>🟣 النوم</h3>
        <label class="badge2"><input type="checkbox" name="insomnia"> صعوبة بداية/استمرار النوم (أرق)</label>
        <label class="badge2"><input type="checkbox" name="hypersomnia"> نوم مفرط / صعوبة القيام</label>
        <label class="badge2"><input type="checkbox" name="nightmares"> كوابيس متكررة</label>
        <label class="badge2"><input type="checkbox" name="irregular_sleep"> مواعيد نوم فوضوية جدًا</label>
      </div>

      <div class="tile">
        <h3>🟣 تركيز / حركة / تنظيم الوقت</h3>
        <label class="badge2"><input type="checkbox" name="adhd_inattention"> تشتت / نسيان أشياء أساسية</label>
        <label class="badge2"><input type="checkbox" name="adhd_hyper"> فرط حركة / اندفاع / صعوبة الجلوس</label>
        <label class="badge2"><input type="checkbox" name="disorganization"> فوضى تنظيم / تأجيل مزمن</label>
        <label class="badge2"><input type="checkbox" name="time_blindness"> ضياع الإحساس بالوقت / التأخير الدائم</label>
      </div>

      <div class="tile">
        <h3>🟣 مزاج مرتفع / طاقة مفرطة</h3>
        <label class="badge2"><input type="checkbox" name="elevated_mood"> مزاج مرتفع جدًا / تهوّر</label>
        <label class="badge2"><input type="checkbox" name="decreased_sleep_need"> أحتاج نوم قليل جدًا وأحس طبيعي</label>
        <label class="badge2"><input type="checkbox" name="grandiosity"> إحساس بالعظمة / قدرات خارقة</label>
        <label class="badge2"><input type="checkbox" name="racing_thoughts"> أفكار سريعة جدًا / ما ألحقها</label>
        <label class="badge2"><input type="checkbox" name="pressured_speech"> كلام سريع/متدفق جدًا</label>
        <label class="badge2"><input type="checkbox" name="risk_spending"> صرف فلوس/مخاطرة عالية بدون تفكير</label>
      </div>

      <div class="tile">
        <h3>🟣 إدراك/تفكير (ذهاني/فصام)</h3>
        <label class="badge2"><input type="checkbox" name="hallucinations"> هلوسات (أسمع/أشوف شي غير طبيعي)</label>
        <label class="badge2"><input type="checkbox" name="delusions"> أفكار مراقبة / مؤامرة / يقين غريب</label>
        <label class="badge2"><input type="checkbox" name="disorganized_speech"> كلام/تفكير متشتت أو غير مفهوم</label>
        <label class="badge2"><input type="checkbox" name="negative_symptoms"> انسحاب / برود عاطفي</label>
        <label class="badge2"><input type="checkbox" name="catatonia"> تجمّد حركي / سلوك غير متجاوب</label>
        <label class="badge2"><input type="checkbox" name="decline_function"> تدهور واضح بالدراسة/العمل/العلاقات</label>
      </div>

      <div class="tile">
        <h3>🟣 الأكل / صورة الجسد</h3>
        <label class="badge2"><input type="checkbox" name="binge_eating"> نوبات أكل شره / فقدان التحكم</label>
        <label class="badge2"><input type="checkbox" name="restrict_eating"> تقييد قوي / تجويع نفسي</label>
        <label class="badge2"><input type="checkbox" name="body_image"> انشغال قوي بالشكل/الوزن</label>
        <label class="badge2"><input type="checkbox" name="purging"> تطهير/إقياء قهري بعد الأكل</label>
      </div>

      <div class="tile">
        <h3>🟣 تعاطي مواد / إدمان</h3>
        <label class="badge2"><input type="checkbox" name="craving"> اشتهاء قوي / أحتاج أستخدم الآن</label>
        <label class="badge2"><input type="checkbox" name="withdrawal"> انسحاب جسدي/نفسي إذا ما استخدمت</label>
        <label class="badge2"><input type="checkbox" name="use_harm"> أستمر رغم ضرر واضح</label>
        <label class="badge2"><input type="checkbox" name="loss_control"> صعوبة إيقاف / فقدان السيطرة</label>
        <label class="badge2"><input type="checkbox" name="relapse_history"> انتكاسات بعد محاولات الإيقاف</label>
      </div>

      <div class="tile">
        <h3>🟣 تنظيم العاطفة / العلاقات / الغضب</h3>
        <label class="badge2"><input type="checkbox" name="emotion_instability"> تقلب مزاج حاد / مشاعر قوية فجأة</label>
        <label class="badge2"><input type="checkbox" name="impulsivity"> اندفاعية / أتصرف قبل ما أفكر</label>
        <label class="badge2"><input type="checkbox" name="anger_issues"> نوبات غضب / صراخ / انفجار سريع</label>
        <label class="badge2"><input type="checkbox" name="perfectionism"> كمالية تعطلني (كل شيء لازم مثالي)</label>
        <label class="badge2"><input type="checkbox" name="dependence"> تعلق عالي / خوف قوي من الهجر</label>
        <label class="badge2"><input type="checkbox" name="social_withdrawal"> انسحاب اجتماعي / صعوبة تواصل</label>
        <label class="badge2"><input type="checkbox" name="self_conf_low"> ثقة بالنفس منخفضة / جلد ذاتي</label>
      </div>

      <div class="tile">
        <h3>🟣 تواصل / حساسية حسّية</h3>
        <label class="badge2"><input type="checkbox" name="asd_social"> صعوبة قراءة الإشارات الاجتماعية</label>
        <label class="badge2"><input type="checkbox" name="sensory"> حساسية حسّية (أصوات/إضاءة/ملمس)</label>
        <label class="badge2"><input type="checkbox" name="rigidity"> تمسّك عالي بروتين/ترتيب (أتضايق لو تغيّر)</label>
      </div>

    </div>

    <div class="divider"></div>

    <div class="tile" style="margin-top:10px">
      <label>ملاحظاتك (اختياري)
        <textarea name="notes" rows="4" placeholder="أهم التفاصيل / متى بدأت / وش اللي مضايقك أكثر الآن؟"></textarea>
      </label>
    </div>

    <div class="row" style="margin-top:14px">
      <button class="btn gold" type="submit">عرض النتيجة</button>
      <a class="btn" href="/cbt">🧠 فتح CBT الآن</a>
    </div>

  </form>

  <script>
    const KEY='case_state_v81';

    function persistCase(){
      const f=document.querySelector('form[action="/case"]');
      const data={};
      if(!f) return;

      f.querySelectorAll('input[type=checkbox]').forEach(function(ch){
        if(ch.checked) data[ch.name]=true;
      });

      ["age","marital","work","notes"].forEach(function(n){
        const el=f.querySelector('[name="'+n+'"]');
        if(el) data[n]=el.value||'';
      });

      try{
        localStorage.setItem(KEY, JSON.stringify(data));
      }catch(e){}
    }

    (function restore(){
      try{
        const d=JSON.parse(localStorage.getItem(KEY)||'{}');
        Object.keys(d).forEach(function(k){
          const el=document.querySelector('[name="'+k+'"]');
          if(!el) return;
          if(el.type==='checkbox' && d[k]) el.checked=true;
          else if(el.tagName==='INPUT' || el.tagName==='TEXTAREA' || el.tagName==='SELECT'){
            el.value=d[k];
          }
        });
      }catch(e){}
    })();
  </script>

</div>
"""

@app.route("/case", methods=["GET", "POST"])
def case():
    if request.method == "GET":
        return shell("دراسة الحالة — " + BRAND, CASE_FORM_HTML, "case")

    form_data = {k: True for k in request.form.keys()
                 if k not in ("age","marital","work","notes")}
    form_data["age_val"]     = request.form.get("age", "").strip()
    form_data["marital_val"] = request.form.get("marital", "").strip()
    form_data["work_val"]    = request.form.get("work", "").strip()
    _notes                   = request.form.get("notes", "").strip()

    picks = preliminary_picks(form_data)
    plans = suggest_plans(form_data)
    html  = build_case_result_html(picks, plans)
    return shell("نتيجة دراسة الحالة — " + BRAND, html, "case")


# ======================== /cbt ========================

CBT_PAGE_HTML = r"""
<div class="card">

  <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
  <div class="small">
    الهدف: تحويل الأعراض إلى خطوات يومية قابلة للتنفيذ.
    <br/>
    اختَر خطة (أو خطتين مع بعض)، حدّد عدد الأيام (7 / 10 / 14)،
    واضغط "إنشاء الجدول" 👇
  </div>
  <div class="note">
    لو جيت من «دراسة الحالة»، بنوسّط لك الخطط المقترحة بخط ذهبي.
    إذا ما جيت من هناك، عادي؛ اختَر يدوي.
  </div>

  <h2>الخطط المتاحة (17 خطة)</h2>
  <div class="grid" id="plans"></div>

  <div class="divider"></div>

  <h2 style="margin-top:18px">📅 مولّد الجدول اليومي</h2>
  <div class="tile">
    <div class="row">

      <label style="flex:1;min-width:160px;">
        الخطة A:
        <select id="planA"></select>
      </label>

      <label style="flex:1;min-width:160px;">
        الخطة B (اختياري):
        <select id="planB"><option value="">— بدون —</option></select>
      </label>

      <label style="flex:1;min-width:120px;">
        المدة (أيام):
        <select id="daysSelect">
          <option value="7">7</option>
          <option value="10">10</option>
          <option value="14">14</option>
        </select>
      </label>

      <button class="btn gold" onclick="buildChecklist()">إنشاء الجدول</button>
      <button class="btn alt" onclick="window.print()">🖨️ طباعة</button>
      <button class="btn" onclick="saveChecklist()">💾 تنزيل JSON</button>
      <a class="btn wa" id="share-wa" target="_blank" rel="noopener">🟢 واتساب</a>
      <a class="btn tg" id="share-tg" target="_blank" rel="noopener">✈️ تيليجرام</a>

    </div>

    <div id="checklist" style="margin-top:16px"></div>
  </div>

  <div class="divider"></div>

  <h3>هل تحتاج بشري الآن؟</h3>
  <div class="row screen-only">
    <a class="btn" href="[[PSYCHO_WA]]" target="_blank" rel="noopener">👨‍🎓 أخصائي نفسي</a>
    <a class="btn" href="[[PSYCH_WA]]"  target="_blank" rel="noopener">👨‍⚕️ طبيب نفسي</a>
    <a class="btn" href="[[SOCIAL_WA]]" target="_blank" rel="noopener">🤝 أخصائي اجتماعي</a>
  </div>

  <script>
    const PLANS = {
      ba:{
        title:"BA — تنشيط سلوكي",
        steps:[
          "3 نشاطات مُجزية أو ممتعة كل يوم حتى لو المزاج منخفض.",
          "أقيس مزاجي قبل وبعد (0-10) عشان أشوف الفرق.",
          "أرفع صعوبة أو اجتماعية النشاط تدريجيًا خلال الأيام."
        ]
      },
      thought_record:{
        title:"TR — سجل أفكار",
        steps:[
          "موقف → فكرة تلقائية (وش خطر ببالي فورًا؟).",
          "دلائل مع و ضد الفكرة (أشيك الواقع مو الإحساس فقط).",
          "أكتب فكرة بديلة واقعية ومتوازنة وأجرّبها في السلوك."
        ]
      },
      sleep_hygiene:{
        title:"SH — نظافة النوم",
        steps:[
          "أثبت وقت نوم/استيقاظ يومي حتى نهاية الأسبوع.",
          "أوقف الشاشات القوية قبل النوم بـ 60 دقيقة.",
          "أمنع الكافيين والنيكوتين قبل النوم بست ساعات."
        ]
      },
      interoceptive_exposure:{
        title:"IE — تعرّض داخلي (هلع)",
        steps:[
          "أخلق إحساس جسدي يشبه الهلع (تنفّس سريع 30 ثانية) في مكان آمن.",
          "أبقى مع الإحساس وأمنع طقوس الطمأنة القهرية.",
          "أكرر لين عقلي يتعلم إن الإحساس ما يقتلني."
        ]
      },
      graded_exposure:{
        title:"GE — تعرّض تدرّجي (رهاب/اجتماعي)",
        steps:[
          "قائمة مواقف من الأسهل للأصعب (0→100 خوف).",
          "أواجه الموقف من الأقل خوفًا وصعود بدون هروب.",
          "أبقى داخل الموقف إلى أن القلق يطيح ~50٪."
        ]
      },
      ocd_erp:{
        title:"ERP — وسواس قهري",
        steps:[
          "أحدد وسواس محدد + الطقس اللي أسويه عادة.",
          "أعرّض نفسي للمثير بدون تنفيذ الطقس.",
          "أقيس القلق (0-100) وأشوف كيف ينزل مع الاستمرار."
        ]
      },
      ptsd_grounding:{
        title:"PTSD — تأريض/تنظيم",
        steps:[
          "تمرين 5-4-3-2-1 حواس للرجوع للحظة الحالية.",
          "تنفّس بطني بطيء (شهيق4/حجز2/زفير6-8) عشر مرات.",
          "روتين أمان قبل النوم (إضاءة هادية/وقت تهدئة ثابت)."
        ]
      },
      problem_solving:{
        title:"PS — حلّ المشكلات",
        steps:[
          "أكتب المشكلة بصيغة محددة وواضحة.",
          "أجمع حلول بدون حكم ثم أقيّم الواقعي منها.",
          "أختار حل واحد وأطبقه اليوم وأراجع آخر اليوم."
        ]
      },
      worry_time:{
        title:"WT — وقت القلق",
        steps:[
          "إذا جا القلق أكتب الفكرة بدل ما أغرق فيها الآن.",
          "أأجل التفكير فيها لوقت محدد (15 دق مثلًا مساء).",
          "وقت القلق المخصص أراجع القائمة بهدوء ومع قلم."
        ]
      },
      mindfulness:{
        title:"MB — يقظة ذهنية",
        steps:[
          "٥ دقائق ملاحظة تنفّسي بدون حكم.",
          "فحص جسدي بطيء من الرأس للقدم وملاحظة الإحساس.",
          "أذكر نفسي: الفكرة مجرد فكرة مو حقيقة إلزامية."
        ]
      },
      behavioral_experiments:{
        title:"BE — تجارب سلوكية",
        steps:[
          "أكتب الاعتقاد السلبي (مثال: لو قلت رأيي بينرفض).",
          "أجرب خطوة صغيرة ضد الاعتقاد مع شخص آمن.",
          "أقارن النتيجة بالتوقع وأكتب وش تعلمت."
        ]
      },
      safety_behaviors:{
        title:"SA — إيقاف سلوكيات الأمان",
        steps:[
          "أحصر سلوك الأمان (اتصال فوري لطمأنة مثلاً).",
          "أقلله شوي شوي بدل ما أقطعه فجأة.",
          "أراقب: هل خوفي يطيح لحاله حتى بدون الطمأنة؟"
        ]
      },
      bipolar_routine:{
        title:"IPSRT — روتين ثنائي القطب",
        steps:[
          "ثبات أوقات النوم/الأكل/النشاط اليومي.",
          "تدوين مزاج يومي (مرتفع/منخفض/مستقر).",
          "أعرف العلامات المبكرة (صرف مجنون، نوم شبه صفر...)."
        ]
      },
      relapse_prevention:{
        title:"RP — منع الانتكاس (إدمان)",
        steps:[
          "أحدد محفزاتي (أماكن/أشخاص/مزاج).",
          "أبني بدائل فورية وقت الرغبة (أطلع، ماء بارد، أكتب، أكلم دعم).",
          "أجهز شبكة دعم ما تحكم ولا تفضح."
        ]
      },
      social_skills:{
        title:"SS — مهارات اجتماعية",
        steps:[
          "أتمرن على جملة حازمة وواضحة (أنا أحتاج...).",
          "أتدرّب على تواصل بصري ونبرة هادية لثواني قصيرة.",
          "تعرض اجتماعي خفيف يوميًا (سلام بسيط، سؤال قصير)."
        ]
      },
      anger_management:{
        title:"AM — إدارة الغضب",
        steps:[
          "أحدد إشارات الغضب المبكرة بجسمي وفكري.",
          "أطبق إيقاف مؤقت + تنفس 4-6-8 (شهيق4/حجز6/زفير8).",
          "أرجع وأتكلم عن السلوك مو عن شخصية الشخص."
        ]
      },
      self_confidence:{
        title:"SC — تعزيز الثقة",
        steps:[
          "أكتب إنجاز صغير كل يوم وأسميه نجاح.",
          "تعرض ثقة تدريجي (خطوة سهلة قبل الصعبة).",
          "أستبدل جلد الذات بجملة واقعية إيجابية ('قاعد أتعلم')."
        ]
      }
    };

    const plansDiv  = document.getElementById('plans');
    const selectA   = document.getElementById('planA');
    const selectB   = document.getElementById('planB');
    const daysSel   = document.getElementById('daysSelect');
    const shareWA   = document.getElementById('share-wa');
    const shareTG   = document.getElementById('share-tg');
    const checklistDiv = document.getElementById('checklist');

    (function renderPlans(){
      let html = '';
      for (const key in PLANS){
        const plan = PLANS[key];
        html += `
          <div class="tile">
            <h3 id="t-${key}">${plan.title}</h3>
            <ol style="padding-right:20px;line-height:1.7;font-size:.9rem;color:#2b1a4c;">
              <li>${plan.steps[0]}</li>
              <li>${plan.steps[1]}</li>
              <li>${plan.steps[2]}</li>
            </ol>
            <div class="row">
              <button class="btn alt" onclick="pick('${key}')">اختيار</button>
              <button class="btn" onclick="dl('${key}')">💾 تنزيل JSON</button>
            </div>
          </div>
        `;
      }
      plansDiv.innerHTML = html;

      for (const key in PLANS){
        const optA = document.createElement('option');
        optA.value = key;
        optA.textContent = PLANS[key].title;
        selectA.appendChild(optA);

        const optB = document.createElement('option');
        optB.value = key;
        optB.textContent = PLANS[key].title;
        selectB.appendChild(optB);
      }

      try {
        const saved = JSON.parse(localStorage.getItem('cbt_state')||'{}');
        if (saved.planA && PLANS[saved.planA]) selectA.value = saved.planA;
        else selectA.value = 'ba';
        if (saved.planB && PLANS[saved.planB]) selectB.value = saved.planB;
        if (saved.days) daysSel.value = String(saved.days);
      } catch(e){ selectA.value='ba'; }

      let suggest = new URLSearchParams(location.search).get('suggest');
      if(!suggest){
        try {
          const fromLocal = JSON.parse(localStorage.getItem('cbt_suggested')||'[]') || [];
          suggest = fromLocal.join(',');
        } catch(e){}
      }
      if(suggest){
        const keys = suggest.split(',').map(s=>s.trim()).filter(Boolean);
        if(keys.length && PLANS[keys[0]]) {
          selectA.value = keys[0];
        }
        keys.forEach(k=>{
          const h = document.getElementById('t-'+k);
          if(h){
            h.style.outline = '3px solid var(--g)';
            h.style.boxShadow = '0 0 0 4px rgba(255,215,0,.25)';
            h.style.borderRadius = '12px';
            h.style.padding = '4px 6px';
          }
        });
      }
    })();

    function persistCBTState(){
      const state = {
        planA: selectA.value,
        planB: selectB.value || '',
        days:  parseInt(daysSel.value,10) || 7
      };
      try { localStorage.setItem('cbt_state', JSON.stringify(state)); } catch(e){}
    }

    window.pick = function(key){
      selectA.value = key;
      persistCBTState();
      window.scrollTo({top: daysSel.offsetTop - 60, behavior:'smooth'});
    };

    window.dl = function(key){
      const data = PLANS[key] || {};
      const a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
      a.download = key + ".json";
      a.click();
      URL.revokeObjectURL(a.href);
    };

    window.buildChecklist = function(){
      persistCBTState();

      const keyA = selectA.value;
      const keyB = selectB.value;
      const days = parseInt(daysSel.value,10);

      if(!keyA || !PLANS[keyA]){
        alert('اختر خطة A أولاً');
        return;
      }

      const planA = PLANS[keyA];
      const planB = keyB && PLANS[keyB] ? PLANS[keyB] : null;

      const steps = [...planA.steps, ...(planB?planB.steps:[])];
      const titleCombo = [planA.title].concat(planB?[planB.title]:[]).join(" + ");

      let html = `<h3 style="margin:6px 0">${titleCombo} — جدول ${days} يوم</h3>`;
      html += "<table class='table'><thead><tr><th>اليوم</th>";
      steps.forEach((s,i)=>{
        html += "<th>"+(i+1)+". "+s+"</th>";
      });
      html += "</tr></thead><tbody>";

      for(let d=1; d<=days; d++){
        html += "<tr><td><b>"+d+"</b></td>";
        for(let c=0; c<steps.length; c++){
          html += "<td><input type='checkbox' /></td>";
        }
        html += "</tr>";
      }
      html += "</tbody></table>";

      checklistDiv.innerHTML = html;

      updateShareLinks(titleCombo, days);
    };

    window.saveChecklist = function(){
      const rows = checklistDiv.querySelectorAll('tbody tr');
      if(!rows.length) return;

      const head = checklistDiv.querySelector('h3')?.innerText || '';
      const parts = head.split(' — جدول ');
      const days = parseInt((parts[1]||'7').split(' ')[0],10);

      const headerCells = [...checklistDiv.querySelectorAll('thead th')]
        .slice(1)
        .map(th=>th.innerText);

      const progress = [];
      rows.forEach((tr, idx)=>{
        const done = [...tr.querySelectorAll('input[type=checkbox]')].map(ch=>ch.checked);
        progress.push({
          day:(idx+1),
          done:done
        });
      });

      const data = {
        title: parts[0] || '',
        steps: headerCells,
        days: days,
        progress: progress,
        created_at: new Date().toISOString(),
        build: window.__BUILD__
      };

      const a=document.createElement('a');
      a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
      a.download='cbt_checklist.json';
      a.click();
      URL.revokeObjectURL(a.href);
    };

    function updateShareLinks(title, days){
      const url = location.origin + '/cbt';
      const msg = "خطة CBT: "+title+"\\nمدة: "+days+" يوم\\n— من {{BRAND}}\\n"+url;
      const text = encodeURIComponent(msg);
      shareWA.href = "{{WA_BASE}}" + '?text=' + text;
      shareTG.href = 'https://t.me/share/url?url=' + encodeURIComponent(url) + '&text=' + text;
    }
  </script>

</div>
"""

def render_cbt_page():
    return (
        CBT_PAGE_HTML
        .replace("{{BRAND}}", BRAND)
        .replace("{{WA_BASE}}", WA_BASE)
        .replace("[[PSYCHO_WA]]", PSYCHO_WA)
        .replace("[[PSYCH_WA]]", PSYCH_WA)
        .replace("[[SOCIAL_WA]]", SOCIAL_WA)
    )

@app.get("/cbt")
def cbt():
    return shell("CBT — خطط وتمارين", render_cbt_page(), "cbt")


# ======================== /tests ========================

TESTS_PAGE_HTML = r"""
<div class="card">
  <h1>📊 اختبارات نفسية / شخصية سريعة</h1>

  <div class="note">
    مهم:
    <br/>• الأسئلة قصيرة جدًا، الهدف وعي ذاتي فقط — مو تشخيص رسمي.
    <br/>• لا تستخدم النتيجة كبديل عن مختص، خصوصًا لو فيه أفكار إيذاء أو انتحار.
    <br/>• ما يتم حفظ إجاباتك على السيرفر. كله يشتغل محلي في جهازك فقط.
  </div>

  <div class="tile">
    <label class="small" style="font-weight:700;">
      اختر الاختبار:
      <select id="testPicker" onchange="renderQuiz()">
        <option value="anxiety">قلق / توتر عام</option>
        <option value="depression">مزاج منخفض / اكتئاب</option>
        <option value="confidence">الثقة بالنفس / صورة الذات</option>
        <option value="anger">غضب / اندفاع</option>
        <option value="addiction">اشتهاء / سلوك إدماني</option>
      </select>
    </label>
  </div>

  <div id="quizBox" class="tile" style="margin-top:14px"></div>

  <div id="resultBox" class="tile" style="margin-top:14px; display:none"></div>

  <script>
    // مقياس كل سؤال:
    // 0 = أبدًا / نادر
    // 1 = أحيانًا
    // 2 = كثير
    // 3 = دائم / تقريبًا يومي

    const TESTS = {
      anxiety:{
        title:"قلق / توتر عام",
        items:[
          "أشعر بقلق أو توتر أغلب اليوم.",
          "صعب أوقف التفكير والقلق.",
          "عضلاتي مشدودة / جسمي متوتر.",
          "صعوبة نوم بسبب القلق.",
          "قلبي يدق بسرعة/رجفة وقت التوتر.",
          "أتوتر من مواقف بسيطة أكثر من اللازم.",
          "أحتاج أطمن نفسي أو حد يطمّني كثير.",
          "أتهرب من مواقف لأن أحس بنحرج أو بنهار.",
          "تركيزي يضيع لأن القلق مسيطر.",
          "أخاف من أن يحصل شي سيئ قريبًا."
        ],
        ranges:[
          {max:7,  text:"الضغط منخفض. حافظ على عادات النوم والراحة 👌"},
          {max:15, text:"قلق متوسط. جرّب تمارين التنفس / CBT (وقت القلق)."},
          {max:22, text:"قلق مرتفع. التعرض التدريجي + وقت القلق المحدد مهم."},
          {max:30, text:"قلق عالي جدًا. الأفضل تكلم مختص أو دعم مباشر 🙏"}
        ]
      },
      depression:{
        title:"مزاج منخفض / اكتئاب",
        items:[
          "مزاجي حزين أو ثقيل أغلب اليوم.",
          "ما عاد أستمتع بأشياء كنت أحبها.",
          "طاقة جسمي قليلة جدًا.",
          "نومي متلخبط (نوم كثير أو قليل).",
          "إحساس بالذنب / إني ما أستحق شيء.",
          "صعوبة أركز أو أقرر قرارات بسيطة.",
          "أفكر أني عديم الفايدة أو عبء.",
          "أحس بتشاؤم تجاه المستقبل.",
          "أحس بجسمي ثقيل / حركتي بطيئة أو العكس عصبية زايدة.",
          "جاتني أفكار إيذاء أو هروب نهائي من الحياة."
        ],
        ranges:[
          {max:7,  text:"مزاجك متأثر بسيط. زوّد نشاطات ممتعة حتى لو متصنع (BA)."},
          {max:15, text:"انخفاض مزاج متوسط. مهم نرفع السلوك الإيجابي اليومي (تنشيط سلوكي)."},
          {max:22, text:"مزاج منخفض واضح. راقب الأمان، وخطة دعم يومية ثابتة."},
          {max:30, text:"أعراض شديدة. دعم مختص مهم جدًا وبسرعة 🙏"}
        ]
      },
      confidence:{
        title:"الثقة بالنفس / صورة الذات",
        items:[
          "أنتقد نفسي بقسوة.",
          "أخاف أغلط قدام الناس لأن بحس بالفضيحة.",
          "أقارن نفسي بالغير وأحس أقل منهم.",
          "صعب أقول 'أنا فخور بنفسي'.",
          "أشعر أني عبء على الناس.",
          "أحقق شيء حلو وبعدين أقلل منه ('عادي أي أحد يقدر').",
          "أغير رأيي بسرعة لو أحد اعترض، حتى لو أنا مقتنع.",
          "أحس أن الآخرين دايم يشوفون عيوبي.",
          "أرضي الناس زيادة عشان ما يزعلون حتى لو أتضرر.",
          "أستحي أطلب احتياجي بوضوح ('أنا أحتاج ...')."
        ],
        ranges:[
          {max:7,  text:"ثقتك إجمالاً كويسة 👏"},
          {max:15, text:"ثقتك تهتز أحيانًا. جرّب خطة SC (تعزيز الثقة)."},
          {max:22, text:"صورة الذات ضعيفة. جرّب الحزم التدريجي (مهارات اجتماعية)."},
          {max:30, text:"جلد ذات عالي. يفضل محادثة دعم نفسي عشان تتخف حدّة الجلد."}
        ]
      },
      anger:{
        title:"غضب / اندفاع",
        items:[
          "أنفجر بسرعة (صياح/اندفاع).",
          "أندم بعدها وأحس بخزي.",
          "أرمي/أكسر/ألوّح بعنف لما أتعصب.",
          "أهدد أو أجرح بالكلام وقت الغضب.",
          "أحس جسمي يولع وقت المشكلة.",
          "صعب أوقف نفسي قبل ما أنفجر.",
          "أغار جداً أو أشك بسرعة.",
          "أقول أشياء جارحة بس عشان أوجع.",
          "أحس الناس يستفزوني/ما يحترموني.",
          "صعب أهدى بسرعة بعد ما أعصب."
        ],
        ranges:[
          {max:7,  text:"انفعالك تحت السيطرة أغلب الوقت 👍"},
          {max:15, text:"في توتر. جرّب خطة AM (إدارة الغضب) ووقت تهدئة قبل الرد."},
          {max:22, text:"الغضب مأثر على علاقتك أو البيت. لازم تدريب إيقاف مؤقت."},
          {max:30, text:"اندفاع عالي جدًا. الأفضل دعم علاجي مباشر لحماية نفسك والناس."}
        ]
      },
      addiction:{
        title:"اشتهاء / سلوك إدماني",
        items:[
          "أفكر بالمادة/السلوك أغلب اليوم.",
          "أحس أني أحتاجها الآن عشان أهدى.",
          "أستمر فيها حتى لو أعرف أنها تضرني.",
          "سببت لي مشاكل أسرية/عملية/دراسية.",
          "أحس ما عندي سيطرة حقيقية عليها.",
          "رجعت لها بعد ما حاولت أترك (انتكاسة).",
          "لو ما حصلتها جسمي أو مزاجي ينهار.",
          "أضيع وقت/فلوس كثير عليها.",
          "أكذب أو أخبي عشان أقدر أستمر.",
          "أقول 'آخر مرة' كثير بس أرجع."
        ],
        ranges:[
          {max:7,  text:"التحكم الحالي معقول. خلك واعي بالمحفزات 👀"},
          {max:15, text:"خطر متوسط. نبغى خطة RP (منع الانتكاس) ودعم من شخص ما يحكم."},
          {max:22, text:"علامات اعتماد واضحة. لا تواجهها لحالك، لازم شبكة دعم آمنة."},
          {max:30, text:"سلوك إدماني عالي. اطلب مساعدة بشرية الآن 🙏"}
        ]
      }
    };

    // يبني قائمة الأسئلة
    function renderQuiz(){
      const picker = document.getElementById('testPicker');
      const box = document.getElementById('quizBox');
      const resultBox = document.getElementById('resultBox');
      resultBox.style.display='none';
      resultBox.innerHTML='';

      const testKey = picker.value;
      const test = TESTS[testKey];
      if(!test){
        box.innerHTML = "<div class='small'>الاختبار غير موجود.</div>";
        return;
      }

      let html = "";
      html += "<h3>"+test.title+"</h3>";
      html += "<div class='small' style='margin-bottom:8px'>جاوب بصراحة عن آخر أسبوعين تقريباً 👇</div>";
      html += "<ol style='padding-right:20px;line-height:1.7;font-size:.9rem;color:#2b1a4c;'>";

      test.items.forEach(function(q,idx){
        html += `
          <li style="margin-bottom:10px;">
            <div style="font-weight:600;margin-bottom:6px;">${q}</div>
            <label class="badge2"><input type="radio" name="q${idx}" value="0"> أبدًا / نادر</label>
            <label class="badge2"><input type="radio" name="q${idx}" value="1"> أحيانًا</label>
            <label class="badge2"><input type="radio" name="q${idx}" value="2"> كثير</label>
            <label class="badge2"><input type="radio" name="q${idx}" value="3"> دائم تقريبًا</label>
          </li>
        `;
      });

      html += "</ol>";

      html += `
        <div class="row" style="margin-top:14px">
          <button class="btn gold" onclick="scoreNow('${testKey}')">احسب درجتي 🔍</button>
          <button class="btn alt" onclick="window.print()">🖨️ طباعة</button>
        </div>
      `;

      box.innerHTML = html;
    }

    // يحسب الدرجة ويفسرها
    window.scoreNow = function(testKey){
      const test = TESTS[testKey];
      if(!test) return;

      let total = 0;
      let answered = 0;

      for (let i=0;i<test.items.length;i++){
        const sel = document.querySelector('input[name="q'+i+'"]:checked');
        if(sel){
          const v = parseInt(sel.value,10);
          if(!isNaN(v)){
            total += v;
            answered += 1;
          }
        }
      }

      // تأكد جاوب على كل الأسئلة
      if(answered < test.items.length){
        alert("جاوب كل الأسئلة لو تقدر 🙏 ("+answered+" من "+test.items.length+")");
        return;
      }

      // نختار الرسالة المناسبة حسب total
      let interp = "ما قدرنا نحدد مستوى واضح.";
      for (let r of test.ranges){
        if(total <= r.max){
          interp = r.text;
          break;
        }
      }

      const resultBox = document.getElementById('resultBox');
      resultBox.style.display='block';
      resultBox.innerHTML = `
        <h3>نتيجتك في: ${test.title}</h3>
        <div class="small">
          الدرجة الكلية: <b>${total}</b> من <b>${test.items.length*3}</b><br/>
          <div class="note" style="margin-top:10px">${interp}</div>
        </div>

        <div class="divider"></div>

        <div class="small">
          مهم: هذه أداة وعي ذاتي. إذا فيه إيذاء، سلوك خطير، أفكار انتحار،
          لا تعتمد على الموقع. كلّف شخص حي يسمعك الآن 🙏
        </div>
      `;
    };

    // أول ما تفتح الصفحة نبين اختبار القلق افتراضياً
    window.addEventListener('DOMContentLoaded', function(){
      renderQuiz();
    });
  </script>

</div>
"""

@app.get("/tests")
def tests():
    return shell("اختبارات سريعة — " + BRAND, TESTS_PAGE_HTML, "tests")


# ======================== /pharm ========================
# دليل الأدوية النفسية (تثقيف فقط)
# مهم: ما ننصح بجرعات محددة، ولا نقول "خذ/لا تأخذ".
# بس: فئة الدواء، عادة ليش ينصرف، تحذير السلامة، متى لازم طوارئ.

PHARM_DB = [
    {
        "name": "سيرترالين (Sertraline)",
        "class": "SSRI (مضاد اكتئاب من نوع مثبط امتصاص السيروتونين)",
        "why": "يستخدم كثير في الاكتئاب، القلق العام، القلق الاجتماعي، الوسواس القهري، أحيانًا بعد الصدمة.",
        "common": "غثيان خفيف بالبداية، اضطراب بسيط بالنوم، صداع، أحيانًا نقص شهية أو تغير رغبة جنسية.",
        "serious": "أفكار انتحارية جديدة خاصة بالبداية أو عند رفع الجرعة، تهيّج وهياج قوي، حس بمانيا (نشاط مفرط، نوم قليل)، أعراض حساسة جدًا مثل تعرّق شديد + رجفة + حرارة (إمكانية متلازمة السيروتونين).",
        "redflag": "إذا فجأة صار عندك أفكار أذى قوية أو سلوك اندفاع خطر أو أعراض عصبية غريبة جدًا → لازم تقييم طبي عاجل."
    },
    {
        "name": "فلوكسيتين (Fluoxetine)",
        "class": "SSRI",
        "why": "اكتئاب، وسواس قهري، أكل قهري أحيانًا، قلق.",
        "common": "قلق/تنشيط أول الأيام، صعوبة نوم، صداع، غثيان.",
        "serious": "تقلب مزاج عالي جدًا (هوس/هياج)، أفكار إيذاء مفاجئة.",
        "redflag": "أي تغيّر حاد في التفكير (خطر، عنف، انتحار) أو أعراض عصبية شديدة → مراجعة عاجلة."
    },
    {
        "name": "إسيتالوبرام (Escitalopram)",
        "class": "SSRI",
        "why": "قلق عام، اكتئاب، قلق اجتماعي.",
        "common": "دوخة خفيفة، غثيان بسيط، تغيّر شهية أو رغبة جنسية.",
        "serious": "أعراض قلبية نادرة (خفقان قوي جدًا/عدم انتظام ملحوظ)، أفكار انتحارية جديدة.",
        "redflag": "لو حسّيت بدوخة مع نبض غير طبيعي أو نية إيذاء قوية مفاجئة → لا تنتظر تقييم."
    },
    {
        "name": "فينلافاكسين (Venlafaxine)",
        "class": "SNRI (سيروتونين + نورأدرينالين)",
        "why": "قلق شديد مستمر، اكتئاب، أحيانًا ألم عصبي.",
        "common": "غثيان، تعرّق، صداع، أرق، ممكن ارتفاع بسيط في الضغط.",
        "serious": "لو وقف فجأة ممكن يسبب أعراض انسحاب مزعجة (دوار قوي، صدمات كهربائية بالرأس شعورياً).",
        "redflag": "صداع + خفقان + ضغط مرتفع جدًا أو أفكار إيذاء جديدة → يحتاج تقييم طبي سريع."
    },
    {
        "name": "كويتيابين (Quetiapine)",
        "class": "مضاد ذهان/مثبّت مزاج (Seroquel)",
        "why": "يُستخدم في الذهان، نوبات هوس/هياج، أحيانًا كمساعد في الاكتئاب المقاوم. بعض الأطباء يستخدمونه بجرعة صغيرة للنوم لكن هذا مو آمن دائماً.",
        "common": "نعاس قوي، زيادة شهية/وزن، دوخة عند الوقوف.",
        "serious": "هبوط ضغط شديد مع دوخة قوية جدًا، أعراض سكر/كولسترول على المدى، حركات عضلية لا إرادية.",
        "redflag": "ارتباك شديد، تلعثم/تيبس قوي، حرارة عالية + تيبس (احتمال نادر: متلازمة خبيثة للدواء) → طوارئ."
    },
    {
        "name": "أولانزابين (Olanzapine)",
        "class": "مضاد ذهان غير تقليدي (Zyprexa)",
        "why": "ذهان، هوس ثنائي القطب، أحيانًا قلق شديد مع اضطراب ذهني.",
        "common": "جوع زايد جدًا، زيادة وزن سريعة، نعاس.",
        "serious": "ارتفاع سكر شديد، كسل شديد جدًا، تيبس أو تململ حركي صعب.",
        "redflag": "تشوش ذهني جديد أو حرارة + تيبس + ارتباك → طوارئ طبية."
    },
    {
        "name": "لاموترجين (Lamotrigine)",
        "class": "مثبّت مزاج/مضاد اختلاجات",
        "why": "نوبات الاكتئاب في الاضطراب ثنائي القطب (خاصة الاكتئاب)، وأحياناً تحكم تقلب المزاج.",
        "common": "صداع خفيف، دوار بسيط، أرق خفيف أو نعاس خفيف.",
        "serious": "طفح جلدي خطير (طفح جديد مع حرارة/ألم فم/عيون) احتمال متلازمة ستيفنز-جونسون (نادر لكن مهم).",
        "redflag": "أي طفح جلدي جديد مع حرارة أو ألم بالفم/العين → هذا طارئ، تواصل مع طبيب فوراً."
    },
    {
        "name": "كلونازيبام / لورازيبام (Clonazepam / Lorazepam)",
        "class": "بنزوديازيبين (مهدئات قلق/هلع قصيرة المدى)",
        "why": "يُصرف غالبًا للقلق الحاد/الهلع/أرق شديد لفترة قصيرة جدًا، مو حل طويل.",
        "common": "نعاس، تباطؤ، ضعف ذاكرة قصيرة، تباطؤ رد الفعل (خطر قيادة).",
        "serious": "اعتماد/تعود، صعوبة إيقافه بدون أعراض انسحاب (رجفة، قلق أسوأ).",
        "redflag": "دوخة شديدة + تداخل كلام + تنفس بطيء جدًا → هذا طارئ."
    },
    {
        "name": "نالتريكسون (Naltrexone)",
        "class": "دواء دعم الإدمان (أفيونات/كحول)",
        "why": "يقلل الرغبة في مواد معيّنة (مثل الكحول/الأفيونات) كجزء من خطة علاج شاملة.",
        "common": "غثيان خفيف، صداع، إرهاق.",
        "serious": "مشاكل كبد (ألم يمين أعلى البطن، اصفرار عين/جلد، بول داكن).",
        "redflag": "أعراض كبد واضحة أو ألم قوي بالبطن + اصفرار → لازم رعاية طبية."
    }
]

def render_pharm_page():
    cards = []
    for med in PHARM_DB:
        cards.append(f"""
        <div class="tile">
          <h3 style="margin-top:0;">💊 {med["name"]}</h3>
          <div class="small"><b>الفئة:</b> {med["class"]}</div>
          <div class="small"><b>ليش عادة ينصرف؟</b> {med["why"]}</div>
          <div class="small"><b>أعراض شائعة (مو خطيرة عادة):</b> {med["common"]}</div>
          <div class="small"><b>مخاوف جدّية لازم تنتبه لها:</b> {med["serious"]}</div>
          <div class="note"><b>🚨 ضروري تتصرف الآن لو:</b> {med["redflag"]}</div>
          <div class="small" style="margin-top:8px;font-weight:600;color:#4b0082;">
            مو معناته لازم توقف الدواء لحالك. الخطوة الصح دايم: تواصل مع طبيبك / طوارئ حسب شدة العَرَض.
          </div>
        </div>
        """)
    meds_html = "\n".join(cards)

    wrap = f"""
<div class="card">
  <h1>💊 دليل الأدوية النفسية (تثقيف فقط)</h1>
  <div class="note">
    المعلومات هنا للتثقيف العام فقط.
    إحنا <b>ما نصف جرعات</b> وما نقول "خذ/أوقف".
    أي تغيير دوائي لازم مع طبيب.
    ولو في أعراض خطيرة / أفكار إيذاء → هذا طارئ.
  </div>

  <div class="grid">
    {meds_html}
  </div>

  <div class="divider"></div>

  <div class="row screen-only">
    <a class="btn" href="{PSYCHO_WA}" target="_blank" rel="noopener">👨‍🎓 أخصائي نفسي</a>
    <a class="btn" href="{PSYCH_WA}"  target="_blank" rel="noopener">👨‍⚕️ طبيب نفسي</a>
    <a class="btn" href="{SOCIAL_WA}" target="_blank" rel="noopener">🤝 أخصائي اجتماعي</a>
  </div>
</div>
"""
    return wrap

@app.get("/pharm")
def pharm():
    return shell("دليل الأدوية — " + BRAND, render_pharm_page(), "pharm")


# ======================== /health ========================

@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "brand": BRAND,
        "build": CACHE_BUST,
        "ts": datetime.utcnow().isoformat()+"Z"
    })


# ======================== تشغيل محلي ========================

if __name__ == "__main__":
    # PORT من Render/Railway أو 5000 لو محلي
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
