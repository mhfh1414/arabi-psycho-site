# -*- coding: utf-8 -*-
from flask import render_template_string

# بنك أسئلة مبسّط (يمكن توسيعه لاحقًا)
TEST_BANK = {
    "phq-9": {
        "title": "PHQ-9 — مقياس الاكتئاب",
        "scale": ["0=أبدًا", "1=عدة أيام", "2=أكثر من النصف", "3=تقريبًا يوميًا"],
        "cutoffs": [(0,4,"حد أدنى/طبيعي"), (5,9,"اكتئاب خفيف"), (10,14,"متوسط"), (15,19,"شديد"), (20,27,"شديد جدًا")],
        "items": [
            "قلة الاهتمام أو المتعة بالأشياء",
            "الشعور بالاكتئاب أو الإحباط أو اليأس",
            "مشكلات النوم (قلة/كثرة)",
            "التعب أو نقص الطاقة",
            "قلة الشهية أو الإفراط في الأكل",
            "شعور سيء تجاه نفسك أو أنك فاشل",
            "صعوبة في التركيز",
            "الحركة/الكلام ببطء شديد أو على العكس توتر زائد",
            "أفكار بأنك ستكون أفضل حالًا لو انتهت حياتك"
        ],
        "max": 27
    },
    "gad-7": {
        "title": "GAD-7 — مقياس القلق",
        "scale": ["0=أبدًا", "1=عدة أيام", "2=أكثر من النصف", "3=تقريبًا يوميًا"],
        "cutoffs": [(0,4,"قلق ضئيل"),(5,9,"خفيف"),(10,14,"متوسط"),(15,21,"شديد")],
        "items": [
            "الشعور بالعصبية أو القلق أو على الحافة",
            "عدم القدرة على إيقاف القلق أو التحكم فيه",
            "القلق المفرط حول مختلف الأشياء",
            "صعوبة الاسترخاء",
            "التململ بحيث يصعب الجلوس",
            "سهولة الانزعاج أو الغضب",
            "الشعور بالخوف كأن شيئًا سيئًا سيحدث"
        ],
        "max": 21
    },
    "pcl-5": {
        "title": "PCL-5 — أعراض ما بعد الصدمة (مختصر)",
        "scale": ["0=أبدًا", "1=قليلًا", "2=متوسط", "3=كثيرًا", "4=بشدة"],
        "cutoffs": [(0,9,"منخفض"),(10,19,"متوسط"),(20,40,"مرتفع — يُنصح بتقييم سريري")],
        "items": [
            "ذكريات متكررة ومؤلمة عن الحدث",
            "أحلام/كوابيس متعلقة بالحدث",
            "مشاعر قوية عند تذكّر الحدث",
            "تجنّب الأفكار أو المشاعر المرتبطة",
            "تجنّب الأماكن/الأشخاص المرتبطين",
            "مشاعر سلبية مستمرة (خوف/غضب/ذنب)",
            "فقدان الاهتمام بالأنشطة",
            "يقظة مفرطة/صعوبة نوم/انفعال"
        ],
        "max": 32
    },
    "big5": {
        "title": "Big Five — السمات الخمس الكبرى (مبسّط)",
        "scale": ["1=لا أوافق بشدة", "2", "3", "4", "5=أوافق بشدة"],
        "cutoffs": [],
        "items": {
            "الانفتاح": [
                "أستمتع بالأفكار الجديدة والتجارب المختلفة",
                "أتخيل حلولًا متعددة للمشكلة"
            ],
            "الضمير الحي": [
                "أنظم وقتي جيدًا",
                "ألتزم بوعودي"
            ],
            "الانبساط": [
                "أستمد طاقتي من التفاعل مع الآخرين",
                "أتحدث بسهولة أمام الناس"
            ],
            "القبول": [
                "أتعاطف مع الآخرين",
                "أتعاون بسهولة ضمن الفريق"
            ],
            "العصابية": [
                "أتوتر بسرعة",
                "أقلق من أمور بسيطة"
            ]
        },
        "max": 50
    }
}

