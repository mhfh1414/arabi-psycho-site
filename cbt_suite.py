from flask import Blueprint, render_template_string, request

cbt_bp = Blueprint("cbt_bp", __name__, url_prefix="/cbt")

BASE = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:#0f1420;color:#eaf2ff}
.card-glass{background:#121a2a88;border:1px solid #2a3b5a;border-radius:16px}
a{text-decoration:none}
</style></head><body class="p-3 p-md-5">
<div class="container">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h3 class="m-0">{{ header }}</h3>
    <div>
      <a class="btn btn-outline-info me-2" href="{{ url_for('cbt_bp.dashboard') }}">لوحة CBT</a>
      <a class="btn btn-secondary" href="{{ url_for('index') }}">الرئيسية</a>
    </div>
  </div>
  {{ body|safe }}
</div>
</body></html>
"""

@cbt_bp.route("/")
def dashboard():
    body = """
    <div class="row g-3">
      <div class="col-12 col-lg-6">
        <div class="card-glass p-3 h-100">
          <h5>دفتر تسجيل الأفكار (Thought Record)</h5>
          <p class="text-light">سجّل الموقف، الفكرة الآلية، الدليل مع/ضد، والفكرة المتوازنة.</p>
          <a class="btn btn-primary" href="{{ url_for('cbt_bp.thought_record') }}">ابدأ التسجيل</a>
        </div>
      </div>
      <div class="col-12 col-lg-6">
        <div class="card-glass p-3 h-100">
          <h5>تفعيل سلوكي (BA)</h5>
          <p class="text-light">خطّط أنشطة ممتعة/ذات قيمة مع درجة توقع المتعة والإنجاز.</p>
          <a class="btn btn-success" href="{{ url_for('cbt_bp.ba') }}">إنشاء خطة</a>
        </div>
      </div>
      <div class="col-12 col-lg-6">
        <div class="card-glass p-3 h-100">
          <h5>سُلّم التعرض (ERP)</h5>
          <p class="text-light">ابنِ قائمة التعرض مع درجات القلق (SUDS) وتصاعد المهام.</p>
          <a class="btn btn-warning" href="{{ url_for('cbt_bp.erp') }}">ابنِ السُلّم</a>
        </div>
      </div>
      <div class="col-12 col-lg-6">
        <div class="card-glass p-3 h-100">
          <h5>سلوكيات الأمان</h5>
          <p class="text-light">تعرف وحدّد السلوكيات التي تُبقي القلق وتعلم بدائل وظيفية.</p>
          <a class="btn btn-info" href="{{ url_for('cbt_bp.safety') }}">سجّل السلوكيات</a>
        </div>
      </div>
    </div>
    """
    html = BASE.replace("{{ body|safe }}", body)
    return render_template_string(html, title="لوحة CBT", header="لوحة CBT")

@cbt_bp.route("/thought", methods=["GET","POST"])
def thought_record():
    result = None
    if request.method == "POST":
        data = {k: request.form.get(k,"") for k in ["situation","auto_thought","emotion","evidence_for","evidence_against","balanced"]}
        result = data
    body = f"""
    <div class="card-glass p-3 mb-3">
      <form method="post" class="row g-3">
        <div class="col-12"><label class="form-label">الموقف</label><textarea name="situation" class="form-control" required></textarea></div>
        <div class="col-12 col-md-6"><label class="form-label">الفكرة الآلية</label><textarea name="auto_thought" class="form-control" required></textarea></div>
        <div class="col-12 col-md-6"><label class="form-label">العاطفة/الشدة</label><input name="emotion" class="form-control" placeholder="قلق 70/100"></div>
        <div class="col-12 col-md-6"><label class="form-label">دلائل مع الفكرة</label><textarea name="evidence_for" class="form-control"></textarea></div>
        <div class="col-12 col-md-6"><label class="form-label">دلائل ضد الفكرة</label><textarea name="evidence_against" class="form-control"></textarea></div>
        <div class="col-12"><label class="form-label">الفكرة المتوازنة</label><textarea name="balanced" class="form-control"></textarea></div>
        <div class="col-12"><button class="btn btn-primary">حفظ المذكرة</button></div>
      </form>
    </div>
    {render_result(result)}
    """
    html = BASE.replace("{{ body|safe }}", body)
    return render_template_string(html, title="دفتر الأفكار", header="دفتر تسجيل الأفكار")

@cbt_bp.route("/ba", methods=["GET","POST"])
def ba():
    plan = None
    if request.method == "POST":
        plan = {
            "activity": request.form.get("activity",""),
            "enjoy": request.form.get("enjoy",""),
            "mastery": request.form.get("mastery",""),
            "when": request.form.get("when","")
        }
    body = f"""
    <div class="card-glass p-3">
      <form method="post" class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label">النشاط</label><input name="activity" class="form-control" required></div>
        <div class="col-6 col-md-3"><label class="form-label">توقع المتعة (0-10)</label><input name="enjoy" class="form-control" type="number" min="0" max="10"></div>
        <div class="col-6 col-md-3"><label class="form-label">توقع الإنجاز (0-10)</label><input name="mastery" class="form-control" type="number" min="0" max="10"></div>
        <div class="col-12 col-md-6"><label class="form-label">متى/أين</label><input name="when" class="form-control" placeholder="اليوم 6م في الحديقة"></div>
        <div class="col-12"><button class="btn btn-success">إضافة</button></div>
      </form>
    </div>
    {render_result(plan)}
    """
    html = BASE.replace("{{ body|safe }}", body)
    return render_template_string(html, title="التفعيل السلوكي", header="التفعيل السلوكي (BA)")

@cbt_bp.route("/erp", methods=["GET","POST"])
def erp():
    item = None
    if request.method == "POST":
        item = {"exposure": request.form.get("exposure",""),
                "suds": request.form.get("suds",""),
                "steps": request.form.get("steps","")}
    body = f"""
    <div class="card-glass p-3">
      <form method="post" class="row g-3">
        <div class="col-12"><label class="form-label">مثير/مهمة التعرض</label><input name="exposure" class="form-control" required></div>
        <div class="col-6 col-md-3"><label class="form-label">SUDS (قلق 0-100)</label><input name="suds" class="form-control" type="number" min="0" max="100"></div>
        <div class="col-12"><label class="form-label">خطوات/تصعيد</label><textarea name="steps" class="form-control" rows="3" placeholder="خطوة 1…"></textarea></div>
        <div class="col-12"><button class="btn btn-warning">إضافة للسُلّم</button></div>
      </form>
    </div>
    {render_result(item)}
    """
    html = BASE.replace("{{ body|safe }}", body)
    return render_template_string(html, title="سُلّم التعرض", header="سُلّم التعرض (ERP)")

@cbt_bp.route("/safety", methods=["GET","POST"])
def safety():
    rec = None
    if request.method == "POST":
        rec = {"behavior": request.form.get("behavior",""),
               "function": request.form.get("function",""),
               "alternative": request.form.get("alternative","")}
    body = f"""
    <div class="card-glass p-3">
      <form method="post" class="row g-3">
        <div class="col-12 col-md-6"><label class="form-label">سلوك الأمان</label><input name="behavior" class="form-control" required></div>
        <div class="col-12 col-md-6"><label class="form-label">وظيفته</label><input name="function" class="form-control" placeholder="خفض القلق مؤقتاً…"></div>
        <div class="col-12"><label class="form-label">بديل وظيفي</label><input name="alternative" class="form-control" placeholder="تعرض تدريجي + منع طقوس"></div>
        <div class="col-12"><button class="btn btn-info">حفظ</button></div>
      </form>
    </div>
    {render_result(rec)}
    """
    html = BASE.replace("{{ body|safe }}", body)
    return render_template_string(html, title="سلوكيات الأمان", header="سلوكيات الأمان")

def render_result(obj):
    if not obj: return ""
    rows = "".join(f"<tr><th class='text-nowrap'>{k}</th><td>{(v or '').strip() or '-'}</td></tr>" for k,v in obj.items())
    return f"""
    <div class='card-glass p-3 mt-3'>
      <h6 class="text-info">تم الحفظ (عرض فوري):</h6>
      <div class="table-responsive"><table class="table table-sm table-borderless text-light">{rows}</table></div>
      <div class="small text-secondary">* ملاحظة: هذا عرض فوري غير مخزن في قاعدة بيانات.</div>
    </div>
    """
