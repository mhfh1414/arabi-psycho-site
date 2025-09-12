# site_app.py
from __future__ import annotations
import importlib
from typing import Optional
from flask import Flask, Blueprint, render_template_string, url_for

app = Flask(__name__)

# ---------- أدوات دمج وحدات اختيارية (DSM/CBT...) ----------
def mount_optional(module_name: str, url_prefix: str, display_name: str) -> str:
    """
    يحاول استيراد الموديول، ثم يبحث عن Blueprint جاهز:
      - متغير اسمه bp أو blueprint
      - أو دالة get_blueprint() تُرجع Blueprint
    إن لم يجد، يضيف Route بسيط يشرح أن الدمج يحتاج تفعيل داخل الملف الخارجي.
    يعيد نص حالة الدمج لعرضه في الصفحة الرئيسية.
    """
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        return f"❌ {display_name}: لم يتم العثور على الملف ({module_name}.py) — {e}"

    # ابحث عن Blueprint جاهز
    cand_names = ("bp", "blueprint")
    bp: Optional[Blueprint] = None
    for name in cand_names:
        if hasattr(mod, name) and isinstance(getattr(mod, name), Blueprint):
            bp = getattr(mod, name)
            break

    # أو دالة ترجع Blueprint
    if bp is None and hasattr(mod, "get_blueprint"):
        try:
            maybe_bp = mod.get_blueprint()
            if isinstance(maybe_bp, Blueprint):
                bp = maybe_bp
        except Exception as e:
            return f"⚠️ {display_name}: get_blueprint() فشلت — {e}"

    # سجّل الـ Blueprint إن وُجد
    if bp is not None:
        try:
            app.register_blueprint(bp, url_prefix=url_prefix)
            return f"✅ {display_name}: تم ربطه على {url_prefix}"
        except Exception as e:
            return f"⚠️ {display_name}: فشل تسجيل الـ Blueprint — {e}"

    # إن لم نجد Blueprint، أضف صفحة تنبيه لطيفة
    route_path = f"{url_prefix}/"
    @app.get(route_path)
    def _module_placeholder():
        return render_template_string(PAGE_SIMPLE, title=display_name, body=f"""
        لم أجد Blueprint داخل <code>{module_name}.py</code>.<br>
        فضلاً أضف داخل الملف أحد الخيارين:
        <ol class="list-decimal ps-4">
          <li>تعريف <code>bp = Blueprint(...)</code> مع ربط المسارات عليه</li>
          <li>أو دالة <code>get_blueprint()</code> تُرجع نفس الـ <code>Blueprint</code></li>
        </ol>
        ثم ادخل إلى: <code>{url_prefix}</code> بعد إعادة النشر.
        """)
    return f"ℹ️ {display_name}: الملف موجود لكن بدون Blueprint — معروض Placeholder على {route_path}"

