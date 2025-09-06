# -*- coding: utf-8 -*-
import re
from flask import render_template_string

# ======================= قاعدة DSM (مبسطة/موسعة) =======================
DSM_DB = {
    # اضطرابات المزاج
    "اضطراب اكتئابي جسيم": [
        "حزن","مزاج منخفض","فقدان المتعة","انعدام المتعة","يأس","شعور بالذنب","بكاء","انسحاب اجتماعي",
        "انتحار","أفكار انتحارية","طاقة منخفضة","إرهاق","تعب","خمول","كسل","بطء نفسي حركي",
        "أرق","قلة نوم","كثرة نوم","اضطراب نوم","فقدان شهية","قلة اكل","ما اقدر آكل","ما اقدر اكل",
        "شهية منخفضة","فقدان وزن","زيادة وزن","تركيز ضعيف","احتقار الذات","تشاؤم","بلا متعة"
    ],
    "اكتئاب مستمر (عسر المزاج)": ["مزاج مكتئب مزمن","تشاؤم مزمن","طاقة قليلة","نوم ضعيف","شهية قليلة","ثقة بالنفس منخفضة","تركيز ضعيف","إنتاجية ضعيفة"],
    "اضطراب ثنائي القطب": ["نوبة هوس","هوس","نشاط زائد","طاقة عالية","قليل نوم","اندفاع","تهور","أفكار سباق","طلاقة الكلام","عظمة","نوبات اكتئاب","تذبذب المزاج"],

    # القلق والطيف
    "اضطراب القلق العام": ["قلق","قلق مفرط","توتر","توجس","أفكار سلبية","شد عضلي","صعوبة تركيز","تعب","قابلية استفزاز","أرق"],
    "اضطراب الهلع": ["نوبة هلع","خفقان","اختناق","ضيق نفس","تعرق","رجفة","دوار","خوف الموت","خوف فقدان السيطرة","خدر","غثيان"],
    "رهاب اجتماعي": ["خوف اجتماعي","خوف التقييم","خجل شديد","تجنب اجتماعي","احمرار","رجفة","قلق أداء","رهبة مواجهة"],
    "رهاب محدد": ["رهاب","خوف شديد","تجنب مواقف","خوف من طيران","خوف من حشرات","خوف من أماكن مرتفعة"],
    "رهاب الساحة (الأماكن)": ["خوف من الأماكن المفتوحة","خوف من الازدحام","تجنب مواصلات","صعوبة الخروج وحيدًا"],

    # الوسواس والصدمة
    "اضطراب الوسواس القهري": ["وسواس","أفكار اقتحامية","طقوس","سلوك قهري","تفقد متكرر","غسل متكرر","تنظيم مفرط","عد قهري","خوف تلوث"],
    "اضطراب ما بعد الصدمة": ["صدمة","حدث صادم","استرجاع الحدث","فلاش باك","كابوس","تجنب","خدر عاطفي","يقظة مفرطة","حساسية صوت"],

    # طيف ذهاني
    "فصام": ["هلوسة","هلاوس سمعية","أوهام","ضلالات","تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني","انعدام إرادة"],
    "اضطراب فصامي عاطفي": ["أعراض ذهانية","اكتئاب شديد","هوس","تذبذب مزاج","هلوسة","أوهام"],
    "اضطراب وهامي": ["ضلالات ثابتة","غيرة وهامية","اضطهاد","عظمة","شك مرضي"],

    # نمائية وعصبية
    "اضطراب فرط الحركة وتشتت الانتباه": ["تشتت","عدم تركيز","فرط حركة","اندفاعية","نسيان","تأجيل","تنظيم ضعيف","كثرة حركة","مقاطعة"],
    "اضطراب طيف التوحد": ["تواصل اجتماعي ضعيف","تواصل غير لفظي ضعيف","صعوبات علاقات","اهتمامات مقيدة","روتين صارم","حساسيات حسية","حركات نمطية","لغة متأخرة"],

    # نوم وأكل وجسد
    "أرق مزمن": ["صعوبة نوم","استيقاظ مبكر","نوم متقطع","عدم راحة","إجهاد نهاري"],
    "اضطراب نهم الطعام": ["نهم","أكل بشراهة","فقدان تحكم","أكل سرًا","ندم بعد الأكل","زيادة وزن"],
    "نهام عصبي": ["نهم متكرر","تطهير","استفراغ","ملينات","صورة جسد مشوهة"],
    "قهم عصبي": ["نقص وزن شديد","خوف من زيادة الوزن","صورة جسد سلبية","تقييد طعام"],
    "أعراض جسدية (سوماتيزيشن)": ["ألم غير مفسر","أعراض جسدية متعددة","انشغال صحي","زيارة أطباء كثيرة"],
    "قلق المرض (هيبوكوندريا)": ["خوف مرض خطير","تفقد جسد","طمأنة متكررة","بحث طبي مستمر"],

    # إدمان مواد
    "اضطراب تعاطي الكحول": ["كحول","سكر متكرر","تحمل","أعراض انسحاب","فقدان سيطرة","مشاكل عمل"],
    "اضطراب تعاطي القنب": ["حشيش","قنب","استخدام يومي","تسامح","انسحاب","قلق بعد الإيقاف"],
    "اضطراب تعاطي المنبهات": ["منشطات","أمفيتامين","كوكايين","سهر","فقدان شهية","بارانويا","استخدام قهري"],
    "اضطراب تعاطي الأفيونات": ["هيروين","مورفين","أوكسيكودون","انسحاب أفيوني","رغبة ملحة","تحمل"],

    # شخصية
    "شخصية حدّية": ["اندفاع","تقلب عاطفي","خوف هجر","إيذاء ذاتي","فراغ مزمن","علاقات غير مستقرة"],
    "شخصية نرجسية": ["عظمة","حاجة إعجاب","تعاطف قليل","استغلالي","حسّاس للنقد"],
    "شخصية معادية للمجتمع": ["خرق قواعد","عدوانية","خداع","اندفاع","لامسؤولية","ندم قليل"],
    "شخصية اجتنابية": ["تجنب نقد","خجل شديد","نقص كفاءة","حساسية رفض"],
    "شخصية اتكالية": ["اتكالية","صعوبة قرار","خوف فراق","احتياج دعم مستمر"],

    # تكيف وولادة وهورمونات ومعرفية
    "اضطراب تكيف": ["توتر موقف","حزن بعد حدث","قلق ظرفي","تراجع أداء بعد ضغط"],
    "اكتئاب ما حول الولادة": ["بعد الولادة","حزن ما بعد الولادة","بكاء","قلق طفل","نوم مضطرب"],
    "اضطراب ما قبل الطمث المزعج": ["تقلب مزاج قبل الدورة","تهيج","حساسية","انتفاخ","شهية"],
    "اضطراب معرفي خفيف/خرف مبكر": ["نسيان جديد","ضياع","بطء معالجة","تراجع تنفيذي"],

    # أخرى
    "وسواس اكتناز": ["اكتناز","صعوبة رمي","تكديس","فوضى منزل"],
    "اضطراب قلق انفصالي (بالغ)": ["قلق انفصال","صعوبة ابتعاد","كابوس فقد","أعراض جسدية عند الفراق"],
    "توريت/عرّات": ["عرات","حركات لا إرادية","أصوات لا إرادية","تفريغ توتر"]
}

