# -*- coding: utf-8 -*-
# home.py — الصفحة الرئيسية لموقع "عربي سايكو"

from __future__ import annotations
from flask import Blueprint, render_template_string, url_for

home_bp = Blueprint("home", __name__)

HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>عربي سايكو | منصة نفسية عربية</title>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg1:#0b3a75; --bg2:#0a65b0; --ink:#0b1324; --card:rgba(255,255,255,.09);
      --line:rgba(255,255,255,.18); --gold:#f4b400; --mint:#22c55e; --rose:#ef4444; --sky:#38bdf8;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0; font-family:"Tajawal",system-ui; color:#fff;
      background:radial-gradient(1200px 500px at 70% -10%, rgba(255,255,255,.1), transparent 60%),
                 linear-gradient(135deg,var(--bg1),var(--bg2)) fixed;
    }
    .shell{max-width:1200px;margin:28px auto;padding:16px}
    .top{
      display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:14px;
    }
    .brand{
      display:flex; align-items:center; gap:12px;
    }
    .logo{
      width:48px; height:48px; border-radius:12px;
      background:
        radial-gradient(14px 14px at 70% 30%, #fff8, transparent 60%),
        linear-gradient(135deg,#f59e0b,#f97316);
      box-shadow:0 6px 18px rgba(0,0,0,.25), inset 0 0 0 2px rgba(255,255,255,.25);
    }
    .title{font-size:1.6rem; font-weight:800; letter-spacing:.5px}
    .subtitle{opacity:.85}
    .tags{display:flex; gap:8px; flex-wrap:wrap}
    .chip{
      background:rgba(255,255,255,.12); border:1px solid var(--line);
      padding:6px 10px; border-radius:999px; font-size:.92rem
    }
    .links{display:flex; gap:8px; flex-wrap:wrap}
    .btn{
      display:inline-block; text-decoration:none; cursor:pointer; user-select:none;
      padding:11px 16px; border-radius:12px; font-weight:800; color:#0b1324;
      background:linear-gradient(180deg,#ffe38a,#f4b400); border:none;
      box-shadow:0 8px 16px rgba(0,0,0,.25);
    }
    .btn.ghost{background:rgba(255,255,255,.12); color:#fff; border:1px solid var(--line); box-shadow:none}
    .grid{
      display:grid; gap:16px; grid-template-columns:2fr 1fr;
    }
    @media (max-width:1080px){ .grid{grid-template-columns:1fr} }
    .card{
      background:var(--card); border:1px solid var(--line); border-radius:16px; padding:18px;
      box-shadow:0 10px 24px rgba(0,0,0,.22);
    }
    h2{margin:.2rem 0 1rem 0}
    .apps{display:grid; gap:12px; grid-template-columns:repeat(3,1fr)}
    @media (max-width:880px){ .apps{grid-template-columns:1fr} }
    .app{
      position:relative; overflow:hidden; border-radius:16px; border:1px solid var(--line); background:rgba(255,255,255,.06);
    }
    .app .cover{
      padding:18px; min-height:150px;
      background:
        radial-gradient(200px 160px at -10% 0%, rgba(255,255,255,.12), transparent 70%),
        linear-gradient(135deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
    }
    .app h3{margin:0 0 6px 0}
    .app p{margin:0; opacity:.9}
    .app .go{display:block; padding:12px 16px; background:rgba(255,255,255,.10); border-top:1px solid var(--line)}
    .app .go .btn{width:100%; text-align:center}
    .pill{display:inline-flex; align-items:center; gap:6px; padding:4px 10px; border-radius:999px; font-size:.85rem}
    .p-gold{background:#fef3c7; color:#854d0e}
    .p-mint{background:#dcfce7; color:#14532d}
    .p-sky{background:#e0f2fe; color:#0c4a6e}
    .p-rose{background:#fee2e2; color:#7f1d1d}
    .foot{
      display:flex; gap:10px; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-top:18px;
      opacity:.92
    }
    .foot .left{display:flex; gap:10px; flex-wrap:wrap}
    .foot .link{color:#fff; opacity:.9; text-decoration:none; border-bottom:1px dashed rgba(255,255,255,.5)}
    .muted{opacity:.75}
  </style>
</head>
<body>
  <div class="shell">

    <!-- رأس الصفحة -->
    <header class="top">
      <div class="brand">
        <div class="logo" aria-hidden="true"></div>
        <div>
          <div class="title">عربي سايكو</div>
          <div class="subtitle">منصة نفسية عربية — تشخيص مبدئي، مقاييس قياسية، وأدوات علاج سلوكي معرفي.</div>
        </div>
      </div>
      <div class="tags">
        <span class="chip">السرية والخصوصية محفوظة</span>
        <span class="chip">لا تُغني عن التقييم السريري</span>
      </div>
    </header>

    <!-- شريط أزرار سريع -->
    <div class="links" style="margin-bottom:16px">
      <a class="btn" href="{{ url_for('dsm.dsm_hub') }}">التشخيص + دراسة حالة (DSM)</a>
      <a class="btn" href="{{ url_for('cbt.dashboard') }}">لوحة CBT (اختبارات وأدوات)</a>
      <a class="btn" href="{{ url_for('addiction.bp_hub') if 'addiction' in blueprints else '#' }}" title="برنامج التعافي من الإدمان">برنامج الإدمان والتعافي</a>
      <a class="btn ghost" href="{{ url_for('home.privacy') }}">الخصوصية</a>
      <a class="btn ghost" href="{{ url_for('home.contact') }}">تواصل</a>
    </div>

    <!-- المحتوى -->
    <main class="grid">
      <!-- التطبيقات الأساسية -->
      <section class="card">
        <h2>الخدمات الرئيسية</h2>
        <div class="apps">
          <div class="app">
            <div class="cover">
              <div class="pill p-gold">DSM-5 مهيأ بالعربية</div>
              <h3>التشخيص + دراسة حالة</h3>
              <p>أدخل أعراضك بوضوح والعمر والمدة والأثر الوظيفي. النظام يرشّح تشخيصًا مرجّحًا واحدًا مع مطابقات.</p>
            </div>
            <div class="go"><a class="btn" href="{{ url_for('dsm.dsm_hub') }}">ابدأ التشخيص</a></div>
          </div>

          <div class="app">
            <div class="cover">
              <div class="pill p-sky">PHQ-9 • GAD-7 • PCL-5 • DASS-21</div>
              <h3>لوحة CBT</h3>
              <p>مقاييس قياسية مع أدوات عملية: سجل الأفكار، التنشيط السلوكي، سُلّم التعرض، وخطة جلسات أولية.</p>
            </div>
            <div class="go"><a class="btn" href="{{ url_for('cbt.dashboard') }}">افتح لوحة CBT</a></div>
          </div>

          <div class="app">
            <div class="cover">
              <div class="pill p-mint">خطة تعافٍ مرنة</div>
              <h3>الإدمان والتعافي</h3>
              <p>الوحدات الأساسية: التحفيز، إدارة المحفزات، بدائل صحية، متابعة انتكاسة. (اختياري)</p>
            </div>
            <div class="go">
              {% if 'addiction' in blueprints %}
                <a class="btn" href="{{ url_for('addiction.bp_hub') }}">ادخل برنامج الإدمان</a>
              {% else %}
                <a class="btn" href="#" onclick="alert('وحدة الإدمان غير مفعلة حالياً'); return false;">غير مفعّل</a>
              {% endif %}
            </div>
          </div>
        </div>
      </section>

      <!-- ملاحظات سريعة -->
      <aside class="card">
        <h2>مهم قبل البدء</h2>
        <ul style="margin-top:.3rem; line-height:1.9">
          <li>نتائج المنصة <strong>استرشادية</strong> لا تُعد تشخيصًا نهائيًا.</li>
          <li>لو كانت هناك أفكار انتحارية أو خطورة فورية، اطلب مساعدة طبية عاجلة.</li>
          <li>ننصح بمتابعة مختص نفسي/طب نفسي عند الشدة المتوسطة فأعلى.</li>
        </ul>
        <div style="height:10px"></div>
        <div class="pill p-rose">دعم سريع</div>
        <p class="muted">يمكنك مراسلتنا للاستفسار الفني أو المقترحات.</p>
      </aside>
    </main>

    <!-- ذيل الصفحة -->
    <footer class="foot">
      <div class="left">
        <a class="link" href="{{ url_for('home.privacy') }}">سياسة الخصوصية</a>
        <a class="link" href="{{ url_for('home.contact') }}">التواصل</a>
      </div>
      <div class="muted">© {{year}} عربي سايكو</div>
    </footer>

  </div>
</body>
</html>
"""

PRIVACY = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>الخصوصية | عربي سايكو</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  body{margin:0;background:linear-gradient(135deg,#0b3a75,#0a65b0);color:#fff;font-family:"Tajawal",system-ui}
  .box{max-width:900px;margin:26px auto;padding:16px}
  .card{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:18px}
  a{color:#fff}
</style></head><body>
<div class="box">
  <h2>سياسة الخصوصية</h2>
  <div class="card">
    <p>نحترم سرّيتك. لا نبيع بياناتك ولا نشاركها لأغراض تسويقية. قد تُستخدم مدخلاتك لتحسين الخدمة تقنيًا بعد إزالة أي مُعرّفات شخصية.</p>
    <p>هذه المنصة للأغراض التعليمية/المساندة ولا تُغني عن الرعاية الطبية المتخصصة.</p>
    <p><a href="{{ url_for('home.index') }}">عودة للواجهة</a></p>
  </div>
</div>
</body></html>
"""

CONTACT = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>تواصل | عربي سايكو</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  body{margin:0;background:linear-gradient(135deg,#0b3a75,#0a65b0);color:#fff;font-family:"Tajawal",system-ui}
  .box{max-width:900px;margin:26px auto;padding:16px}
  .card{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:18px}
  a{color:#fff}
</style></head><body>
<div class="box">
  <h2>تواصل معنا</h2>
  <div class="card">
    <p>للدعم الفني والملاحظات: راسلنا عبر التليجرام أو البريد.</p>
    <ul>
      <li>Telegram: <a href="https://t.me/" target="_blank" rel="noopener">قناة الدعم</a></li>
      <li>Email: support@example.com</li>
    </ul>
    <p><a href="{{ url_for('home.index') }}">عودة للواجهة</a></p>
  </div>
</div>
</body></html>
"""

@home_bp.route("/")
def index():
    # نمرر وجود بلوبرنت الإدمان لنعرض زر فعّال إذا كان مسجلاً
    try:
        blueprints = set(home_bp.server_blueprint_names)  # سيُضبط في register_home() أدناه
    except Exception:
        blueprints = set()
    return render_template_string(HTML, year=2025, blueprints=blueprints)

@home_bp.route("/privacy")
def privacy():
    return render_template_string(PRIVACY)

@home_bp.route("/contact")
def contact():
    return render_template_string(CONTACT)

# --- مساعد اختياري: نداءه من site_app.py بعد تسجيل كل البلوبرنتس ---
def register_home(app):
    """
    يُستخدم اختياريًا داخل site_app.py بعد register_blueprint
    لتمرير أسماء البلوبرنت المسجلة لواجهة الهوم (لزر الإدمان).
    مثال:
        app = Flask(__name__)
        app.register_blueprint(dsm_bp)
        app.register_blueprint(cbt_bp, url_prefix="/cbt")
        app.register_blueprint(addiction_bp, url_prefix="/addiction")
        register_home(app)
    """
    try:
        names = list(app.blueprints.keys())
        # نخزّن الأسماء داخل البلوبرنت حتى نقرأها في index()
        home_bp.server_blueprint_names = names  # type: ignore[attr-defined]
    except Exception:
        pass
