# -*- coding: utf-8 -*-
# cbt_suite.py — حزمة CBT + اختبارات نفسية في ملف واحد (بدون مجلدات/قوالب)

from flask import Blueprint, request, render_template_string

cbt_bp = Blueprint("cbt", __name__)

# ========================= إعداد عام للاختبارات =========================
TESTS = {
    # ---------------- PHQ-9 (الاكتئاب) ----------------
    "phq9": {
        "title": "PHQ-9 — فحص أعراض الاكتئاب",
        "about": "يقدّر شدة أعراض الاكتئاب خلال آخر أسبوعين.",
        "scale": {0: "أبدًا", 1: "عدة أيام", 2: "أكثر من نصف الأيام", 3: "تقريبًا كل يوم"},
        "questions": [
            "قلة الاهتمام أو المتعة في فعل الأشياء",
            "الشعور بالحزن أو الاكتئاب أو اليأس",
            "صعوبة النوم أو النوم المفرط",
            "الشعور بالتعب أو قلة الطاقة",
            "ضعف الشهية أو فرط الأكل",
            "الشعور بسوء تجاه نفسك أو أنك فاشل",
            "صعوبة التركيز (كالقراءة أو التلفاز)",
            "التحرك/الكلام ببطء شديد أو العكس بتوتر زائد",
            "أفكار أنك ستموت أو إيذاء النفس"
        ],
        "max": 27,
        "severity": [
            (4,  "خفيف جدًا",  "#2e7d32"),
            (9,  "خفيف",      "#558b2f"),
            (14, "متوسط",     "#f9a825"),
            (19, "متوسط-شديد","#f57c00"),
            (27, "شديد",      "#c62828"),
        ],
        "suicide_index": 8,  # بند الانتحار للتنبيه
    },

    # ---------------- GAD-7 (القلق) ----------------
    "gad7": {
        "title": "GAD-7 — فحص القلق العام",
        "about": "يقدّر شدة القلق خلال آخر أسبوعين.",
        "scale": {0: "أبدًا", 1: "عدة أيام", 2: "أكثر من نصف الأيام", 3: "تقريبًا كل يوم"},
        "questions": [
            "الشعور بالعصبية أو التوتر أو على الحافة",
            "عدم القدرة على إيقاف القلق أو التحكم فيه",
            "القلق المفرط بشأن أشياء مختلفة",
            "صعوبة الاسترخاء",
            "التململ لدرجة صعوبة الجلوس هادئًا",
            "الانزعاج بسهولة أو التهيّج",
            "الخوف من أن يحدث شيء فظيع"
        ],
        "max": 21,
        "severity": [
            (4,  "خفيف جدًا", "#2e7d32"),
            (9,  "خفيف",     "#558b2f"),
            (14, "متوسط",    "#f9a825"),
            (21, "شديد",     "#c62828"),
        ],
    },

    # ---------------- PCL-5 (الصدمة) — مختصر 12 بند (0-4) ----------------
    "pcl5": {
        "title": "PCL-5 — مؤشر أعراض ما بعد الصدمة (مختصر 12 بندًا)",
        "about": "نسخة مختصرة لتقدير أعراض ما بعد الصدمة المرتبطة بحدث صادم.",
        "scale": {0: "لا شيء", 1: "قليل", 2: "متوسط", 3: "شديد", 4: "شديد جدًا"},
        "questions": [
            "ذكريات متطفّلة للحدث الصادم",
            "أحلام مزعجة مرتبطة بالحدث",
            "ردود فعل تشبه إعادة المعايشة",
            "انزعاج شديد عند المثيرات المرتبطة",
            "تجنّب الأفكار والذكريات المرتبطة",
            "تجنّب الأماكن/الأشخاص المرتبطين",
            "صعوبات تذكّر جوانب مهمة من الحدث",
            "معتقدات سلبية مستمرة عن الذات/العالم",
            "مشاعر سلبية قوية (خوف/غضب/ذنب/خجل)",
            "فقدان الاهتمام بالأنشطة",
            "اليقظة المفرطة وسهولة الفزع",
            "مشكلات في النوم والتركيز"
        ],
        "max": 48,
        "severity": [
            (12, "خفيف",    "#2e7d32"),
            (24, "متوسط",   "#f9a825"),
            (48, "شديد",    "#c62828"),
        ],
    },

    # ---------------- Y-BOCS (وسواس قهري) — مختصر 10 بنود (0-4) ----------------
    "y_bocs": {
        "title": "Y-BOCS — مؤشر شدة الوسواس القهري (مختصر)",
        "about": "يقدّر شدة الانشغالات والطقوس القهرية خلال الأسبوع الماضي.",
        "scale": {0: "لا شيء", 1: "خفيف", 2: "متوسط", 3: "شديد", 4: "شديد جدًا"},
        "questions": [
            "الوقت المستغرق في الأفكار الوسواسية",
            "الضيق الناتج عن الوساوس",
            "قدرة مقاومة الوساوس",
            "التحكم في الوساوس",
            "تأثير الوساوس على الأداء",
            "الوقت المستغرق في الطقوس القهرية",
            "الضيق الناتج عن الطقوس",
            "قدرة مقاومة الطقوس",
            "التحكم في الطقوس",
            "تأثير الطقوس على الأداء"
        ],
        "max": 40,
        "severity": [
            (7,  "خفيف جدًا", "#2e7d32"),
            (15, "خفيف",      "#558b2f"),
            (23, "متوسط",     "#f9a825"),
            (31, "شديد",      "#f57c00"),
            (40, "شديد جدًا", "#c62828"),
        ],
    },

    # ---------------- ASRS (بالغين ADHD) — القسم A (6 بنود) ----------------
    "asrs": {
        "title": "ASRS — مؤشر نقص الانتباه/فرط الحركة (بالغين) — القسم A",
        "about": "مؤشر سريع لاشتباه ADHD لدى البالغين.",
        "scale": {0: "أبدًا", 1: "نادرًا", 2: "أحيانًا", 3: "غالبًا", 4: "دائمًا"},
        "questions": [
            "صعوبة إنهاء التفاصيل بعد مهمة طويلة",
            "صعوبة ترتيب الأمور عند أداء مهمة",
            "مشكلات تذكّر المواعيد/الالتزامات",
            "تجنّب/تأجيل المهام التي تتطلب جهدًا ذهنيًا",
            "التململ والحركة أثناء الجلوس الطويل",
            "الاندفاعية/مقاطعة الآخرين"
        ],
        "max": 24,
        "severity": [
            (9,  "مؤشرات قليلة", "#2e7d32"),
            (14, "اشتباه متوسط", "#f9a825"),
            (24, "اشتباه مرتفع", "#c62828"),
        ],
    },

    # ---------------- اختبار شخصية (خماسي مختصر 10 بنود) ----------------
    "bfi10": {
        "title": "BFI-10 — لمحة خماسية عن السمات الشخصية (مختصر)",
        "about": "مؤشر مختصر (10 بنود) لخمسة أبعاد: الانبساط، التوافقية، الضمير، الاستقرار العاطفي، الانفتاح.",
        "scale": {1: "أعارض بشدّة", 2: "أعارض", 3: "محايد", 4: "أوافق", 5: "أوافق بشدّة"},
        "questions": [
            "أرى نفسي منفتحًا واجتماعيًا (انبساط)",
            "أرى نفسي متعاطفًا ومراعياً للآخرين (توافقية)",
            "أرى نفسي منظّمًا وذا انضباط (ضمير)",
            "أرى نفسي هادئًا ومستقرًا عاطفيًا (استقرار)",
            "أرى نفسي واسع الخيال ومبتكرًا (انفتاح)",
            "أرى نفسي قليل الانفتاح على الآخرين (انعزال) [عكسي]",
            "أرى نفسي يميل إلى الجدال/الخشونة [عكسي]",
            "أرى نفسي يميل إلى الإهمال [عكسي]",
            "أرى نفسي متقلب المزاج/قلق [عكسي]",
            "أرى نفسي تقليديًا قليل الفضول [عكسي]"
        ],
        "max": 50,
        "personality": True  # معالجة خاصة لإخراج 5 درجات فرعية
    },
}