_BASE = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
    body{font-family:"Tajawal",system-ui;background:linear-gradient(135deg,#0b3a75,#0a65b0) fixed;color:#fff;margin:0}
    .wrap{max-width:1000px;margin:24px auto;padding:16px}
    .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px;backdrop-filter:blur(6px)}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
    a.btn{display:inline-block;background:#f4b400;color:#2b1b02;border-radius:14px;padding:10px 14px;text-decoration:none;font-weight:800}
    label{display:block;margin:8px 2px;color:#ffe28a}
    select{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:10px}
  </style>
</head>
<body>
  <div class="wrap">
    {{ body|safe }}
  </div>
</body>
</html>
"""

def _render(title, body):
    return render_template_string(_BASE, title=title, body=body)

def render_cbt_home():
    body = """
    <h2 style="margin:0 0 12px">💡 العلاج السلوكي المعرفي (CBT) + الاختبارات</h2>
    <p>اختر اختبارًا لبدء التقييم:</p>
    <div class="grid">
      <div class="card"><h3>PHQ-9 — اكتئاب</h3><a class="btn" href="/cbt/tests/phq-9">ابدأ</a></div>
      <div class="card"><h3>GAD-7 — قلق</h3><a class="btn" href="/cbt/tests/gad-7">ابدأ</a></div>
      <div class="card"><h3>PCL-5 — ما بعد الصدمة (مختصر)</h3><a class="btn" href="/cbt/tests/pcl-5">ابدأ</a></div>
      <div class="card"><h3>Big Five — السمات الخمس</h3><a class="btn" href="/cbt/tests/big5">ابدأ</a></div>
    </div>
    <p style="margin-top:14px"><a class="btn" href="/">الواجهة</a></p>
    """
    return _render("CBT + اختبارات", body)

def render_test(slug, request):
    if slug not in TEST_BANK:
        return _render("اختبار غير موجود", "<div class='card'>الاختبار غير متاح. <a class='btn' href='/cbt'>رجوع</a></div>")

    test = TEST_BANK[slug]
    title = test["title"]
    scale = test["scale"]

    # Big Five (تصميم خاص)
    if slug == "big5":
        if request.method == "POST":
            total = 0
            dims = {k:0 for k in test["items"].keys()}
            count = {k:0 for k in test["items"].keys()}
            for dim, qs in test["items"].items():
                for i, _ in enumerate(qs, 1):
                    v = int(request.form.get(f"{dim}-{i}", "3"))
                    dims[dim] += v
                    count[dim] += 1
                    total += v
            body = "<div class='card'><h3>النتيجة</h3><ul>"
            for dim in dims:
                avg = round(dims[dim]/max(1,count[dim]), 2)
                body += f"<li><strong>{dim}:</strong> مجموع {dims[dim]} / متوسط {avg}</li>"
            body += f"</ul><p><strong>المجموع الكلي:</strong> {total}</p><a class='btn' href='/cbt'>رجوع</a></div>"
            return _render(title, body)

        # GET form
        form = "<div class='card'><form method='post'>"
        for dim, qs in test["items"].items():
            form += f"<h3>{dim}</h3>"
            for i, q in enumerate(qs, 1):
                form += f"<label>{q}</label><select name='{dim}-{i}'>" + "".join([f"<option value='{idx+1}'>{opt}</option>" for idx,opt in enumerate(scale)]) + "</select>"
        form += "<div style='margin-top:10px'><button class='btn' type='submit'>احسب النتائج</button></div></form>"
        form += "<p style='margin-top:12px'><a class='btn' href='/cbt'>رجوع</a></p></div>"
        return _render(title, form)

    # بقية الاختبارات بنمط رقمي بسيط 0..3 أو 0..4
    items = test["items"]
    max_score = test["max"]
    cutoffs = test["cutoffs"]

    if request.method == "POST":
        total = 0
        for i, _ in enumerate(items, 1):
            v = int(request.form.get(f"q{i}", "0"))
            total += v
        # تحديد الفئة
        label = "—"
        for lo, hi, lab in cutoffs:
            if lo <= total <= hi:
                label = lab
                break
        body = f"<div class='card'><h3>النتيجة</h3><p><strong>المجموع:</strong> {total} / {max_score}</p><p><strong>التقدير:</strong> {label}</p><a class='btn' href='/cbt'>رجوع</a></div>"
        return _render(title, body)

    # GET form
    form = f"<div class='card'><form method='post'><p>مقياس الإجابة: {' | '.join(scale)}</p>"
    for i, q in enumerate(items, 1):
        options = "".join([f"<option value='{idx}'>{opt}</option>" for idx, opt in enumerate(scale)])
        form += f"<label>{i}. {q}</label><select name='q{i}'>{options}</select>"
    form += "<div style='margin-top:10px'><button class='btn' type='submit'>احسب النتائج</button></div></form>"
    form += "<p style='margin-top:12px'><a class='btn' href='/cbt'>رجوع</a></p></div>"
    return _render(title, form)
