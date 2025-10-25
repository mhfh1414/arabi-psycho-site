# -*- coding: utf-8 -*-
# ======================================================================
# عربي سايكو — ملف واحد كامل (Purple × Gold) v7.0
#
# صفحات:
#   /        الرئيسية
#   /case    دراسة الحالة (DSM + إدمان مدمج)
#   /cbt     خطط CBT + مولد الجدول
#   /pharm   دليل الأدوية النفسية (تثقيف فقط، بدون جرعات)
#
# ملاحظات أمان مهمّة:
# - لا تعتبر أي شي هنا تشخيص طبي أو وصفة علاج. لازم طبيب/صيدلي مختص.
# - لا تبدأ أو توقف دواء بدون إشراف طبي مباشر.
#
# تشغيل محلّي:
#   python app.py
#
# تشغيل على Render / Railway / أي استضافة:
#   gunicorn app:app --bind 0.0.0.0:$PORT
# ======================================================================

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# ======================== إعدادات عامة ========================

BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO  = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")

TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696")
WA_BASE = WA_URL.split("?")[0]

PSYCHO_WA = os.environ.get("PSYCHOLOGIST_WA", "https://wa.me/966530565696")
PSYCH_WA  = os.environ.get("PSYCHIATRIST_WA", "https://wa.me/966530565696")
SOCIAL_WA = os.environ.get("SOCIAL_WORKER_WA", "https://wa.me/966530565696")

CACHE_BUST = os.environ.get("CACHE_BUST", datetime.utcnow().strftime("%Y%m%d%H%M%S"))

SLOGAN = "«نراك بعين الاحترام، ونسير معك بخطوات عملية.»"


# ======================== Layout موحّد ========================

def shell(title, content, active="home"):
    html = r"""
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
  border:1px solid var(--card-border);
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
  border:1px solid var(--card-border);
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
  border:1px dashed var(--note-border);
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
  border:1px solid #000;
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
  border:1px solid var(--card-border);
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
  border:1px solid var(--g);
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
  border:1px solid #eee;
  padding:8px;
  text-align:center;
  vertical-align:top;
  line-height:1.5;
  min-width:60px;
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
  border-bottom:1px solid var(--line);
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
  border-top:1px solid var(--line);
  margin:12px 0;
}
label.badge2 input[type=checkbox]{
  margin-left:6px;
  transform:scale(1.2);
}
input, select, textarea{
  width:100%;
  border:1px solid #ddd;
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
  border:1px solid #ffc1c1;
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
  border-top:1px solid #000;
  border-bottom:1px solid #000;
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
    border:1px solid #000;
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
        <span>🧠 العلاج السلوكي المعرفي CBT</span>
        <small>الخطط + الجدول</small>
      </a>
      <a href="/pharm" class="[[A_PHARM]]">
        <span>💊 دليل الأدوية النفسية</span>
        <small>متى يُصرف / التحذيرات</small>
      </a>
    </nav>

    <div class="ref-box">
      <h4>📞 دعم مباشر الآن</h4>
      <div class="ref-links">
        <a href="[[PSYCHO_WA]]" target="_blank" rel="noopener">
          👨‍🎓 أخصائي نفسي
          <span>خطة سلوكية/سلوكية معرفية</span>
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
""".replace("[[TITLE]]", title)\
     .replace("[[LOGO]]", LOGO)\
     .replace("[[BRAND]]", BRAND)\
     .replace("[[TG_URL]]", TG_URL)\
     .replace("[[WA_URL]]", WA_URL)\
     .replace("[[SLOGAN]]", SLOGAN)\
     .replace("[[BUILD]]", CACHE_BUST)\
     .replace("[[PSYCHO_WA]]", PSYCHO_WA)\
     .replace("[[PSYCH_WA]]", PSYCH_WA)\
     .replace("[[SOCIAL_WA]]", SOCIAL_WA)\
     .replace("[[A_HOME]]", "active" if active=="home" else "")\
     .replace("[[A_CASE]]", "active" if active=="case" else "")\
     .replace("[[A_CBT]]", "active" if active=="cbt" else "")\
     .replace("[[A_PHARM]]", "active" if active=="pharm" else "")\
     .replace("[[CONTENT]]", content)
    return html


# ======================== تحليل الأعراض ========================

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
        "safety_behaviors": "SA — إيقاف سلوكيات آمنة/طمأنة",
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

    js = f"""
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
        "هذه ليست تشخيص نهائي طبي، لكنها خريطة أولية لمساعدتك على اختيار الخطة السلوكية."
    )

    html = f"""
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
  <ol id="diag-items" style="line-height:1.95; padding-inline-start: 20px">{lis}</ol>

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

  {js}
</div>
"""
    return html


# ======================== /home ========================

@app.get("/")
def home():
    content = f"""
<div class="card" style="margin-bottom:18px; border:2px solid #000;">
  <h1>مرحبًا بك في {BRAND}</h1>
  <div class="small">
    هذه مساحة آمنة تساعدك تحلل وضعك بصراحة، بدون حُكم.
    <br/>
    الخطوات عندنا واضحة:
    <br/>1) 📝 قيّم نفسك في «دراسة الحالة»
    <br/>2) 🧠 ننشئ لك خطة CBT يومية عملية (7 / 10 / 14 يوم)
    <br/>3) 🤝 لو احتجت دعم بشري مباشر: أخصائي نفسي / طبيب نفسي / أخصائي اجتماعي — بزر واحد تكلمهم.
    <br/>4) 💊 تبغى تعرف عن الأدوية النفسية والآثار الجانبية وليش تنصرف؟ افتح «دليل الأدوية».
  </div>
  <div class="note">"نحن نحترمك، ونعامل ألمك كشيء حقيقي يستحق خطة — مش ضعف."</div>
</div>