# ========================= صفحات HTML العامة (inline) =========================
BASE_CSS = """
:root{--bg:#0a3a75;--bg2:#0a65b0;--gold:#f4b400;--pane:rgba(255,255,255,.08);--border:rgba(255,255,255,.14)}
*{box-sizing:border-box}body{margin:0;font-family:'Tajawal',system-ui;background:linear-gradient(135deg,var(--bg),var(--bg2));color:#fff}
.wrap{max-width:1000px;margin:36px auto;padding:0 16px}
.card{background:var(--pane);border:1px solid var(--border);border-radius:16px;padding:18px}
.btn{display:inline-block;background:linear-gradient(145deg,#ffd86a,var(--gold));color:#2b1b02;padding:10px 16px;border-radius:12px;text-decoration:none;font-weight:800;border:none;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.badge{display:inline-block;padding:4px 10px;border-radius:10px;margin-inline:6px}
"""

HUB_HTML = f"""
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>CBT — مركز الاختبارات</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{BASE_CSS}</style></head><body>
<div class="wrap">
  <h1>🧠 العلاج السلوكي المعرفي — مركز الاختبارات</h1>
  <div class="grid" style="margin-top:18px">
    {{% for tid, t in tests.items() %}}
      <div class="card">
        <h3>{{{{ t['title'] }}}}</h3>
        <p style="opacity:.9">{{{{ t['about'] }}}}</p>
        <a class="btn" href="/cbt/{{{{ tid }}}}">ابدأ</a>
      </div>
    {{% endfor %}}
  </div>
  <p style="margin-top:16px"><a class="btn" href="/">الرجوع للرئيسية</a></p>
</div>
</body></html>
"""

