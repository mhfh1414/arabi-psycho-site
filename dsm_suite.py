from flask import Blueprint, render_template_string, request, url_for

dsm_bp = Blueprint("dsm_bp", __name__, url_prefix="/dsm")

# بيانات مختصرة توضيحية (قابلة للتوسيع)
DISORDERS = {
    "mdd": {
        "name": "اضطراب الاكتئاب الجسيم (MDD)",
        "symptoms": [
            "مزاج مكتئب معظم اليوم",
            "فقدان الاهتمام أو المتعة",
            "تغير في الشهية أو الوزن",
            "أرق أو فرط نوم",
            "إجهاد أو بطء حركي نفسي",
            "تعب أو فقدان طاقة",
            "مشاعر ذنب مفرطة/عديمة القيمة",
            "انخفاض التركيز أو التردد",
            "أفكار موت/انتحار"
        ],
        "notes": "نوبتان على الأقل لمدة ≥ أسبوعين مع تدهور ملحوظ وظيفيًا."
    },
    "gad": {
        "name": "اضطراب القلق المعمّم (GAD)",
        "symptoms": [
            "قلق مفرط معظم الأيام ≥ 6 أشهر",
            "صعوبة في التحكم بالقلق",
            "أرق/توتر/سهولة الاستثارة",
            "إجهاد سريع/تعب",
            "صعوبة التركيز/فراغ ذهني",
            "توتر عضلي",
            "اضطراب النوم"
        ],
        "notes": "يسبب ضائقة أو خلل وظيفي وليس بسبب مادة/حالة طبية."
    },
    "pd": {
        "name": "اضطراب الهلع (Panic Disorder)",
        "symptoms": [
            "نوبات هلع متكررة غير متوقعة",
            "قلق دائم من نوبات إضافية",
            "تغييرات سلوكية تجنّبية مرتبطة بالنوبات"
        ],
        "notes": "انتبه للترابط مع الأجروفوبيا."
    },
    "ocd": {
        "name": "الوسواس القهري (OCD)",
        "symptoms": [
            "أفكار/اندفاعات/صور وسواسية متكررة",
            "سلوكيات/طقوس قهرية لتخفيف القلق",
            "تستهلك وقتًا أو تسبب خللاً وظيفيًا"
        ],
        "notes": "لا تُفسَّر بأفضل باضطراب آخر."
    },
    "ptsd": {
        "name": "اضطراب ما بعد الصدمة (PTSD)",
        "symptoms": [
            "تعرّض لحدث صادم",
            "أعراض غازية (ذكريات/كوابيس/فلاشباك)",
            "تجنّب للمثيرات",
            "تغيّرات سلبية بالمعرفة/المزاج",
            "استثارة/يقظة مفرطة",
            "المدة > شهر وخلل وظيفي"
        ],
        "notes": "ميّز عن اضطراب التكيّف والقلق الحاد."
    },
}

INDEX_HTML = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>DSM – نظرة عامة</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:#0f1420;color:#eaf2ff}
.card-glass{background:#121a2a88;border:1px solid #2a3b5a;border-radius:16px}
.search{background:#0f1b2f;border:1px solid #2a3b5a;color:#9ec5ff}
a{text-decoration:none}
</style></head><body class="p-3 p-md-5">
<div class="container">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="m-0">DSM – قائمة مختصرة</h2>
    <a class="btn btn-secondary" href="{{ url_for('index') }}">الرجوع للرئيسية</a>
  </div>

  <form class="mb-4" method="get">
    <input class="form-control search" name="q" placeholder="ابحث باسم الاضطراب أو العَرَض…" value="{{ q or '' }}">
  </form>

  <div class="row g-3">
    {% for key, d in results %}
    <div class="col-12 col-md-6">
      <div class="p-3 card-glass h-100">
        <h5 class="mb-2">{{ d.name }}</h5>
        <div class="small text-info mb-2">أعراض شائعة:</div>
        <ul class="mb-3">
          {% for s in d.symptoms[:4] %}<li>{{ s }}</li>{% endfor %}
        </ul>
        <a class="btn btn-success btn-sm" href="{{ url_for('dsm_bp.disorder', code=key) }}">التفاصيل</a>
      </div>
    </div>
    {% endfor %}
    {% if not results %}
      <div class="col-12"><div class="alert alert-warning">لا نتائج مطابقة.</div></div>
    {% endif %}
  </div>
</div>
</body></html>
"""

DETAIL_HTML = """
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ d.name }}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:#0f1420;color:#eaf2ff}
.card-glass{background:#121a2a88;border:1px solid #2a3b5a;border-radius:16px}
</style></head><body class="p-3 p-md-5">
<div class="container">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h3 class="m-0">{{ d.name }}</h3>
    <div>
      <a class="btn btn-outline-info me-2" href="{{ url_for('dsm_bp.index') }}">قائمة DSM</a>
      <a class="btn btn-secondary" href="{{ url_for('index') }}">الرئيسية</a>
    </div>
  </div>
  <div class="card-glass p-3 mb-3">
    <h5 class="text-info">الأعراض/المعايير</h5>
    <ul class="mb-0">{% for s in d.symptoms %}<li>{{ s }}</li>{% endfor %}</ul>
  </div>
  {% if d.notes %}
  <div class="card-glass p-3">
    <h6 class="text-warning">ملاحظات إكلينيكية</h6>
    <p class="mb-0">{{ d.notes }}</p>
  </div>
  {% endif %}
</div>
</body></html>
"""

@dsm_bp.route("/")
def index():
    q = (request.args.get("q") or "").strip().lower()
    items = DISORDERS.items()
    if q:
        def match(d):
            text = (d["name"] + " " + " ".join(d["symptoms"])).lower()
            return q in text
        items = [(k, v) for k, v in items if match(v)]
    return render_template_string(INDEX_HTML, results=items, q=q)

@dsm_bp.route("/<code>")
def disorder(code):
    d = DISORDERS.get(code)
    if not d:
        return "غير موجود", 404
    return render_template_string(DETAIL_HTML, d=d)