<div class="grid">

  <div class="tile" style="border:2px solid #000;">
    <h3>📝 دراسة الحالة (DSM + الإدمان مدمج)</h3>
    <p class="small">
      أكثر من 70 عرض (مزاج، قلق، وسواس، صدمة، نوم، تركيز، ثقة، غضب، تعاطي مواد...)
      <br/>بعدها يطلع لك ملخص مبدئي + توصيات CBT + زر تحويل مباشر للاختصاصي.
    </p>
    <a class="btn gold" href="/case">ابدأ الآن</a>
  </div>

  <div class="tile" style="border:2px solid #000;">
    <h3>🧠 CBT العلاج السلوكي المعرفي</h3>
    <p class="small">
      17 خطة واضحة (تنشيط سلوكي، إدارة الغضب، تعزيز الثقة بالنفس، نوم، هلع، وسواس...).
      <br/>الموقع يبني لك جدول يومي قابل للطباعة والمشاركة.
    </p>
    <a class="btn" href="/cbt">افتح CBT</a>
  </div>

  <div class="tile" style="border:2px solid #000;">
    <h3>💊 دليل الأدوية النفسية</h3>
    <p class="small">
      SSRIs, مثبت مزاج, أدوية الذهان, القلق, الإدمان...
      <br/>ليش ينصرف الدواء؟ أهم الأعراض الجانبية؟ متى لازم دكتور فورًا؟
    </p>
    <a class="btn alt" href="/pharm">استعرض الأدوية</a>
  </div>

  <div class="tile" style="border:2px solid #000;">
    <h3>📞 تواصل سريع</h3>
    <p class="small">
      تحتاج تتكلم مع بشر حقيقي؟
      <br/>نوصلك مباشرة.
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
<div class="card" style="border:2px solid #000;">
  <h1>📝 دراسة الحالة — (DSM + الإدمان مدمج)</h1>
  <div class="small">
    اختر الأعراض اللي تحس إنها <b>عندك فعلاً</b> بالفترة الحالية.
    بعدها اضغط «عرض النتيجة».
    <br/>مهم: هذا مو تشخيص طبي نهائي. هذا مسار مبدئي يساعدك تبني خطة سلوكية محترمة.
  </div>
  <div class="note">
    هذه بيانات حساسة. يتم حفظ اختياراتك محليًا في جهازك (localStorage) وليس في السيرفر.
  </div>

  <form method="post" action="/case" oninput="persistCase()">

    <h2>1) معلومات أساسية</h2>
    <div class="grid">
      <div class="tile" style="border:1px solid #000;">
        <label>العمر
          <input name="age" type="number" min="5" max="120" placeholder="28">
        </label>
      </div>
      <div class="tile" style="border:1px solid #000;">
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
      <div class="tile" style="border:1px solid #000;">
        <label>العمل / الدراسة
          <input name="work" placeholder="طالب / موظف / باحث عن عمل / غير ذلك">
        </label>
      </div>
    </div>

    <div class="divider"></div>

    <h2>2) الأعراض الحالية (اختر ما ينطبق فعلاً)</h2>

    <div class="grid">

      <div class="tile" style="border:1px solid #000;">
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

      <div class="tile" style="border:1px solid #000;">
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

      <div class="tile" style="border:1px solid #000;">
        <h3>🟣 وسواس قهري (OCD)</h3>
        <label class="badge2"><input type="checkbox" name="obsessions"> أفكار/صور مُلِحّة ما أقدر أوقفها</label>
        <label class="badge2"><input type="checkbox" name="compulsions"> أفعال قهرية (غسل/تفقد/ترتيب...)</label>
        <label class="badge2"><input type="checkbox" name="contamination"> هوس تلوّث / غسل مفرط</label>
        <label class="badge2"><input type="checkbox" name="checking"> تفقد الأبواب/القفل/الأشياء كثير</label>
        <label class="badge2"><input type="checkbox" name="ordering"> لازم ترتيب/تماثل كامل</label>
        <label class="badge2"><input type="checkbox" name="harm_obs"> وساوس أذى (أخاف أضر نفسي/غيري)</label>
        <label class="badge2"><input type="checkbox" name="scrupulosity"> تدقيق ديني/أخلاقي قهري</label>
      </div>

      <div class="tile" style="border:1px solid #000;">
        <h3>🟣 الصدمة / ما بعد الصدمة</h3>
        <label class="badge2"><input type="checkbox" name="flashbacks"> استرجاعات / كوابيس عن حدث صعب</label>
        <label class="badge2"><input type="checkbox" name="hypervigilance"> يقظة مفرطة / دائمًا على أهبة الاستعداد</label>
        <label class="badge2"><input type="checkbox" name="startle"> فزع مفرط من الأصوات/المفاجآت</label>
        <label class="badge2"><input type="checkbox" name="numbing"> خدر عاطفي / كأني مو موجود</label>
        <label class="badge2"><input type="checkbox" name="trauma_avoid"> أتجنب أي تذكير بالحدث (أماكن/كلام)</label>
        <label class="badge2"><input type="checkbox" name="guilt_trauma"> شعور بالذنب تجاه الحدث</label>
      </div>

      <div class="tile" style="border:1px solid #000;">
        <h3>🟣 النوم</h3>
        <label class="badge2"><input type="checkbox" name="insomnia"> صعوبة بداية/استمرار النوم (أرق)</label>
        <label class="badge2"><input type="checkbox" name="hypersomnia"> نوم مفرط / صعوبة القيام</label>
        <label class="badge2"><input type="checkbox" name="nightmares"> كوابيس متكررة</label>
        <label class="badge2"><input type="checkbox" name="irregular_sleep"> مواعيد نوم فوضوية جدًا</label>
      </div>

      <div class="tile" style="border:1px solid #000;">
        <h3>🟣 تركيز / حركة / تنظيم الوقت</h3>
        <label class="badge2"><input type="checkbox" name="adhd_inattention"> تشتت / نسيان أشياء أساسية</label>
        <label class="badge2"><input type="checkbox" name="adhd_hyper"> فرط حركة / اندفاع / صعوبة الجلوس</label>
        <label class="badge2"><input type="checkbox" name="disorganization"> فوضى تنظيم / تأجيل مزمن</label>
        <label class="badge2"><input type="checkbox" name="time_blindness"> ضياع الإحساس بالوقت / التأخير الدائم</label>
      </div>

      <div class="tile" style="border:1px solid #000;">
        <h3>🟣 مزاج مرتفع / طاقة مفرطة</h3>
        <label class="badge2"><input type="checkbox" name="elevated_mood"> مزاج مرتفع جدًا / تهوّر</label>
        <label class="badge2"><input type="checkbox" name="decreased_sleep_need"> أحتاج نوم قليل جدًا وأحس طبيعي</label>
        <label class="badge2"><input type="checkbox" name="grandiosity"> إحساس بالعظمة / قدرات خارقة</label>
        <label class="badge2"><input type="checkbox" name="racing_thoughts"> أفكار سريعة جدًا / ما ألحقها</label>
        <label class="badge2"><input type="checkbox" name="pressured_speech"> كلام سريع/متدفق جدًا</label>
        <label class="badge2"><input type="checkbox" name="risk_spending"> صرف فلوس/مخاطرة عالية بدون تفكير</label>
      </div>

      <div class="tile" style="border:1px solid #000;">
        <h3>🟣 إدراك/تفكير (ذهاني/فصام)</h3>
        <label class="badge2"><input type="checkbox" name="hallucinations"> هلوسات (أسمع/أشوف شي غير طبيعي)</label>
        <label class="badge2"><input type="checkbox" name="delusions"> أفكار مراقبة / مؤامرة / يقين غريب</label>
        <label class="badge2"><input type="checkbox" name="disorganized_speech"> كلام/تفكير متشتت أو غير مفهوم</label>
        <label class="badge2"><input type="checkbox" name="negative_symptoms"> انسحاب / برود عاطفي</label>
        <label class="badge2"><input type="checkbox" name="catatonia"> تجمّد حركي / سلوك غير متجاوب</label>
        <label class="badge2"><input type="checkbox" name="decline_function"> تدهور واضح بالدراسة/العمل/العلاقات</label>
      </div>

      <div class="tile" style="border:1px solid #000;">
        <h3>🟣 الأكل / صورة الجسد</h3>
        <label class="badge2"><input type="checkbox" name="binge_eating"> نوبات أكل شره / فقدان التحكم</label>
        <label class="badge2"><input type="checkbox" name="restrict_eating"> تقييد قوي / تجويع نفسي</label>
        <label class="badge2"><input type="checkbox" name="body_image"> انشغال قوي بالشكل/الوزن</label>
        <label class="badge2"><input type="checkbox" name="purging"> تطهير/إقياء قهري بعد الأكل</label>
      </div>

      <div class="tile" style="border:1px solid #000;">
        <h3>🟣 تعاطي مواد / إدمان</h3>
        <label class="badge2"><input type="checkbox" name="craving"> اشتهاء قوي / أحتاج أستخدم الآن</label>
        <label class="badge2"><input type="checkbox" name="withdrawal"> انسحاب جسدي/نفسي إذا ما استخدمت</label>
        <label class="badge2"><input type="checkbox" name="use_harm"> أستمر رغم ضرر واضح</label>
        <label class="badge2"><input type="checkbox" name="loss_control"> صعوبة إيقاف / فقدان السيطرة</label>
        <label class="badge2"><input type="checkbox" name="relapse_history"> انتكاسات بعد محاولات الإيقاف</label>
      </div>

      <div class="tile" style="border:1px solid #000;">
        <h3>🟣 تنظيم العاطفة / العلاقات / الغضب</h3>
        <label class="badge2"><input type="checkbox" name="emotion_instability"> تقلب مزاج حاد / مشاعر قوية فجأة</label>
        <label class="badge2"><input type="checkbox" name="impulsivity"> اندفاعية / أتصرف قبل ما أفكر</label>
        <label class="badge2"><input type="checkbox" name="anger_issues"> نوبات غضب / صراخ / انفجار سريع</label>
        <label class="badge2"><input type="checkbox" name="perfectionism"> كمالية تعطلني (كل شيء لازم مثالي)</label>
        <label class="badge2"><input type="checkbox" name="dependence"> تعلق عالي / خوف قوي من الهجر</label>
        <label class="badge2"><input type="checkbox" name="social_withdrawal"> انسحاب اجتماعي / صعوبة تواصل</label>
        <label class="badge2"><input type="checkbox" name="self_conf_low"> ثقة بالنفس منخفضة / جلد ذاتي</label>
      </div>

      <div class="tile" style="border:1px solid #000;">
        <h3>🟣 تواصل / حساسية حسّية</h3>
        <label class="badge2"><input type="checkbox" name="asd_social"> صعوبة قراءة الإشارات الاجتماعية</label>
        <label class="badge2"><input type="checkbox" name="sensory"> حساسية حسّية (أصوات/إضاءة/ملمس)</label>
        <label class="badge2"><input type="checkbox" name="rigidity"> تمسّك عالي بروتين/ترتيب (أتضايق لو تغيّر)</label>
      </div>

    </div>

    <div class="divider"></div>

    <div class="tile" style="border:1px solid #000; margin-top:10px">
      <label>ملاحظاتك (اختياري)
        <textarea name="notes" rows="4" placeholder="أهم التفاصيل بالنسبة لك / متى بدأت / وش اللي مضايقك أكثر الآن؟"></textarea>
      </label>
    </div>

    <div class="row" style="margin-top:14px">
      <button class="btn gold" type="submit">عرض النتيجة</button>
      <a class="btn" href="/cbt">🧠 فتح CBT الآن</a>
    </div>

  </form>

  <script>
    const KEY='case_state_v7';

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

    form_data = {k: True for k in request.form.keys() if k not in ("age","marital","work","notes")}
    form_data["age_val"] = request.form.get("age", "").strip()
    form_data["marital_val"] = request.form.get("marital", "").strip()
    form_data["work_val"] = request.form.get("work", "").strip()
    _ = request.form.get("notes", "").strip()  # ملاحظات المستخدم (ممكن نستخدمها مستقبلاً)

    picks = preliminary_picks(form_data)
    plans = suggest_plans(form_data)
    html = build_case_result_html(picks, plans)
    return shell("نتيجة دراسة الحالة — " + BRAND, html, "case")


# ======================== /cbt ========================

