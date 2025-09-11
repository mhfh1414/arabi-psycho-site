# -*- coding: utf-8 -*-
# home.py — ملف التشغيل الرئيسي (Flask) + الواجهة الفخمة + ربط جميع الوحدات
# يشغّل: DSM + CBT + Addiction
# شغّل بالأمر:  python home.py

from __future__ import annotations
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)

# ========================= استيراد البلوبرنتس =========================
# تأكد أن الملفات التالية موجودة:
# - dsm_suite.py      (يعرّف: dsm_bp  /dsm)
# - cbt/__init__.py   (يعرّف: cbt_bp  /cbt)
# - addiction_suite.py(يعرّف: addiction_bp  /addiction)  ← إن لم يوجد، لن يتسجّل
#
# ملاحظة: إذا كان اسم الملف مختلفًا لديك، عدّل أسطر الاستيراد أدناه.

# DSM (إلزامي للموقع)
from dsm_suite import dsm_bp

# CBT (اختبارات + أدوات علاجية)
try:
    from cbt import cbt_bp
    _HAS_CBT = True
except Exception:
    _HAS_CBT = False

# Addiction (تقييم/خطة علاج الإدمان)
try:
    from addiction_suite import addiction_bp
    _HAS_ADD = True
except Exception:
    _HAS_ADD = False


# ========================= تسجيل البلوبرنتس =========================
app.register_blueprint(dsm_bp)  # /dsm

if _HAS_CBT:
    app.register_blueprint(cbt_bp)  # /cbt

if _HAS_ADD:
    app.register_blueprint(addiction_bp)  # /addiction