FORM_HTML = f"""
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{{{{ T['title'] }}}}</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{BASE_CSS}
label{{display:block;margin:.6rem 0 .3rem;font-weight:700}}
.opt{{display:flex;gap:10px;flex-wrap:wrap}}
.opt label{{background:var(--pane);border:1px solid var(--border);padding:8px 10px;border-radius:10px;cursor:pointer}}
.opt input{{display:none}}
.opt input:checked+span{{background:linear-gradient(145deg,#ffd86a,var(--gold));color:#2b1b02;font-weight:800}}
</style></head><body>
<div class="wrap">
  <h2>{{{{ T['title'] }}}}</h2>
  <p style="opacity:.9">{{{{ T['about'] }}}}</p>
  <form class="card" method="post">
    {{% for q in T['questions'] %}}
      <div class="q">
        <label>({{{{ loop.index }}}}) {{{{ q }}}}</label>
        <div class="opt">
          {{% for val,txt in T['scale'].items() %}}
            <label><input type="radio" name="q{{{{loop.index}}}}" value="{{{{val}}}}" required><span>{{{{txt}}}}</span></label>
          {{% endfor %}}
        </div>
      </div>
    {{% endfor %}}
    <button class="btn" type="submit">احسب النتيجة</button>
    <a class="btn" href="/cbt" style="margin-inline-start:8px">رجوع</a>
  </form>
</div>
</body></html>
"""

RESULT_HTML = f"""
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>نتيجة — {{{{ T['title'] }}}}</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{BASE_CSS}.bar{{height:12px;background:#263238;border-radius:8px;overflow:hidden}}
.fill{{height:100%;background:#f4b400}}
</style></head><body>
<div class="wrap">
  <h2>نتيجة — {{{{ T['title'] }}}}</h2>
  <div class="card">
    <p>الدرجة: <b>{{{{ score }}}}</b> / {{{{ T['max'] }}}}
      <span class="badge" style="background: {{{{ color }}}}; color:#000">{{{{ label }}}}</span>
    </p>
    <div class="bar"><div class="fill" style="width: {{{{ percent }}}}%"></div></div>
    {{{{ extra_html|safe }}}}
    <p style="margin-top:12px"><a class="btn" href="/cbt">عودة لمركز الاختبارات</a></p>
  </div>
</div>
</body></html>
"""