CBT_PAGE_HTML = r"""
<div class="card" style="border:2px solid #000;">

  <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
  <div class="small">
    الهدف: تحويل الأعراض إلى خطوات يومية قابلة للتنفيذ.
    <br/>
    اختَر خطة (أو خطتين مع بعض)، حدّد عدد الأيام (7 / 10 / 14)،
    واضغط "إنشاء الجدول" 👇
  </div>
  <div class="note">
    لو جيت من «دراسة الحالة»، بنوسّط لك الخطط المقترحة بخط ذهبي.
    إذا ما جيت من هناك، عادي؛ تقدر تختار يدوي.
  </div>

  <h2>الخطط المتاحة (17 خطة)</h2>
  <div class="grid" id="plans"></div>

  <div class="divider"></div>

  <h2 style="margin-top:18px">📅 مولّد الجدول اليومي</h2>
  <div class="tile" style="border:1px solid #000;">
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
          "أحصر سلوك الأمان (اتصال فوري لطمأنة، مثلاً).",
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
          <div class="tile" style="border:1px solid #000;">
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
    return CBT_PAGE_HTML.replace("{{BRAND}}", BRAND)\
                        .replace("{{WA_BASE}}", WA_BASE)\
                        .replace("[[PSYCHO_WA]]", PSYCHO_WA)\
                        .replace("[[PSYCH_WA]]", PSYCH_WA)\
                        .replace("[[SOCIAL_WA]]", SOCIAL_WA)

@app.get("/cbt")
def cbt():
    return shell("CBT — خطط وتمارين", render_cbt_page(), "cbt")


# ======================== /pharm ========================
# صفحة الأدوية النفسية / العصبية: تثقيف فقط (ليش يوصف الدواء؟ أعراض جانبية شائعة؟ متى لازم تراجع فورًا؟)
# لا نذكر جرعات ولا جداول استعمال، ونحذر من الإيقاف المفاجئ لأن هذا ممكن يكون خطير.

PHARM_PAGE_HTML = r"""
<div class="card" style="border:2px solid #000;">
  <h1>💊 دليل الأدوية النفسية (فارماسي)</h1>

  <div class="note">
    مهم جدًا:
    <br/>• هذه الصفحة تثقيف فقط — مو وصفة علاج.
    <br/>• لا تبدأ ولا توقف دواء بدون طبيب/صيدلي مختص.
    <br/>• بعض الأدوية إيقافها فجأة خطر (انسحاب، هلع، تشنجات، انتكاس شديد).
    <br/>• لو فيه أفكار إيذاء نفسك أو غيرك لازم دعم طبي عاجل.
  </div>

  <div class="tile" style="border:1px solid #000; margin-bottom:16px;">
    <label class="small" style="font-weight:700;">بحث باسم الدواء / الحالة
      <input id="drugSearch" placeholder="مثال: سيرترالين / قلق / ذهان / ليريكا" oninput="filterMeds()">
    </label>
  </div>

  <div id="medList" class="grid"></div>

  <div class="divider"></div>

  <h3>أحتاج مختص الآن؟</h3>
  <div class="row screen-only">
    <a class="btn" href="[[PSYCHO_WA]]" target="_blank" rel="noopener">👨‍🎓 أخصائي نفسي (سلوكي)</a>
    <a class="btn" href="[[PSYCH_WA]]"  target="_blank" rel="noopener">👨‍⚕️ طبيب نفسي (دوائي)</a>
    <a class="btn" href="[[SOCIAL_WA]]" target="_blank" rel="noopener">🤝 أخصائي اجتماعي (دعم حياتي)</a>
  </div>

  <script>
    // قائمة أدوية شائعة في الطب النفسي / العصبي
    // بدون جرعات، فقط: متى يُستخدم غالبًا / آثار جانبية / تحذير

    const MEDS = [
      // SSRIs
      {
        name:"سيرترالين (Sertraline)",
        klass:"SSRI مضاد اكتئاب/قلق",
        uses:"اكتئاب، قلق عام، وسواس قهري، هلع، قلق اجتماعي",
        sfx:"غثيان، إسهال، صداع، أرق بسيط، تأخير القذف/ضعف الرغبة",
        warn:"يحتاج متابعة طبيب. لا توقف فجأة بدون جدول نزول."
      },
      {
        name:"فلوكستين (Fluoxetine / بروزاك)",
        klass:"SSRI",
        uses:"اكتئاب، وسواس قهري، أكل بنوبات شَرَه",
        sfx:"تنشيط/أرق بالبداية، غثيان، صداع",
        warn:"طويل المفعول. لا تخلطه مع أدوية سيروتونين ثانية بدون طبيب."
      },
      {
        name:"إسيتالوبرام (Escitalopram)",
        klass:"SSRI",
        uses:"قلق عام، اكتئاب",
        sfx:"غثيان خفيف، صداع، تغييرات جنسية",
        warn:"يراقب طبيب أي زيادة قلق بالبداية."
      },
      {
        name:"باروكسيتين (Paroxetine)",
        klass:"SSRI",
        uses:"قلق شديد، هلع، اكتئاب",
        sfx:"نعاس، زيادة وزن محتملة، صعوبة إيقاف مفاجئ",
        warn:"إيقافه فجأة يعطي أعراض انسحاب مزعجة."
      },
      {
        name:"سيتالوبرام (Citalopram)",
        klass:"SSRI",
        uses:"اكتئاب، قلق",
        sfx:"غثيان، دوخة، نعاس خفيف",
        warn:"جرعات أعلى تحتاج مراقبة نظم القلب عند البعض."
      },
      {
        name:"فلوفوكسامين (Fluvoxamine)",
        klass:"SSRI",
        uses:"وسواس قهري بشكل خاص",
        sfx:"نعاس أو تنبيه، اضطراب معدة",
        warn:"يتداخل مع أدوية ثانية كثيرة؛ لازم دكتور يتابع."
      },

      // SNRIs
      {
        name:"فينلافاكسين (Venlafaxine / إيفكسور)",
        klass:"SNRI مضاد اكتئاب/قلق",
        uses:"قلق معمّم قوي، اكتئاب، هلع",
        sfx:"خفقان، تعرّق، احتمال ارتفاع ضغط بسيط",
        warn:"إيقاف سريع = دوخة/صدمات كهربائية بالرأس. لازم نزول تدريجي."
      },
      {
        name:"ديسفينلافاكسين (Desvenlafaxine)",
        klass:"SNRI",
        uses:"اكتئاب",
        sfx:"غثيان، تعرّق، خدران خفيف",
        warn:"نفس مبدأ فينلافاكسين بخصوص ضرورة الإيقاف التدريجي."
      },
      {
        name:"دولوكستين (Duloxetine / سيمبالتا)",
        klass:"SNRI",
        uses:"اكتئاب، ألم عصبي، قلق عام",
        sfx:"غثيان، جفاف فم، تعرّق",
        warn:"أحيانًا يراقب الكبد. يحتاج إشراف طبي."
      },

      // مضادات اكتئاب غير تقليدية
      {
        name:"بوبروبيون (Bupropion / ويلبوترين)",
        klass:"مضاد اكتئاب NDRI (دوبامين/نورأدرينالين)",
        uses:"اكتئاب، مساعد للإقلاع عن التدخين، نقص طاقة/دافعية",
        sfx:"أرق، قلق، صداع",
        warn:"يرفع خطر التشنجات بجرعات عالية أو مع أكل قليل جدًا."
      },
      {
        name:"ميرتازابين (Mirtazapine / ريميرون)",
        klass:"مضاد اكتئاب مهدئ",
        uses:"اكتئاب مع أرق أو فقدان وزن/شهية",
        sfx:"نعاس قوي، زيادة شهية وزيادة وزن",
        warn:"عادةً يُؤخذ ليل. لازم طبيب يقرر إذا مناسب."
      },
      {
        name:"ترازودون (Trazodone)",
        klass:"مضاد اكتئاب يُستخدم كثير للنوم",
        uses:"أرق مرتبط باكتئاب/قلق",
        sfx:"نعاس، دوخة صباح، جفاف فم",
        warn:"نادر جدًا يسبب انتصاب مؤلم طويل عند الرجال؛ هذي طوارئ."
      },
      {
        name:"فورتييوكسيتين (Vortioxetine)",
        klass:"مضاد اكتئاب متعدد المستقبلات السيروتونينية",
        uses:"اكتئاب مع مشاكل تركيز/تفكير",
        sfx:"غثيان خفيف غالبًا",
        warn:"أي أفكار إيذاء لازم تُبلغ الطبيب فورًا."
      },

      // مثبتات مزاج / ثنائي القطب
      {
        name:"ليثيوم (Lithium)",
        klass:"مثبت مزاج كلاسيكي",
        uses:"ثنائي القطب (نوبات هوس/اكتئاب)، يقلل خطر الانتحار عند بعض المرضى",
        sfx:"عطش، تبول متكرر، رعشة خفيفة باليد، زيادة وزن بسيطة",
        warn:"لازم فحوص دم للمستوى. جرعة خطأ ممكن تسمم خطير."
      },
      {
        name:"فالبروات / ديفالبروإكس (Valproate / Depakote)",
        klass:"مثبت مزاج/مضاد نوبات",
        uses:"هوس حاد، نوبات غضب وانفجار عند بعض الحالات",
        sfx:"زيادة وزن، نعاس، غثيان",
        warn:"يراقب الكبد والدم. يمنع الحمل بدون إشراف صارم لأنه خطير على الجنين."
      },
      {
        name:"لاموتريجين (Lamotrigine / لامكتال)",
        klass:"مثبت مزاج (يركز على الاكتئاب ثنائي القطب)",
        uses:"يقلل نوبات الاكتئاب في ثنائي القطب",
        sfx:"صداع، دوخة خفيفة",
        warn:"أي طفح جلدي جديد = طوارئ (نادر جدًا بس مهم)."
      },
      {
        name:"كاربامازيبين (Carbamazepine / تجريتول)",
        klass:"مضاد نوبات/مثبت مزاج",
        uses:"هوس، تهيج شديد، ألم عصبي وجهي",
        sfx:"دوار، نعاس، غثيان",
        warn:"يراقب تعداد الدم وإنزيمات الكبد. يتداخل مع أدوية كثيرة."
      },

      // مضادات الذهان (ذهان / فصام / هوس شديد)
      {
        name:"كويتيابين (Quetiapine / سيروكويل)",
        klass:"مضاد ذهان غير نمطي",
        uses:"ذهان، هوس، أرق شديد/قلق شديد بجرعات صغيرة (بإشراف طبي)",
        sfx:"نعاس، زيادة وزن، شهية عالية",
        warn:"يسبب خمول. لا تسوق لو نعسان."
      },
      {
        name:"أولانزابين (Olanzapine / زيبريكسا)",
        klass:"مضاد ذهان غير نمطي",
        uses:"ذهان، هوس حاد",
        sfx:"زيادة وزن قوية، جوع، نعاس",
        warn:"يراقب سكر الدم والدهون؛ ممكن يرفعها."
      },
      {
        name:"ريسبيريدون (Risperidone / ريسبردال)",
        klass:"مضاد ذهان غير نمطي",
        uses:"فصام، هوس، اندفاع/عدوانية ببعض الاضطرابات السلوكية",
        sfx:"تيبّس عضلي بسيط، نعاس، زيادة وزن متوسطة",
        warn:"بجرعات أعلى ممكن يرفع هرمون الحليب (حساسية بالصدر/إفراز)."
      },
      {
        name:"باليبيريدون (Paliperidone)",
        klass:"مضاد ذهان غير نمطي (مشابه ريسبيريدون)",
        uses:"فصام، ذهان مستمر",
        sfx:"تململ، تيبّس، زيادة وزن متوسطة",
        warn:"فيه نسخ حقن طويلة المفعول (شهرية/أكثر) بس فقط تحت إشراف طبي."
      },
      {
        name:"أريببرازول (Aripiprazole / أبيليفاي)",
        klass:"مضاد ذهان غير نمطي جزئي التأثير",
        uses:"ذهان، هوس، وأحيانًا يُضاف للاكتئاب المقاوم",
        sfx:"نشاط/أرق/عصبية بدل النعاس عند بعض الناس",
        warn:"راقب أي سلوك اندفاعي جديد (صرف فلوس بدون تفكير، أكل قهري...)."
      },
      {
        name:"زيبراسيدون (Ziprasidone / جيوودون)",
        klass:"مضاد ذهان غير نمطي",
        uses:"ذهان، هوس",
        sfx:"غثيان، دوار، احتمال تأثير على نبض القلب",
        warn:"ينبلع غالبًا مع الأكل ويحتاج مراقبة نظم القلب عند بعض المرضى."
      },
      {
        name:"لوراسيدون (Lurasidone / لاتودا)",
        klass:"مضاد ذهان غير نمطي",
        uses:"اكتئاب ثنائي القطب، ذهان",
        sfx:"غثيان خفيف، نعاس أو بالعكس تنبيه بسيط",
        warn:"عادةً أقل زيادة وزن من بعض الأدوية الثانية بس لازم إشراف."
      },
      {
        name:"كلوزابين (Clozapine / كلوزاريل)",
        klass:"مضاد ذهان غير نمطي قوي",
        uses:"فصام شديد ما تحسّن مع أدوية ثانية",
        sfx:"نعاس، سيلان لعاب، زيادة وزن",
        warn:"لازم فحوص دم دورية لكريات الدم البيضاء. بدون طبيب مستحيل يُصرف."
      },
      {
        name:"هالوبيريدول (Haloperidol / هالدول)",
        klass:"مضاد ذهان نموذجي (قديم)",
        uses:"ذهان حاد، هياج شديد (أحيانًا طوارئ)",
        sfx:"تيبّس/تشنجات عضلية حادة خصوصًا بجرعات عالية",
        warn:"يستعمل غالبًا في بيئة طبية وتحت رقابة مباشرة."
      },

      // مهدئات / قلق / نوم / أعصاب
      {
        name:"كلونازيبام (Clonazepam)",
        klass:"بنزوديازبين مهدئ",
        uses:"هلع حاد، قلق شديد مؤقت، نوبات صرع",
        sfx:"نعاس قوي، بطء تفكير، اعتماد جسدي",
        warn:"إدماني. الإيقاف المفاجئ ممكن يسبب انسحاب خطير/تشنجات."
      },
      {
        name:"ألبرازولام (Alprazolam / زاناكس)",
        klass:"بنزوديازبين قصير المفعول",
        uses:"نوبات هلع حادة، قلق شديد قصير المدى",
        sfx:"نعاس، نسيان قصير، تعلّق سريع",
        warn:"قابل للإدمان بسرعة. مو حل بعيد المدى."
      },
      {
        name:"لورازيبام (Lorazepam / أتيفان)",
        klass:"بنزوديازبين",
        uses:"قلق حاد، أرق قصير المدى، تشنجات",
        sfx:"نعاس، دوار، بطء حركة",
        warn:"نفس العائلة الإدمانية. لا توقف بدون طبيب."
      },
      {
        name:"ديازيبام (Diazepam / فاليوم)",
        klass:"بنزوديازبين أطول شوي",
        uses:"قلق، شد عضلي، انسحاب كحول طبي بإشراف",
        sfx:"نعاس، تشوش، بطء رد الفعل",
        warn:"خطر مع القيادة/الآلات. قابل للإدمان."
      },
      {
        name:"بوسبيرون (Buspirone)",
        klass:"مضاد قلق غير مهدئ تقليديًا",
        uses:"قلق معمّم طويل المدى",
        sfx:"دوار خفيف، صداع، غثيان",
        warn:"مو مسعف فوري للهلع. يحتاج وقت حتى يشتغل."
      },
      {
        name:"هيدروكسيزين (Hydroxyzine / أتركس)",
        klass:"مضاد هستامين مهدئ",
        uses:"قلق قصير المدى، صعوبة نوم بسيطة",
        sfx:"نعاس، جفاف فم",
        warn:"يسبب نوم قوي عند بعض الناس. لا تسوق قبل ما تتأكد."
      },
      {
        name:"بروبرانولول (Propranolol)",
        klass:"حاصر بيتا (ضغط/نبض)",
        uses:"قلق الأداء الجسدي (رجفة، خفقان قبل عرض أو موقف اجتماعي)",
        sfx:"تعب، برودة الأطراف، دوار خفيف",
        warn:"ما يناسب بعض حالات الربو أو الضغط المنخفض إلا بإذن طبي."
      },
      {
        name:"بريجابالين (Pregabalin / ليريكا)",
        klass:"مضاد قلق/ألم عصبي",
        uses:"قلق عام ببعض الدول، ألم أعصاب، آلام مزمنة",
        sfx:"دوخة، نعاس، إحساس 'هاي' عند بعض الناس",
        warn:"قابل لسوء الاستخدام/الإدمان، يصرف تحت إشراف فقط."
      },
      {
        name:"جابابنتين (Gabapentin)",
        klass:"عصب/ألم مزمن",
        uses:"ألم أعصاب، وأحيانًا قلق/أرق خفيف تحت إشراف",
        sfx:"دوخة، ترنّح، نعاس",
        warn:"صار يُساء استخدامه عند البعض. مو مسكّن حر."
      },
      {
        name:"زولبيديم (Zolpidem / أمبيان)",
        klass:"منوّم قصير المدى",
        uses:"أرق حاد قصير المدى",
        sfx:"نعاس، أحيانًا سلوكيات نوم غريبة (مشي/أكل)",
        warn:"مو للاستخدام الدائم يوميًا بدون تقييم. لا تاخذه مع كحول."
      },

      // ADHD / التركيز
      {
        name:"ميثيل فينيدات (Methylphenidate / ريتالين)",
        klass:"منشّط للجهاز العصبي المركزي",
        uses:"اضطراب فرط الحركة وتشتت الانتباه ADHD",
        sfx:"نقص شهية، أرق، خفقان",
        warn:"يُصرف بضوابط شديدة. إساءة الاستخدام خطر."
      },
      {
        name:"ليزدكسامفيتامين (Lisdexamfetamine / فيفانس)",
        klass:"منشّط طويل المفعول نسبيًا",
        uses:"ADHD، وأحيانًا أكل شره تحت إشراف",
        sfx:"نبض سريع، نقص شهية، أرق",
        warn:"مادة مراقَبة. لازم متابعة نبض/ضغط/وزن."
      },

      // إدمان / تعاطي
      {
        name:"نالتريكسون (Naltrexone)",
        klass:"مضاد مستقبلات الأفيون",
        uses:"تقليل الرغبة في الكحول وبعض الأفيونات",
        sfx:"غثيان، صداع، تعب",
        warn:"لا يُستخدم إذا فيه أفيون نشط بالجسم حاليًا بدون إشراف، ومهم فحص الكبد."
      },
      {
        name:"أكامبروسيت (Acamprosate / كامبرال)",
        klass:"منظّم للشهوة الكحولية بعد الإيقاف",
        uses:"يساعد يحافظ الامتناع عن شرب الكحول بعد التوقف",
        sfx:"إسهال، غثيان خفيف، أرق بسيط",
        warn:"يحتاج تقييم كلى. مهم أنك أصلًا موقف شرب قبل ما ينصرف."
      },
      {
        name:"ديسلفيرام (Disulfiram / أنتابيوس)",
        klass:"دواء ينفّر من الكحول",
        uses:"يُستخدم ببعض الحالات لمنع الشرب (يخلي شرب الكحول تجربة سيئة جدًا)",
        sfx:"غثيان شديد/خفقان/احمرار لو شربت كحول",
        warn:"لو تشرب كحول فوقه ممكن يصير تفاعل قوي جدًا وخطر. لازم وعي تام ومتابعة."
      },
      {
        name:"بوبـرينورفين/نالكسون (Buprenorphine + Naloxone / سوبوكسون)",
        klass:"علاج بديل منظم للأفيونات",
        uses:"إدمان أفيونات (هروين/مسكنات قوية)، يقلل الرغبة والانسحاب",
        sfx:"إمساك، نعاس، صداع",
        warn:"ينصرف بأنظمة مرخّصة فقط وتحت إشراف شديد. إيقافه فجأة ممكن يسبب انسحاب قوي."
      }
    ];

    function cardHTML(m){
      return `
        <div class="tile" style="border:1px solid #000;">
          <h3>${m.name}</h3>
          <div class="small"><b>الفئة:</b> ${m.klass}</div>
          <div class="small"><b>يُصرف غالبًا لـ:</b> ${m.uses}</div>
          <div class="small"><b>أعراض جانبية شائعة:</b> ${m.sfx}</div>
          <div class="note" style="margin-top:10px;">
            <b>تحذير سريع:</b> ${m.warn}
          </div>
          <div class="small" style="margin-top:8px;color:#444;font-weight:600;">
            هذا ليس بديل زيارة طبيب/صيدلي. لا تعدّل جرعة ولا توقف فجأة بدون إشراف.
          </div>
        </div>
      `;
    }

    function renderAll(){
      const box = document.getElementById('medList');
      if(!box) return;
      let out = "";
      MEDS.forEach(m => { out += cardHTML(m); });
      box.innerHTML = out;
    }

    window.filterMeds = function(){
      const q = (document.getElementById('drugSearch').value || "").toLowerCase().trim();
      const box = document.getElementById('medList');
      if(!box) return;
      if(!q){
        renderAll();
        return;
      }
      let out = "";
      MEDS.forEach(m=>{
        const blob = (m.name+" "+m.klass+" "+m.uses).toLowerCase();
        if(blob.indexOf(q)>=0){
          out += cardHTML(m);
        }
      });
      if(!out){
        out = `
          <div class="tile" style="border:1px solid #000;">
            <h3>ما لقينا</h3>
            <div class="small">جرّب تكتب جزء من اسم الدواء أو الحالة (مثال: "ذهان" أو "قلق")</div>
          </div>
        `;
      }
      box.innerHTML = out;
    };

    // أول ما تفتح الصفحة نرسم كل الأدوية
    renderAll();
  </script>

