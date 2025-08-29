# -*- coding: utf-8 -*-
"""
Unified DSM-5 Arabic site + Telegram bot + WhatsApp webhook (Twilio)
ملف: site_app.py

المتطلبات (pip):
    flask
    python-telegram-bot==21.*   # للبوت تيليجرام (اختياري)
    twilio                      # لو بتفعّل واتساب عبر Twilio (اختياري)

هيكلة متوقعة:
project_root/
    site_app.py
    dsm_index.py
    DSM5/  (الملفات 01..19)

ENV:
    BOT_TOKEN=<توكن BotFather>   # لتشغيل تيليجرام (اختياري)
    TELEGRAM_ENABLE=1            # افتراضي 1 إذا وُجد التوكن
    PORT=5000
"""

from __future__ import annotations

import os, json, threading
from flask import Flask, request, jsonify, abort, Response, render_template_string
import dsm_index as dsm

# Twilio (واتساب) — اختياري
try:
    from twilio.twiml.messaging_response import MessagingResponse
    TWILIO_OK = True
except Exception:
    TWILIO_OK = False

# Telegram — اختياري
TELEGRAM_AVAILABLE = False
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters
    TELEGRAM_AVAILABLE = True
except Exception:
    TELEGRAM_AVAILABLE = False

APP_TITLE = "DSM-5 (AR) — موسى"
PORT = int(os.getenv("PORT", "5000"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_ENABLE = os.getenv("TELEGRAM_ENABLE", "1") == "1" and bool(BOT_TOKEN)

app = Flask(__name__)

# ============================= HTML Templates =============================
BASE_HTML = r"""
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ title or 'DSM-5 Arabic' }}</title>
  <style>
    :root { --bg:#0f172a; --card:#111827; --muted:#9ca3af; --txt:#f8fafc; --accent:#60a5fa; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Tahoma, Arial, sans-serif; background: var(--bg); color: var(--txt); }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }
    header { padding: 18px 20px; background: #0b1220; position: sticky; top:0; z-index: 2; border-bottom: 1px solid #1f2937;}
    header .brand { font-weight: 800; letter-spacing: .5px; }
    main { max-width: 1100px; margin: 24px auto; padding: 0 16px 48px; }
    .grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); }
    .card { background: var(--card); border: 1px solid #1f2937; border-radius: 14px; padding: 16px; box-shadow: 0 4px 16px rgb(0 0 0 / .2); }
    .card h3 { margin: 0 0 6px; font-size: 18px; }
    .meta { color: var(--muted); font-size: 12px; }
    .pill { display: inline-block; padding: 4px 8px; border-radius: 999px; background: #0b1220; border: 1px solid #1f2937; font-size: 12px; color: var(--muted); }
    .row { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
    .toolbar { display: flex; gap: 10px; align-items: center; margin: 14px 0 20px; }
    input[type="search"] { width: 320px; max-width: 100%; background: #0b1220; border: 1px solid #1f2937; color: var(--txt); padding: 10px 12px; border-radius: 10px; outline: none; }
    button, .btn { background: #1d4ed8; color: #fff; border: none; padding: 10px 14px; border-radius: 10px; cursor: pointer; font-weight: 600; }
    .btn.secondary { background: #374151; }
    .btn:hover { filter: brightness(1.1); }
    .kbd { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 12px; background: #0b1220; border: 1px solid #1f2937; padding: 2px 6px; border-radius: 6px; color: var(--muted); }
    .markdown h1 { font-size: 26px; margin: 10px 0 6px; }
    .markdown ul { line-height: 1.9; }
    footer { color: var(--muted); text-align: center; padding: 24px 0; }
    .empty { color: var(--muted); padding: 24px 0; }
    .badge { background:#0b1220; border:1px solid #1f2937; padding:2px 8px; border-radius:8px; font-size:12px; color:#cbd5e1; }
  </style>
</head>
<body>
  <header>
    <div class="row">
      <div class="brand"><a href="{{ url_for('home') }}">DSM-5 (AR)</a></div>
      <form action="{{ url_for('search_page') }}" method="get" style="margin-inline-start:auto">
        <input type="search" name="q" placeholder="ابحث: قلق، OCD، PTSD..." value="{{ request.args.get('q','') }}">
        <button>بحث</button>
      </form>
    </div>
  </header>
  <main>
    {% block content %}{% endblock %}
  </main>
  <footer>موسى — نسخة تعليمية معاد صياغتها بالعربية • {{ request.path }}</footer>
</body>
</html>
"""

INDEX_HTML = r"""
{% extends "base.html" %}
{% block content %}
  <h1>الفئات</h1>
  <div class="toolbar">
    <a class="btn secondary" href="{{ url_for('export_all_json_route') }}">تصدير JSON كامل</a>
    <span class="kbd">/dsm/&lt;category&gt;/&lt;key&gt;</span>
    <span class="kbd">/api/dsm/&lt;category&gt;/&lt;key&gt;</span>
  </div>
  <div class="grid">
    {% for cat in cats %}
      <div class="card">
        <h3><a href="{{ url_for('category_page', category=cat.key) }}">{{ cat.label_ar }}</a></h3>
        <div class="meta">{{ cat.key }}</div>
        <div class="row" style="margin-top:8px">
          <span class="pill">عدد الاضطرابات: {{ cat.count }}</span>
        </div>
      </div>
    {% endfor %}
  </div>
{% endblock %}
"""

CATEGORY_HTML = r"""
{% extends "base.html" %}
{% block content %}
  <div class="row">
    <h1 style="margin:0">{{ label_ar }}</h1>
    <span class="badge">{{ category }}</span>
  </div>
  <div class="toolbar">
    <a class="btn secondary" href="{{ url_for('home') }}">الرجوع للفئات</a>
  </div>
  {% if items %}
  <div class="grid">
    {% for item in items %}
      <div class="card">
        <h3><a href="{{ url_for('disorder_page', category=category, key=item.key) }}">{{ item.name_ar }}</a></h3>
        <div class="meta">{{ item.name_en }}</div>
        <div class="row" style="margin-top:10px">
          <a class="btn" href="{{ url_for('disorder_page', category=category, key=item.key) }}">عرض</a>
          <a class="btn secondary" href="{{ url_for('disorder_api', category=category, key=item.key) }}">JSON</a>
        </div>
      </div>
    {% endfor %}
  </div>
  {% else %}
    <div class="empty">لا توجد عناصر في هذه الفئة.</div>
  {% endif %}
{% endblock %}
"""

DISORDER_HTML = r"""
{% extends "base.html" %}
{% block content %}
  <div class="row">
    <h1 style="margin:0">{{ d.get('name_ar','') }}</h1>
    <span class="badge">{{ category }} / {{ key }}</span>
  </div>
  <div class="meta">{{ d.get('name_en','') }}</div>

  <div class="toolbar">
    <a class="btn secondary" href="{{ url_for('category_page', category=category) }}">رجوع</a>
    <a class="btn" href="{{ url_for('disorder_api', category=category, key=key) }}">JSON</a>
  </div>

  <div class="card markdown">
    <p><b>نظرة عامة:</b> {{ d.get('overview','') }}</p>
    <p><b>المدة الشائعة/الشرط الزمني:</b> {{ d.get('duration','—') }}</p>
    <h3>المعايير التشخيصية (ملخص)</h3>
    <ul>
      {% for c in d.get('criteria', []) %}
        <li>({{ c.get('code','?') }}) {{ c.get('text','') }}</li>
      {% endfor %}
    </ul>

    {% if d.get('specifiers') %}
      <p><b>محددات/أنماط فرعية:</b> {{ d.get('specifiers')|join(', ') }}</p>
    {% endif %}
    {% if d.get('severity_guidance') %}
      <p><b>توجيه تقدير الشدة:</b> {{ d.get('severity_guidance') }}</p>
    {% endif %}
    {% if d.get('differentials') %}
      <p><b>تشاخيص تفريقية مختصرة:</b> {{ d.get('differentials')|join(', ') }}</p>
    {% endif %}
  </div>
{% endblock %}
"""

SEARCH_HTML = r"""
{% extends "base.html" %}
{% block content %}
  <h1>نتائج البحث</h1>
  <div class="toolbar">
    <form action="{{ url_for('search_page') }}" method="get">
      <input type="search" name="q" placeholder="ابحث..." value="{{ q or '' }}">
      <button>بحث</button>
    </form>
    <a class="btn secondary" href="{{ url_for('home') }}">الصفحة الرئيسية</a>
  </div>

  {% if hits %}
    <div class="grid">
      {% for h in hits %}
        <div class="card">
          <h3><a href="{{ url_for('disorder_page', category=h.category, key=h.key) }}">{{ h.name_ar }}</a></h3>
          <div class="meta">{{ h.category }} / {{ h.key }}</div>
          <div class="row" style="margin-top:10px">
            <a class="btn" href="{{ url_for('disorder_page', category=h.category, key=h.key) }}">عرض</a>
            <a class="btn secondary" href="{{ url_for('disorder_api', category=h.category, key=h.key) }}">JSON</a>
          </div>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <div class="empty">لا توجد نتائج لـ <b>{{ q }}</b></div>
  {% endif %}
{% endblock %}
"""

# ============================= Website & API =============================
@app.route("/")
def home():
    labels = {
        "anxiety": "اضطرابات القلق", "ocd_related": "الوسواس القهري والمرتبطة", "mood": "اضطرابات المزاج",
        "schizo_spectrum": "طيف الفصام", "neurodevelopmental": "اضطرابات النمو العصبي",
        "trauma_stressor": "اضطرابات الكرب والشدّة", "dissociative": "اضطرابات تفارقية",
        "somatic": "أعراض جسدية وما يرتبط بها", "feeding_eating": "اضطرابات الأكل",
        "elimination": "اضطرابات الإطراح", "sleep_wake": "النوم/الاستيقاظ",
        "sexual_dys": "الوظائف الجنسية", "gender_dysphoria": "الهوية الجندرية",
        "disruptive_impulse": "الاضطرابات التخريبية والاندفاع", "substance": "الاضطرابات المتعلقة بالمواد",
        "neurocognitive": "الاضطرابات الإدراكية", "personality": "اضطرابات الشخصية",
        "paraphilic": "الولع الجنسي", "other": "أخرى/غير محددة",
    }
    cats = []
    for cat in dsm.categories():
        cats.append({"key": cat, "label_ar": labels.get(cat, cat), "count": len(dsm.REGISTRY.get(cat, {}))})
    page = render_template_string(BASE_HTML, title="الفئات")
    page += render_template_string(INDEX_HTML, cats=cats)
    return page

@app.route("/cat/<category>")
def category_page(category):
    if category not in dsm.REGISTRY:
        abort(404)
    ds = dsm.REGISTRY[category]
    items = [{"key": k, "name_ar": v.get("name_ar",""), "name_en": v.get("name_en","")} for k, v in ds.items()]
    labels = {
        "anxiety": "اضطرابات القلق", "ocd_related": "الوسواس القهري والمرتبطة", "mood": "اضطرابات المزاج",
        "schizo_spectrum": "طيف الفصام", "neurodevelopmental": "اضطرابات النمو العصبي",
        "trauma_stressor": "اضطرابات الكرب والشدّة", "dissociative": "اضطرابات تفارقية",
        "somatic": "أعراض جسدية وما يرتبط بها", "feeding_eating": "اضطرابات الأكل",
        "elimination": "اضطرابات الإطراح", "sleep_wake": "النوم/الاستيقاظ",
        "sexual_dys": "الوظائف الجنسية", "gender_dysphoria": "الهوية الجندرية",
        "disruptive_impulse": "الاضطرابات التخريبية والاندفاع", "substance": "الاضطرابات المتعلقة بالمواد",
        "neurocognitive": "الاضطرابات الإدراكية", "personality": "اضطرابات الشخصية",
        "paraphilic": "الولع الجنسي", "other": "أخرى/غير محددة",
    }
    label_ar = labels.get(category, category)
    page = render_template_string(BASE_HTML, title=label_ar)
    page += render_template_string(CATEGORY_HTML, category=category, items=items, label_ar=label_ar)
    return page

@app.route("/dsm/<category>/<key>")
def disorder_page(category, key):
    try:
        d = dsm.get(category, key)
    except KeyError:
        abort(404)
    title = f"{d.get('name_ar','')} — {category}/{key}"
    page = render_template_string(BASE_HTML, title=title)
    page += render_template_string(DISORDER_HTML, category=category, key=key, d=d)
    return page

@app.route("/search")
def search_page():
    q = request.args.get("q", "").strip()
    hits = dsm.search_all(q) if q else []
    page = render_template_string(BASE_HTML, title="بحث")
    page += render_template_string(SEARCH_HTML, hits=hits, q=q)
    return page

# REST API
@app.get("/api/categories")
def categories_api():
    return jsonify(dsm.categories())

@app.get("/api/cat/<category>")
def category_api(category):
    if category not in dsm.REGISTRY:
        abort(404)
    items = [{"key": k, "name_ar": v.get("name_ar",""), "name_en": v.get("name_en","")} for k, v in dsm.REGISTRY[category].items()]
    return jsonify(items)

@app.get("/api/dsm/<category>/<key>")
def disorder_api(category, key):
    try:
        d = dsm.get(category, key)
    except KeyError:
        abort(404)
    return jsonify(d)

@app.get("/api/search")
def search_api():
    q = request.args.get("q", "").strip()
    return jsonify(dsm.search_all(q) if q else [])

@app.get("/export/json")
def export_all_json_route():
    data = dsm.export_all_json(indent=2)
    return Response(data, mimetype="application/json")

# ============================= WhatsApp (Twilio) =============================
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    if not TWILIO_OK:
        return "Twilio غير مُثبّت على هذا السيرفر.", 500
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()
    if not incoming_msg:
        msg.body("أرسل اسم اضطراب أو كلمة مفتاحية (مثال: PTSD، قلق، وسواس).")
        return str(resp)
    hits = dsm.search_all(incoming_msg)
    if not hits:
        msg.body("ما لقيت نتيجة 🔍 — جرّب: anxiety, ocd, ptsd")
    else:
        h = hits[0]
        md = dsm.to_markdown(h["category"], h["key"])
        msg.body(md)
    return str(resp)

# ============================= Telegram (background) =============================
def start_telegram_bot_in_background():
    if not TELEGRAM_AVAILABLE or not TELEGRAM_ENABLE:
        print("Telegram bot disabled or unavailable.")
        return

    async def start(update, context):
        cats = dsm.categories()
        msg = "أهلاً بك 👋\nاكتب اسم فئة أو اضطراب، مثل: anxiety, mood, ptsd, gad\n\nالفئات:\n" + "\n".join(cats)
        await update.message.reply_text(msg)

    async def search_handler(update, context):
        text = (update.message.text or "").strip()
        hits = dsm.search_all(text)
        if not hits:
            await update.message.reply_text("ما لقيت نتيجة 🔍 — جرّب: anxiety, ocd, ptsd")
            return
        for h in hits[:3]:
            md = dsm.to_markdown(h["category"], h["key"])
            await update.message.reply_text(md)

    async def run_async():
        app_tg = Application.builder().token(BOT_TOKEN).build()
        app_tg.add_handler(CommandHandler("start", start))
        app_tg.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))
        print("Telegram bot started.")
        await app_tg.initialize()
        await app_tg.start()
        await app_tg.updater.start_polling()

    def runner():
        import asyncio
        asyncio.run(run_async())

    threading.Thread(target=runner, daemon=True).start()

# ============================= Run =============================
@app.errorhandler(404)
def not_found(e):
    page = render_template_string(BASE_HTML, title="غير موجود")
    page += render_template_string(
        r"""{% extends "base.html" %}{% block content %}<div class="empty">العنصر المطلوب غير موجود.</div>{% endblock %}"""
    )
    return page, 404

if __name__ == "__main__":
    start_telegram_bot_in_background()
    print(f"Running Flask on 0.0.0.0:{PORT} • Telegram={'ON' if TELEGRAM_ENABLE else 'OFF'} • WhatsApp=/whatsapp")
    app.run(host="0.0.0.0", port=PORT, debug=True)