# ---------- صفحات HTML (قوالب) ----------
PAGE_HOME = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>العيادة النفسية العربية</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: radial-gradient(1200px 600px at 80% 0%, #0ea5e9 0%, #0f172a 55%); min-height: 100vh; color: #e5e7eb;}
    .hero { padding: 56px 0; }
    .brand { font-weight:800; letter-spacing:0.5px; }
    .card { background: rgba(15,23,42,.65); border: 1px solid rgba(148,163,184,.25); }
    .btn-pill { border-radius: 999px; padding: .75rem 1.25rem; font-weight: 600; }
    .badge-soft { background: rgba(56,189,248,.15); color:#67e8f9; border:1px solid rgba(56,189,248,.25)}
    .footer { color:#94a3b8 }
    a, a:hover { color:#67e8f9; text-decoration: none; }
  </style>
</head>
<body>
<div class="container hero">
  <div class="row justify-content-center">
    <div class="col-lg-10">
      <div class="text-center mb-4">
        <span class="badge badge-soft px-3 py-2">نسخة تجريبية</span>
        <h1 class="display-5 brand mt-3">العيادة النفسيّة العربية</h1>
        <p class="lead mt-2">واجهة موحّدة لأدوات التشخيص والدعم العلاجي (DSM | CBT | الإدمان).<br>تم تصميمها لتكون أنيقة، واضحة، وسريعة.</p>
      </div>

      <div class="row g-4">
        <div class="col-md-4">
          <div class="card p-4 h-100">
            <h5 class="mb-2">التشخيص السريري (DSM)</h5>
            <p class="mb-4 text-light">نظام تصنيفي للأعراض والاضطرابات مع توثيق سريري مختصر.</p>
            <div class="d-grid">
              <a href="{{ url_for('dsm_entry') }}" class="btn btn-primary btn-pill">فتح DSM</a>
            </div>
            <small class="mt-3 d-block footer">{{ dsm_status }}</small>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card p-4 h-100">
            <h5 class="mb-2">العلاج المعرفي السلوكي (CBT)</h5>
            <p class="mb-4 text-light">تمارين الأفكار التلقائية، إعادة البناء المعرفي، وسُلّم السلوكيات.</p>
            <div class="d-grid">
              <a href="{{ url_for('cbt_entry') }}" class="btn btn-success btn-pill">فتح CBT</a>
            </div>
            <small class="mt-3 d-block footer">{{ cbt_status }}</small>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card p-4 h-100">
            <h5 class="mb-2">برنامج الإدمان</h5>
            <p class="mb-4 text-light">مراقبة الشغف، محفزات الانتكاس، وخطة الامتناع مع قياس يومي.</p>
            <div class="d-grid">
              <a href="{{ url_for('addiction_entry') }}" class="btn btn-warning btn-pill">فتح الإدمان</a>
            </div>
            <small class="mt-3 d-block footer">{{ addiction_status }}</small>
          </div>
        </div>
      </div>

      <div class="text-center mt-5 footer">
        <a href="{{ url_for('healthz') }}">Health</a> •
        <a href="https://render.com/docs/troubleshooting-deploys" target="_blank">Troubleshoot</a>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

PAGE_SIMPLE = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <title>{{ title }}</title>
  <style> body{background:#0f172a;color:#e5e7eb} a{color:#67e8f9} </style>
</head>
<body class="container py-5">
  <h2 class="mb-3">{{ title }}</h2>
  <div class="card p-4" style="background:rgba(15,23,42,.65);border:1px solid rgba(148,163,184,.25)">
    <div class="lh-lg">{{ body|safe }}</div>
    <a class="btn btn-primary mt-4" href="{{ url_for('home') }}">العودة للواجهة</a>
  </div>
</body>
</html>
"""

# ---------- مسارات أساسية ----------
@app.get("/")
def home():
    return render_template_string(
        PAGE_HOME,
        dsm_status=mount_results.get("dsm", "—"),
        cbt_status=mount_results.get("cbt", "—"),
        addiction_status=mount_results.get("addiction", "—"),
    )

@app.get("/healthz")
def healthz():
    return {"status": "ok", "app": "site_app"}, 200

# روابط دخول واضحة لكل وحدة (تؤدي لجذر الـ prefix)
@app.get("/dsm")
def dsm_entry():
    return render_template_string(PAGE_SIMPLE, title="DSM", body=f"اذهب إلى <code>/dsm/</code>.")

@app.get("/cbt")
def cbt_entry():
    return render_template_string(PAGE_SIMPLE, title="CBT", body=f"اذهب إلى <code>/cbt/</code>.")

@app.get("/addiction")
def addiction_entry():
    return render_template_string(PAGE_SIMPLE, title="الإدمان", body=f"اذهب إلى <code>/addiction/</code>.")

# ---------- تركيب الوحدات الاختيارية ----------
mount_results = {}
mount_results["dsm"] = mount_optional("dsm_suite", "/dsm", "DSM")
mount_results["cbt"] = mount_optional("cbt_suite", "/cbt", "CBT")
mount_results["addiction"] = mount_optional("addiction_suite", "/addiction", "برنامج الإدمان")

# ---------- أخطاء لطيفة ----------
@app.errorhandler(404)
def not_found(e):
    return render_template_string(PAGE_SIMPLE, title="404", body="الصفحة غير موجودة."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template_string(PAGE_SIMPLE, title="خطأ داخلي", body="حصل خطأ داخلي في الخادم."), 500

if __name__ == "__main__":
    app.run(debug=True)