</div>
"""

def render_pharm_page():
    return PHARM_PAGE_HTML\
        .replace("[[PSYCHO_WA]]", PSYCHO_WA)\
        .replace("[[PSYCH_WA]]", PSYCH_WA)\
        .replace("[[SOCIAL_WA]]", SOCIAL_WA)

@app.get("/pharm")
def pharm():
    return shell("دليل الأدوية النفسية — " + BRAND, render_pharm_page(), "pharm")


# ======================== /health ========================

@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "brand": BRAND,
        "build": CACHE_BUST
    }), 200


# ======================== Security headers ========================

@app.after_request
def add_headers(resp):
    # CSP يحمي قدر الإمكان (يسمح بالـ inline لأن الصفحة ملف واحد)
    csp = (
        "default-src 'self' data: blob: https://t.me https://wa.me https://api.whatsapp.com; "
        "script-src 'self' 'unsafe-inline' data: blob: https://t.me https://wa.me https://api.whatsapp.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob: *; "
        "connect-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors *"
    )
    resp.headers['Content-Security-Policy'] = csp
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return resp
# ========= [اختبارات نفسية / شخصية] =========
# نحط هذا المقطع داخل app.py مع بقية الكود
# 1) الداتا
TESTS_DATA = [
    {
        "code": "phq9",
        "name": "مقياس الاكتئاب (PHQ-9)",
        "desc": "يساعدك تشوف شدة الأعراض الاكتئابية مثل المزاج المنخفض، فقدان المتعة، التعب… آخر أسبوعين.",
        "items": [
            "قلة الاهتمام / عدم الاستمتاع بالأشياء",
            "شعور بالحزن أو الإحباط أو اليأس",
            "مشاكل في النوم (زيادة أو قلة نوم)",
            "إرهاق أو نقص بالطاقة",
            "قلة الشهية أو أكل كثير",
            "شعور سيّئ عن نفسك أو أنك فاشل",
            "صعوبة التركيز (مثل قراءة أو متابعة برنامج)",
            "الحركة بطيئة جدًا أو عصبية/تململ زيادة",
            "أفكار أنك تؤذي نفسك أو لو أنك تموت"
        ],
        "score_help": "10 نقاط أو أكثر = يفضل تقييم طبي/نفسي حقيقي، خصوصًا لو فيه أفكار أذى."
    },
    {
        "code": "gad7",
        "name": "مقياس القلق (GAD-7)",
        "desc": "يقيس التوتر/القلق العام: توتر، صعوبة تهدئة النفس، عصبية، توتر عضلي… آخر أسبوعين.",
        "items": [
            "الشعور بالتوتر أو القلق أو على أعصابك",
            "عدم القدرة على إيقاف القلق أو السيطرة عليه",
            "القلق الزائد عن أشياء يومية",
            "صعوبة الاسترخاء",
            "الشعور بالعصبية لدرجة صعبة تجلس بثبات",
            "الانزعاج بسهولة أو العصبية السريعة",
            "الخوف من أن شيء سيء سيحدث"
        ],
        "score_help": "درجات أعلى تعني قلق أعلى. إذا القلق معطل حياتك اليومية → استشارة مختص."
    },
    {
        "code": "asd",
        "name": "مؤشرات تشتت/اندفاع (نمط ADHD ذاتي)",
        "desc": "مؤشرات صعوبة التركيز/الاندفاع/التنظيم عند البالغين. هذا مو تشخيص رسمي.",
        "items": [
            "سهولة التشتت / الشرود الذهني",
            "نسيان مواعيد أو أشياء أساسية",
            "تترك المهام مفتوحة بدون إنهاء",
            "اندفاع بالكلام / المقاطعة قبل دورك",
            "صعوبة الجلوس فترة طويلة بدون حركة",
            "ضعف تنظيم الوقت / دايم مستعجل أو متأخر",
            "تأجيل مزمن حتى مع مهام مهمة"
        ],
        "score_help": "إذا أغلبها ‘غالبًا/دائمًا’ وتسبب مشاكل في الدراسة/الوظيفة → فحص عند مختص اضطرابات انتباه."
    },
    {
        "code": "bsi_ang",
        "name": "غضب / تحكم في الانفعال",
        "desc": "يساعدك تعرف إذا الغضب صار سريع أو خطر على علاقاتك/أمانك.",
        "items": [
            "أصرخ أو أنفجر بسرعة",
            "أندم بعد النوبة لأنني جرحت شخص قريب مني",
            "صعوبة أهدى لما أحد يستفزني",
            "أفكّر أنفجر جسديًا (أكسر شي/أدفع أحد)",
            "يحصل خلافات حادة بشكل متكرر",
            "أقسو على نفسي بعد الغضب ('أنا وحش / ما أستحق أحد')"
        ],
        "score_help": "لو فيه غضب مع عنف أو أفكار أذية لغيرك → تدخل عاجل مع مختص أو تدخل أسري آمن."
    }
]

# 2) صفحة HTML ديناميكية
def render_tests_page():
    cards_html_parts = []
    for t in TESTS_DATA:
        q_list = []
        for idx, q in enumerate(t["items"], start=1):
            q_html = f"""
            <div style="border:1px solid #000;border-radius:12px;padding:10px;margin-bottom:10px;background:#fff;">
              <div style="font-weight:700;color:var(--p);margin-bottom:6px;">{idx}. {q}</div>
              <div class="row" style="gap:6px;">
                <label class="badge2"><input type="radio" name="{t['code']}_q{idx}" value="0"> أبداً</label>
                <label class="badge2"><input type="radio" name="{t['code']}_q{idx}" value="1"> أحياناً</label>
                <label class="badge2"><input type="radio" name="{t['code']}_q{idx}" value="2"> غالباً</label>
                <label class="badge2"><input type="radio" name="{t['code']}_q{idx}" value="3"> دائمًا / مزعج جدًا</label>
              </div>
            </div>
            """
            q_list.append(q_html)

        card_html = f"""
        <div class="tile" style="border:2px solid #000;">
          <h3 style="margin-bottom:4px;">🧪 {t['name']}</h3>
          <p class="small" style="margin-top:0;">{t['desc']}</p>

          <div style="font-size:.8rem;font-weight:600;color:#5c4a00;background:var(--note-bg);border:1px dashed var(--note-border);border-radius:var(--radius-md);padding:8px 10px;margin:10px 0;">
            اختيارك هنا يبقى في جهازك فقط (localStorage). ما نرسل أي إجابات للسيرفر.
          </div>

          <div id="{t['code']}_block">
            {''.join(q_list)}
          </div>

          <div class="row" style="margin-top:10px;">
            <button class="btn gold" onclick="calcScore('{t['code']}', {len(t['items'])}, '{t['score_help']}')">احسب الدرجة</button>
            <button class="btn alt" onclick="saveTest('{t['code']}', '{t['name']}', {len(t['items'])})">💾 حفظ JSON</button>
          </div>

          <div id="{t['code']}_result" style="margin-top:10px;font-size:.9rem;font-weight:700;color:#4b0082;"></div>
        </div>
        """
        cards_html_parts.append(card_html)

    page_html = f"""
