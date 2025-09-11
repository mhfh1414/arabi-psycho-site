# -*- coding: utf-8 -*-
# home.py — الواجهة الرئيسية لمنصة عربي سايكو

from __future__ import annotations
from flask import Blueprint, render_template_string, url_for
from datetime import datetime

home_bp = Blueprint("home", __name__)

def _year() -> int:
    try:
        return datetime.now().year
    except Exception:
        return 2025

# صفحة الهوم (HTML/CSS داخل نص متعدد الأسطر — مغلق بإحكام)
PAGE = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>عربي سايكو | منصة نفسية عربية</title>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg1:#0b3a75; --bg2:#0a65b0; --ink:#0b1324; --gold:#f4b400;
      --card:rgba(255,255,255,.09); --line:rgba(255,255,255,.22); --w:#fff;
      --mint:#34d399; --pink:#f472b6; --sky:#38bdf8; --amber:#f59e0b;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0; font-family:"Tajawal", system-ui, -apple-system;
      color:var(--w);
      background: radial-gradient(1200px 600px at 80% -10%, #1a4d8d33, transparent 70%),
                  radial-gradient(1000px 500px at -10% 120%, #0d59b833, transparent 70%),
                  linear-gradient(135deg, var(--bg1), var(--bg2));
    }
    .wrap{max-width:1200px;margin:24px auto;padding:16px}
    /* شريط أعلى */
    .top{
      display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px
    }
    .brand{
      display:flex;align-items:center;gap:10px
    }
    .logo{
      width:44px;height:44px;border-radius:12px;
      background: conic-gradient(from 210deg, var(--gold), #ffd86a, #ffcf33, var(--gold));
      box-shadow: 0 6px 18px #00000040 inset, 0 3px 10px #00000026;
      display:grid;place-items:center;color:#2b1b02;font-weight:900
    }
    .title{margin:0;font-size:1.55rem;font-weight:800;letter-spacing:.3px}
    .sub{opacity:.85;margin-top:2px}
    .badges{display:flex;gap:8px;flex-wrap:wrap}
    .badge{
      display:inline-flex;align-items:center;gap:6px;
      background:rgba(255,255,255,.12); border:1px solid var(--line);
      padding:6px 10px; border-radius:999px; font-size:.86rem
    }
    .badge i{font-style:normal; opacity:.9}

    /* بطاقات */
    .grid{display:grid;grid-template-columns:1.2fr .8fr;gap:16px}
    @media(max-width:1000px){.grid{grid-template-columns:1fr}}
    .card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px}
    .hero h1{margin:.2rem 0 0;font-size:1.8rem}
    .hero p{opacity:.9;line-height:1.9;margin:.4rem 0 0}

    .cta{display:flex;flex-direction:column;gap:12px;margin-top:14px}
    .btn{
      display:flex;align-items:center;justify-content:space-between;
      background:linear-gradient(180deg,#ffd86a,var(--gold)); color:#2b1b02;
      border:none; padding:14px 16px; border-radius:14px; font-weight:800; cursor:pointer;
      text-decoration:none; box-shadow:0 10px 24px #0000002b;
      transition:transform .06s ease;
    }
    .btn:hover{transform:translateY(-1px)}
    .btn i{font-style:normal; opacity:.9}

    .tiles{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
    @media(max-width:700px){.tiles{grid-template-columns:1fr}}
    .tile{
      background:var(--card); border:1px solid var(--line); border-radius:16px; padding:16px; position:relative;
      overflow:hidden; min-height:120px;
    }
    .tile h3{margin:0 0 6px;font-size:1.1rem}
    .tile p{margin:0;opacity:.9}
    .chip{
      position:absolute; top:12px; left:12px; padding:4px 10px; border-radius:999px;
      font-size:.8rem; color:#0c141f; font-weight:800; background:#fff8; backdrop-filter: blur(6px);
    }
    .chip.mint{background:linear-gradient(180deg,#b7f7de,#7be6bd)}
    .chip.pink{background:linear-gradient(180deg,#ffd0e6,#ff9fc9)}
    .chip.sky{background:linear-gradient(180deg,#d5f1ff,#9bddff)}
    .chip.amber{background:linear-gradient(180deg,#ffe6b0,#ffd06a)}
    .tile .go{
      position:absolute; bottom:12px; right:12px; background:rgba(255,255,255,.15);
      border:1px solid var(--line); color:#fff; text-decoration:none; padding:8px 12px; border-radius:12px; font-weight:700
    }

    footer{opacity:.75;margin-top:22px;text-align:center}
  </style>
</head>
<body>
  <div class="wrap">

    <!-- الهيدر -->
    <div class="top">
      <div class="brand">
        <div class="logo">AS</div>
        <div>
          <h1 class="title">عربي سايكو</h1>
          <div class="sub">منصة نفسية عربية — تشخيص مبدئي، أدوات CBT، واختبارات معيارية</div>
        </div>
      </div>
      <div class="badges">
        <span class="badge"><i>🔒</i> السرية والخصوصية</span>
        <span class="badge"><i>🧪</i> أدوات قياسية (PHQ-9 / GAD-7 / PCL-5 / DASS-21)</span>
        <span class="badge"><i>⚕️</i> لا تغني عن التقييم السريري</span>
      </div>
    </div>

    <!-- المحتوى -->
    <div class="grid">
      <!-- يمين: هيرو + أزرار رئيسية -->
      <section class="card hero">
        <h1>اختر خدمتك بسرعة</h1>
        <p>ابدأ بدراسة حالة سريعة مع مطابقة DSM (تشخيص مرجّح واحد)، أو انتقل إلى لوحة العلاج السلوكي المعرفي لاستخدام سجل الأفكار، التنشيط السلوكي، وسُلّم التعرض، مع اختبارات معيارية لمتابعة التحسن.</p>
        <div class="cta">
          <a class="btn" href="/dsm">التشخيص + دراسة حالة (DSM) <i>→</i></a>
          <a class="btn" href="/cbt/">لوحة العلاج السلوكي المعرفي (CBT) <i>→</i></a>
          <a class="btn" href="/addiction">برنامج الإدمان والتعافي <i>→</i></a>
        </div>
      </section>

      <!-- يسار: مربعات معلومات/اختصارات -->
      <aside class="tiles">
        <div class="tile">
          <span class="chip mint">DSM</span>
          <h3>تشخيص مرجّح واحد</h3>
          <p>محرك لغة عربية يطابق الأعراض مع معايير DSM ويُظهر أقوى تشخيص بناءً على الشدة والمدة والأثر الوظيفي.</p>
          <a class="go" href="/dsm">اذهب</a>
        </div>
        <div class="tile">
          <span class="chip sky">CBT</span>
          <h3>لوحة CBT متكاملة</h3>
          <p>سجل أفكار (REBT/CBT)، تنشيط سلوكي (BA)، تعرّض تدريجي (ERP)، وخطة جلسات أولية قابلة للتعديل.</p>
          <a class="go" href="/cbt/">فتح اللوحة</a>
        </div>
        <div class="tile">
          <span class="chip pink">Tests</span>
          <h3>اختبارات معيارية</h3>
          <p>PHQ-9 للاكتئاب، GAD-7 للقلق العام، PCL-5 لاضطراب ما بعد الصدمة، DASS-21 للقلق/الاكتئاب/التوتر.</p>
          <a class="go" href="/cbt">ابدأ القياس</a>
        </div>
        <div class="tile">
          <span class="chip amber">Support</span>
          <h3>تواصل خاص</h3>
          <p>للاستشارات أو الدعم، راسلنا عبر البريد أو التليجرام — خصوصيتك أولويتنا.</p>
          <a class="go" href="/contact">تواصل</a>
        </div>
      </aside>
    </div>

    <footer>© {{ year }} عربي سايكو — جميع الحقوق محفوظة</footer>
  </div>
</body>
</html>
"""

@home_bp.route("/")
@home_bp.route("/home")
def home_page():
    return render_template_string(PAGE, year=_year())

# مسار فحص الجاهزية للبنشر/المراقبة
@home_bp.route("/healthz")
def healthz():
    return {"ok": True, "service": "arabi-psycho", "time": _year()}, 200
