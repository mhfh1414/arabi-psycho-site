# -*- coding: utf-8 -*-
from flask import render_template_string

_BASE = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
    body{font-family:"Tajawal",system-ui;background:linear-gradient(135deg,#0b3a75,#0a65b0) fixed;color:#fff;margin:0}
    .wrap{max-width:900px;margin:24px auto;padding:16px}
    .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px;backdrop-filter:blur(6px)}
    label{display:block;margin:8px 2px;color:#ffe28a}
    input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:10px}
    .btn{display:inline-block;background:#f4b400;color:#2b1b02;border-radius:14px;padding:10px 14px;text-decoration:none;font-weight:800}
  </style>
</head>
<body>
  <div class="wrap">{{ body|safe }}</div>
</body>
</html>
"""

def _render(title, body):
    return render_template_string(_BASE, title=title, body=body)

def render_addiction_get():
    form = """
    <div class="card">
      <h2 style="margin-top:0">🚭 تقييم أولي لعلاج الإدمان</h2>
      <form method="post">
        <label>نوع المادة</label>
        <select name="substance">
          <option>كحول</option><option>قنب/حشيش</option><option>منشطات (أمفيتامين/كوكايين)</option>
          <option>أفيونات (هيروين/مورفين)</option><option>أدوية نفسية بإساءة استخدام</option><option>أخرى</option>
        </select>
        <label>مدة الاستخدام (أشهر)</label>
        <input name="months" type="number" min="0" placeholder="مثال: 6">
        <label>وتيرة الاستخدام</label>
        <select name="freq">
          <option>متقطع</option><option>أسبوعي</option><option>يومي</option><option>عدة مرات يوميًا</option>
        </select>
        <label>أعراض انسحاب (اختياري)</label>
        <textarea name="withdrawal" placeholder="رجفان، تعرّق، أرق، قلق، ألم..."></textarea>
        <label>مشاكل وظيفية/اجتماعية (اختياري)</label>
        <textarea name="impact" placeholder="مشاكل عمل/علاقات/قانون..."></textarea>
        <div style="margin-top:10px"><button class="btn" type="submit">تحليل أولي</button> <a class="btn" href="/">الواجهة</a></div>
      </form>
    </div>
    """
    return _render("علاج الإدمان", form)

def render_addiction_post(form):
    substance = form.get("substance","")
    months = int(form.get("months","0") or 0)
    freq = form.get("freq","")
    withdrawal = (form.get("withdrawal","") or "").strip()
    impact = (form.get("impact","") or "").strip()

    risk = 0
    if months >= 6: risk += 1
    if freq in ["يومي","عدة مرات يوميًا"]: risk += 2
    if withdrawal: risk += 1
    if impact: risk += 1

    if risk <= 1:
        level = "مستوى خطورة منخفض — توعية ودعم نفسي مبكر."
    elif risk == 2:
        level = "متوسط — خطة علاجية خارجية + متابعات."
    elif risk == 3:
        level = "متوسط إلى مرتفع — برنامج مكثف مع إشراف متخصص."
    else:
        level = "مرتفع — يُنصح ببرنامج علاجي منظّم وقد يحتاج إزالة سمية طبية."

    plan = f"""
    <div class="card">
      <h2 style="margin-top:0">📋 النتيجة الأولية</h2>
      <p><strong>المادة:</strong> {substance} | <strong>المدة (أشهر):</strong> {months} | <strong>الوتيرة:</strong> {freq}</p>
      <p><strong>تقدير الخطورة:</strong> {level}</p>
      <h3>🧭 الخطوات المقترحة:</h3>
      <ul>
        <li>تثقيف حول المخاطر واستراتيجيات الوقاية من الانتكاس.</li>
        <li>جلسات علاج سلوكي معرفي فردية/جماعية.</li>
        <li>إشراك الأسرة/الدعم الاجتماعي عند الملاءمة.</li>
        <li>مراجعة طبية للأدوية الممكنة للأعراض الانسحابية (حسب الحالة).</li>
        <li>خطة طوارئ عند الرغبة الشديدة/الانتكاس.</li>
      </ul>
      <p>⚠️ هذه نتيجة أولية للمساعدة وليست تشخيصًا نهائيًا.</p>
      <p><a class="btn" href="/addiction">رجوع</a> <a class="btn" href="/">الواجهة</a></p>
    </div>
    """
    return _render("علاج الإدمان — نتيجة", plan)