<div class="card" style="border:2px solid #000;">
  <h1>🧪 اختبارات نفسية / شخصية (تقدير ذاتي)</h1>

  <div class="note">
    مهم:
    <br/>• هذه أدوات فرز مبدئي (screening)، مو تشخيص نهائي.
    <br/>• الدرجات العالية = يستحسن تشوف مختص بشري.
    <br/>• لو عندك أفكار أذى نفسك أو غيرك هذا طارئ، مو مجرد اختبار.
  </div>

  <p class="small">
    اختر إجابة لكل سؤال، بعدها اضغط "احسب الدرجة".
    تقدر بعدين تحفظ نتيجتك كملف JSON عندك.
  </p>

  <div class="grid">
    {''.join(cards_html_parts)}
  </div>

  <div class="divider"></div>

  <h3>هل تحتاج تتكلم مع أحد الآن؟</h3>
  <div class="row screen-only">
    <a class="btn" href="{PSYCHO_WA}" target="_blank" rel="noopener">👨‍🎓 أخصائي نفسي (CBT / سلوكي)</a>
    <a class="btn" href="{PSYCH_WA}"  target="_blank" rel="noopener">👨‍⚕️ طبيب نفسي (أدوية)</a>
    <a class="btn" href="{SOCIAL_WA}" target="_blank" rel="noopener">🤝 أخصائي اجتماعي (دعم حياتي)</a>
  </div>
  <script>
// حساب مجموع النقاط وعرض النتيجة
function calcScore(code, count, helpText) {
  let total = :0
  for (let i = 1; i <= count; i++) {
    const sel = document.querySelector('input[name="'+code+'_'+i+'"]:checked');
    if (sel) {
      total += parseInt(sel.value || "0", 10);
    }
  }

  const out = document.getElementById(code + "_result");
  out.innerHTML = "<p>المجموع الكلي: <b>" + total + "</b><br/><br/>" + helpText + "<br/><span style='font-size:.8rem;color:#a00;'>⚠️ هذه ليست تشخيصًا نهائيًا. إذا لديك خطر على نفسك أو غيرك تواصل فورًا مع مختص.</span></p>";

  try {
    const key = "test_history_" + code;
    localStorage.setItem(key, JSON.stringify({ score: total, ts: new Date().toISOString() }));
  } catch(e) {}
}
</script>
  const answers = [];
      for (let i=1;i<=count;i++){
        const sel = document.querySelector('input[name="'+code+'_q'+i+'"]:checked');
        answers.push(sel ? parseInt(sel.value,10) : null);
      }
      const data = {{
        test: code,
        name: name,
        answers: answers,
        build: window.__BUILD__,
        saved_at: new Date().toISOString()
      }};
      const a = document.createElement('a');
      a.href = URL.createObjectURL(
        new Blob([JSON.stringify(data,null,2)], {{type:'application/json'}})
      );
      a.download = code + "_result.json";
      a.click();
      URL.revokeObjectURL(a.href);
    }
  </script>

</div>
"""
    return page_html

# 3) الراوت الجديد /tests
@app.route("/tests")
def tests_page():
    page_html = r"""
<div class="card" style="border:2px solid #000;max-width:900px;margin:auto;">
  <h1>🧪 اختبارات نفسية / شخصية (مساعدة ذاتية)</h1>

  <div class="small">
    هذه الأدوات تعطيك فكرة عن نمط الأعراض أو السمات، مو تشخيص طبي رسمي.
    إذا النتيجة عالية جدًا أو فيها خطر على سلامتك، تواصل مع مختص فورًا.
  </div>

  <div class="note">
    ⚠️ النتائج تُحسب محليًا في جهازك (JavaScript + localStorage)
    وما تنرفع لسيرفر. يعني خصوصيتك عندك.
  </div>

  <h2 style="margin-top:24px">اختَر اختبار:</h2>

  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;">
    <div class="tile" style="border:1px solid #000;">
      <h3>اكتئاب / مزاج منخفض (تقريبي)</h3>
      <p class="small">
        أسئلة عن المزاج، الطاقة، الإحساس بالقيمة الذاتية، والأفكار السلبية.
      </p>
      <button class="btn gold" onclick="openTest('dep')">ابدأ</button>
    </div>

    <div class="tile" style="border:1px solid #000;">
      <h3>قلق عام / توتر مزمن</h3>
      <p class="small">
        قلق زائد، صعوبة تهدئة المخ، شد عضلي، نوم متأثر.
      </p>
      <button class="btn gold" onclick="openTest('anx')">ابدأ</button>
    </div>

    <div class="tile" style="border:1px solid #000;">
      <h3>نوبات هلع / خوف من الهلع</h3>
      <p class="small">
        أسئلة حول الأعراض الجسدية المفاجئة، الخوف من تكرارها، وتجنّب أماكن.
      </p>
      <button class="btn gold" onclick="openTest('panic')">ابدأ</button>
    </div>

    <div class="tile" style="border:1px solid #000;">
      <h3>تنظيم الغضب / الاندفاع</h3>
      <p class="small">
        هل الغضب يطلع بسرعة وبقوة؟ هل تندم بعد الانفجار؟
      </p>
      <button class="btn gold" onclick="openTest('anger')">ابدأ</button>
    </div>

    <div class="tile" style="border:1px solid #000;">
      <h3>تشتت / تفرّد الانتباه (سمات ADHD)</h3>
      <p class="small">
        تشتت، نسيان، عدم تنظيم، اندفاع.
      </p>
      <button class="btn gold" onclick="openTest('adhd')">ابدأ</button>
    </div>
  </div>

  <div class="divider" style="margin-top:24px;"></div>

  <h2 id="test-title" style="display:none;margin-top:10px;"></h2>

  <form id="test-form" style="display:none;">
    <div id="test-questions" class="small" style="line-height:1.9;"></div>

    <div class="row" style="margin-top:16px;flex-wrap:wrap;">
      <button class="btn gold" type="button" onclick="calcScore()">احسب الدرجة</button>
      <button class="btn alt" type="button" onclick="resetTest()">مسح</button>
      <button class="btn" type="button" onclick="window.print()">🖨️ طباعة</button>
    </div>

    <div id="score-box" class="note" style="margin-top:16px; display:none;"></div>
  </form>

  <div class="divider" style="margin-top:24px;"></div>

  <div class="row screen-only" style="margin-top:10px">
    <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">🟢 واتساب دعم</a>
    <a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">✈️ تيليجرام دعم</a>
    <a class="btn" href="{PSYCHO_WA}" target="_blank" rel="noopener">👨‍🎓 أخصائي نفسي</a>
    <a class="btn" href="{PSYCH_WA}"  target="_blank" rel="noopener">👨‍⚕️ طبيب نفسي</a>
  </div>

  <script>
    // بنك الأسئلة
    // كل اختبار له:
    //  title: عنوان
    //  help:  نص توضيح بعد الحساب
    //  items: مصفوفة أسئلة (0=أبدا ... 3=شديد مثلا)
    const TESTS = {
      dep: {
        title: "مؤشرات مزاج منخفض / اكتئاب",
        help: "درجة أعلى = مزاج منخفض وتأثير واضح على الحياة اليومية. هذا لا يغني عن تقييم مختص. لو فيه أفكار إيذاء النفس/انتحار لازم دعم عاجل.",
        items: [
          "أحس مزاجي نازل/حزين أغلب اليوم؟",
          "صرت أفقد الاهتمام أو المتعة بالأشياء اللي كانت تهمني؟",
          "تعب شديد / طاقة منخفضة حتى لو ما سويت شي؟",
          "نوم مضروب (أرق أو نوم كثير جدًا)؟",
          "أحس بقيمة ذاتية منخفضة / جلد ذاتي / ذنب؟",
          "تركيزي صار أضعف / أفكاري بطيئة؟",
          "أفكار الموت / الانسحاب من الحياة / ما أبغى أكمّل؟"
        ]
      },
      anx: {
        title: "قلق معمّم / توتر مستمر",
        help: "درجة أعلى = قلق عالي أو توتر جسدي/ذهني مستمر. لو القلق قاعد يخرب نومك أو شغلك أو علاقاتك اطلب دعم.",
        items: [
          "أقلق على أشياء كثيرة بنفس الوقت وصعب أوقف التفكير؟",
          "عضلاتي مشدودة / جسمي متوتر أغلب الوقت؟",
          "صرت أنفجر بسرعة (نرفزة/انفعال عالي)؟",
          "القلق مأثر على نومي؟",
          "انتباهي/تركيزي يروح بسرعة بسبب القلق؟",
          "قلبي يدق بسرعة/أحس برجفة أو ضيق صدر بدون سبب واضح؟",
          "أخاف إنه بيصير شي سيء قريب (كارثة جاية)؟"
        ]
      },
      panic: {
        title: "نوبات هلع / خوف من الهلع",
        help: "درجة أعلى = احتمال وجود نوبات هلع أو خوف/تجنّب بسببها. نوبات الهلع بحد ذاتها مو قاتلة، لكن الإحساس فعلاً يخوّف. لو توصل لحد ما تظن أنك بتموت اتصل بمختص.",
        items: [
          "صار لي فجأة خفقان قوي / صعوبة تنفس / دوخة / إحساس بموت قريب؟",
          "الفجعة كانت خلال دقائق، قوية جدًا؟",
          "بعدها بقي عندي خوف إنها ترجع؟",
          "صرت أتجنّب أماكن أو مواقف عشان ما تجيني النوبة؟",
          "أحتاج أحد يكون جنبي (شعور أمان) عشان أطلع لبعض الأماكن؟",
          "أقرأ جسمي وأراقب أي إحساس بسيط وأفسره كأنه خطر كبير؟"
        ]
      },
      anger: {
        title: "التحكم بالغضب / الاندفاع",
        help: "درجة أعلى = صعوبة تهدئة الغضب أو اندفاع بالأفعال/الكلام قبل التفكير. لو الغضب يسبب أذى لنفسك أو للي حولك اطلب تدخل محترف.",
        items: [
          "أغضب بسرعة وبقوة أكثر من أغلب الناس؟",
          "أصرخ/أكسر/أهدد بدون ما أفكر؟",
          "بعد ما أهدى أندم على اللي قلت/سويت؟",
          "أحس الغضب يطلع بدون تحكم، كأنه ينفجر؟",
          "الناس حولي يخافون من ردة فعلي؟",
          "الغضب يخرب علاقاتي أو شغلي؟"
        ]
      },
      adhd: {
        title: "سمات تشتت/اندفاع (نمط ADHD)",
        help: "درجة أعلى = صعوبة مستمرة في الانتباه/التنظيم/الوقت، أو اندفاع. التشخيص الرسمي لاضطراب فرط الحركة وتشتت الانتباه لازم يكون من مختص ويشمل تاريخ من الطفولة.",
        items: [
          "أنسى أشياء أساسية (مواعيد، أغراض، مهام) بسهولة؟",
          "أدخل في مهام وأتشتت بسرعة حتى لو مهمة؟",
          "أأجل بشكل مزمن وأتورط في آخر لحظة؟",
          "صعب أجلس مكاني بدون حركة / أتوتر بسرعة؟",
          "أقاطع الناس أو أتكلم قبل ما يخلصوا؟",
          "أضيع الإحساس بالوقت وأتأخر كثير؟",
          "التنظيم اليومي (أوراق/فلوس/مشتريات) فوضى؟"
        ]
      }
    };

    // الحالة الحالية
    let currentCode = null;

    // فتح اختبار
    function openTest(code){
      if(!TESTS[code]) return;
      currentCode = code;

      const boxTitle = document.getElementById('test-title');
      const formEl   = document.getElementById('test-form');
      const qBox     = document.getElementById('test-questions');
      const scoreBox = document.getElementById('score-box');

      // عنوان
      boxTitle.textContent = "📋 " + TESTS[code].title;
      boxTitle.style.display = 'block';

      // بناء الأسئلة
      const items = TESTS[code].items;
      let html = "<div style='font-size:.95rem;color:#2b1a4c;'>";
      html += "<p><b>التعليمات:</b> لكل سطر اختر أقرب شي لك بالفترة الحالية.<br/>0 = أبداً / نادرًا &nbsp;·&nbsp; 1 = شوي &nbsp;·&nbsp; 2 = واضح &nbsp;·&nbsp; 3 = شديد</p>";
      for(let i=0;i<items.length;i++){
        html += "<div style='margin:10px 0;padding:12px;border:1px solid #ddd;border-radius:8px;background:#fff;box-shadow:0 4px 10px rgba(0,0,0,.03);'>";
        html += "<div style='margin-bottom:8px;font-weight:600;color:#4b0082;'>"+(i+1)+") "+items[i]+"</div>";
        html += "<label class='badge2' style='margin-left:8px;'>0 <input type='radio' name='q"+i+"' value='0'></label>";
        html += "<label class='badge2' style='margin-left:8px;'>1 <input type='radio' name='q"+i+"' value='1'></label>";
        html += "<label class='badge2' style='margin-left:8px;'>2 <input type='radio' name='q"+i+"' value='2'></label>";
        html += "<label class='badge2' style='margin-left:8px;'>3 <input type='radio' name='q"+i+"' value='3'></label>";
        html += "</div>";
      }
      html += "</div>";

      qBox.innerHTML = html;
      formEl.style.display = 'block';
      scoreBox.style.display = 'none';
      scoreBox.innerHTML = '';
      window.scrollTo({top: boxTitle.offsetTop-20, behavior:'smooth'});
    }

    // مسح
    function resetTest(){
      if(!currentCode) return;
      const formEl   = document.getElementById('test-form');
      const scoreBox = document.getElementById('score-box');
      formEl.querySelectorAll('input[type=radio]').forEach(r => { r.checked = false; });
      scoreBox.style.display='none';
      scoreBox.innerHTML='';
    }

    // حساب الدرجة
    function calcScore(){
      if(!currentCode || !TESTS[currentCode]) return;
      const items = TESTS[currentCode].items;
      let total = 0;
      for (let i=0;i<items.length;i++){
        const sel = document.querySelector('input[name="q'+i+'"]:checked');
        if(sel){
          total += parseInt(sel.value,10);
        }
      }

      const helpText = TESTS[currentCode].help;
      const scoreBox = document.getElementById('score-box');
      scoreBox.style.display='block';
      scoreBox.innerHTML =
        "الدرجة الكلية: <b>"+total+"</b><br/>"+
        helpText+
        "<br/><span style='font-size:.8rem;color:#a00;'>🔴 في حال وجود أفكار أذى للنفس أو للآخرين: هذا طارئ نفسي/طبي الآن، لا تنتظر.</span>";

      // حفظ محلي
      try{
        localStorage.setItem(
          "last_score_"+currentCode,
          JSON.stringify({score:total, ts:new Date().toISOString()})
        );
      }catch(e){}
    }
  </script>

