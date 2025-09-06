# -*- coding: utf-8 -*-
# site_app.py — ملف واحد يشغّل كل شيء
from flask import Flask, request, redirect, url_for, render_template_string
import re

app = Flask(__name__)

# ======================= قاعدة DSM (مبسّطة وقابلة للتوسيع) =======================
DSM_DB = {
    # اضطرابات المزاج
    "اضطراب اكتئابي جسيم": [
        "حزن","مزاج منخفض","فقدان المتعة","انعدام المتعة","يأس","شعور بالذنب","بكاء","انسحاب اجتماعي",
        "انتحار","أفكار انتحارية","طاقة منخفضة","إرهاق","تعب","خمول","كسل","بطء نفسي حركي",
        "أرق","قلة نوم","كثرة نوم","اضطراب نوم","فقدان شهية","قلة اكل","شهية منخفضة",
        "فقدان وزن","زيادة وزن","تركيز ضعيف","احتقار الذات"
    ],
    "اكتئاب مستمر (عسر المزاج)": [
        "مزاج مكتئب مزمن","تشاؤم مزمن","طاقة قليلة","نوم ضعيف","شهية قليلة","ثقة بالنفس منخفضة","تركيز ضعيف","إنتاجية ضعيفة"
    ],
    "اضطراب ثنائي القطب": [
        "نوبة هوس","هوس","نشاط زائد","طاقة عالية","قليل نوم","اندفاع","تهور","أفكار سباق","طلاقة الكلام",
        "عظمة","نوبات اكتئاب","تذبذب المزاج"
    ],
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

# ======================= أدوات مطابقة مبسطة =======================
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

# ======================= قوالب HTML مدمجة =======================
INDEX_TMPL = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | الرئيسية</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body{margin:0;font-family:"Tajawal",system-ui;background:linear-gradient(135deg,#0b3a75,#0a65b0);color:#fff}
    .hero{min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:20px}
    .box{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:18px;padding:28px 26px;backdrop-filter:blur(6px)}
    h1{font-size:36px;margin:0 0 6px}
    p{color:#cbd5e1;margin:0 0 18px}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:16px}
    a.btn{display:inline-block;background:#f4b400;color:#062241;border-radius:14px;padding:12px 18px;font-weight:700;text-decoration:none}
    a.tile{display:block;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);padding:12px;border-radius:12px;color:#fff;text-decoration:none}
    a.tile:hover{background:rgba(255,255,255,.18)}
  </style>
</head>
<body>
  <div class="hero">
    <div class="box">
      <h1>مركز عربي سايكو يرحب بكم</h1>
      <p>نخدمك أينما كنت | صديق الجميع</p>
      <a class="btn" href="{{ url_for('dsm') }}">ابدأ دراسة الحالة + التشخيص (DSM)</a>
      <div class="grid">
        <a class="tile" href="{{ url_for('tests') }}">🧪 الاختبارات النفسية والشخصية</a>
        <a class="tile" href="{{ url_for('cbt') }}">💡 العلاج السلوكي المعرفي (CBT)</a>
        <a class="tile" href="{{ url_for('addiction') }}">🚭 علاج الإدمان</a>
        <a class="tile" href="{{ url_for('request_doctor') }}">👨‍⚕️ طلب الطبيب</a>
        <a class="tile" href="{{ url_for('request_specialist') }}">🧑‍💼 طلب الأخصائي النفسي</a>
      </div>
    </div>
  </div>
</body>
</html>
"""

DSM_TMPL = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>DSM-5 | دراسة حالة وتشخيص</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body{font-family:"Tajawal",system-ui;-webkit-font-smoothing:antialiased;background:linear-gradient(135deg,#0b3a75,#0a65b0);color:#fff;margin:0}
    .wrap{max-width:980px;margin:24px auto;padding:16px}
    .bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
    a.home{color:#ffe28a;text-decoration:none}
    .grid{display:grid;grid-template-columns:1.2fr .8fr;gap:16px}
    @media(max-width:900px){.grid{grid-template-columns:1fr}}
    .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px;backdrop-filter:blur(6px)}
    label{font-size:.95rem;color:#ffe28a;margin:8px 3px 6px;display:block}
    input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:12px 14px;outline:none}
    input::placeholder,textarea::placeholder{color:#d0defa}
    textarea{min-height:120px;resize:vertical}
    .btn{appearance:none;border:none;border-radius:12px;padding:12px 18px;font-weight:800;cursor:pointer;background:#f4b400;color:#2b1b02}
    .result{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px}
    .badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:4px 0}
    .ok{background:#16a34a;color:#fff}
    .warn{background:#ef4444;color:#fff}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="bar">
      <h2 style="margin:0">🗂️ دراسة حالة + تشخيص (DSM-5)</h2>
      <a class="home" href="{{ url_for('home') }}">← العودة للواجهة</a>
    </div>

    <div class="grid">
      <!-- نموذج دراسة الحالة -->
      <section class="card">
        <form method="post">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div>
              <label>الاسم الكامل</label>
              <input name="name" value="{{ name or '' }}" placeholder="مثال: مشرف العنزي">
            </div>
            <div>
              <label>العمر</label>
              <input name="age" value="{{ age or '' }}" placeholder="30">
            </div>
            <div>
              <label>الجنس</label>
              <select name="gender">
                <option value="" {% if not gender %}selected{% endif %}>— اختر —</option>
                <option value="ذكر" {% if gender=='ذكر' %}selected{% endif %}>ذكر</option>
                <option value="أنثى" {% if gender=='أنثى' %}selected{% endif %}>أنثى</option>
              </select>
            </div>
            <div>
              <label>مدة الأعراض (بالأيام)</label>
              <input name="duration" value="{{ duration or '' }}" placeholder="مثال: 30">
            </div>
          </div>

          <label>الأعراض (أضف بدقة)</label>
          <textarea name="symptoms" placeholder="مثال: حزن، خمول، قلة نوم، فقدان شهية…">{{ symptoms or '' }}</textarea>

          <label>التاريخ الطبي/النفسي (اختياري)</label>
          <textarea name="history" placeholder="أدوية حالية، جلسات سابقة، أمراض جسدية…">{{ history or '' }}</textarea>

          <div style="display:flex;gap:10px;margin-top:10px">
            <button class="btn" type="submit">تشخيص مبدئي</button>
            <a class="btn" style="background:#22c55e" href="{{ url_for('home') }}">الواجهة</a>
          </div>
        </form>
      </section>

      <!-- النتيجة -->
      <aside class="result">
        <h3>📋 نتيجة التشخيص</h3>
        {% if diagnosis %}
          <div style="line-height:1.9">
            <strong>الاسم:</strong> {{ name or '—' }} &nbsp;|&nbsp;
            <strong>العمر:</strong> {{ age or '—' }} &nbsp;|&nbsp;
            <strong>الجنس:</strong> {{ gender or '—' }} &nbsp;|&nbsp;
            <strong>المدة:</strong> {{ duration or '—' }}
          </div>
          <div style="margin-top:8px">{% autoescape false %}{{ diagnosis }}{% endautoescape %}</div>
          <p style="opacity:.85;margin-top:8px">⚠️ نتيجة تقديرية آلية للمساعدة، وتتطلب تأكيدًا سريريًا.</p>
        {% else %}
          <span class="badge warn">لا توجد نتيجة بعد</span>
          <p style="opacity:.85">املأ الأعراض ثم اضغط "تشخيص مبدئي".</p>
        {% endif %}
      </aside>
    </div>
  </div>
</body>
</html>
"""

SIMPLE_TMPL = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body{margin:0;min-height:100vh;display:grid;place-items:center;font-family:"Tajawal",system-ui;background:linear-gradient(135deg,#0b3a75,#0a65b0);color:#fff}
    .box{max-width:800px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:18px;padding:26px;backdrop-filter:blur(6px);text-align:center}
    a{color:#ffe28a;text-decoration:none}
    .btn{display:inline-block;margin-top:12px;background:#f4b400;color:#062241;border-radius:14px;padding:10px 16px;font-weight:800;text-decoration:none}
  </style>
</head>
<body>
  <div class="box">
    <h1 style="margin:0 0 6px">{{ title }}</h1>
    <p style="opacity:.9">{{ subtitle }}</p>
    <a class="btn" href="{{ url_for('home') }}">العودة للواجهة</a>
  </div>
</body>
</html>
"""

# ======================= المسارات =======================
@app.route("/")
def home():
    return render_template_string(INDEX_TMPL)

@app.route("/dsm", methods=["GET","POST"])
def dsm():
    name = request.form.get("name","")
    age = request.form.get("age","")
    gender = request.form.get("gender","")
    duration = request.form.get("duration","")
    symptoms = request.form.get("symptoms","")
    history = request.form.get("history","")

    diagnosis_html = None
    if request.method == "POST":
        ranked = score_diagnoses(symptoms)
        if ranked:
            top = [f"{d} <span class='badge ok'>مطابقة تقريبية ({pts})</span>" for d, pts in ranked[:3]]
            diagnosis_html = "<strong>أقرب التشخيصات:</strong><br>" + "<br>".join(top)
        else:
            diagnosis_html = "<span class='badge warn'>لا توجد أعراض كافية للتشخيص.</span>"

    return render_template_string(
        DSM_TMPL,
        name=name, age=age, gender=gender, duration=duration,
        symptoms=symptoms, history=history, diagnosis=diagnosis_html
    )

# أزرار أخرى (صفحات مبسطة لمنع أخطاء الروابط)
@app.route("/tests")
def tests():
    return render_template_string(SIMPLE_TMPL, title="🧪 الاختبارات النفسية والشخصية", subtitle="سيتم ربطها لاحقًا بنتائج DSM/CBT.")

@app.route("/cbt")
def cbt():
    return render_template_string(SIMPLE_TMPL, title="💡 العلاج السلوكي المعرفي (CBT)", subtitle="خطة علاجية تُخصص لاحقًا حسب نتائج الاختبارات.")

@app.route("/addiction")
def addiction():
    return render_template_string(SIMPLE_TMPL, title="🚭 علاج الإدمان", subtitle="برنامج علاجي مستقل يمكن تغذيته لاحقًا.")

@app.route("/request_doctor")
def request_doctor():
    return render_template_string(SIMPLE_TMPL, title="👨‍⚕️ طلب الطبيب", subtitle="نموذج طلب استشارة طبيب — قريبًا.")

@app.route("/request_specialist")
def request_specialist():
    return render_template_string(SIMPLE_TMPL, title="🧑‍💼 طلب الأخصائي النفسي", subtitle="نموذج طلب أخصائي نفسي — قريبًا.")

# توافق خلفي لمسارات قديمة
@app.route("/case_study")
@app.route("/case_dsm")
@app.route("/dsm.html")
def legacy_to_dsm():
    return redirect(url_for("dsm"), code=301)

# تشغيل محلي
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
