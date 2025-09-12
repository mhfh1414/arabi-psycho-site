# -*- coding: utf-8 -*-
# home_app.py  —  واجهة الهوم + تشغيل التطبيق على Render

from __future__ import annotations
from flask import Flask, render_template_string, url_for
from datetime import datetime

app = Flask(__name__)

# حاول تسجيل البلوبرنتات إن وُجدت (CBT/DSM/الإدمان)
def _try_register(bp_import_path: str, name: str) -> bool:
    try:
        mod = __import__(bp_import_path, fromlist=["*"])
        # يبحث عن أي Blueprint داخل الموديول
        for attr in dir(mod):
            obj = getattr(mod, attr)
            try:
                from flask import Blueprint  # type: ignore
                if isinstance(obj, Blueprint):
                    app.register_blueprint(obj)
                    return True
            except Exception:
                pass
    except Exception:
        return False
    return False

HAS_CBT  = _try_register("cbt_suite", "CBT")
HAS_DSM  = _try_register("dsm_suite", "DSM")
HAS_ADD  = _try_register("addiction_suite", "Addiction")

# --------------------------- القالب العام ---------------------------
BASE = """
<!doctype html><html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>عربي سايكو | منصة نفسية تخدم الجميع</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{
  --bg1:#0b2d55; --bg2:#0e5596; --panel:rgba(255,255,255,.08);
  --glass:rgba(255,255,255,.12); --stroke:rgba(255,255,255,.18);
  --gold:#f4b400; --mint:#34d399; --rose:#fb7185; --sky:#38bdf8; --w:#fff
}
*{box-sizing:border-box}
body{margin:0;font-family:"Tajawal",system-ui; background:linear-gradient(135deg,var(--bg1),var(--bg2)) fixed; color:var(--w)}
.wrap{max-width:1200px;margin:auto;padding:20px}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:16px}
.logo{display:flex;align-items:center;gap:12px}
.logo .mark{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,#ffd86a,var(--gold));box-shadow:0 6px 18px rgba(0,0,0,.25);display:grid;place-items:center;color:#2b1b02;font-weight:900}
.logo h1{font-size:1.35rem; margin:0}
.meta{opacity:.9;font-size:.9rem}
.meta span{margin-inline-start:12px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:18px}
@media(max-width:980px){.grid{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--stroke);border-radius:18px;padding:18px;backdrop-filter:blur(6px)}
.card h3{margin-top:0}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem}
.b-ok{background:var(--mint)} .b-warn{background:var(--rose)} .b-info{background:var(--sky)}
.btns{display:flex;flex-wrap:wrap;gap:10px}
a.btn,button.btn{
  display:inline-flex;align-items:center;gap:8px; text-decoration:none; border:none; cursor:pointer;
  padding:12px 16px; font-weight:800; border-radius:14px; color:#1d1600;
  background:linear-gradient(180deg,#ffe082,var(--gold)); box-shadow:0 8px 18px rgba(0,0,0,.22)
}
a.btn.dim{pointer-events:none;opacity:.55;filter:grayscale(30%)}
.footer{opacity:.8;margin-top:22px;font-size:.9rem}
.hero{display:grid;grid-template-columns:2.1fr 1fr; gap:16px}
@media(max-width:980px){.hero{grid-template-columns:1fr}}
.lead{font-size:1.05rem;line-height:1.9}
.kpis{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}
.kpis .chip{background:var(--glass);border:1px solid var(--stroke);padding:8px 12px;border-radius:999px}
</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <div class="logo">
      <div class="mark"></div>
      <h1>عربي سايكو</h1>
    </div>
    <div class="meta">
      <span>السرية والخصوصية محفوظة</span> •
      <span>منصة نفسية تخدم الجميع</span>
    </div>
  </div>

  <div class="hero">
    <div class="card">
      <h2 style="margin:0 0 8px">مرحبًا بك 🌿</h2>
      <p class="lead">
        منصة عربية متخصصة بالصحة النفسية: <strong>تشخيص سريري مبسّط (DSM)</strong>،
        <strong>اختبارات قياس</strong> معتمدة (PHQ-9, GAD-7, PCL-5, DASS-21)،
        و<strong>أدوات CBT</strong> عملية (سجل الأفكار، التنشيط السلوكي، التعرض)
        لمتابعة تقدّمك بأمان.
      </p>
      <div class="kpis">
        <div class="chip">واجهة عربية كاملة</div>
        <div class="chip">توافق جوّال/كمبيوتر</div>
        <div class="chip">لا تُخزّن بيانات حساسة</div>
      </div>
    </div>
    <div class="card">
      <h3>روابط سريعة</h3>
      <div class="btns">
        <a class="btn {{ 'dim' if not has_dsm }}" href="/dsm">📋 التشخيص (DSM)</a>
        <a class="btn {{ 'dim' if not has_cbt }}" href="/cbt">🧠 لوحة CBT</a>
        <a class="btn {{ 'dim' if not has_add }}" href="/addiction">🚫 أدوات الإدمان</a>
      </div>
      <p style="margin-top:10px;opacity:.9">
        {{ '✅ جميع الوحدات جاهزة.' if all_ready else '⚠️ بعض الوحدات غير مُفعّلة حالياً.' }}
      </p>
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <h3>🧪 اختبارات قياس معتمدة</h3>
      <p>مقاييس موثوقة لمتابعة الشدة والأعراض عبر الزمن.</p>
      <div class="btns">
        <a class="btn {{ 'dim' if not has_cbt }}" href="/cbt/phq9">PHQ-9</a>
        <a class="btn {{ 'dim' if not has_cbt }}" href="/cbt/gad7">GAD-7</a>
        <a class="btn {{ 'dim' if not has_cbt }}" href="/cbt/pcl5">PCL-5</a>
        <a class="btn {{ 'dim' if not has_cbt }}" href="/cbt/dass21">DASS-21</a>
      </div>
    </div>

    <div class="card">
      <h3>💡 العلاج المعرفي السلوكي (CBT)</h3>
      <p>خطوات عملية تُترجم النتائج إلى تغيير سلوكي وفكري.</p>
      <div class="btns">
        <a class="btn {{ 'dim' if not has_cbt }}" href="/cbt/thought-record">سجل الأفكار</a>
        <a class="btn {{ 'dim' if not has_cbt }}" href="/cbt/ba">التنشيط السلوكي</a>
        <a class="btn {{ 'dim' if not has_cbt }}" href="/cbt/exposures">سُلّم التعرض</a>
        <a class="btn {{ 'dim' if not has_cbt }}" href="/cbt/plan">خطة جلسات</a>
      </div>
    </div>

    <div class="card">
      <h3>📘 التشخيص السريري (DSM)</h3>
      <p>ملف أمراض + أعراض بشكل مبسّط لتكوين الانطباع التشخيصي الأوّلي.</p>
      <div class="btns">
        <a class="btn {{ 'dim' if not has_dsm }}" href="/dsm">فتح واجهة DSM</a>
      </div>
    </div>
  </div>

  <div class="footer">© {{year}} عربي سايكو — منصة نفسية عربية متكاملة</div>
</div>
</body></html>
"""