</div>
"""
    return page_html
    # ======================== /tests ========================
# صفحة اختبارات نفسية بسيطة (اكتئاب / قلق) مع جمع النقاط بالـ JS فقط.
# ملاحظة: هذا للتوعية فقط، مو تشخيص طبي.

@app.get("/tests")
def tests_page():
    return """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>الاختبارات النفسية الأولية</title>
<style>
  body{
    background:#f8f6ff;
    font-family:"Tajawal","Segoe UI",system-ui,sans-serif;
    line-height:1.8;
    color:#2b1a4c;
    padding:20px;
    direction:rtl;
    text-align:right;
  }
  .wrap{
    max-width:800px;
    margin:0 auto;
    background:#fff;
    border:2px solid #000;
    border-radius:16px;
    box-shadow:0 10px 24px rgba(0,0,0,.06);
    padding:20px 20px 32px;
  }
  h1{
    font-size:24px;
    font-weight:800;
    color:#4B0082;
    margin-top:0;
    line-height:1.4;
  }
  h2{
    font-size:18px;
    font-weight:800;
    color:#4B0082;
    margin:24px 0 8px;
  }
  .note{
    background:#fff7d1;
    border:1px dashed #e5c100;
    border-radius:10px;
    padding:10px 12px;
    font-size:.9rem;
    font-weight:600;
    color:#5c4a00;
    box-shadow:0 4px 10px rgba(0,0,0,.05);
    line-height:1.6;
  }
  .q-block{
    background:#fafafa;
    border:1px solid #ddd;
    border-radius:12px;
    padding:14px;
    margin:10px 0 16px;
    box-shadow:0 6px 12px rgba(0,0,0,.04);
  }
  .q-title{
    font-weight:700;
    color:#2b1a4c;
    font-size:1rem;
    margin-bottom:8px;
  }
  label.opt{
    display:block;
    background:#fff;
    border:1px solid #ccc;
    border-radius:10px;
    padding:8px 10px;
    margin:6px 0;
    font-size:.9rem;
    line-height:1.5;
    cursor:pointer;
    box-shadow:0 4px 10px rgba(0,0,0,.03);
  }
  label.opt input{
    margin-left:6px;
    transform:scale(1.2);
  }
  .btn-row{
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    margin-top:20px;
  }
  .btn{
    background:#4B0082;
    color:#fff;
    font-weight:800;
    text-decoration:none;
    border:1px solid #000;
    border-radius:10px;
    box-shadow:0 4px 12px rgba(0,0,0,.25);
    padding:10px 14px;
    font-size:.9rem;
    line-height:1.4;
    cursor:pointer;
    min-width:fit-content;
    text-align:center;
  }
  .btn.gold{
    background:#FFD700;
    color:#4B0082;
  }
  .result-box{
    margin-top:24px;
    background:#fff;
    border:2px solid #000;
    border-radius:12px;
    padding:16px;
    box-shadow:0 10px 24px rgba(0,0,0,.07);
    font-size:.95rem;
    line-height:1.7;
  }
  .result-box h3{
    margin-top:0;
    font-size:1rem;
    font-weight:800;
    color:#4B0082;
  }
  .danger{
    color:#a00000;
    font-weight:700;
  }
  .links-row{
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    margin-top:16px;
  }
  .mini-link{
    background:#fff;
    border:1px solid #000;
    border-radius:10px;
    padding:8px 10px;
    font-weight:700;
    font-size:.8rem;
    text-decoration:none;
    color:#4B0082;
    box-shadow:0 4px 10px rgba(0,0,0,.1);
  }
</style>
</head>
<body>

