# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ===============================
# 1) أدوات مساعدة للّغة العربية
# ===============================
def strip_diacritics(s: str) -> str:
    if not s:
        return ""
    # إزالة التشكيل + توحيد أشكال الحروف الشائعة
    repl = (
        ("\u064B", ""),("\u064C",""),("\u064D",""),("\u064E",""),
        ("\u064F",""),("\u0650",""),("\u0651",""),("\u0652",""),
        ("أ","ا"),("إ","ا"),("آ","ا"),("ى","ي"),("ة","ه"),
        ("ؤ","و"),("ئ","ي")
    )
    for a,b in repl:
        s = s.replace(a,b)
    return s

def norm(text: str) -> str:
    t = (text or "").lower()
    t = "".join(ch if ("0" <= ch <= "9") or ("a" <= ch <= "z")
                or ("\u0600" <= ch <= "\u06FF") or ch.isspace() else " "
                for ch in t)
    t = " ".join(t.split())
    return strip_diacritics(t)

def has_any(text, arr):  # هل يحتوي أي كلمة
    return any(k in text for k in arr)

def count_hits(text, arr):  # عدد التطابقات
    return sum(1 for k in arr if k in text)

# =========================================
# 2) قاعدة DSM موسعة (كلمات مفتاحية مختصرة)
#    تقدر توسّعها بإضافة عناصر على نفس النمط
#    كل عنصر: code, name, any[], aka?[], all?[], exclude?[], min_days?
# =========================================
DSM_CATALOG = [
    # -------- مزاج/اكتئاب --------
    {"code":"MDD","name":"الاكتئاب الشديد (MDD)",
     "aka":["اكتئاب","حزن","ضيقه","مزاج منخفض","كتمه"],
     "any":["حزن","فقدان المتعه","انعدام المتعه","ذنب","انعدام قيمه","ياس","انسحاب","ارهاق","ارق","نوم زائد","انتحار","تفكير بالموت"],
     "min_days":14},
    {"code":"PDD","name":"الاكتئاب المستمر (ديستيميا)",
     "any":["حزن مزمن","مزاج منخفض","طاقه منخفضه","تشاؤم","نقص ثقه"],
     "min_days":365},
    {"code":"PMDD","name":"الاضطراب المزعج السابق للحيض",
     "any":["تقلب قبل الدوره","تهيج قبل الدوره","اكتئاب قبل الدوره"]},

    # -------- ثنائي القطب --------
    {"code":"BP1","name":"ثنائي القطب النوع الأول",
     "any":["نوبه هوس","هوس","نشوه","قله نوم دون تعب","افكار عظمه","اندفاع","انفاق زائد","كلام سريع"],
     "exclude":["حزن فقط"], "min_days":7},
    {"code":"BP2","name":"ثنائي القطب النوع الثاني (هوس خفيف + اكتئاب)",
     "any":["هوس خفيف","طاقه عاليه","قله نوم","اكتئاب"], "min_days":4},

    # -------- قلق/رهاب --------
    {"code":"GAD","name":"قلق معمّم (GAD)",
     "aka":["توتر","تفكير زايد","ضيقه"],
     "any":["قلق","توتر","تفكير زايد","شد عضلي","تعب سريع","صعوبه تركيز","ارق"],
     "min_days":180},
    {"code":"PD","name":"نوبات هلع",
     "aka":["فجعه"],
     "any":["نوبه هلع","خفقان","اختناق","دوخه","رجفه","خوف موت","خوف فقد السيطره"]},
    {"code":"SOC","name":"رهاب اجتماعي",
     "any":["خوف اجتماعي","خوف من تقييم الناس","احمرار","تجنب اجتماعات","رعشه امام الجمهور"],
     "min_days":180},
    {"code":"Agoraphobia","name":"رهاب الميادين/الازدحام",
     "any":["خوف من الخروج","خوف من الزحام","تجنب مواصلات"], "min_days":180},
    {"code":"SP","name":"رهاب محدد",
     "any":["خوف من العناكب","خوف من الطيران","خوف من الحقن","فوبيا"]},

    # -------- وسواس قهري --------
    {"code":"OCD","name":"الوسواس القهري",
     "aka":["وسواس","قهري"],
     "any":["افكار تسلطيه","غسل متكرر","تفقد","طقوس","تنظيم قهري","عد","تكرار"],
     "min_days":90},
    {"code":"BDD","name":"تشوّه صورة الجسد",
     "any":["انشغال بعيب شكلي","تفقد مرايه","اخفاء ملامح"], "min_days":90},
    {"code":"Tricho","name":"نتف الشعر",
     "any":["نتف شعر","شد شعر","فراغات"]},
    {"code":"Onycho","name":"قضم الاظافر القهري",
     "any":["قضم اظافر","اكل اظافر"]},

    # -------- صدمات --------
    {"code":"PTSD","name":"اضطراب ما بعد الصدمة (PTSD)",
     "any":["صدمة","كابوس","استرجاع","تجنب","يقظه مفرطه","خدر"], "min_days":30},
    {"code":"ASD","name":"اضطراب كرب حاد",
     "any":["صدمة حديثه","كابوس","استرجاع","خدر"], "min_days":3},

    # -------- ذهانيات --------
    {"code":"SCHZ","name":"فصام",
     "any":["هلاوس سمعيه","ضلالات","تفكك كلام","انسحاب","تبلد وجداني"], "min_days":180},
    {"code":"Schizoaff","name":"اضطراب فصامي عاطفي",
     "any":["اعراض فصام","نوبات مزاج"]},
    {"code":"BriefPsych","name":"اضطراب ذهاني وجيز",
     "any":["هلاوس","ضلالات","تفكك","ضغط نفسي قوي"], "min_days":1},

    # -------- انتباه/تنفيذي --------
    {"code":"ADHD","name":"فرط حركة/تشتت (بالغين)",
     "aka":["نسايين"],
     "any":["تشتت","نسيان","تاجيل","اندفاع","تنظيم وقت ضعيف","حركه زايده"], "min_days":180},

    # -------- نوم --------
    {"code":"INS","name":"أرق مزمن",
     "any":["ارق","صعوبه نوم","استيقاظ مبكر","نوم سطحي"], "min_days":90},
    {"code":"Hypersomnia","name":"فرط النعاس",
     "any":["نعاس نهاري","نوم طويل","غفوات"]},
    {"code":"Parasomnia","name":"اضطرابات نوم (كوابيس/مشي نوم)",
     "any":["كابوس","مشي اثناء النوم","هلع ليلي"]},

    # -------- أكل --------
    {"code":"AN","name":"فقدان الشهية العصبي",
     "any":["نقص وزن شديد","خوف زياده وزن","صوره جسم مشوهه","تقييد اكل"], "min_days":90},
    {"code":"BN","name":"نهام عصبي",
     "any":["نهم اكل","قيء تعويضي","ملينات","تذبذب وزن"], "min_days":90},
    {"code":"BED","name":"نهم الطعام",
     "any":["اكل كميات كبيره","فقد السيطره على الاكل","ندم بعد الاكل"], "min_days":90},

    # -------- جسدية الشكل/قلق صحي --------
    {"code":"SOM","name":"اضطراب أعراض جسدية",
     "any":["الام متنقله","اعراض جسديه كثيره","فحوصات سليمه","انشغال صحي"], "min_days":180},
    {"code":"IAD","name":"قلق المرض (هيبوكوندريا)",
     "any":["خوف من المرض","تفقد جسد","قراءة طبيه مفرطه"], "min_days":180},

    # -------- تفارقي --------
    {"code":"DID","name":"اضطراب الهوية التفارقي",
     "any":["هويات متعدده","فجوات ذاكره","انفصال"]},
    {"code":"DPDR","name":"اختلال الآنية/الواقع",
     "any":["لاواقعيه","انفصال عن الذات","ضبابيه العالم"], "min_days":30},

    # -------- تعاطي/إدمان --------
    {"code":"AUD","name":"تعاطي الكحول",
     "any":["خمر","كحول","ثماله","انسحاب","فقد السيطره"]},
    {"code":"CUD","name":"تعاطي الحشيش",
     "any":["حشيش","قنب","استخدام يومي","نسيان"]},
    {"code":"OUD","name":"تعاطي الأفيونات",
     "any":["هيروين","مسكنات افيونيه","انسحاب","تحمل"]},
    {"code":"STIM","name":"تعاطي المنبهات",
     "any":["امفيتامين","كوكايين","كبتاجون","سهر طويل","بارانويا"]},
    {"code":"BDZ","name":"إساءة البنزوديازبين",
     "any":["زاناكس","فاليوم","انسحاب","تحمل"]},
    {"code":"TobUse","name":"تعاطي نيكوتين/تبغ",
     "any":["تدخين","سجائر","سحبات","رغبه شديده"]},

    # -------- نمو عصبي --------
    {"code":"ASD","name":"طيف التوحد (بالغين)",
     "any":["صعوبات تواصل اجتماعي","اهتمامات حصريه","حساسيه حسيه"]},

    # -------- شخصية (مؤشرات) --------
    {"code":"BPD","name":"سمات حدّية",
     "any":["اندفاع شديد","تقلب حاد","خوف هجر","ايذاء ذاتي"]},
    {"code":"AvPD","name":"شخصية تجنّبية",
     "any":["تجنب اجتماعي شديد","حساسيه للنقد","خجل مفرط"]},
    {"code":"OCPD","name":"شخصية قسرية",
     "any":["مثاليه مفرطه","صرامه","انشغال بالنظام"]},

    # -------- مؤشرات طبية لاستبعاد --------
    {"code":"Thy","name":"اشتباه اضطراب درقي (طبي)",
     "any":["خفقان","تعرق","نقص وزن غير مفسر","رجفه"]},
    {"code":"Anemia","name":"اشتباه فقر دم (طبي)",
     "any":["ارهاق مزمن","دوخه","شحوب"]},

    # -------- تكيّف/ضغوط --------
    {"code":"ADJ","name":"اضطراب تكيّف",
     "any":["حزن بعد حدث","قلق بعد حدث","صعوبه تكيف","ضغوط حياتيه"]},
    {"code":"Grief","name":"حزن/فجيعه مطوّل",
     "any":["فقد شخص","حزن مستمر","اشتياق مرير"], "min_days":180},

    # -------- اندفاع/عادات --------
    {"code":"IED","name":"انفجارات غضب (IED)",
     "any":["نوبات غضب لا تتناسب","عدوان اندفاعي"]},
    {"code":"Klepto","name":"هوس سرقة (مؤشر)",
     "any":["سرقه متكرره بلا مكسب","توتر قبل الفعل","راحه بعده"]},
    {"code":"Pyro","name":"هوس اشعال حرائق (مؤشر)",
     "any":["اشعال متكرر","اهتمام بالنار"]},

    # -------- أخرى لتوسيع الالتقاط --------
    {"code":"HealthAnx","name":"قلق صحي بعد جائحه/عدوى",
     "any":["خوف من العدوى","تعقيم مفرط","تفقد حراره"]},
    {"code":"Rumination","name":"اجترار افكار قهري",
     "any":["تفكير دائري","اعاده تحليل الماضي","لوم الذات المستمر"]},
    {"code":"DrivePhobia","name":"رهاب القياده/الطرق",
     "any":["خوف من القياده","تجنب الطرق","خوف حوادث"]}
]

