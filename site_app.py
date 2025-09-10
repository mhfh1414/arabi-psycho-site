# -*- coding: utf-8 -*-
# site_app.py — ملف التشغيل الرئيسي: يشغّل DSM + CBT + الإدمان + الواجهة

from __future__ import annotations
import os
from flask import Flask, render_template, render_template_string, send_from_directory

def create_app():
    # نخلي القوالب من نفس مجلد المشروع (مهم لو عندك home.html)
    app = Flask(__name__, template_folder=".", static_folder=None)
    app.config.update(JSON_AS_ASCII=False)

    # ===== تسجيل البلوبرنتات إن وُجدت =====
    # DSM
    try:
        from dsm import dsm_bp
        app.register_blueprint(dsm_bp)     # /dsm
        print("✔ DSM blueprint registered at /dsm")
    except Exception as e:
        print(f"⚠ DSM not registered: {e}")

    # CBT
    try:
        from cbt import cbt_bp
        app.register_blueprint(cbt_bp)     # /cbt
        print("✔ CBT blueprint registered at /cbt")
    except Exception as e:
        print(f"⚠ CBT not registered: {e}")

    # Addiction
    try:
        from addiction import addiction_bp
        app.register_blueprint(addiction_bp)  # /addiction
        print("✔ Addiction blueprint registered at /addiction")
    except Exception as e:
        print(f"⚠ Addiction not registered: {e}")

    # ===== الواجهة الرئيسية =====
    @app.route("/")
    def home():
        """
        لو عندك ملف واجهة اسمه home.html في نفس المجلد، بنعرضه.
        لو غير موجود، نعرض واجهة افتراضية مرتبة.
        """
        if os.path.exists("home.html"):
            # مهم: تأكد أن home.html لا يحتوي Jinja غير معرّف؛ يستخدم روابط مباشرة:
            #   /dsm  /cbt  /addiction  (أو غيّرها كما تحب)
            return render_template("home.html", year=_year())
        # واجهة افتراضية خفيفة
        fallback_html = """
        <!doctype html><html lang="ar" dir="rtl">
        <head>
          <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
          <title>عربي سايكو | الرئيسية</title>
          <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
          <style>
            :root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400;--w:#fff}
            *{box-sizing:border-box} body{margin:0;font-family:"Tajawal",system-ui;background:
              linear-gradient(135deg,var(--bg1),var(--bg2)) fixed;color:var(--w)}
            .wrap{max-width:1220px;margin:28px auto;padding:16px}
            .brand{display:flex;align-items:center;gap:12px}
            .badge{width:56px;height:56px;border-radius:16px;background:#0d2c54;border:1px solid #ffffff33;display:grid;place-items:center;font-weight:800}
            .title{margin:0;font-size:32px}
            .subtitle{margin:.25rem 0 0;color:#cfe0ff}
            .hero{margin:22px 0;padding:22px;background:rgba(255,255,255,.06);border:1px solid #ffffff22;border-radius:18px}
            .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
            @media(max-width:980px){.grid{grid-template-columns:1fr}}
            .card{background:rgba(255,255,255,.08);border:1px solid #ffffff22;border-radius:16px;padding:18px}
            .btn{display:inline-block;background:linear-gradient(180deg,#ffd86a,#f4b400);color:#2b1b02;
                 padding:12px 16px;border-radius:14px;text-decoration:none;font-weight:800}
            a.btn.block{display:block;text-align:center}
          </style>
        </head>
        <body><div class="wrap">
          <header class="brand">
            <div class="badge">AS</div>
            <div>
              <h1 class="title">عربي سايكو</h1>
              <p class="subtitle">مركز عربي سايكو يرحّب بكم — نخدمك أينما كنت</p>
            </div>
          </header>
          <section class="hero">
            <a class="btn" href="/dsm">🗂️ دراسة الحالة + DSM (ابدأ)</a>
          </section>
          <section class="grid">
            <div class="card"><h3>📖 DSM-5</h3><p>تشخيص مرجّح من دراسة الحالة.</p><a class="btn block" href="/dsm">ابدأ الآن</a></div>
            <div class="card"><h3>🧠 CBT + اختبارات</h3><p>لوحة اختبارات وبرامج علاج سلوكي معرفي.</p><a class="btn block" href="/cbt">فتح</a></div>
            <div class="card"><h3>🚭 علاج الإدمان</h3><p>تقييم وبرامج متخصصة للتعافي.</p><a class="btn block" href="/addiction">فتح</a></div>
          </section>
          <p style="opacity:.8;margin-top:14px">© {{year}} عربي سايكو — جميع الحقوق محفوظة</p>
        </div></body></html>
        """
        return render_template_string(fallback_html, year=_year())

    # ===== صحّة الخدمة =====
    @app.route("/health")
    def health():
        return {"ok": True, "service": "arabipsycho", "version": "1.0.0"}

    # ===== أيقونة (اختياري) =====
    @app.route("/favicon.ico")
    def favicon():
        if os.path.exists("favicon.ico"):
            return send_from_directory(".", "favicon.ico")
        return ("", 204)

    # ===== أخطاء مخصّصة خفيفة =====
    @app.errorhandler(404)
    def not_found(e):
        return render_template_string("""
        <!doctype html><meta charset="utf-8">
        <div style="font-family:Tajawal,system-ui;direction:rtl;padding:40px">
        <h2>404 — المسار غير موجود</h2>
        <p><a href="/">العودة للواجهة</a></p></div>"""), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template_string("""
        <!doctype html><meta charset="utf-8">
        <div style="font-family:Tajawal,system-ui;direction:rtl;padding:40px">
        <h2>خطأ داخلي</h2><p>حدث خطأ غير متوقع.</p><p><a href="/">العودة للواجهة</a></p></div>"""), 500

    return app

def _year():
    try:
        from datetime import datetime
        return datetime.now().year
    except:
        return 2025

if __name__ == "__main__":
    app = create_app()
    # المنفذ 10000 حسب اللي تعودنا عليه
    app.run(host="0.0.0.0", port=10000, debug=True)
