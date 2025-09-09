# -*- coding: utf-8 -*-
# site_app.py — مشغّل رئيسي مرن لكل البلوبرنتس المتاحة

from __future__ import annotations
from flask import Flask, jsonify, redirect, url_for, render_template_string, request
import importlib
import traceback

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        JSON_AS_ASCII=False,             # عرض عربي صحيح
        TEMPLATES_AUTO_RELOAD=True
    )

    # فعّل CORS إن وُجدت المكتبة، وإلا أكمل طبيعي
    try:
        from flask_cors import CORS
        CORS(app)
    except Exception:
        pass

    # ====== أداة تسجيل مرنة لأي بلوبرنت ======
    def try_register(mod_name: str, attr_candidates: list[str]) -> bool:
        """
        يحاول استيراد module وتسجيل أول Blueprint يجده من الأسماء المعطاة.
        يرجع True إذا سُجّل شيء.
        """
        try:
            mod = importlib.import_module(mod_name)
        except Exception as e:
            print(f"[site_app] لم أستطع استيراد {mod_name}: {e}")
            return False

        for attr in attr_candidates:
            bp = getattr(mod, attr, None)
            if bp is not None:
                try:
                    app.register_blueprint(bp)
                    print(f"[site_app] سُجّل Blueprint من {mod_name}.{attr} على البادئة: {getattr(bp, 'url_prefix', '')}")
                    return True
                except Exception as e:
                    print(f"[site_app] فشل تسجيل {mod_name}.{attr}: {e}")
                    traceback.print_exc()
        print(f"[site_app] لم أجد Blueprint مناسب داخل {mod_name} (بحثت في {attr_candidates})")
        return False

    # ====== جرّب تسجيل بلوبرنت الملفات المعروفة ======
    # home.py        => home.bp أو home.home_bp
    # dsm_suite.py   => dsm_suite.dsm_bp
    # cbt_suite.py   => cbt_suite.cbt_bp
    # addiction_suite.py => addiction_suite.addiction_bp
    registered = {
        "home":            try_register("home", ["bp", "home_bp"]),
        "dsm_suite":       try_register("dsm_suite", ["dsm_bp", "bp"]),
        "cbt_suite":       try_register("cbt_suite", ["cbt_bp", "bp"]),
        "addiction_suite": try_register("addiction_suite", ["addiction_bp", "bp"]),
    }
    print("[site_app] حالة التسجيل:", registered)

    # ====== صفحة هوم بديلة إذا ما وُجد home blueprint ======
    if not registered.get("home"):
        @app.route("/")
        def fallback_home():
            # بناء روابط متاحة تلقائيًا
            links = []
            for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
                if rule.endpoint in ("static", "fallback_home", "health", "ready", "routes"):
                    continue
                methods = ",".join(sorted(m for m in rule.methods if m in {"GET","POST"}))
                links.append(f"<tr><td>{rule.rule}</td><td>{methods}</td><td>{rule.endpoint}</td></tr>")
            table = "".join(links) or "<tr><td colspan=3>لا توجد مسارات أخرى.</td></tr>"

            html = f"""
            <!doctype html><html lang="ar" dir="rtl"><head>
            <meta charset="utf-8"><title>عربي سايكو | الرئيسية (افتراضية)</title>
            <meta name="viewport" content="width=device-width, initial-scale=1"/>
            <style>
              body{{font-family:system-ui,'Tajawal',sans-serif;background:#0b3a75;color:#fff;margin:0}}
              .wrap{{max-width:1000px;margin:24px auto;padding:16px}}
              .card{{background:rgba(255,255,255,.08);border:1px solid #ffffff33;border-radius:16px;padding:18px}}
              a.btn{{display:inline-block;background:#f4b400;color:#2b1b02;padding:10px 14px;border-radius:12px;
                    text-decoration:none;font-weight:800;margin:6px 8px 0 0}}
              table{{width:100%;border-collapse:collapse;margin-top:12px}}
              th,td{{border-bottom:1px solid #ffffff22;padding:8px 6px;text-align:right}}
              th{{color:#ffd86a}}
            </style></head><body><div class="wrap">
            <div class="card">
              <h2>عربي سايكو — لوحة وصول سريعة</h2>
              <p>تم تشغيل التطبيق. لم أجد بلوبرنت <b>home</b>، لذلك هذه الصفحة بديلة.</p>
              <div>
                <a class="btn" href="/dsm">DSM</a>
                <a class="btn" href="/cbt">CBT</a>
                <a class="btn" href="/addiction">الإدمان</a>
              </div>
              <h3 style="margin-top:16px">المسارات المتاحة</h3>
              <table><thead><tr><th>المسار</th><th>الطرق</th><th>الـ endpoint</th></tr></thead>
              <tbody>{table}</tbody></table>
            </div></div></body></html>
            """
            return html

    # ====== نقاط صحّة وخدمات مفيدة ======
    @app.route("/health")
    def health():
        return jsonify(ok=True, service="arabipsycho", ip=request.headers.get("X-Forwarded-For", request.remote_addr)), 200

    @app.route("/ready")
    def ready():
        return "OK", 200

    @app.route("/routes")
    def routes():
        data = []
        for rule in app.url_map.iter_rules():
            data.append({
                "rule": rule.rule,
                "endpoint": rule.endpoint,
                "methods": sorted(list(rule.methods)),
            })
        return jsonify(data)

    # 404 مُحسّنة
    @app.errorhandler(404)
    def not_found(e):
        return render_template_string("""
        <!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8">
        <title>الصفحة غير موجودة</title>
        <body style="font-family:system-ui; background:#0a244d; color:#fff">
          <div style="max-width:800px; margin:60px auto; padding:20px">
            <h2>404 — الصفحة غير موجودة</h2>
            <p>تأكد من الرابط. اطّلع على <a href="/routes" style="color:#ffd86a">/routes</a> لمعرفة المسارات المتاحة.</p>
            <p><a href="/" style="color:#ffd86a">العودة للرئيسية</a></p>
          </div>
        </body></html>
        """), 404

    return app


# كائن التطبيق الذي سيستخدمه gunicorn
app = create_app()

if __name__ == "__main__":
    # تشغيل محلي/تجريبي
    app.run(host="0.0.0.0", port=10000, debug=True)