# ============================
# 3) محرك الترشيح/التشخيص
# ============================
def score_disorder(text: str, duration_days: int, d: dict) -> int:
    score = 0
    # مرادفات
    score += count_hits(text, [norm(k) for k in d.get("aka", [])])
    # كلمات أيّاً منها
    score += count_hits(text, [norm(k) for k in d.get("any", [])])
    # كلمات يجب توفرها (إن وجدت)
    score += 2 * count_hits(text, [norm(k) for k in d.get("all", [])])
    # استثناءات تقلّل الدرجة
    if d.get("exclude") and has_any(text, [norm(k) for k in d["exclude"]]):
        score -= 2
    # عامل المدة (إن وُجد حد أدنى)
    if d.get("min_days") and duration_days is not None:
        try:
            if int(duration_days) >= int(d["min_days"]):
                score += 2
        except Exception:
            pass
    return max(score, 0)

def run_dsm_engine(symptoms: str, history: str, duration_days: int):
    text = norm((symptoms or "") + " " + (history or ""))
    results = []
    for d in DSM_CATALOG:
        sc = score_disorder(text, duration_days, d)
        if sc > 0:
            results.append((d["name"], sc))
    # ترتيب ونرجع أعلى 10 فقط
    results.sort(key=lambda x: x[1], reverse=True)
    top = results[:10]
    # صياغة نصية بسيطة متوافقة مع dsm.html (قائمة سطور)
    formatted = [f"{name} — درجة {score}" for name, score in top]
    return formatted