# ========================= صفحة الهوم (واجهة فخمة) =========================
HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>عربي سايكو | المنصة العربية للصحة النفسية</title>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{
  --bg1:#0b3a75; --bg2:#0a65b0; --dark:#071338;
  --gold:#f4b400; --lg:#ffd86a; --w:#fff; --glass:rgba(255,255,255,.08);
  --border:rgba(255,255,255,.14);
}
*{box-sizing:border-box}
body{
  margin:0; font-family:"Tajawal",system-ui;
  background: radial-gradient(900px 420px at 85% -10%, #1a4bbd22, transparent),
             linear-gradient(135deg,var(--bg1),var(--bg2));
  color:var(--w); line-height:1.6; background-attachment: fixed;
}
.container{max-width:1240px;margin:0 auto;padding:18px}
header{
  position:sticky;top:0;z-index:10;
  backdrop-filter: blur(10px);
  background: rgba(7,19,56,.55); border-bottom:1px solid var(--border);
}
.header-wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 0}
.brand{display:flex;align-items:center;gap:14px}
.logo{
  width:56px;height:56px;border-radius:16px;display:grid;place-items:center;
  background:linear-gradient(145deg,#0a1330,#0b3a75); color:var(--gold);
  font-weight:900;font-size:22px; border:1px solid var(--border); box-shadow:0 6px 18px rgba(0,0,0,.25)
}
.brand h1{
  margin:0; font-size:28px;
  background:linear-gradient(90deg,var(--lg),var(--gold));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.brand p{margin:.2rem 0 0; color:#cfe0ff; font-size:14px}
.nav{display:flex;gap:10px;flex-wrap:wrap}
.a{
  display:inline-flex;align-items:center;gap:8px;text-decoration:none;color:var(--w);
  padding:10px 14px;border-radius:12px;background:var(--glass);border:1px solid var(--border);
}
.a:hover{background:rgba(255,255,255,.16)}

.hero{padding:42px 0}
.hero-inner{max-width:900px;margin:0 auto;text-align:center}
.hero h2{font-size:40px;margin:0 0 10px}
.hero p{color:#d7e6ff;margin:0 0 18px}

.cta{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:10px}
.btn{
  display:inline-flex;align-items:center;gap:10px;font-weight:800;text-decoration:none;
  padding:14px 18px;border-radius:14px;box-shadow:0 8px 22px rgba(0,0,0,.2)
}
.btn-primary{background:linear-gradient(180deg,var(--lg),var(--gold)); color:#2b1b02}
.btn-secondary{background:linear-gradient(180deg,#9cc5ff,#63a4ff); color:#04122c}

.section{padding:30px 0}
.title{font-size:26px;text-align:center;margin:0 0 22px;position:relative}
.title:after{content:"";width:80px;height:4px;border-radius:2px;background:linear-gradient(90deg,var(--lg),var(--gold));position:absolute;right:50%;transform:translateX(50%);bottom:-10px}

.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:980px){.grid{grid-template-columns:1fr}}
.card{
  background:var(--glass);border:1px solid var(--border);border-radius:16px;padding:18px;
  display:flex;flex-direction:column;gap:10px
}
.card h3{margin:0 0 6px}
.card p{margin:0;color:#dce7ff}
.card .btn{align-self:flex-start}

.footer{
  margin-top:28px;border-top:1px solid var(--border);background:rgba(7,19,56,.7)
}
.footer-wrap{
  display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap;padding:16px 0;
  color:#cfe0ff;font-size:14px
}
.badges{display:flex;gap:8px;flex-wrap:wrap}
.kit{display:inline-block;padding:6px 10px;border-radius:10px;background:rgba(255,255,255,.09);border:1px solid var(--border)}
.privacy{display:flex;align-items:center;gap:8px}
</style>
</head>
<body>

<header>
  <div class="container header-wrap">
    <div class="brand">
      <div class="logo">AS</div>
      <div>
        <h1>عربي سايكو</h1>
        <p>منصة نفسية تخدم الجميع — نخدمك أينما كنت</p>
      </div>
    </div>
    <nav class="nav">
      <a class="a" href="{{ url_for('contact_whatsapp') }}">واتساب</a>
      <a class="a" href="{{ url_for('contact_telegram') }}">تلجرام</a>
      <a class="a" href="{{ url_for('contact_email') }}">إيميل</a>
    </nav>
  </div>
</header>

<main class="container">
  <section class="hero">
    <div class="hero-inner">
      <h2>رعاية نفسية متكاملة — تشخيص دقيق وعلاج مبني على الأدلة</h2>
      <p>واجهة موحّدة: دراسة الحالة + DSM، الاختبارات النفسية وCBT، وبرامج علاج الإدمان. كل ذلك بسرية وخصوصية عالية.</p>
      <div class="cta">
        <a class="btn btn-primary" href="{{ url_for('dsm.dsm_hub') }}">🗂️ دراسة الحالة + DSM</a>
        {% if has_cbt %}
        <a class="btn btn-secondary" href="{{ url_for('cbt.dashboard') }}">🧠 لوحة CBT والاختبارات</a>
        {% else %}
        <span class="btn btn-secondary" style="opacity:.7;cursor:not-allowed">🧠 لوحة CBT (قريبًا)</span>
        {% endif %}
        {% if has_add %}
        <a class="btn btn-primary" href="/addiction">🚭 علاج الإدمان</a>
        {% else %}
        <span class="btn btn-primary" style="opacity:.7;cursor:not-allowed">🚭 علاج الإدمان (قريبًا)</span>
        {% endif %}
      </div>
    </div>
  </section>

  <section class="section">
    <h3 class="title">خدماتنا</h3>
    <div class="grid">
      <div class="card">
        <h3>📖 التشخيص وفق DSM</h3>
        <p>محرك مطابقات موسّع مع مرادفات عامية + ترجيح حسب المدة والأثر الوظيفي لإخراج تشخيص مرجّح واحد.</p>
        <a class="btn btn-primary" href="{{ url_for('dsm.dsm_hub') }}">ابدأ التشخيص</a>
      </div>
      <div class="card">
        <h3>🧪 الاختبارات + CBT</h3>
        <p>PHQ-9، GAD-7، PCL-5، DASS-21 + أدوات عملية: سجل الأفكار، التنشيط السلوكي، التعرض، وخطة الجلسات.</p>
        {% if has_cbt %}<a class="btn btn-secondary" href="{{ url_for('cbt.dashboard') }}">افتح اللوحة</a>{% endif %}
      </div>
      <div class="card">
        <h3>🚭 برامج علاج الإدمان</h3>
        <p>تقييم أولي وخطة علاج وتأهيل فردية مع متابعة مستمرة ودعم وقائي للانتكاس.</p>
        {% if has_add %}<a class="btn btn-primary" href="/addiction">ابدأ التقييم</a>{% endif %}
      </div>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="container footer-wrap">
    <div class="privacy">
      <span class="kit">🔒 سرية تامة</span>
      <span class="kit">🛡️ خصوصية عالية</span>
      <span class="kit">🎧 دعم عن بعد</span>
    </div>
    <div>© {{ year }} عربي سايكو — جميع الحقوق محفوظة</div>
  </div>
</footer>

</body>
</html>
"""

@app.route("/")
def home():
    from datetime import datetime
    return render_template_string(
        HOME_HTML,
        year=datetime.now().year,
        has_cbt=_HAS_CBT,
        has_add=_HAS_ADD
    )

# ========================= روابط تواصل سريعة =========================
@app.route("/contact/whatsapp")
def contact_whatsapp():
    return redirect("https://wa.me/9665XXXXXXXX", code=302)

@app.route("/contact/telegram")
def contact_telegram():
    return redirect("https://t.me/USERNAME", code=302)

@app.route("/contact/email")
def contact_email():
    return redirect("mailto:info@arabipsycho.com", code=302)

# ========================= نقطة التشغيل =========================
if __name__ == "__main__":
    # غيّر المنفذ إذا كنت على Render/railway حسب حاجتك
    app.run(host="0.0.0.0", port=10000, debug=True)