<div class="wrap">
  <h1>🧪 اختبارات أولية (اكتئاب / قلق)</h1>

  <div class="note">
    هذي أسئلة سريعة تساعدك تشوف "هل الوضع يستاهل اهتمام؟".
    مو تشخيص طبي نهائي، ولا تغني عن دكتور أو أخصائي.
    لو فيه أفكار انتحار/إيذاء نفسك أو غيرك 👇 هذا طارئ.
  </div>

  <!-- ===== اكتئاب (نمط PHQ-9 مبسّط) ===== -->
  <h2>أولًا: المزاج / الاكتئاب آخر أسبوعين</h2>

  <div class="q-block">
    <div class="q-title">1. مزاج منخفض / إحساس بالحزن أو الفراغ أغلب اليوم؟</div>
    <label class="opt"><input type="radio" name="dep1" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="dep1" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="dep1" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="dep1" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="q-block">
    <div class="q-title">2. فقدان الاهتمام / ما عاد تتهنى بأشياء كنت تحبها؟</div>
    <label class="opt"><input type="radio" name="dep2" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="dep2" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="dep2" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="dep2" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="q-block">
    <div class="q-title">3. نومك (صعوبة نوم / نوم كثير بزيادة / تقوم تعبان)؟</div>
    <label class="opt"><input type="radio" name="dep3" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="dep3" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="dep3" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="dep3" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="q-block">
    <div class="q-title">4. إحساس بالتعب / نقص طاقة حتى لو ما سويت شيء كبير؟</div>
    <label class="opt"><input type="radio" name="dep4" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="dep4" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="dep4" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="dep4" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="q-block">
    <div class="q-title">5. جلد ذات / إحساس إنك فاشل أو عبء على الناس؟</div>
    <label class="opt"><input type="radio" name="dep5" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="dep5" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="dep5" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="dep5" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="q-block">
    <div class="q-title">6. صعوبة تركيز (تشتت، ما تقدر تكمّل شغلة بسيطة)؟</div>
    <label class="opt"><input type="radio" name="dep6" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="dep6" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="dep6" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="dep6" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="q-block">
    <div class="q-title danger">7. أفكار أذى نفسك / ما تبي تكمل / تمني الموت؟</div>
    <label class="opt"><input type="radio" name="dep7" value="0">أبدًا ما جاني كذا</label>
    <label class="opt"><input type="radio" name="dep7" value="1">مر علي شوي</label>
    <label class="opt"><input type="radio" name="dep7" value="2">يوميًا تقريبًا</label>
    <label class="opt"><input type="radio" name="dep7" value="3">أفكار قوية ومخيفة الآن</label>
  </div>

  <!-- ===== قلق (GAD-7 مبسّط) ===== -->
  <h2>ثانيًا: القلق / التوتر آخر أسبوعين</h2>

  <div class="q-block">
    <div class="q-title">1. قلق أو توتر زيادة عن اللزوم، صعب تهديه؟</div>
    <label class="opt"><input type="radio" name="anx1" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="anx1" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="anx1" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="anx1" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="q-block">
    <div class="q-title">2. صعوبة تتحكم بالقلق / يسيطر على بالك؟</div>
    <label class="opt"><input type="radio" name="anx2" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="anx2" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="anx2" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="anx2" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="q-block">
    <div class="q-title">3. توتر جسدي (شد عضلات، قلب يدق بقوة، تململ)؟</div>
    <label class="opt"><input type="radio" name="anx3" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="anx3" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="anx3" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="anx3" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="q-block">
    <div class="q-title">4. صرت عصبي وسريع الانفعال بسهولة؟</div>
    <label class="opt"><input type="radio" name="anx4" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="anx4" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="anx4" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="anx4" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="q-block">
    <div class="q-title">5. صعوبة تهدى / تهدي مخك قبل النوم؟</div>
    <label class="opt"><input type="radio" name="anx5" value="0">تقريبًا أبدًا</label>
    <label class="opt"><input type="radio" name="anx5" value="1">بعض الأيام</label>
    <label class="opt"><input type="radio" name="anx5" value="2">نصف الوقت تقريبًا</label>
    <label class="opt"><input type="radio" name="anx5" value="3">تقريبًا كل يوم</label>
  </div>

  <div class="btn-row">
    <button class="btn gold" onclick="calcAll()">احسب النتيجة</button>
    <a class="btn" href="/">🏠 الرئيسية</a>
    <a class="btn" href="/case">📝 دراسة الحالة</a>
    <a class="btn" href="/cbt">🧠 CBT</a>
    <a class="btn" href="/pharm">💊 الأدوية</a>
  </div>

  <div id="resultsBox" class="result-box" style="display:none;">
    <h3>نتيجتك المبدئية</h3>
    <div id="resText" style="white-space:pre-line"></div>

    <div class="links-row">
      <a class="mini-link" href="/cbt">خطط CBT لك</a>
      <a class="mini-link" href="/case">إعادة دراسة الحالة</a>
      <a class="mini-link" href="/pharm">معلومات الأدوية</a>
    </div>

    <div style="margin-top:12px;font-size:.8rem;color:#555;line-height:1.6;">
      هذا الكلام للتوعية فقط، مو بديل تشخيص طبي رسمي.
      لو فيه أفكار أذى نفسك أو غيرك: هذا طارئ، لازم دعم فوري.
    </div>
  </div>

</div>

<script>
function sumGroup(prefix, count){
  let total = 0;
  for(let i=1;i<=count;i++){
    const sel = document.querySelector('input[name="'+prefix+i+'"]:checked');
    if(sel){
      total += parseInt(sel.value,10);
    }
  }
  return total;
}

function levelDesc(score, type){
  // type = "dep" أو "anx"
  // وصف بسيط بناءً على مجموع النقاط
  if(type==="dep"){
    if(score>=15) return "أعراض اكتئابية عالية. تحتاج تدخل مهني بسرعة.";
    if(score>=10) return "أعراض اكتئابية متوسطة. واضح أنك تعاني، مهم تتكلم مع مختص.";
    if(score>=5)  return "أعراض اكتئابية خفيفة/ملحوظة. راقب مزاجك وخذها جد.";
    return "أعراض اكتئابية قليلة حسب إجاباتك.";
  }
  if(type==="anx"){
    if(score>=15) return "توتر/قلق عالي جدًا مأثر على يومك.";
    if(score>=10) return "قلق متوسط. واضح أنه مسبب ضغط عليك.";
    if(score>=5)  return "قلق خفيف/ملحوظ. انتبه لنومك وتنفسك.";
    return "قلق منخفض حسب إجاباتك.";
  }
  return "";
}

function calcAll(){
  const depScore = sumGroup("dep",7);
  const anxScore = sumGroup("anx",5);

  let crisis = false;
  const dep7 = document.querySelector('input[name="dep7"]:checked');
  if(dep7){
    const v = parseInt(dep7.value,10);
    if(v>=2){ crisis = true; }
  }

  let text = "";
  text += "مجموع (اكتئاب/المزاج): " + depScore + "/21\n";
  text += levelDesc(depScore,"dep") + "\n\n";

  text += "مجموع (القلق/التوتر): " + anxScore + "/15\n";
  text += levelDesc(anxScore,"anx") + "\n\n";

  if(crisis){
    text += "🚨 تنبيه أمان مهم:\n";
    text += "ذكرت أفكار إيذاء/انتحار قوية.\n";
    text += "هذا وضع طارئ، لازم تواصل مع مختص الآن أو دعم طوارئ محلّي.\n";
  } else {
    text += "💡 نصيحة:\n";
    text += "لو حسّيت الوضع قاعد يطلع عن سيطرتك، خلك شجاع واطلب مساعدة مهنية.\n";
  }

  const box  = document.getElementById("resultsBox");
  const out  = document.getElementById("resText");
  out.textContent = text;
  box.style.display = "block";
}
</script>