# ========================= دوال مساعدة =========================
def _pct(score, mx):
    try:
        return round((score / float(mx)) * 100, 1)
    except ZeroDivisionError:
        return 0.0

def _severity(sev_table, score):
    for mx, label, color in sev_table:
        if score <= mx:
            return label, color
    return sev_table[-1][1], sev_table[-1][2]

def _render_form(test_id):
    T = TESTS[test_id]
    return render_template_string(FORM_HTML, T=T)

def _render_result(test_id, answers):
    T = TESTS[test_id]
    score = sum(answers)
    label, color = _severity(T["severity"], score)
    percent = _pct(score, T["max"])

    extra_html = ""
    # تنبيه بند الانتحار في PHQ-9
    if test_id == "phq9" and T.get("suicide_index") is not None:
        try:
            si = T["suicide_index"]
            if answers[si] >= 1:
                extra_html += "<p style='color:#ffccbc;margin-top:10px'>⚠️ أشرت إلى أفكار إيذاء النفس. إن كان لديك خطر فوري، تواصل مع الطوارئ أو مختص فورًا.</p>"
        except Exception:
            pass

    # استخراج الخمسة أبعاد في BFI-10 (بشكل مبسّط)
    if test_id == "bfi10" and T.get("personality"):
        # البنود (1,6) للانبساط مع عكسي، (2,7) توافقية، (3,8) ضمير، (4,9) استقرار، (5,10) انفتاح
        # البنود العكسية تُقلب: 6,7,8,9,10
        def flip(x): return 6 - x  # 1↔5, 2↔4, 3↔3
        E = answers[0] + flip(answers[5])
        A = answers[1] + flip(answers[6])
        C = answers[2] + flip(answers[7])
        N = answers[3] + flip(answers[8])  # هنا N = الاستقرار (العكس للاندفاع/العصابية)
        O = answers[4] + flip(answers[9])
        extra_html += f"""
        <div class="card" style="margin-top:12px">
          <h3>الأبعاد الخمسة (مجموع/10):</h3>
          <ul>
            <li>الانبساط: <b>{E}</b> / 10</li>
            <li>التوافقية: <b>{A}</b> / 10</li>
            <li>الضمير: <b>{C}</b> / 10</li>
            <li>الاستقرار العاطفي: <b>{N}</b> / 10</li>
            <li>الانفتاح: <b>{O}</b> / 10</li>
          </ul>
        </div>
        """

    return render_template_string(
        RESULT_HTML,
        T=T, score=score, percent=percent, label=label, color=color,
        extra_html=extra_html
    )

# ========================= المسارات =========================
@cbt_bp.route("/")
def cbt_home():
    # صفحة مركزية تسرد كل الاختبارات
    return render_template_string(HUB_HTML, tests=TESTS)

@cbt_bp.route("/<test_id>", methods=["GET", "POST"])
def cbt_router(test_id):
    if test_id not in TESTS:
        # رجوع للصفحة المركزية إن كان الاسم غير صحيح
        return render_template_string(HUB_HTML, tests=TESTS)

    if request.method == "POST":
        T = TESTS[test_id]
        answers = []
        for i in range(1, len(T["questions"]) + 1):
            try:
                val = int(request.form.get(f"q{i}", "0"))
            except ValueError:
                val = 0
            # تأكيد أن القيمة ضمن السلم
            if test_id == "bfi10":
                val = min(max(val, 1), 5)
            else:
                val = min(max(val, min(T["scale"].keys())), max(T["scale"].keys()))
            answers.append(val)
        return _render_result(test_id, answers)

    # GET → عرض النموذج
    return _render_form(test_id)
