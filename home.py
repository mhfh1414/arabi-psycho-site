# -*- coding: utf-8 -*-
# home.py — ملف التشغيل الرئيسي + الواجهة
from __future__ import annotations
from flask import Flask, render_template_string, url_for, redirect

app = Flask(__name__)

# -------- تسجيل البلوبريات (DSM/CBT/إدمان) إن وُجدت --------
# كل واحد موضوع في ملف مستقل: dsm_suite.py / cbt_suite.py / addiction_suite.py
# كل ملف يعرّف Blueprint باسم: dsm_bp / cbt_bp / addiction_bp
def _safe_register(import_path: str, bp_name: str, url_prefix: str | None = None):
    try:
        mod = __import__(import_path, fromlist=[bp_name])
        bp = getattr(mod, bp_name)
        app.register_blueprint(bp, url_prefix=url_prefix)
        print(f"[OK] Registered {bp_name} from {import_path} at {url_prefix or bp.url_prefix or '/'}")
    except Exception as e:
        print(f"[WARN] Could not register {bp_name} from {import_path}: {e}")

_safe_register("dsm_suite", "dsm_bp")                 # /dsm داخل الملف
_safe_register("cbt_suite", "cbt_bp", url_prefix="/cbt")
_safe_register("addiction_suite", "addiction_bp", url_prefix="/addiction")

# -------- صفحة رئيسية أنيقة --------
HOME_HTML = """
<!doctype html><html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>عربي سايكو | منصة نفسية</title>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{--bg1:#0b3a75;--bg2:#0a65b0;--glass:rgba(255,255,255,.08);--line:rgba(255,255,255,.18);--gold:#f4b400}
    *{box-sizing:border-box}
    body{margin:0;font-family:"Tajawal",system-ui;background:radial-gradient(60% 80% at 80% -10%, #1282ff33, transparent 60%),linear-gradient(135deg,var(--bg1),var(--bg2));color:#fff}
    .wrap{max-width:1100px;margin:32px auto;padding:16px}
    .bar{display:flex;gap:12px;align-items:center;justify-content:space-between}
    .brand{display:flex;gap:12px;align-items:center}
    .logo{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;background:#1112;box-shadow:0 8px 20px #0002}
    .logo svg{width:28px;height:28px}
    .brand h1{margin:0;font-size:1.6rem;letter-spacing:.5px}
    .brand small{opacity:.85}
    .tags{display:flex;gap:8px;flex-wrap:wrap}
    .tag{background:#10b981;padding:4px 10px;border-radius:999px;font-size:.85rem}
    .tag.sec{background:#6366f1}.tag.safe{background:#22c55e}.tag.ai{background:#f59e0b}
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:18px}
    @media(max-width:1000px){.grid{grid-template-columns:1fr}}
    .card{background:var(--glass);border:1px solid var(--line);border-radius:18px;padding:18px}
    .card h3{margin:.2rem 0 1rem}
    .btn{display:block;width:100%;text-align:center;text-decoration:none;
         background:linear-gradient(180deg,#ffd86a,#f4b400);color:#2b1b02;
         border-radius:14px;padding:12px 14px;font-weight:800;border:none}
    .btn.alt{background:linear-gradient(180deg,#9bd5ff,#5bbcff);color:#08213a}
    .btn.ghost{background:transparent;color:#fff;border:1px solid var(--line)}
    ul{list-style:none;padding:0;margin:0;display:grid;gap:10px}
    footer{opacity:.8;margin-top:18px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="bar">
      <div class="brand">
        <div class="logo" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M4 12a8 8 0 1116 0v5a3 3 0 01-3 3h-2v-6" stroke="#ffd86a" stroke-width="2" stroke-linecap="round"/>
            <path d="M8 20v-6a4 4 0 014-4h2" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <div>
          <h1>عربي سايكو</h1>
          <small>منصة نفسية عربية — تشخيص مبدئي، اختبارات قياسية، وأدوات علاج سلوكي معرفي</small>
        </div>
      </div>
      <div class="tags">
        <span class="tag safe">سرية وخصوصية</span>
        <span class="tag sec">https</span>
        <span class="tag ai">مدعوم بالذكاء الاصطناعي</span>
      </div>
    </div>

    <div class="grid">
      <section class="card">
        <h3>🗂️ دراسة حالة + DSM-5</h3>
        <p>نموذج ذكي يقرأ الأعراض بصياغة عربية ويقترح تشخيصًا مرجحًا (غير مُلزم طبيًا).</p>
        <ul>
          <li><a class="btn" href="/dsm">ابدأ التشخيص الآن</a></li>
          <li><a class="btn ghost" href="/dsm">كيف أكتب الأعراض بشكل واضح؟</a></li>
        </ul>
      </section>
      <section class="card">
        <h3>🧪 اختبارات قياسية</h3>
        <p>قياسات معتمدة: PHQ-9 للاكتئاب، GAD-7 للقلق، PCL-5 للصدمة، DASS-21.</p>
        <ul>
          <li><a class="btn alt" href="/cbt">لوحة CBT المتكاملة</a></li>
        </ul>
      </section>
      <section class="card">
        <h3>💡 أدوات CBT عملية</h3>
        <p>سجل الأفكار (REBT/CBT)، التنشيط السلوكي (BA)، سُلّم التعرض (ERP)، وخطة جلسات أولية.</p>
        <ul>
          <li><a class="btn" href="/cbt">افتح الأدوات الآن</a></li>
        </ul>
      </section>
    </div>

    <footer>
      <div>© {{year}} عربي سايكو</div>
      <div style="display:flex;gap:10px">
        <a class="btn ghost" href="/healthz">الحالة</a>
        <a class="btn ghost" href="/">الواجهة</a>
      </div>
    </footer>
  </div>
</body>
</html>
"""

@app.route("/")
def home():
    from datetime import datetime
    return render_template_string(HOME_HTML, year=datetime.now().year)

# -------- مسارات مساعدة --------
@app.route("/healthz")
def healthz():
    return {"status": "ok", "app": "arabi-psycho", "routes": ["/", "/dsm", "/cbt", "/addiction"]}, 200

# 404 مخصص: رجّع المستخدم للواجهة مع كود 404
@app.errorhandler(404)
def not_found(e):
    return redirect(url_for("home")), 302

# للتشغيل المحلي (اختياري)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