</body>
</html>
"""
# ======================== /tests ========================
# صفحة الاختبارات النفسية والشخصية
# ملاحظة مهمة:
# - النتائج هنا توعوية فقط، مو تشخيص نهائي ولا تقرير رسمي.
# - إذا النتيجة عالية أو فيها خطر على الأمان الشخصي → لازم مختص بشري / طوارئ.

TESTS_DATA = {
    "depression_phq9": {
        "title": "فحص الاكتئاب (PHQ-9 مبسّط)",
        "about": "يقيس أعراض الاكتئاب (مزاج منخفض، متعة قليلة، نوم، طاقة...). يستعمل عالمياً كأداة فحص أولي.",
        "disclaimer": "لو النتيجة عالية أو عندك أفكار إيذاء نفسك لازم دكتور/أمان فوري.",
        "questions": [
            "خلال آخر أسبوعين: مزاجك منخفض أو حزين؟",
            "ما عاد تستمتع بالأشياء اللي كانت تعجبك؟",
            "نومك متلخبط (قلة نوم أو نوم كثير)؟",
            "تشعر بتعب أو نقص طاقة أغلب الوقت؟",
            "شهيتك قليلة أو بالعكس تاكل زيادة غير طبيعي؟",
            "تحس إنك فاشل / سيء / تلوم نفسك زيادة؟",
            "صاير تركيزك ضعيف (حتى أشياء بسيطة)؟",
            "حركتك بطيئة أو بالعكس عصبي ومتوتر طول اليوم؟",
            "جتك أفكار إنه ما في داعي تعيش / أفكار بإيذاء نفسك؟"
        ],
        "risk_flag_question_index": 8  # لو هذا السؤال = "نعم" نرفع تحذير أمان
    },

    "anxiety_gad7": {
        "title": "فحص القلق العام (GAD-7 مبسّط)",
        "about": "يشيّك هل القلق مسيطر عليك بشكل مبالغ (توتر، عصبية، صعوبة استرخاء...).",
        "disclaimer": "القلق العالي يحتاج خطة سلوكية أو تدخل مختص.",
        "questions": [
            "تشعر بتوتر أو قلق أغلب اليوم؟",
            "صعب عليك توقف التفكير والقلق؟",
            "في جسمك شد / رجفة / خفقان ملحوظ؟",
            "تنرفز بسرعة / أعصابك تولّع بسرعة؟",
            "صاير عندك خوف من شيء سيء بيصير؟",
            "صعوبة تنام لأن بالك مشغول بالقلق؟",
            "صعب تركز لأن بالك مشغول بالخوف؟"
        ],
        "risk_flag_question_index": None
    },

    "panic_screen": {
        "title": "فحص نوبات الهلع السريعة",
        "about": "هذا يساعد يفرّق بين قلق عام و(نوبات هلع مفاجئة قوية جدًا بجسمك وخوف من الموت).",
        "disclaimer": "لو عندك أعراض قلب/تنفس قوية لازم استبعاد طبي فوري.",
        "questions": [
            "يجيك فجأة خفقان قلب قوي / ضيق نفس / دوخة قوية مرة؟",
            "تحس لحظتها إنك بتموت أو بتفقد السيطرة؟",
            "صرت تخاف ترجع لك النوبة من جديد؟",
            "بدأت تتجنب أماكن معيّنة خوف تجيك فيها النوبة؟"
        ],
        "risk_flag_question_index": 0
    },

    "ocd_check": {
        "title": "فحص وسواس قهري (وساوس + أفعال قهرية)",
        "about": "يساعد يوضح إذا عندك أفكار مزعجة/متكررة تدفعك لطقوس (غسل، تفقد، ترتيب...).",
        "disclaimer": "علاج الـOCD غالباً يكون سلوكي معرفي (ERP) وأحيانًا دواء تحت إشراف طبي.",
        "questions": [
            "تجيك أفكار أو صور مزعجة ملزِمة ما تقدر توقفها (وساوس)؟",
            "تحس لازم تسوي طقوس معيّنة (غسل، تفقد، ترتيب) عشان تهدى مؤقت؟",
            "هذه الأشياء تاخذ وقت طويل من يومك أو تعطل حياتك؟",
            "لو ما قدرت تسوي الطقس تحس قلقك يولّع مرة؟"
        ],
        "risk_flag_question_index": None
    },

    "adhd_adult": {
        "title": "فحص تشتت/فرط حركة (نمط بالغ)",
        "about": "مو تشخيص رسمي ADHD، لكن يساعدك تشوف إذا فيه نمط تشتت ونقص تنظيم وتأجيل مزمن.",
        "disclaimer": "التشخيص الحقيقي يحتاج مختص (نفسي/عصبي/طب نفسي).",
        "questions": [
            "كثير تنسى أشياء أساسية (مواعيد، مفاتيح، مهام بسيطة)؟",
            "تبدأ أشياء كثير وما تكمّلها؟",
            "عندك صعوبة تظل جالس/هادي وقت لازم تركّز؟",
            "يطلع كلامك/ردك قبل ما تفكر أحيانًا (اندفاعية)؟",
            "التأجيل عندك مزمن يعطل شغلك/دراستك؟",
            "صعب تنظّم وقتك واليوم يضيع فجأة؟"
        ],
        "risk_flag_question_index": None
    },

    "bipolar_mood": {
        "title": "فحص سمات المزاج المرتفع / الهوس",
        "about": "يساعد يفرّق بين 'مزاج مرتفع طبيعي' وبين 'دورات طاقة عالية جداً + نوم قليل + اندفاع خطير'.",
        "disclaimer": "الهوس/الهوس الخفيف موضوع طبي لازم طبيب نفسي لأنه أحيانًا يحتاج مثبت مزاج.",
        "questions": [
            "في أيام تحس طاقتك خارقة ونومك قليل جدًا بدون تعب؟",
            "تحس أفكارك تركض بسرعة بسرعة وأنت ما تلحقها؟",
            "ثقة عالية مرررة/إحساس بالعظمة (أنا ما أغلط / ما أحد يوقفني)؟",
            "صرف فلوس/مخاطرات قوية (قيادة مجنونة، استثمارات مجنونة، مشاكل اجتماعية)؟",
            "قالوا لك ناس حولك: صوتك عالي/كلامك سريع/ما تسكت؟"
        ],
        "risk_flag_question_index": 3
    },

    "social_anxiety": {
        "title": "فحص القلق الاجتماعي",
        "about": "يركز على الخوف من تقييم الناس والحرج، وتجنّب المواقف الاجتماعية.",
        "disclaimer": "العلاج السلوكي (تعرّض اجتماعي تدريجي + تعديل أفكار) مفيد جدًا هنا.",
        "questions": [
            "تتوتر بقوة إذا كنت محور الانتباه (اجتماع، فصل، جمعة)؟",
            "تخاف تقول رأيك لأنك خايف الناس تحكم عليك؟",
            "تتفادى مواقف اجتماعية حتى لو مهمة لحياتك؟",
            "قلبك يدق/ترجف إذا حسّيت الناس يطالعونك كثير؟"
        ],
        "risk_flag_question_index": None
    },

    "ptsd_screen": {
        "title": "فحص أعراض ما بعد الصدمة (PTSD)",
        "about": "يشيّك على الاسترجاع، الكوابيس، التجنّب، اليقظة المفرطة بعد حدث مؤلم.",
        "disclaimer": "لو الأعراض قوية/تعطل حياتك لازم دعم علاجي متخصص بالصدمة.",
        "questions": [
            "عندك استرجاعات قوية/كوابيس عن حدث سيء صار لك؟",
            "تتجنب ناس/أماكن/كلام يذكرك باللي صار؟",
            "تحس دايمًا على أعصابك/مترقّب الخطر؟",
            "صاير نومك وهدوءك خربان من وقت الحدث؟",
            "تحس بذنب/عار شديد على شيء صار حتى لو مو ذنبك؟"
        ],
        "risk_flag_question_index": 0
    },

    "anger_control": {
        "title": "فحص تنظيم الغضب/الانفجار",
        "about": "يساعدك تشوف لو الانفعال والغضب قاعد يخرب علاقاتك أو يسبب مشاكل يومية.",
        "disclaimer": "الـCBT عندكم بالموقع فيه خطة 'إدارة الغضب' تشتغل على هذا بالضبط.",
        "questions": [
            "يغلي دمك بسرعة لدرجة تصرخ/تكسر/تسبب مشكلة؟",
            "بعد ما تهدأ تندم وتقول ما كان يستاهل؟",
            "فيه لحظات تحس ما تقدر توقف نفسك وانت منفعل؟",
            "غضبك سبب مشكلة أسرية/دراسية/وظيفية حقيقية؟"
        ],
        "risk_flag_question_index": 0
    },

    "self_esteem": {
        "title": "فحص نظرة الذات / الثقة بالنفس",
        "about": "مو مرض. هذا بس يقيس إذا جلد الذات مرتفع بشكل غير طبيعي.",
        "disclaimer": "لو ثقتك بنفسك محطمة، نشتغل على خطة 'تعزيز الثقة' في صفحة CBT.",
        "questions": [
            "تحس إنك أقل من الناس؟",
            "صوتك الداخلي قاسي عليك زيادة ('أنا فاشل / ما أستاهل')؟",
            "تتراجع عن فرص (شغل/علاقات) لأنك حاسب نفسك ما تنفع؟",
            "تمدح غيرك بسهولة، بس ما تقدر تقول شي جيد عن نفسك؟"
        ],
        "risk_flag_question_index": None
    }
}


def render_tests_list():
    # كروت كل اختبار + زر "ابدأ"
    cards_html = []
    for test_id, t in TESTS_DATA.items():
        card = f"""
        <div class="tile" style="border:2px solid #000;">
          <h3 style="margin-top:0;">🧪 {t['title']}</h3>
          <div class="small" style="margin-bottom:8px;">
            {t['about']}
          </div>
          <div class="note" style="font-size:.8rem;line-height:1.6;">
            {t['disclaimer']}
          </div>
          <button class="btn gold" onclick="openTest('{test_id}')">ابدأ الاختبار الآن</button>
        </div>
        """
        cards_html.append(card)

    script = r"""
    <script>
    const TESTS = %TESTS_JSON%;

    function openTest(id){
      const t = TESTS[id];
      if(!t){ alert("الاختبار غير متاح"); return; }

      // نبني نموذج الأسئلة
      let html = "";
      html += `<h2 style="margin-top:0;">🧪 ${t.title}</h2>`;
      html += `<div class="small" style="margin-bottom:8px;">${t.about}</div>`;
      html += `<div class="note" style="font-size:.8rem;line-height:1.6;">${t.disclaimer}</div>`;
      html += `<form id="quizForm" style="margin-top:14px;border:1px solid #000;border-radius:12px;padding:14px;">`;

      t.questions.forEach(function(q, idx){
        html += `
        <div style="margin-bottom:12px;">
          <div style="font-weight:700;font-size:.95rem;color:#4B0082;margin-bottom:6px;">
            ${idx+1}. ${q}
          </div>
          <label class="badge2" style="cursor:pointer;">
            <input type="radio" name="q${idx}" value="0"> أبداً / تقريباً أبداً
          </label>
          <label class="badge2" style="cursor:pointer;">
            <input type="radio" name="q${idx}" value="1"> أحياناً
          </label>
          <label class="badge2" style="cursor:pointer;">
            <input type="radio" name="q${idx}" value="2"> كثير
          </label>
          <label class="badge2" style="cursor:pointer;">
            <input type="radio" name="q${idx}" value="3"> تقريباً طول الوقت
          </label>
        </div>`;
      });

      html += `
        <div class="row" style="margin-top:16px;">
          <button type="button" class="btn gold" onclick="calcResult('${id}')">احسب النتيجة</button>
          <button type="button" class="btn alt" onclick="window.print()">🖨️ طباعة</button>
        </div>
      `;

      html += `</form>
      <div id="quizResult" style="margin-top:16px;"></div>
      <div class="divider"></div>
      <div class="row screen-only" style="margin-top:10px;">
        <a class="btn" href="` + %(PSYCHO_WA)s + `" target="_blank" rel="noopener">👨‍🎓 أخصائي نفسي</a>
        <a class="btn" href="` + %(PSYCH_WA)s + `"  target="_blank" rel="noopener">👨‍⚕️ طبيب نفسي</a>
        <a class="btn" href="` + %(SOCIAL_WA)s + `" target="_blank" rel="noopener">🤝 أخصائي اجتماعي</a>
      </div>
      `;

      document.getElementById('testArea').innerHTML = html;
      window.scrollTo({top:0,behavior:'smooth'});
    }

    function calcResult(id){
      const t = TESTS[id];
      if(!t){return;}

      let sum = 0;
      let answeredAll = true;
      let danger = false;

      t.questions.forEach(function(q, idx){
        const radios = document.querySelectorAll(`[name="q${idx}"]`);
        let got = null;
        radios.forEach(r=>{ if(r.checked){ got = parseInt(r.value); } });
        if(got===null || got===undefined){
          answeredAll = false;
        } else {
          sum += got;
          if(t.risk_flag_question_index === idx){
            if(got >= 2){ danger = true; }
          }
        }
      });

      if(!answeredAll){
        alert("جاوب على كل النقاط لو سمحت 🙏");
        return;
      }

      let msg = "";
      msg += "<div class='note' style='font-size:.9rem;line-height:1.7;'>";
      msg += "النتيجة المجمّعة: <b>" + sum + "</b><br/>";
      msg += "كل ما ارتفع الرقم يعني الأعراض أقوى أو أكثر تكراراً.";
      msg += "<br/><br/>هذه نتيجة فحص أولي فقط، مو تشخيص نهائي.";
      msg += "</div>";

      if(danger){
        msg += "<div class='note' style='background:#ffe5e5;border-color:#ff0000;color:#5c0000;font-weight:700;'>";
        msg += "⚠ مهم جدًا: أجبت بإجابة فيها خطر على السلامة/الانفعالات العنيفة/أفكار أذى.";
        msg += "<br/>نوصي تتواصل الآن مع مختص بشري (طوارئ أو طبيب نفسي).";
        msg += "</div>";
      }

      msg += `
      <div class="row screen-only" style="margin-top:12px;">
        <a class="btn" href="` + %(PSYCHO_WA)s + `" target="_blank" rel="noopener">👨‍🎓 أخصائي نفسي</a>
        <a class="btn" href="` + %(PSYCH_WA)s + `"  target="_blank" rel="noopener">👨‍⚕️ طبيب نفسي</a>
        <a class="btn" href="` + %(SOCIAL_WA)s + `" target="_blank" rel="noopener">🤝 أخصائي اجتماعي</a>
      </div>`;

      document.getElementById('quizResult').innerHTML = msg;
      window.scrollTo({top:document.getElementById('quizResult').offsetTop-40,behavior:'smooth'});
    }
    </script>
    """

    full_html = f"""
<div class="card" style="border:2px solid #000;">
  <h1>🧪 اختبارات نفسية / شخصية (تقييم ذاتي)</h1>

  <div class="note">
    هذا مو تشخيص رسمي ولا تقرير طبي.
    النتيجة تساعدك تفهم نمط الأعراض وتقرر:
    هل أحتاج خطة CBT؟ ولا لازم أكلم مختص بشري الآن؟
  </div>

  <div class="small" style="font-weight:700;">
    اختر الاختبار 👇
  </div>

  <div class="grid" style="margin-top:14px;">
    {''.join(cards_html)}
  </div>

  <div class="divider" style="margin-top:20px;"></div>

  <div id="testArea" class="tile" style="border:2px solid #000;">
    <div class="small" style="opacity:.8;">
      لما تختار اختبار من فوق، الأسئلة راح تظهر هنا.
    </div>
  </div>

  {script.replace("%TESTS_JSON%", json.dumps(TESTS_DATA, ensure_ascii=False))}
</div>
"""
    return full_html


@app.get("/tests")
def tests_page():
    content = render_tests_list()
    return shell("الاختبارات النفسية — " + BRAND, content, active="tests")


# مهم: لو عندك nav في shell() لازم نضيف زر /tests فيها
# في دالة shell الأصلية (اللي فوق عندك) في الـ <nav class="nav"> ضيف:
#   <a href="/tests" class="[[A_TESTS]]">
#     <span>🧪 اختبارات نفسية</span>
#     <small>اكتئاب / قلق / تركيز...</small>
#   </a>
#
# وبعدين في نهاية shell(...) استبدل:
#   .replace("[[A_PHARM]]", "active" if active=="pharm" else "")\
# بـ نسخة موسعة فيها tests كمان:
#   .replace("[[A_PHARM]]", "active" if active=="pharm" else "")\
#   .replace("[[A_TESTS]]", "active" if active=="tests" else "")\
#
# وإذا ما كان فيه [[A_TESTS]] أصلاً، أضفها، عادي.


# ======================== (نهاية مقطع /tests) ========================
# ======================== Run ========================

if __name__ == "__main__":
    # محلي (بيثون مباشر):
    #   python app.py
    #
    # على Render / Railway:
    #   gunicorn app:app --bind 0.0.0.0:$PORT
    #
    # ملاحظة: Render يعطي env PORT تلقائي
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