# ============================
# 4) المسارات (Routes)
# ============================
@app.route("/")
def home():
    return render_template("index.html")

# الواجهة الموحّدة: دراسة حالة + DSM (في قالب واحد dsm.html)
@app.route("/dsm", methods=["GET","POST"])
def dsm():
    if request.method == "POST":
        name     = request.form.get("name","").strip()
        age      = request.form.get("age","").strip()
        gender   = request.form.get("gender","").strip()
        duration = request.form.get("duration","").strip()
        symptoms = request.form.get("symptoms","").strip()

        diagnosis = run_dsm_engine(symptoms, history="", duration_days=int(duration) if duration else 0)
        if not diagnosis:
            diagnosis = ["❌ لا توجد أعراض كافية للتشخيص"]

        return render_template("dsm.html",
                               name=name, age=age, gender=gender,
                               duration=duration, symptoms=symptoms,
                               diagnosis=diagnosis)
    return render_template("dsm.html", diagnosis=None)

# تحويل للمسار القديم لو استُخدم
@app.route("/case_study", methods=["GET","POST"])
def case_study_legacy():
    return redirect(url_for("dsm"), code=301)

# صفحات ثانوية للتنقل (Placeholder)
@app.route("/tests")
def tests():
    return render_template("tests.html") if template_exists("tests.html") else "<h1>🧪 الاختبارات النفسية والشخصية</h1>"

@app.route("/cbt")
def cbt():
    return render_template("cbt.html") if template_exists("cbt.html") else "<h1>💡 العلاج السلوكي المعرفي (CBT)</h1>"

@app.route("/addiction")
def addiction():
    return render_template("addiction.html") if template_exists("addiction.html") else "<h1>🚭 علاج الإدمان</h1>"

@app.route("/request_doctor")
def request_doctor():
    return render_template("request_doctor.html") if template_exists("request_doctor.html") else "<h1>👨‍⚕️ طلب الطبيب</h1>"

@app.route("/request_specialist")
def request_specialist():
    return render_template("request_specialist.html") if template_exists("request_specialist.html") else "<h1>👨‍💼 طلب الأخصائي النفسي</h1>"

# أداة بسيطة للتأكد من وجود القالب (حتى لا يتعطل السيرفر لو الصفحة ناقصة)
def template_exists(name: str) -> bool:
    import os
    return os.path.exists(os.path.join(app.root_path, "templates", name))

# تشغيل محلي
if __name__ == "__main__":
    # على Render/خادم إنتاج استخدم Procfile + gunicorn
    app.run(host="0.0.0.0", port=5000)