# --------------------------- مسارات أساسية ---------------------------
@app.route("/")
def home():
    return render_template_string(
        BASE,
        year=datetime.now().year,
        has_cbt=HAS_CBT, has_dsm=HAS_DSM, has_add=HAS_ADD,
        all_ready=(HAS_CBT and HAS_DSM and HAS_ADD)
    )

@app.route("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}

# صفحة 404 عربية أنيقة
@app.errorhandler(404)
def not_found(e):
    html = """
    <div style="display:grid;place-items:center;height:100vh;background:linear-gradient(135deg,#0b2d55,#0e5596);color:#fff;font-family:Tajawal">
      <div style="text-align:center;max-width:700px;padding:24px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px">
        <h1 style="margin:0 0 6px">الصفحة غير موجودة — 404</h1>
        <p style="opacity:.9;margin:0 0 14px">رابط الصفحة غير صحيح أو لم تعد متاحة.</p>
        <a href="/" style="display:inline-block;background:linear-gradient(180deg,#ffe082,#f4b400);color:#1d1600;padding:12px 16px;font-weight:800;border-radius:14px;text-decoration:none">العودة للواجهة</a>
      </div>
    </div>"""
    return html, 404

# نقطة تشغيل gunicorn
if __name__ == "__main__":
    app.run(debug=True)
