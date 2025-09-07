# -*- coding: utf-8 -*-
# addiction_suite.py — تقييمات الإدمان (ASSIST-lite + DSM-5 SUD)

from flask import Blueprint, render_template_string, request

addiction_bp = Blueprint("addiction_bp", __name__, url_prefix="/addiction")

BASE = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{{title}}</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{--p1:#0b3a75;--p2:#0a65b0;--gold:#f4b400;--w:#fff;--glass:rgba(255,255,255,.08);--b:rgba(255,255,255,.14)}
*{box-sizing:border-box}body{margin:0;font-family:Tajawal,system-ui;background:linear-gradient(135deg,var(--p1),var(--p2)) fixed;color:#fff}
.wrap{max-width:1100px;margin:26px auto;padding:16px}
.card{background:var(--glass);border:1px solid var(--b);border-radius:16px;padding:18px}
a.btn,button.btn{display:inline-block;background:var(--gold);color:#2b1b02;border-radius:14px;padding:10px 14px;text-decoration:none;font-weight:800;border:none;cursor:pointer}
label{display:block;margin:8px 0;color:#ffe28a}
.q{margin:10px 0;padding:10px;border-radius:12px;border:1px solid var(--b)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:4px 0}
.ok{background:#16a34a;color:#fff}.warn{background:#ef4444;color:#fff}.mid{background:#f59e0b;color:#1f1302}
</style></head><body><div class="wrap">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
  <h2 style="margin:0">{{heading}}</h2>
  <div><a class="btn" href="/">الواجهة</a> <a class="btn" href="/addiction">لوحة الإدمان</a></div>
</div>
{{body|safe}}
</div></body></html>
"""

@addiction_bp.route("/")
def hub():
    body = """
    <div class="card">
      <p>اختر أداة التقييم:</p>
      <div class="grid">
        <a class="btn" href="/addiction/assist">ASSIST-Lite (متعدد المواد)</a>
        <a class="btn" href="/addiction/dsm?sub=alcohol">DSM-5 للمواد — كحول</a>
        <a class="btn" href="/addiction/dsm?sub=cannabis">DSM-5 — قنب/حشيش</a>
        <a class="btn" href="/addiction/dsm?sub=opioids">DSM-5 — أفيونات</a>
        <a class="btn" href="/addiction/dsm?sub=stimulants">DSM-5 — منبهات</a>
      </div>
    </div>
    """
    return render_template_string(BASE, title="الإدمان | لوحة", heading="🚭 تقييمات الإدمان", body=body)

# ---------------- ASSIST-lite ----------------
ASSIST_SUBS = [
    ("alcohol","كحول"),
    ("cannabis","قنب/حشيش"),
    ("opioids","أفيونات"),
    ("stimulants","منبهات"),
    ("sedatives","مهدئات/بنزوديازبينات"),
    ("tobacco","تبغ/نيكوتين")
]
ASSIST_Q = [
    "خلال الأشهر الثلاثة الماضية: كم مرة استخدمت المادة؟",
    "كم مرة رغبت بقوة أو عانيت شوقًا للمادة؟",
    "هل سبب الاستخدام مشاكل صحية أو نفسية أو اجتماعية؟",
    "هل فشلت بالتزاماتك بسبب الاستخدام؟",
    "هل لاحظ أحد (أقارب/أصدقاء/طبيب) وأبدى قلقًا من استخدامك؟",
]
ASSIST_OPTS = [("أبدًا",0),("مرة شهرية",1),("مرات شهرية",2),("أسبوعيًا",3),("يوميًا/تقريبًا يوميًا",4)]

@addiction_bp.route("/assist", methods=["GET","POST"])
def assist():
    if request.method=="GET":
        blocks=[]
        idx=1
        for key,lab in ASSIST_SUBS:
            blocks.append(f"<h3>• {lab}</h3>")
            for q in ASSIST_Q:
                radios = "".join([f"<label><input type='radio' name='q{idx}' value='{v}' required> {t}</label>" for t,v in ASSIST_OPTS])
                blocks.append(f"<div class='q'><b>{q}</b><div>{radios}</div></div>")
                idx+=1
        form = "<form method='post'>"+"".join(blocks)+"<button class='btn'>احسب</button></form>"
        return render_template_string(BASE, title="ASSIST-Lite", heading="ASSIST-Lite — فحص متعدد المواد", body=f"<div class='card'>{form}</div>")
    # حساب
    scores=[]
    n_per_sub = len(ASSIST_Q)
    for s in range(len(ASSIST_SUBS)):
        subtotal = 0
        for i in range(s*n_per_sub+1, s*n_per_sub+n_per_sub+1):
            subtotal += int(request.form.get(f"q{i}",0))
        key,lab = ASSIST_SUBS[s]
        level = "منخفض" if subtotal<=2 else ("متوسط" if subtotal<=8 else "مرتفع")
        color = "ok" if level=="منخفض" else ("mid" if level=="متوسط" else "warn")
        scores.append((lab, subtotal, level, color))
    rows = "".join([f"<tr><td>{lab}</td><td>{sc}</td><td><span class='badge {col}'>{lvl}</span></td></tr>" for lab,sc,lvl,col in scores])
    body = f"""
    <div class="card">
      <h3>نتائج ASSIST-Lite</h3>
      <table style="width:100%;border-collapse:collapse">
        <thead><tr><th>المادة</th><th>المجموع</th><th>مستوى الخطورة</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <p style="margin-top:8px">المستوى المرتفع يستدعي تقييمًا علاجيًا وخطة تقليل الأذى/الامتناع.</p>
      <a class="btn" href="/addiction">عودة</a>
    </div>"""
    return render_template_string(BASE, title="ASSIST-Lite نتيجة", heading="ASSIST-Lite — النتائج", body=body)

# ---------------- DSM-5 SUD (11 معيارًا) ----------------
DSM_LABELS = {
    "alcohol":"الكحول",
    "cannabis":"القنب/الحشيش",
    "opioids":"الأفيونات",
    "stimulants":"المنبهات",
}
DSM_ITEMS = [
    "تُستخدم المادة أكثر أو لمدة أطول من المقصود",
    "رغبة مستمرة أو محاولات غير ناجحة للتقليل/الإيقاف",
    "وقت طويل للحصول على/استخدام/التعافي من المادة",
    "الرغبة الشديدة (Craving)",
    "فشل بالواجبات (عمل/دراسة/منزل)",
    "استمرار الاستخدام رغم مشاكل اجتماعية/علاقات",
    "تخلّي عن أنشطة مهمة بسبب المادة",
    "استخدام بمواقف خطرة (قيادة/آلات...)",
    "استمرار الاستخدام رغم مشاكل جسدية/نفسية سببتها المادة",
    "تحمل (زيادة الكمية/تأثير أقل)",
    "انسحاب (أعراض عند التوقف أو أخذ المادة لتجنبها)"
]

@addiction_bp.route("/dsm", methods=["GET","POST"])
def dsm_sud():
    sub = request.args.get("sub","alcohol")
    label = DSM_LABELS.get(sub, "المادة")
    if request.method=="GET":
        radios = "<label><input type='radio' name='X' value='0' checked hidden></label>"
        qs=[]
        for i,q in enumerate(DSM_ITEMS,1):
            qs.append(f"<div class='q'><b>{i}.</b> {q}<div><label><input type='checkbox' name='q{i}' value='1'> موجود آخر 12 شهرًا</label></div></div>")
        form = "<form method='post'>" + "".join(qs) + f"<input type='hidden' name='sub' value='{sub}'/>" + "<button class='btn'>احسب</button></form>"
        return render_template_string(BASE, title=f"DSM-5 — {label}", heading=f"DSM-5 — معايير اضطراب استخدام {label}", body=f"<div class='card'>{form}</div>")
    sub = request.form.get("sub","alcohol"); label = DSM_LABELS.get(sub, "المادة")
    total = sum(1 for i in range(1, len(DSM_ITEMS)+1) if request.form.get(f"q{i}")=="1")
    if   total<=1: sev="لا ينطبق/خفيف جدًا"; color="ok"
    elif total<=2: sev="خفيف"; color="mid"
    elif total<=5: sev="متوسط"; color="mid"
    else:          sev="شديد"; color="warn"
    body = f"""
    <div class="card">
      <h3>عدد المعايير المتحققة: {total} / 11</h3>
      <span class="badge {color}">{sev}</span>
      <p>وجود التحمل/الانسحاب وحده مع الاستخدام الموصوف طبيًا لا يكفي للتشخيص.</p>
      <a class="btn" href="/addiction">عودة</a>
    </div>"""
    return render_template_string(BASE, title=f"DSM-5 {label} — نتيجة", heading=f"DSM-5 — {label}: النتيجة", body=body)