# ======================= أدوات مطابقة =======================
def normalize(s: str) -> str:
    s = re.sub(r"[ًٌٍَُِّْـ]", "", (s or "").strip())
    s = s.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ة","ه").replace("ى","ي")
    return s

def score_diagnoses(symptoms_text: str):
    text = normalize(symptoms_text)
    scores = {}
    for disorder, keywords in DSM_DB.items():
        sc = sum(1 for kw in keywords if normalize(kw) in text)
        if sc:
            scores[disorder] = sc
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# ======================= قوالب الصفحة =======================
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
    .bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
    .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px;backdrop-filter:blur(6px)}
    a.btn{display:inline-block;background:#f4b400;color:#2b1b02;border-radius:14px;padding:10px 14px;text-decoration:none;font-weight:800}
    label{display:block;color:#ffe28a;margin:8px 2px 6px}
    input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:12px 14px}
    textarea{min-height:120px;resize:vertical}
    .grid{display:grid;grid-template-columns:1.2fr .8fr;gap:16px}
    @media(max-width:900px){.grid{grid-template-columns:1fr}}
    .result{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px}
    .badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:4px 0}
    .ok{background:#16a34a;color:#fff}
    .warn{background:#ef4444;color:#fff}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="bar">
      <h2 style="margin:0">{{ heading }}</h2>
      <a class="btn" href="/">الواجهة</a>
    </div>
    {{ body|safe }}
  </div>
</body>
</html>
"""

def _render(title, heading, body):
    return render_template_string(_BASE, title=title, heading=heading, body=body)

# ======================= العرض =======================
def render_dsm_get():
    form_html = """
    <div class="grid">
      <section class="card">
        <form method="post">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label>الاسم الكامل</label><input name="name" placeholder="مثال: مشرف العنزي"></div>
            <div><label>العمر</label><input name="age" placeholder="30"></div>
            <div><label>الجنس</label>
              <select name="gender"><option value="">— اختر —</option><option>ذكر</option><option>أنثى</option></select>
            </div>
            <div><label>مدة الأعراض (بالأيام)</label><input name="duration" placeholder="مثال: 30"></div>
          </div>
          <label>الأعراض (أدخل بدقة)</label>
          <textarea name="symptoms" placeholder="مثال: حزن، خمول، قلة نوم، فقدان شهية…"></textarea>
          <label>التاريخ الطبي/النفسي (اختياري)</label>
          <textarea name="history" placeholder="أدوية حالية، جلسات سابقة، أمراض جسدية…"></textarea>
          <div style="margin-top:10px"><button class="btn" type="submit">تشخيص مبدئي</button></div>
        </form>
      </section>
      <aside class="result"><span class="badge warn">لا توجد نتيجة بعد</span><p>املأ النموذج ثم اضغط تشخيص.</p></aside>
    </div>
    """
    return _render("DSM-5 | دراسة حالة وتشخيص", "🗂️ دراسة حالة + تشخيص (DSM-5)", form_html)

def render_dsm_post(form):
    name = form.get("name","")
    age = form.get("age","")
    gender = form.get("gender","")
    duration = form.get("duration","")
    symptoms = form.get("symptoms","")
    history = form.get("history","")

    ranked = score_diagnoses(symptoms)
    if ranked:
        top = [f"{d} <span class='badge ok'>مطابقة تقريبية ({pts})</span>" for d, pts in ranked[:3]]
        diag_html = "<strong>أقرب التشخيصات:</strong><br>" + "<br>".join(top)
    else:
        diag_html = "<span class='badge warn'>لا توجد أعراض كافية للتشخيص.</span>"

    body = f"""
    <div class="grid">
      <section class="card">
        <form method="post">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label>الاسم الكامل</label><input name="name" value="{name}"></div>
            <div><label>العمر</label><input name="age" value="{age}"></div>
            <div><label>الجنس</label>
              <select name="gender">
                <option value="" {"selected" if not gender else ""}>— اختر —</option>
                <option {"selected" if gender=="ذكر" else ""}>ذكر</option>
                <option {"selected" if gender=="أنثى" else ""}>أنثى</option>
              </select>
            </div>
            <div><label>مدة الأعراض (بالأيام)</label><input name="duration" value="{duration}"></div>
          </div>
          <label>الأعراض (أدخل بدقة)</label>
          <textarea name="symptoms">{symptoms}</textarea>
          <label>التاريخ الطبي/النفسي (اختياري)</label>
          <textarea name="history">{history}</textarea>
          <div style="margin-top:10px"><button class="btn" type="submit">إعادة التشخيص</button></div>
        </form>
      </section>
      <aside class="result">
        <h3>📋 النتيجة</h3>
        <div><strong>الاسم:</strong> {name or "—"} | <strong>العمر:</strong> {age or "—"} | <strong>الجنس:</strong> {gender or "—"} | <strong>المدة:</strong> {duration or "—"}</div>
        <div style="margin-top:8px">{diag_html}</div>
        <p style="opacity:.85;margin-top:8px">⚠️ نتيجة تقديرية للمساعدة، وتحتاج تأكيدًا سريريًا.</p>
      </aside>
    </div>
    """
    return _render("DSM-5 | دراسة حالة وتشخيص", "🗂️ دراسة حالة + تشخيص (DSM-5)", body)
