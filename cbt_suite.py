# -*- coding: utf-8 -*-
# cbt_suite.py — لوحة اختبارات CBT (استبيانات قياسية) + حساب الدرجات

from flask import Blueprint, render_template_string, request, redirect, url_for

cbt_bp = Blueprint("cbt_bp", __name__, url_prefix="/cbt")

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
.grid{display:grid;grid-template-columns:repeat(auto-fit, minmax(260px,1fr));gap:14px}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:4px 0}
.ok{background:#16a34a;color:#fff}.warn{background:#ef4444;color:#fff}.mid{background:#f59e0b;color:#1f1302}
</style></head><body><div class="wrap">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
  <h2 style="margin:0">{{heading}}</h2>
  <div>
    <a class="btn" href="/">الواجهة</a>
    <a class="btn" href="/cbt">لوحة الاختبارات</a>
  </div>
</div>
{{body|safe}}
</div></body></html>
"""

# ------------------ لوحة الاختبارات ------------------
@cbt_bp.route("/")
def hub():
    body = """
    <div class="card">
      <p>اختر اختبارًا:</p>
      <div class="grid">
        <a class="btn" href="/cbt/phq9">PHQ-9 (اكتئاب)</a>
        <a class="btn" href="/cbt/gad7">GAD-7 (قلق)</a>
        <a class="btn" href="/cbt/dass21">DASS-21 (اكتئاب/قلق/توتر)</a>
        <a class="btn" href="/cbt/pcl5">PCL-5 (صدمة)</a>
        <a class="btn" href="/cbt/asrs">ASRS v1.1 (ADHD بالغين)</a>
        <a class="btn" href="/cbt/oci">OCI-R (وسواس قهري)</a>
        <a class="btn" href="/cbt/audit">AUDIT / AUDIT-C (كحول)</a>
        <a class="btn" href="/cbt/brs">BRS (الصمود النفسي)</a>
      </div>
    </div>
    """
    return render_template_string(BASE, title="CBT | لوحة الاختبارات", heading="🧪 اختبارات نفسية وشخصية", body=body)

# ============ أدوات عامة لبناء النماذج والنتائج ============
def _radio(name, options):
    html = []
    for i, (label, val) in enumerate(options):
        html.append(f'<label><input type="radio" name="{name}" value="{val}" required> {label}</label>')
    return "<div class='q'>" + "".join(html) + "</div>"

def _render_test(title, heading, items, scale, post_to):
    qs = []
    for idx, q in enumerate(items, 1):
        qs.append(f"<div><b>{idx}.</b> {q}{_radio(f'q{idx}', scale)}</div>")
    form = f"<form method='post'>{''.join(qs)}<button class='btn' type='submit'>احسب النتيجة</button></form>"
    return render_template_string(BASE, title=title, heading=heading, body=f"<div class='card'>{form}</div>")

def _score_from_form(n):
    s = 0
    for i in range(1, n+1):
        s += int(request.form.get(f"q{i}", 0))
    return s

# ============ PHQ-9 ============
PHQ9_ITEMS = [
    "قلة الاهتمام أو المتعة بالقيام بالأشياء",
    "الشعور بالاكتئاب أو اليأس",
    "صعوبة النوم أو النوم الزائد",
    "التعب أو قلة الطاقة",
    "ضعف الشهية أو الإفراط بالأكل",
    "الشعور بسوء تجاه النفس",
    "صعوبة التركيز",
    "التحرك أو الكلام ببطء شديد أو العكس (توتر)",
    "أفكار بأنك ستكون أفضل ميّتًا أو إيذاء النفس"
]
PHQ9_SCALE = [("أبدًا",0),("عدة أيام",1),("أكثر من النصف",2),("تقريبًا كل يوم",3)]

@cbt_bp.route("/phq9", methods=["GET","POST"])
def phq9():
    if request.method=="GET":
        return _render_test("PHQ-9", "PHQ-9 — اكتئاب", PHQ9_ITEMS, PHQ9_SCALE, "/cbt/phq9")
    total = _score_from_form(len(PHQ9_ITEMS))
    if   total<=4:   sev="طبيعي"; color="ok"
    elif total<=9:   sev="خفيف";  color="mid"
    elif total<=14:  sev="متوسط"; color="mid"
    elif total<=19:  sev="شديد";  color="warn"
    else:            sev="شديد جدًا"; color="warn"
    body = f"""
    <div class="card">
      <h3>النتيجة الكلية: {total} / 27</h3>
      <span class="badge {color}">شدة: {sev}</span>
      <p>إذا وُجدت أفكار إيذاء النفس (السؤال 9) بدرجة ≥ 1 فاستشر مختصًا فورًا.</p>
      <a class="btn" href="/cbt">عودة للوحة</a>
    </div>"""
    return render_template_string(BASE, title="PHQ-9 نتيجة", heading="PHQ-9 — النتيجة", body=body)

# ============ GAD-7 ============
GAD7_ITEMS = [
    "الشعور بالعصبية أو القلق أو على الحافة",
    "عدم القدرة على التوقف عن القلق أو السيطرة عليه",
    "القلق المفرط على مختلف الأمور",
    "صعوبة الاسترخاء",
    "التوتر بحيث يصعب الجلوس ساكنًا",
    "الانزعاج أو الضيق بسهولة",
    "الشعور بالخوف كأن شيئًا سيئًا قد يحدث"
]
GAD7_SCALE = PHQ9_SCALE

@cbt_bp.route("/gad7", methods=["GET","POST"])
def gad7():
    if request.method=="GET":
        return _render_test("GAD-7", "GAD-7 — قلق عام", GAD7_ITEMS, GAD7_SCALE, "/cbt/gad7")
    total = _score_from_form(len(GAD7_ITEMS))
    if   total<=4:  sev="طبيعي"; color="ok"
    elif total<=9:  sev="خفيف";  color="mid"
    elif total<=14: sev="متوسط"; color="mid"
    else:           sev="شديد";  color="warn"
    body = f"""
    <div class="card"><h3>النتيجة الكلية: {total} / 21</h3>
    <span class="badge {color}">شدة: {sev}</span>
    <a class="btn" href="/cbt">عودة</a></div>"""
    return render_template_string(BASE, title="GAD-7 نتيجة", heading="GAD-7 — النتيجة", body=body)

# ============ DASS-21 (3 مقاييس) ============
DASS21_ITEMS = [
    # اكتئاب
    "وجدت صعوبة في الشعور بالمتعة",
    "شعرت بأنه لا أمل بالمستقبل",
    "شعرت بالحزن والاكتئاب",
    "لم أستطع الشعور بالحماس لأي شيء",
    "شعرت بأن لا قيمة لي",
    "لم أستطع الاستمرار في أي شيء",
    "شعرت أن حياتي لا معنى لها",
    # قلق
    "شعرت بجفاف الفم",
    "عانيت من ضيق في التنفس بدون جهد",
    "شعرت بالارتجاف (اهتزاز)",
    "شعرت بالقلق من التعرض لموقف يسبب الذعر",
    "شعرت بالانزعاج العصبي",
    "عانيت من ضربات قلب سريعة دون جهد",
    "شعرت بالخوف بدون سبب جيد",
    # توتر
    "وجدت صعوبة في الاسترخاء",
    "كنت أتفاعل بشكل مبالغ مع المواقف",
    "صرت سريع الانفعال",
    "وجدت نفسي مضطربًا",
    "صرت غير متسامح مع العرقلة والتأخير",
    "كنت متوترًا ومشدودًا"
]
DASS21_SCALE = [("أبدًا",0),("أحيانًا",1),("غالبًا",2),("دائمًا",3)]

@cbt_bp.route("/dass21", methods=["GET","POST"])
def dass21():
    if request.method=="GET":
        return _render_test("DASS-21", "DASS-21 — اكتئاب/قلق/توتر", DASS21_ITEMS, DASS21_SCALE, "/cbt/dass21")
    total = _score_from_form(len(DASS21_ITEMS))
    dep = sum(int(request.form.get(f"q{i}",0)) for i in range(1, 8)) * 2
    anx = sum(int(request.form.get(f"q{i}",0)) for i in range(8, 15)) * 2
    str_ = sum(int(request.form.get(f"q{i}",0)) for i in range(15, 22)) * 2
    def band(v, cut):
        for name, th in [("طبيعي",cut[0]),("خفيف",cut[1]),("متوسط",cut[2]),("شديد",cut[3])]:
            if v<=th: return name
        return "شديد جدًا"
    dep_s = band(dep, (9,13,20,27))
    anx_s = band(anx, (7,9,14,19))
    str_s = band(str_, (14,18,25,33))
    body = f"""
    <div class="card">
      <h3>المجاميع (×2):</h3>
      <ul>
        <li>اكتئاب: <b>{dep}</b> — {dep_s}</li>
        <li>قلق: <b>{anx}</b> — {anx_s}</li>
        <li>توتر: <b>{str_}</b> — {str_s}</li>
      </ul>
      <a class="btn" href="/cbt">عودة</a>
    </div>"""
    return render_template_string(BASE, title="DASS-21 نتيجة", heading="DASS-21 — النتيجة", body=body)

# ============ PCL-5 ============
PCL5_ITEMS = [
    "ذكريات متطفلة مزعجة عن الحدث",
    "أحلام مزعجة متكررة عن الحدث",
    "ردود فعل مفاجِئة عند التذكير بالحدث",
    "تجنب الأفكار أو المشاعر المتعلقة بالحدث",
    "تجنب المواقف التي تذكر بالحدث",
    "صعوبة تذكر جوانب من الحدث",
    "مشاعر سلبية مستمرة (خوف/غضب/ذنب/خزي)",
    "فقدان الاهتمام بالأنشطة",
    "الشعور بالانفصال عن الآخرين",
    "صعوبة الشعور بالمشاعر الإيجابية",
    "تهيج/انفعال شديد",
    "سلوك متهور أو مدمر",
    "اليقظة المفرطة",
    "صعوبة التركيز",
    "صعوبة النوم"
]
PCL5_SCALE = [("أبدًا",0),("قليلًا",1),("متوسط",2),("شديد",3),("شديد جدًا",4)]

@cbt_bp.route("/pcl5", methods=["GET","POST"])
def pcl5():
    if request.method=="GET":
        return _render_test("PCL-5", "PCL-5 — أعراض ما بعد الصدمة", PCL5_ITEMS, PCL5_SCALE, "/cbt/pcl5")
    total = _score_from_form(len(PCL5_ITEMS))
    flag = "يحتمل وجود اضطراب ما بعد الصدمة" if total>=31 else "أقل من العتبة المؤشرة"
    badge = "warn" if total>=31 else "ok"
    body = f"<div class='card'><h3>المجموع: {total} / 60</h3><span class='badge {badge}'>{flag}</span><a class='btn' href='/cbt'>عودة</a></div>"
    return render_template_string(BASE, title="PCL-5 نتيجة", heading="PCL-5 — النتيجة", body=body)

# ============ ASRS v1.1 (ADHD بالغين — جزء A: 6 أسئلة) ============
ASRS_A = [
    "كم مرة تواجه صعوبة في إنهاء التفاصيل عند إكمال مهمة؟",
    "كم مرة تواجه صعوبة في تنظيم المهام؟",
    "كم مرة تؤجل البدء بمهام تتطلب جهدًا؟",
    "كم مرة تتحرك أو تشعر بالتململ عند الجلوس طويلًا؟",
    "كم مرة تشعر بفرط النشاط وتندفع؟",
    "كم مرة تنسى المواعيد أو الالتزامات؟",
]
ASRS_SCALE = [("أبدًا",0),("نادرًا",1),("أحيانًا",2),("غالبًا",3),("دائمًا",4)]

@cbt_bp.route("/asrs", methods=["GET","POST"])
def asrs():
    if request.method=="GET":
        return _render_test("ASRS v1.1", "ASRS v1.1 — فحص ADHD (بالغين)", ASRS_A, ASRS_SCALE, "/cbt/asrs")
    total = _score_from_form(len(ASRS_A))
    flag = "نتيجة تشير لاحتمال ADHD — يُنصح بتقييم سريري" if total>=12 else "أقل من العتبة المؤشرة"
    badge = "warn" if total>=12 else "ok"
    body = f"<div class='card'><h3>المجموع: {total} / 24</h3><span class='badge {badge}'>{flag}</span><a class='btn' href='/cbt'>عودة</a></div>"
    return render_template_string(BASE, title="ASRS نتيجة", heading="ASRS — النتيجة", body=body)

# ============ OCI-R (وسواس قهري مختصر) ============
OCI_ITEMS = [
    "أتحقق مرارًا من الأشياء (الأبواب/الأجهزة)",
    "أغسل يدي بشكل مفرط أو أتجنب التلوث",
    "أعدّ أو أرتب الأشياء بشكل قهري",
    "أتعرض لأفكار متطفلة مزعجة",
    "أحتفظ بأشياء غير لازمة (اكتناز)",
    "أشعر بضرورة التماثل/الدقة في الأشياء"
]
OCI_SCALE = [("لا أزعج إطلاقًا",0),("قليلًا",1),("متوسط",2),("شديد",3),("شديد جدًا",4)]

@cbt_bp.route("/oci", methods=["GET","POST"])
def oci():
    if request.method=="GET":
        return _render_test("OCI-R", "OCI-R — مؤشرات الوسواس القهري", OCI_ITEMS, OCI_SCALE, "/cbt/oci")
    total = _score_from_form(len(OCI_ITEMS))
    flag = "مؤشرات ملحوظة لوسواس قهري" if total>=14 else "ضمن الحدود"
    badge = "warn" if total>=14 else "ok"
    body = f"<div class='card'><h3>المجموع: {total} / 24</h3><span class='badge {badge}'>{flag}</span><a class='btn' href='/cbt'>عودة</a></div>"
    return render_template_string(BASE, title="OCI-R نتيجة", heading="OCI-R — النتيجة", body=body)

# ============ AUDIT / AUDIT-C ============
AUDITC_ITEMS = [
    "كم مرة تشرب مشروبات كحولية؟",
    "كم عدد المشروبات في يوم الشرب المعتاد؟",
    "كم مرة تشرب 6 مشروبات أو أكثر في مناسبة واحدة؟"
]
AUDITC_SCALE = [
    [("أبدًا",0),("شهريًا أو أقل",1),("2-4 مرات/شهر",2),("2-3 مرات/أسبوع",3),("4+ مرات/أسبوع",4)],
    [("1-2",0),("3-4",1),("5-6",2),("7-9",3),("10+",4)],
    [("أبدًا",0),("أقل من شهري",1),("شهري",2),("أسبوعي",3),("يوميًا تقريبًا",4)],
]
@cbt_bp.route("/audit", methods=["GET","POST"])
def audit():
    if request.method=="GET":
        blocks=[]
        for i,q in enumerate(AUDITC_ITEMS,1):
            opts = "".join([f"<label><input type='radio' name='q{i}' value='{val}' required> {lab}</label>" for lab,val in AUDITC_SCALE[i-1]])
            blocks.append(f"<div class='q'><b>{i}.</b> {q}<div>{opts}</div></div>")
        form = "<form method='post'>"+"".join(blocks)+"<button class='btn'>احسب</button></form>"
        return render_template_string(BASE, title="AUDIT-C", heading="AUDIT-C — كحول", body=f"<div class='card'>{form}</div>")
    total = _score_from_form(3)
    flag = "مؤشر مخاطرة كحولية" if total>=5 else "محدود"
    badge = "warn" if total>=5 else "ok"
    body = f"<div class='card'><h3>المجموع: {total} / 12</h3><span class='badge {badge}'>{flag}</span><a class='btn' href='/cbt'>عودة</a></div>"
    return render_template_string(BASE, title="AUDIT-C نتيجة", heading="AUDIT-C — النتيجة", body=body)

# ============ BRS (الصمود) ============
BRS_ITEMS = [
    "أتعافى بسرعة بعد الأوقات الصعبة",
    "أميل للارتداد من المشكلات",
    "من الصعب عليّ أن أعود لطبيعتي بعد حدث صعب (عكسي)",
    "لا أشعر بالإحباط لفترة طويلة (عكسي)",
    "أتعامل مع الضغوط بفعالية",
    "أميل للعودة سريعًا بعد المرض أو الصعوبات"
]
BRS_SCALE = [("لا أوافق إطلاقًا",1),("لا أوافق",2),("محايد",3),("أوافق",4),("أوافق تمامًا",5)]
BRS_REVERSE = {3,4}

@cbt_bp.route("/brs", methods=["GET","POST"])
def brs():
    if request.method=="GET":
        return _render_test("BRS", "BRS — مقياس الصمود", BRS_ITEMS, BRS_SCALE, "/cbt/brs")
    total = 0
    for i in range(1, len(BRS_ITEMS)+1):
        v = int(request.form.get(f"q{i}",1))
        total += (6-v) if i in BRS_REVERSE else v
    avg = round(total/6,2)
    if   avg<3:  sev="صمود منخفض"; color="warn"
    elif avg<4.3: sev="متوسط"; color="mid"
    else: sev="مرتفع"; color="ok"
    body = f"<div class='card'><h3>المتوسط: {avg} / 5</h3><span class='badge {color}'>{sev}</span><a class='btn' href='/cbt'>عودة</a></div>"
    return render_template_string(BASE, title="BRS نتيجة", heading="BRS — النتيجة", body=body)
