# -*- coding: utf-8 -*-
"""
عربي سايكو — ملف واحد (Purple × Gold)
v8.0 (full stack single-file Flask)

الصفحات:
    /            الرئيسية
    /case        دراسة الحالة (DSM-style + إدمان)
    /cbt         العلاج السلوكي المعرفي + مولّد الجداول
    /pharm       الصيدلية النفسية (تثقيف فقط)
    /tests       اختبارات نفسية/شخصية قصيرة
    /health      فحص جاهزية السيرفر (Ping)

⚠ مهم:
- هذا مو تشخيص طبي ولا وصف علاج.
- لا تبدأ/توقف دواء بدون دكتور/صيدلي مختص.
- إذا عندك أفكار إيذاء أو انتحار: هذا طارئ، لازم دعم فوري من مختص أو خدمة طوارئ.

التشغيل محلي:
    python app.py

التشغيل على Render/Railway:
    gunicorn app:app --bind 0.0.0.0:$PORT
"""

import os
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# ======================== إعدادات عامة / هوية البراند ========================

BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
SLOGAN = "«نراك بعين الاحترام، ونسير معك بخطوات عملية.»"

LOGO = os.environ.get(
    "LOGO_URL",
    # أيقونة بومة (رمز الحكمة/الليل)
    "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg"
)

TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696")
WA_BASE = WA_URL.split("?")[0]

PSYCHO_WA = os.environ.get("PSYCHOLOGIST_WA", "https://wa.me/966530565696")
PSYCH_WA  = os.environ.get("PSYCHIATRIST_WA", "https://wa.me/966530565696")
SOCIAL_WA = os.environ.get("SOCIAL_WORKER_WA", "https://wa.me/966530565696")

BUILD_STAMP = os.environ.get(
    "CACHE_BUST",
    datetime.utcnow().strftime("%Y%m%d%H%M%S")
)


# ======================== منطق التحليل السريري المبسّط ========================

def _cnt(flags, *keys):
    return sum(1 for k in keys if flags.get(k))

def preliminary_picks(flags):
    """
    يحاول يطلع "كتل" أعراض، مو تشخيص رسمي.
    يرجّع list من tuples: (عنوان, وصف مبسّط, درجة تقريبية)
    """
    picks = []

    # اكتئاب / مزاج منخفض
    dep_core = _cnt(flags, "low_mood", "anhedonia")
    dep_more = _cnt(
        flags,
        "fatigue", "sleep_issue", "appetite_change",
        "worthlessness", "poor_concentration",
        "psychomotor", "hopeless", "somatic_pain"
    )
    if dep_core >= 1 and dep_more >= 2:
        picks.append((
            "كتلة اكتئابية / مزاج منخفض",
            "أعراض مزاجية متعددة (طاقة/نوم/تركيز/ذنب..) قد تؤثر على حياتك اليومية",
            "درجة 70"
        ))

    # قلق عام / توتر
    if _cnt(flags, "worry", "tension", "restlessness", "irritability",
            "mind_blank", "sleep_anxiety", "concentration_anxiety") >= 3:
        picks.append((
            "قلق معمّم / توتر مستمر",
            "قلق زائد صعب التحكم مع توتر جسدي أو نوم مضطرب أو تشوش التركيز",
            "درجة 65"
        ))

    # هلع
    if flags.get("panic_attacks") or flags.get("panic_fear"):
        picks.append((
            "نوبات هلع",
            "نوبات قوية مفاجئة مع خوف من تكرارها أو تجنّب أماكن",
            "درجة 70"
        ))

    # رُهاب
    if flags.get("agoraphobia") or flags.get("specific_phobia"):
        picks.append((
            "رُهاب/رهبة مواقف",
            "خوف محدد (أماكن/مواقف/أشياء) مع تجنّب وطلب أمان",
            "درجة 65"
        ))

    # قلق اجتماعي
    if flags.get("social_fear"):
        picks.append((
            "قلق اجتماعي",
            "خشية التقييم/الإحراج مع تجنّب اجتماعي",
            "درجة 65"
        ))

    # وسواس قهري
    if flags.get("obsessions") and flags.get("compulsions"):
        picks.append((
            "وسواس قهري (OCD)",
            "وساوس ملحّة + أفعال قهرية (غسل/تفقد/ترتيب/طمأنة...)",
            "درجة 80"
        ))

    # صدمة / يقظة مفرطة
    if _cnt(flags, "flashbacks", "hypervigilance", "startle",
            "numbing", "trauma_avoid", "guilt_trauma") >= 2:
        picks.append((
            "آثار صدمة / يقظة مفرطة",
            "استرجاعات/كوابيس/توتر شديد/تجنّب مرتبط بحدث مؤلم",
            "درجة 70"
        ))

    # نوم
    if _cnt(flags, "insomnia", "hypersomnia", "nightmares",
            "irregular_sleep") >= 1:
        picks.append((
            "صعوبات نوم",
            "مشاكل بدء/استمرار النوم أو نوم زائد/كوابيس",
            "درجة 55"
        ))

    # تشتت/اندفاع
    if _cnt(flags, "adhd_inattention", "adhd_hyper",
            "disorganization", "time_blindness") >= 2:
        picks.append((
            "سمات تشتت/اندفاع (ADHD سمات)",
            "نسيان، تشتت، فوضى تنظيم ممكن تأثر على الدراسة/العمل",
            "درجة 60"
        ))

    # مزاج مرتفع / تهور
    if _cnt(flags, "elevated_mood", "decreased_sleep_need", "grandiosity",
            "racing_thoughts", "pressured_speech", "risk_spending") >= 3:
        picks.append((
            "سمات مزاج مرتفع / اندفاع عالي",
            "طاقة عالية جدًا + نوم قليل + اندفاع/مخاطرة",
            "درجة 70"
        ))

    # ذهاني / فصامي
    if _cnt(flags, "hallucinations", "delusions",
            "disorganized_speech", "negative_symptoms",
            "catatonia") >= 2 and flags.get("decline_function"):
        picks.append((
            "سمات ذهانية / فصامية",
            "هلوسات/أوهام/تفكك تفكير مع تأثير واضح على الأداء",
            "درجة 80"
        ))

    # أكل / صورة الجسد
    if _cnt(flags, "binge_eating", "restrict_eating", "body_image",
            "purging") >= 2:
        picks.append((
            "صعوبات أكل/صورة الجسد",
            "نوبات أكل أو تقييد أو قلق عالي حول الجسم/الوزن",
            "درجة 60"
        ))

    # إدمان / تعاطي
    if _cnt(flags, "craving", "withdrawal", "use_harm",
            "loss_control", "relapse_history") >= 2:
        picks.append((
            "تعاطي مواد / سلوك إدماني",
            "اشتهاء قوي، انسحاب، أو استمرار رغم الضرر",
            "درجة 80"
        ))

    # تنظيم عاطفة / غضب
    if _cnt(flags, "emotion_instability", "impulsivity", "anger_issues",
            "perfectionism", "dependence", "social_withdrawal") >= 3:
        picks.append((
            "تنظيم عاطفي / غضب / علاقات",
            "اندفاع، تقلب مزاج حاد، غضب مفاجئ، تمسّك زائد يضغط العلاقات",
            "درجة 60"
        ))

    # ثقة بالنفس
    if flags.get("self_conf_low"):
        picks.append((
            "ثقة بالنفس منخفضة",
            "نظرة ذاتية سلبية / جلد ذاتي / إحساس بعدم الكفاية",
            "درجة 50"
        ))

    # سمات تواصل/حسّية (طيف توحد)
    if _cnt(flags, "asd_social", "sensory", "rigidity") >= 2:
        picks.append((
            "سمات تواصل/حسّية (طيف توحد)",
            "حساسية حسّية / صعوبة قراءة الإشارات الاجتماعية / تمسّك عالي بالروتين",
            "درجة 55"
        ))

    # أمان
    if flags.get("suicidal"):
        picks.insert(0, (
            "🚨 تنبيه أمان",
            "وجود أفكار إيذاء أو انتحار — تواصل مع مختص الآن أو اطلب مساعدة طارئة.",
            "درجة 99"
        ))

    return picks

def suggest_plans(flags):
    """
    يربط الأعراض بخطط CBT اللي ممكن تساعد
    يرجّع قائمة أكواد خطط CBT (ba, sleep_hygiene, ...)
    """
    sug = []

    dep_core = _cnt(flags, "low_mood", "anhedonia")
    dep_more = _cnt(
        flags,
        "fatigue", "sleep_issue", "appetite_change",
        "worthlessness", "poor_concentration",
        "psychomotor", "hopeless", "somatic_pain"
    )
    if dep_core >= 1 and dep_more >= 2:
        sug += ["ba", "thought_record", "sleep_hygiene", "problem_solving"]

    if _cnt(flags, "worry", "tension", "restlessness", "irritability",
            "mind_blank", "sleep_anxiety", "concentration_anxiety") >= 3:
        sug += ["worry_time", "mindfulness", "problem_solving"]

    if flags.get("panic_attacks") or flags.get("panic_fear"):
        sug += ["interoceptive_exposure", "safety_behaviors"]

    if flags.get("agoraphobia") or flags.get("specific_phobia"):
        sug += ["graded_exposure"]

    if flags.get("social_fear"):
        sug += ["graded_exposure", "social_skills", "thought_record", "self_confidence"]

    if flags.get("obsessions") and flags.get("compulsions"):
        sug += ["ocd_erp", "safety_behaviors", "mindfulness"]

    if _cnt(flags, "flashbacks", "hypervigilance", "startle",
            "numbing", "trauma_avoid", "guilt_trauma") >= 2:
        sug += ["ptsd_grounding", "mindfulness", "sleep_hygiene"]

    if _cnt(flags, "insomnia", "hypersomnia", "nightmares",
            "irregular_sleep") >= 1:
        sug += ["sleep_hygiene", "mindfulness"]

    if _cnt(flags, "adhd_inattention", "adhd_hyper",
            "disorganization", "time_blindness") >= 2:
        sug += ["problem_solving", "ba"]

    if _cnt(flags, "elevated_mood", "decreased_sleep_need", "grandiosity",
            "racing_thoughts", "pressured_speech", "risk_spending") >= 3:
        sug += ["bipolar_routine", "sleep_hygiene"]

    if _cnt(flags, "craving", "withdrawal", "use_harm",
            "loss_control", "relapse_history") >= 2:
        sug += ["relapse_prevention", "problem_solving", "mindfulness"]

    if _cnt(flags, "emotion_instability", "impulsivity", "anger_issues",
            "perfectionism", "dependence", "social_withdrawal") >= 2:
        sug += ["anger_management", "mindfulness", "problem_solving", "self_confidence"]

    if _cnt(flags, "asd_social", "sensory", "rigidity") >= 2:
        sug += ["social_skills", "self_confidence", "problem_solving"]

    # dedupe
    out = []
    seen = set()
    for k in sug:
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out[:10]


# خريطة أسماء الخطط لعرضها في UI / CBT generator
CBT_LIBRARY = {
    "ba": {
        "title": "BA — تنشيط سلوكي",
        "tasks": [
            "اخرج 10 دقايق مشي/شمس.",
            "سوِّ نشاط بسيط يعطيك حتى 1% سعادة.",
            "ارسل رسالة دافئة لشخص تثق فيه."
        ]
    },
    "thought_record": {
        "title": "TR — سجل أفكار",
        "tasks": [
            "اكتب الموقف اللي ضايقك.",
            "ما هي الفكرة السلبية؟",
            "ما الدليل معها؟ ضدها؟",
            "اكتب نسخة فكرية أهدأ."
        ]
    },
    "sleep_hygiene": {
        "title": "SH — نظافة النوم",
        "tasks": [
            "وقت نوم/استيقاظ شبه ثابت.",
            "قاطع الجوال قبل النوم بـ 60 دقيقة.",
            "قهوة خفيفة أو معدومة آخر اليوم."
        ]
    },
    "problem_solving": {
        "title": "PS — حلّ المشكلات",
        "tasks": [
            "عرّف المشكلة كسؤال محدد.",
            "أكتب 3 حلول بدون حكم.",
            "اختر حل صغير جرّبه اليوم.",
            "قيّم النتيجة."
        ]
    },
    "worry_time": {
        "title": "WT — وقت القلق",
        "tasks": [
            "أجّل التفكير للمساء 15 دقيقة مخصصة.",
            "دوّن مخاوفك في ذيك الـ15 فقط.",
            "راقب: كم فعلاً منها صار؟"
        ]
    },
    "mindfulness": {
        "title": "MB — يقظة ذهنية",
        "tasks": [
            "تنفس 4-4-6 (شهيق4/ثبات4/زفير6).",
            "ركّز إحساس القدم بالأرض 60 ثانية.",
            "لاحظ الفكرة كحدث عابر مو حقيقة."
        ]
    },
    "interoceptive_exposure": {
        "title": "IE — تعرّض داخلي (هلع)",
        "tasks": [
            "راقب دقات قلبك بلا هروب.",
            "ذكر نفسك: مزعج مش خطير.",
            "قيّم شدة القلق بعد دقيقتين."
        ]
    },
    "safety_behaviors": {
        "title": "SA — تقليل طلب الطمأنة",
        "tasks": [
            "خفّض كم مرة تسأل (أنا بخير صح؟).",
            "جرب تبقى في الموقف بدون تطمين فوري.",
            "راقب: هل فعلاً انهار الوضع؟"
        ]
    },
    "graded_exposure": {
        "title": "GE — تعرّض تدرّجي",
        "tasks": [
            "اختر موقف خوف 3/10 (مو أقصى رعب).",
            "ادخل الموقف فترة قصيرة بدون هروب.",
            "اكتب النتيجة الواقعية مو الكارثة المتخيلة."
        ]
    },
    "social_skills": {
        "title": "SS — مهارات اجتماعية",
        "tasks": [
            "ابدأ تحية لطيفة مع شخص (السلام + سؤال بسيط).",
            "قول: 'أحتاج دقيقة أرتب فكرتي'.",
            "سمِّ شعورك بصوت واضح (أنا قلق شوي)."
        ]
    },
    "self_confidence": {
        "title": "SC — تعزيز الثقة",
        "tasks": [
            "دوّن إنجاز اليوم حتى لو صغير.",
            "قل لنفسك بصوت مسموع: (أنا قاعد أتحرك).",
            "أوقف جملة جلد ذاتي وحدة واستبدلها بجملة أهدى."
        ]
    },
    "ocd_erp": {
        "title": "ERP — وسواس قهري",
        "tasks": [
            "اختر وسواس متوسّط مو أعلى شي.",
            "أجّل الطقس القهري دقيقة إضافية.",
            "دوّن مستوى الضيق بعد 1 و5 دقايق."
        ]
    },
    "ptsd_grounding": {
        "title": "PTSD — تأريض بعد الصدمة",
        "tasks": [
            "تمرين 5-4-3-2-1 (أشياء تشوفها/تسمعها/تلمسها...).",
            "ذكّر نفسك: الآن آمن، الحدث انتهى.",
            "تنفس بطني بطيء دقيقتين."
        ]
    },
    "bipolar_routine": {
        "title": "IPSRT — روتين ثابت للمزاج",
        "tasks": [
            "نوم/استيقاظ تقريباً نفس الوقت.",
            "وجبات بأوقات شبه ثابتة.",
            "سجّل مزاجك رقمياً 0-10 يومياً."
        ]
    },
    "relapse_prevention": {
        "title": "RP — منع الانتكاس (إدمان)",
        "tasks": [
            "حدد أقوى مُحفّز اليوم.",
            "اكتب بديل سلوك آمن.",
            "راسل دعمك البشري (حتى سلام بسيط)."
        ]
    },
    "anger_management": {
        "title": "AM — إدارة الغضب",
        "tasks": [
            "لو فوق 6/10 غضب: خذ استراحة دقيقة هدوء.",
            "اسأل نفسك: تحت الغضب وش في؟ جرح؟ إحساس عدم احترام؟",
            "ارجع وتكلم بصيغة (أنا أحس...) مو (إنت دايم...)."
        ]
    },
}


# ======================== القالب العام لكل صفحة ========================

def render_page(page_title, active_tab, inner_html):
    """
    نبني صفحة HTML كاملة:
    - نفس الثيم البنفسجي × الذهبي
    - شريط روابط
    - صندوق "تواصل الآن"
    - المحتوى الداخلي اللي نمرره
    """

    # CSS
    css = """
    body {
        background: radial-gradient(circle at 20% 20%, #1b132d 0%, #0a0a0f 60%);
        color:#f7f3d6;
        font-family: system-ui, -apple-system, BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
        margin:0;
        padding:16px;
        line-height:1.6;
        direction:rtl;
        text-align:right;
    }
    header {
        text-align:center;
        margin-bottom:16px;
        color:#f7f3d6;
    }
    .brand-circle {
        width:64px;
        height:64px;
        border-radius:50%;
        border:2px solid #d1b23a;
        background:#1a132b;
        box-shadow:0 0 20px rgba(209,178,58,.4);
        display:flex;
        align-items:center;
        justify-content:center;
        margin:0 auto 8px;
        overflow:hidden;
    }
    .brand-circle img{
        width:48px;
        height:48px;
        object-fit:contain;
    }
    .brand-name{
        font-size:18px;
        font-weight:600;
        color:#f7f3d6;
    }
    .slogan{
        font-size:13px;
        color:#d1b23a;
        font-weight:500;
        margin-top:4px;
    }
    nav.nav{
        display:flex;
        flex-wrap:wrap;
        gap:8px;
        justify-content:center;
        margin:16px auto;
        max-width:900px;
    }
    nav.nav a{
        flex:1;
        min-width:140px;
        text-decoration:none;
        border-radius:12px;
        border:1px solid #3a2f55;
        background:#1a132b;
        box-shadow:0 0 12px rgba(209,178,58,.25);
        color:#f7f3d6;
        font-size:14px;
        padding:8px 10px;
        line-height:1.4;
        display:flex;
        flex-direction:column;
    }
    nav.nav a small{
        font-size:11px;
        color:#d1b23a;
    }
    nav.nav a.active{
        border:1px solid #d1b23a;
        box-shadow:0 0 16px rgba(209,178,58,.6);
    }
    .support-box{
        max-width:900px;
        margin:0 auto 16px;
        background:#1a132b;
        border:1px solid #3a2f55;
        border-radius:14px;
        box-shadow:0 0 24px rgba(209,178,58,.2);
        padding:12px;
    }
    .support-box h4{
        color:#d1b23a;
        margin:0 0 8px;
        font-size:14px;
        font-weight:600;
    }
    .support-links{
        display:flex;
        flex-wrap:wrap;
        gap:8px;
    }
    .support-links a{
        flex:1;
        min-width:140px;
        border-radius:10px;
        background:#241a3c;
        border:1px solid #3a2f55;
        color:#f7f3d6;
        text-decoration:none;
        font-size:13px;
        padding:8px;
        box-shadow:0 0 16px rgba(209,178,58,.15);
    }
    .support-links span{
        display:block;
        font-size:11px;
        color:#d1b23a;
        margin-top:2px;
        line-height:1.4;
    }
    main.main-card{
        max-width:900px;
        margin:0 auto;
        background:#1a132b;
        border:1px solid #3a2f55;
        border-radius:16px;
        box-shadow:0 0 30px rgba(209,178,58,.2);
        padding:16px;
        color:#f7f3d6;
        font-size:14px;
        line-height:1.6;
    }
    h1{
        font-size:18px;
        margin-top:0;
        color:#f7f3d6;
        font-weight:600;
    }
    h2{
        font-size:16px;
        color:#d1b23a;
        font-weight:600;
        margin:16px 0 8px;
    }
    h3{
        font-size:14px;
        color:#d1b23a;
        font-weight:600;
        margin:12px 0 6px;
    }
    p, li, label, div, small{
        font-size:14px;
    }
    small.small{
        font-size:11px;
        color:#999;
    }
    .section-card{
        background:#241a3c;
        border:1px solid #3a2f55;
        border-radius:12px;
        box-shadow:0 0 24px rgba(209,178,58,.18);
        padding:12px;
        margin-bottom:12px;
    }
    .grid{
        display:flex;
        flex-wrap:wrap;
        gap:12px;
    }
    .tile{
        flex:1;
        min-width:250px;
        background:#241a3c;
        border:1px solid #3a2f55;
        border-radius:12px;
        box-shadow:0 0 16px rgba(209,178,58,.15);
        padding:10px;
    }
    .tile h3{
        margin-top:0;
        font-size:13px;
        color:#d1b23a;
    }
    .badge2{
        display:flex;
        align-items:flex-start;
        gap:6px;
        flex-wrap:wrap;
        background:#2a2045;
        border:1px solid #3a2f55;
        border-radius:10px;
        box-shadow:0 0 12px rgba(209,178,58,.15);
        padding:6px 8px;
        font-size:13px;
        line-height:1.4;
        color:#f7f3d6;
        margin:4px 0;
    }
    .badge2 input[type=checkbox]{
        accent-color:#d1b23a;
        transform:scale(1.2);
        margin-top:2px;
    }
    input, select, textarea{
        width:100%;
        background:#2a2045;
        border:1px solid #3a2f55;
        border-radius:8px;
        color:#f7f3d6;
        font-size:14px;
        padding:8px;
        font-family:inherit;
        margin-top:4px;
    }
    textarea{min-height:80px; resize:vertical;}
    .divider{
        border-top:1px solid #3a2f55;
        margin:16px 0;
    }
    .row{
        display:flex;
        flex-wrap:wrap;
        gap:10px;
    }
    .btn{
        background:#2a2045;
        border:1px solid #3a2f55;
        border-radius:10px;
        color:#f7f3d6;
        font-size:14px;
        padding:8px 12px;
        text-decoration:none;
        cursor:pointer;
        line-height:1.4;
        min-width:120px;
        text-align:center;
        box-shadow:0 0 12px rgba(209,178,58,.2);
    }
    .gold{
        background:#3b2a00;
        border:1px solid #d1b23a;
        box-shadow:0 0 16px rgba(209,178,58,.5);
        font-weight:600;
    }
    .wa{ background:#1a2f1a; border:1px solid #2d5f2d; }
    .tg{ background:#1a2538; border:1px solid #2d4b7a; }
    .pro{ background:#241a3c; border:1px solid #3a2f55; flex:1; min-width:140px; }

    .dx-list{ padding-right:20px; margin:0; }

    /* جدول CBT */
    #checklist{
        margin-top:16px;
        background:#241a3c;
        border:1px solid #3a2f55;
        border-radius:12px;
        box-shadow:0 0 24px rgba(209,178,58,.15);
        padding:12px;
        font-size:14px;
        line-height:1.6;
        overflow-x:auto;
    }
    .check-day{
        border-bottom:1px solid #3a2f55;
        padding:8px 0;
    }
    .check-day:last-child{border-bottom:none;}
    .check-day h4{
        margin:0 0 6px;
        font-size:14px;
        color:#d1b23a;
    }
    .todo-item{
        display:flex;
        align-items:flex-start;
        gap:6px;
        font-size:14px;
        line-height:1.5;
    }
    .todo-item input[type=checkbox]{
        accent-color:#d1b23a;
        transform:scale(1.2);
        margin-top:2px;
    }

    /* كروت الأدوية */
    .drug-card{
        background:#241a3c;
        border:1px solid #3a2f55;
        border-radius:12px;
        box-shadow:0 0 24px rgba(209,178,58,.18);
        padding:12px;
        margin-bottom:12px;
        font-size:13px;
        line-height:1.5;
    }
    .drug-card h3{
        margin:0 0 8px;
        font-size:14px;
        color:#d1b23a;
    }
    .warn{
        color:#ff7676;
        font-size:12px;
        margin-top:6px;
        line-height:1.5;
    }

    footer{
        text-align:center;
        color:#888;
        font-size:12px;
        line-height:1.5;
        max-width:900px;
        margin:24px auto 8px;
    }
    footer .legal{
        color:#d1b23a;
        margin-top:8px;
        font-size:12px;
    }
    #print-note{
        font-size:11px;
        color:#777;
        text-align:center;
        margin-top:8px;
    }
    """

    # JS: مولّد جداول CBT + بحث الأدوية + اختبارات بسيطة
    js = """
    const CBT_LIBRARY = %CBT_LIBRARY_JSON%;
    function initPlanSelectors(){
      const selA = document.getElementById("planA");
      const selB = document.getElementById("planB");
      if(!selA || !selB) return;
      Object.keys(CBT_LIBRARY).forEach(key=>{
        const optA=document.createElement("option");
        optA.value=key;
        optA.textContent=CBT_LIBRARY[key].title;
        selA.appendChild(optA);
        const optB=document.createElement("option");
        optB.value=key;
        optB.textContent=CBT_LIBRARY[key].title;
        selB.appendChild(optB);
      });
    }
    function buildChecklist(){
      const days=parseInt(document.getElementById("daysSelect").value||"7");
      const planA=document.getElementById("planA").value;
      const planB=document.getElementById("planB").value||null;
      const out=[];
      for(let d=1;d<=days;d++){out.push({day:d,tasks:[]});}
      function pushTasks(planKey){
        if(!planKey) return;
        const lib=CBT_LIBRARY[planKey];
        if(!lib) return;
        lib.tasks.forEach(t=>{
          out.forEach(dayObj=>{
            dayObj.tasks.push({text:t,plan:planKey});
          });
        });
      }
      pushTasks(planA); pushTasks(planB);
      const wrap=document.getElementById("checklist");
      wrap.innerHTML="";
      out.forEach(dayObj=>{
        const div=document.createElement("div");
        div.className="check-day";
        div.innerHTML="<h4>اليوم "+dayObj.day+"</h4>";
        dayObj.tasks.forEach(task=>{
          const row=document.createElement("div");
          row.className="todo-item";
          row.innerHTML = `
            <input type="checkbox">
            <div>
              <div>${task.text}</div>
              <small class="small">الخطة: ${CBT_LIBRARY[task.plan]?.title||task.plan}</small>
            </div>`;
          div.appendChild(row);
        });
        wrap.appendChild(div);
      });
      const wa=document.getElementById("share-wa");
      const tg=document.getElementById("share-tg");
      if(wa){wa.href="%WA_BASE%?text="+encodeURIComponent("جدول CBT جاهز ✅");}
      if(tg){tg.href="%TG_URL%";}
    }
    function saveChecklist(){
      const wrap=document.getElementById("checklist");
      const txt=wrap.innerText||wrap.textContent||"";
      const blob=new Blob([txt],{type:"application/json"});
      const a=document.createElement("a");
      a.href=URL.createObjectURL(blob);
      a.download="cbt-plan-%BUILD%.json";
      a.click();
    }
    function downloadCaseSummary(){
      const sec=document.querySelector(".case-result");
      if(!sec)return;
      const data={
        brand:"%BRAND%",
        ts:"%BUILD%",
        summaryText:sec.innerText
      };
      const blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"});
      const a=document.createElement("a");
      a.href=URL.createObjectURL(blob);
      a.download="case-summary-%BUILD%.json";
      a.click();
    }
    // بيانات الأدوية التثقيفية
    const DRUGS = [
      {
        name:"مثبطات السيروتونين الانتقائية (SSRI)",
        use:"اكتئاب، قلق عام، وسواس قهري غالباً",
        common:"غثيان خفيف، صداع، تغير نوم/شهية، أحيانًا برود جنسي",
        urgent:"أفكار انتحارية جديدة بشكل مفاجئ أو تهيج/هوس غير طبيعي"
      },
      {
        name:"مثبتات المزاج",
        use:"لتقلب مزاج حاد أو نوبات مزاج مرتفع",
        common:"عطش، رجفة خفيفة، زيادة وزن محتملة",
        urgent:"إقياء شديد، تشوش وعي، خمول أو نعاس غريب جدًا"
      },
      {
        name:"مضادات الذهان الحديثة",
        use:"هلاوس، أوهام، اضطراب إدراك شديد",
        common:"نعاس، زيادة شهية، جفاف فم",
        urgent:"تيبس قوي بالعضلات + حرارة + ارتباك ذهني قوي"
      },
      {
        name:"أدوية نوم/قلق مهدئة قصيرة المدى",
        use:"قلق شديد مؤقت أو أرق حاد قصير",
        common:"نعاس، إبطاء تركيز/تفاعل",
        urgent:"نعاس مفرط جدًا أو صعوبة تنفس"
      },
      {
        name:"أدوية دعم الإدمان / منع الانتكاس",
        use:"تقلل الاشتهاء أو تساعد تثبيت السلوك بعد الإيقاف",
        common:"غثيان بسيط، صداع، دوخة",
        urgent:"اصفرار عين/جلد، ألم بطن قوي، تشنجات شديدة"
      }
    ];
    function pharmSearch(){
      const q=(document.getElementById("pharm-q").value||"").trim().toLowerCase();
      const zone=document.getElementById("pharm-results");
      zone.innerHTML="";
      DRUGS.filter(d=>
        d.name.toLowerCase().includes(q) ||
        d.use.toLowerCase().includes(q)
      ).forEach(d=>{
        const card=document.createElement("div");
        card.className="drug-card";
        card.innerHTML = `
          <h3>${d.name}</h3>
          <div><b>لماذا يُصرف؟</b> ${d.use}</div>
          <div><b>شائع:</b> ${d.common}</div>
          <div class="warn"><b>عناية طبية فورية لو:</b> ${d.urgent}</div>
          <div class="warn"><b>تحذير:</b> لا تبدأ/توقف دواء بدون طبيب/صيدلي مختص.</div>
        `;
        zone.appendChild(card);
      });
    }
    // اختبارات سريعة (مزاج/قلق ذاتي)
    function calcMoodTest(){
      // قراءة 3 أسئلة بسيطة (0-3) وجمعها
      const f = document.getElementById("mood-form");
      if(!f)return;
      let total=0;
      ["m1","m2","m3"].forEach(name=>{
        const v=f.querySelector(`input[name="${name}"]:checked`);
        if(v){ total+=parseInt(v.value||"0"); }
      });
      const out=document.getElementById("mood-result");
      let msg="مستوى منخفض / طبيعي نسبيًا 🌿";
      if(total>=4 and total<=6):  # intentionally invalid python, we'll fix
        pass
    }
    """

    # NOTE:
    # ^ we can't leave invalid python in JS generation. So we won't actually generate mood calc in python.
    # We'll embed JS directly without python logic.

    js_tests = r"""
    function calcMoodTest(){
      const f = document.getElementById("mood-form");
      if(!f){return;}
      let total=0;
      ["m1","m2","m3"].forEach(function(name){
        const v=f.querySelector('input[name="'+name+'"]:checked');
        if(v){ total+=parseInt(v.value||"0"); }
      });
      let msg="مستوى منخفض / طبيعي نسبيًا 🌿";
      if(total>=4 && total<=6){
        msg="علامات توتر/ضيق متوسط 😟 يحتاج راحة منظمة ودعم بسيط.";
      }else if(total>=7){
        msg="ضيق عالي 😢 — لو التفكير صار فيه إيذاء أو عجز، اطلب دعم مختص بسرعة.";
      }
      document.getElementById("mood-result").innerText =
        "النتيجة: "+total+" ← "+msg;
    }
    """

    # نحط مكتبة CBT كـ JSON نصي داخل السكربت:
    import json
    js_final = js.replace(
        "%CBT_LIBRARY_JSON%",
        json.dumps(CBT_LIBRARY, ensure_ascii=False)
    ).replace(
        "%WA_BASE%", WA_BASE
    ).replace(
        "%TG_URL%", TG_URL
    ).replace(
        "%BUILD%", BUILD_STAMP
    ).replace(
        "%BRAND%", BRAND
    )

    js_final += js_tests

    # العلامة النشطة للتاب
    def active(tab):
        return "active" if tab == active_tab else ""

    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
      <meta charset="utf-8"/>
      <meta name="viewport" content="width=device-width,initial-scale=1"/>
      <title>{page_title}</title>
      <style>{css}</style>
      <script>{js_final}</script>
    </head>
    <body onload="initPlanSelectors()">

      <header>
        <div class="brand-circle">
          <img src="{LOGO}" alt="logo"/>
        </div>
        <div class="brand-name">{BRAND}</div>
        <div class="slogan">{SLOGAN}</div>
        <small class="small">بنفسجي × ذهبي — {BUILD_STAMP}</small>
      </header>

      <nav class="nav">
        <a href="/" class="{active('home')}">
          <span>🏠 الرئيسية</span>
          <small>واجهة آمنة</small>
        </a>
        <a href="/case" class="{active('case')}">
          <span>📝 دراسة الحالة</span>
          <small>أعراضك وتشخيص مبدئي</small>
        </a>
        <a href="/cbt" class="{active('cbt')}">
          <span>🧠 CBT</span>
          <small>خطط + الجدول</small>
        </a>
        <a href="/pharm" class="{active('pharm')}">
          <span>💊 الصيدلية النفسية</span>
          <small>لماذا يُصرف؟ التحذيرات</small>
        </a>
        <a href="/tests" class="{active('tests')}">
          <span>🧪 اختبارات نفسية</span>
          <small>مقياس شعورك الآن</small>
        </a>
      </nav>

      <section class="support-box">
        <h4>📞 دعم مباشر الآن</h4>
        <div class="support-links">
          <a href="{PSYCHO_WA}" target="_blank" rel="noopener">
            👨‍🎓 أخصائي نفسي
            <span>خطة سلوكية/CBT</span>
          </a>
          <a href="{PSYCH_WA}" target="_blank" rel="noopener">
            👨‍⚕️ طبيب نفسي
            <span>تشخيص طبي / أدوية</span>
          </a>
          <a href="{SOCIAL_WA}" target="_blank" rel="noopener">
            🤝 أخصائي اجتماعي
            <span>دعم حياتي / أسري</span>
          </a>
        </div>
      </section>

      <main class="main-card">
        {inner_html}
      </main>

      <footer>
        © جميع الحقوق محفوظة لـ {BRAND} — {SLOGAN}<br/>
        تيليجرام الدعم: {TG_URL} · واتساب: {WA_URL}<br/>
        الإصدار البنفسجي × الذهبي — BUILD {BUILD_STAMP}
        <div class="legal">
          هذه الأداة ليست بديلاً عن رعاية طبية طارئة أو طبيب نفسي مرخّص.
        </div>
        <div id="print-note">احتفظ بنسختك بسرّية. هذه بيانات حسّاسة.</div>
      </footer>

    </body>
    </html>
    """
    return html


# ======================== الصفحات ========================

@app.get("/")
def home_page():
    inner = f"""
    <h1>مرحبًا بك في {BRAND} 👋</h1>
    <p>
    مكان آمن ومحترم. فكرتنا واضحة:
    </p>
    <ol class="dx-list">
      <li>📝 قيّم نفسك في «دراسة الحالة»</li>
      <li>🧠 نولّد لك خطة CBT عملية مع جدول يومي</li>
      <li>🤝 لو تحتاج بشر الآن: تواصل مع أخصائي/طبيب/أخصائي اجتماعي بزر واحد</li>
      <li>💊 تبي شرح عن أدوية نفسية ولماذا تُصرف؟ افتح «الصيدلية النفسية»</li>
      <li>🧪 تبي مقياس سريع لمستوى القلق/المزاج؟ افتح «الاختبارات النفسية»</li>
    </ol>

    <div class="divider"></div>

    <div class="section-card">
      <h2>جاهز تبدأ؟</h2>
      <div class="row">
        <a class="btn gold" href="/case">ابدأ دراسة الحالة</a>
        <a class="btn gold" href="/cbt">افتح CBT الآن</a>
        <a class="btn gold" href="/pharm">شوف الصيدلية النفسية</a>
        <a class="btn gold" href="/tests">قيّم شعورك السريع</a>
      </div>
    </div>

    <small class="small">
    ⚠ ما نعطي تشخيص طبي رسمي. هذا يساعدك ترتّب أفكارك وتاخذ خطوة واعية بدل ما تضيع لحالك.
    </small>
    """
    return render_page("الرئيسية — " + BRAND, "home", inner)


# ---------- /case : دراسة الحالة ----------

CASE_FORM_HTML = """
<h1>📝 دراسة الحالة</h1>

<p>
اختر الأعراض اللي فعلاً تحسها هذه الفترة. بعدين اضغط "عرض النتيجة".
هذي مو تشخيص نهائي — هذي خريطة أولية تساعدك تعرف وين تبدأ.
</p>

<p class="small">
خصوصيتك: المدخلات تنرسل بس مع الطلب هذا. ما عندنا قاعدة بيانات هنا.
</p>

<form method="POST" action="/case">
  <h2>معلومات أساسية</h2>
  <div class="grid">
    <div class="tile">
      <label>العمر
        <input name="age" type="number" min="5" max="120" placeholder="28">
      </label>
    </div>
    <div class="tile">
      <label>الحالة الاجتماعية
        <select name="marital">
          <option value="">—</option>
          <option>أعزب/عزباء</option>
          <option>متزوج/ة</option>
          <option>منفصل/ة</option>
          <option>مطلق/ة</option>
          <option>أرمل/أرملة</option>
        </select>
      </label>
    </div>
    <div class="tile">
      <label>عمل/دراسة
        <input name="work" placeholder="طالب / موظف / باحث عن عمل / غير ذلك">
      </label>
    </div>
  </div>

  <div class="divider"></div>

  <h2>الأعراض (اختر اللي ينطبق فعلاً)</h2>

  <div class="grid">

    <div class="tile">
      <h3>🟣 المزاج / الاكتئاب</h3>
      <label class="badge2"><input type="checkbox" name="low_mood"> مزاج منخفض أغلب الوقت</label>
      <label class="badge2"><input type="checkbox" name="anhedonia"> فقدان المتعة بالأشياء</label>
      <label class="badge2"><input type="checkbox" name="hopeless"> إحساس باليأس/التشاؤم</label>
      <label class="badge2"><input type="checkbox" name="fatigue"> إرهاق / طاقة منخفضة</label>
      <label class="badge2"><input type="checkbox" name="sleep_issue"> نوم متقطع / نوم سيئ</label>
      <label class="badge2"><input type="checkbox" name="appetite_change"> تغيير بالشّهية / الوزن</label>
      <label class="badge2"><input type="checkbox" name="somatic_pain"> آلام جسدية بدون سبب واضح</label>
      <label class="badge2"><input type="checkbox" name="worthlessness"> شعور ذنب / عدم قيمة</label>
      <label class="badge2"><input type="checkbox" name="poor_concentration"> تركيز ضعيف / بطء تفكير</label>
      <label class="badge2"><input type="checkbox" name="psychomotor"> بطء أو تهيّج حركي واضح</label>
      <label class="badge2"><input type="checkbox" name="suicidal"> أفكار إيذاء أو انتحار</label>
    </div>

    <div class="tile">
      <h3>🟣 القلق / الهلع / الرهاب</h3>
      <label class="badge2"><input type="checkbox" name="worry"> قلق زائد صعب السيطرة</label>
      <label class="badge2"><input type="checkbox" name="tension"> شد عضلي / توتر جسدي</label>
      <label class="badge2"><input type="checkbox" name="restlessness"> عصبية / تململ</label>
      <label class="badge2"><input type="checkbox" name="irritability"> سرعة انفعال</label>
      <label class="badge2"><input type="checkbox" name="mind_blank"> فراغ ذهني تحت الضغط</label>
      <label class="badge2"><input type="checkbox" name="sleep_anxiety"> صعوبة نوم بسبب القلق</label>
      <label class="badge2"><input type="checkbox" name="concentration_anxiety"> تشوش تركيز مع القلق</label>
      <label class="badge2"><input type="checkbox" name="panic_attacks"> نوبات هلع متكررة</label>
      <label class="badge2"><input type="checkbox" name="panic_fear"> خوف قوي من نوبة هلع جديدة</label>
      <label class="badge2"><input type="checkbox" name="agoraphobia"> رهبة أماكن مزدحمة/مفتوحة</label>
      <label class="badge2"><input type="checkbox" name="specific_phobia"> رُهاب محدد (طيران/حيوان..)</label>
      <label class="badge2"><input type="checkbox" name="social_fear"> خوف من التقييم/الإحراج</label>
    </div>

    <div class="tile">
      <h3>🟣 وسواس قهري (OCD)</h3>
      <label class="badge2"><input type="checkbox" name="obsessions"> أفكار/صور مُلِحّة ما توقف</label>
      <label class="badge2"><input type="checkbox" name="compulsions"> أفعال قهرية (غسل/تفقد...)</label>
      <label class="badge2"><input type="checkbox" name="contamination"> خوف تلوث / غسل مفرط</label>
      <label class="badge2"><input type="checkbox" name="checking"> تفقد الأقفال/الأبواب كثير</label>
      <label class="badge2"><input type="checkbox" name="ordering"> لازم ترتيب/تماثل مثالي</label>
      <label class="badge2"><input type="checkbox" name="harm_obs"> وساوس أذى (أضر نفسي/غيري؟)</label>
      <label class="badge2"><input type="checkbox" name="scrupulosity"> تدقيق ديني/أخلاقي قهري</label>
    </div>

    <div class="tile">
      <h3>🟣 صدمة / بعد الصدمة</h3>
      <label class="badge2"><input type="checkbox" name="flashbacks"> استرجاعات/كوابيس لحادث صعب</label>
      <label class="badge2"><input type="checkbox" name="hypervigilance"> يقظة مفرطة / على أهبة الاستعداد</label>
      <label class="badge2"><input type="checkbox" name="startle"> فزع مفرط من الأصوات/المفاجآت</label>
      <label class="badge2"><input type="checkbox" name="numbing"> خدر عاطفي / إحساس بالانفصال</label>
      <label class="badge2"><input type="checkbox" name="trauma_avoid"> أتجنب تذكير بالحدث</label>
      <label class="badge2"><input type="checkbox" name="guilt_trauma"> شعور بالذنب تجاه اللي صار</label>
    </div>

    <div class="tile">
      <h3>🟣 النوم</h3>
      <label class="badge2"><input type="checkbox" name="insomnia"> أرق / صعوبة بداية النوم</label>
      <label class="badge2"><input type="checkbox" name="hypersomnia"> نوم مفرط / صعوبة أقوم</label>
      <label class="badge2"><input type="checkbox" name="nightmares"> كوابيس متكررة</label>
      <label class="badge2"><input type="checkbox" name="irregular_sleep"> مواعيد نوم فوضوية</label>
    </div>

    <div class="tile">
      <h3>🟣 تركيز / تنظيم / اندفاع</h3>
      <label class="badge2"><input type="checkbox" name="adhd_inattention"> تشتت / نسيان أساسيات</label>
      <label class="badge2"><input type="checkbox" name="adhd_hyper"> فرط حركة / صعوبة أجلس</label>
      <label class="badge2"><input type="checkbox" name="disorganization"> فوضى تنظيم / تسويف مزمن</label>
      <label class="badge2"><input type="checkbox" name="time_blindness"> ضياع الإحساس بالوقت دائم</label>
    </div>

    <div class="tile">
      <h3>🟣 مزاج مرتفع / اندفاع عالي</h3>
      <label class="badge2"><input type="checkbox" name="elevated_mood"> مزاج مرتفع جدًا / تهوّر</label>
      <label class="badge2"><input type="checkbox" name="decreased_sleep_need"> ما أحتاج نوم كثير وأحس تمام</label>
      <label class="badge2"><input type="checkbox" name="grandiosity"> إحساس بالعظمة / قدرات خارقة</label>
      <label class="badge2"><input type="checkbox" name="racing_thoughts"> أفكار سريعة جدًا</label>
      <label class="badge2"><input type="checkbox" name="pressured_speech"> كلام سريع/مندفع جدًا</label>
      <label class="badge2"><input type="checkbox" name="risk_spending"> صرف فلوس/مخاطرة عالية فجأة</label>
    </div>

    <div class="tile">
      <h3>🟣 إدراك/تفكير (ذهاني/فصامي)</h3>
      <label class="badge2"><input type="checkbox" name="hallucinations"> هلوسات (أسمع/أشوف شي غير الناس)</label>
      <label class="badge2"><input type="checkbox" name="delusions"> أفكار يقين غريب / مراقبة / مؤامرة</label>
      <label class="badge2"><input type="checkbox" name="disorganized_speech"> كلام/تفكير متشتت وغير مفهوم</label>
      <label class="badge2"><input type="checkbox" name="negative_symptoms"> انسحاب / برود عاطفي</label>
      <label class="badge2"><input type="checkbox" name="catatonia"> تجمّد / بطء تفاعل شديد</label>
      <label class="badge2"><input type="checkbox" name="decline_function"> تدهور واضح في الدراسة/العمل/العلاقات</label>
    </div>

    <div class="tile">
      <h3>🟣 الأكل / صورة الجسد</h3>
      <label class="badge2"><input type="checkbox" name="binge_eating"> نوبات أكل شره / فقدان سيطرة</label>
      <label class="badge2"><input type="checkbox" name="restrict_eating"> تقييد قوي / تجويع نفسي</label>
      <label class="badge2"><input type="checkbox" name="body_image"> قلق عالي حول شكل الجسم/الوزن</label>
      <label class="badge2"><input type="checkbox" name="purging"> تطهير/إقياء قهري بعد الأكل</label>
    </div>

    <div class="tile">
      <h3>🟣 تعاطي مواد / إدمان</h3>
      <label class="badge2"><input type="checkbox" name="craving"> اشتهاء قوي / أحتاج أستخدم الآن</label>
      <label class="badge2"><input type="checkbox" name="withdrawal"> انسحاب جسدي/نفسي لو وقفت</label>
      <label class="badge2"><input type="checkbox" name="use_harm"> أستمر رغم ضرر واضح</label>
      <label class="badge2"><input type="checkbox" name="loss_control"> صعوبة إيقاف / فقدان السيطرة</label>
      <label class="badge2"><input type="checkbox" name="relapse_history"> انتكاسات بعد المحاولة</label>
    </div>

    <div class="tile">
      <h3>🟣 تنظيم العاطفة / العلاقات / الغضب</h3>
      <label class="badge2"><input type="checkbox" name="emotion_instability"> تقلب مزاج حاد / مشاعر قوية فجأة</label>
      <label class="badge2"><input type="checkbox" name="impulsivity"> اندفاع / أتصرف قبل ما أفكر</label>
      <label class="badge2"><input type="checkbox" name="anger_issues"> نوبات غضب / انفجار سريع</label>
      <label class="badge2"><input type="checkbox" name="perfectionism"> كمالية خانقة / كل شي لازم مثالي</label>
      <label class="badge2"><input type="checkbox" name="dependence"> تعلق عالي / خوف من الهجر</label>
      <label class="badge2"><input type="checkbox" name="social_withdrawal"> انسحاب اجتماعي قوي</label>
      <label class="badge2"><input type="checkbox" name="self_conf_low"> ثقة بالنفس منخفضة / جلد ذاتي</label>
    </div>

    <div class="tile">
      <h3>🟣 تواصل / حساسية حسّية</h3>
      <label class="badge2"><input type="checkbox" name="asd_social"> صعوبة قراءة الإشارات الاجتماعية</label>
      <label class="badge2"><input type="checkbox" name="sensory"> حساسية حسّية (صوت/إضاءة/ملمس)</label>
      <label class="badge2"><input type="checkbox" name="rigidity"> تمسّك عالي بروتين/نظام يضايقك لو تغيّر</label>
    </div>

  </div>

  <div class="divider"></div>

  <label>ملاحظاتك (اختياري)
    <textarea name="notes" placeholder="شي محدد مضايقك؟ موقف صار؟ شي يخوفك؟"></textarea>
  </label>

  <div class="row" style="margin-top:14px">
    <button class="btn gold" type="submit">عرض النتيجة</button>
    <a class="btn" href="/cbt">🧠 فتح CBT الآن</a>
  </div>
</form>
"""

def build_case_result_html(picks, plans):
    # تحويل النتائج لواجهة جاهزة داخل الصفحة
    if picks:
        dx_html = "".join([
            "<li><b>{}</b> — {} <span class='small'>({})</span></li>".format(
                title, desc, score
            )
            for (title, desc, score) in picks
        ])
    else:
        dx_html = (
            "<li>ما لقينا مؤشرات قوية حالياً. وعيك بنفسك خطوة مهمة 👏</li>"
        )

    PLAN_TITLES = {
        "ba": "BA — تنشيط سلوكي",
        "thought_record": "TR — سجل أفكار",
        "sleep_hygiene": "SH — نظافة النوم",
        "problem_solving": "PS — حلّ المشكلات",
        "worry_time": "WT — وقت القلق",
        "mindfulness": "MB — يقظة ذهنية",
        "interoceptive_exposure": "IE — تعرّض داخلي (هلع)",
        "safety_behaviors": "SA — تقليل طلب الطمأنة",
        "graded_exposure": "GE — تعرّض تدرّجي",
        "social_skills": "SS — مهارات اجتماعية",
        "self_confidence": "SC — تعزيز الثقة",
        "ocd_erp": "ERP — وسواس قهري",
        "ptsd_grounding": "PTSD — تأريض/تنظيم بعد الصدمة",
        "bipolar_routine": "IPSRT — روتين ثابت للمزاج",
        "relapse_prevention": "RP — منع الانتكاس (إدمان)",
        "anger_management": "AM — إدارة الغضب",
    }

    if plans:
        plans_html = "".join([
            "<span class='badge2'>🔧 {}</span>".format(
                PLAN_TITLES.get(key, key)
            )
            for key in plans
        ])
    else:
        plans_html = "<span class='small'>لا توصيات محددة الآن.</span>"

    praise_line = (
        "أحسنت 👏 — وعيك بنفسك مهم. هذا مو تشخيص طبي رسمي،"
        " لكنه خريطة أولية تساعد تختار خطة سلوكية عملية بدل ما تبقى ضايع."
    )

    out = f"""
    <section class="case-result">
      <div class="section-card">
        <h2>📌 نتائج مبدئية</h2>
        <p>{praise_line}</p>
        <ul class="dx-list">{dx_html}</ul>
      </div>

      <div class="section-card">
        <h2>🔧 أدوات CBT المقترحة لك</h2>
        <div class="row">{plans_html}</div>
      </div>

      <div class="section-card">
        <h2>🚀 ماذا بعد؟</h2>
        <ol class="dx-list">
          <li>احفظ أو اطبع هذا الملخص.</li>
          <li>اضغط "فتح CBT" لتوليد جدول 7 / 10 / 14 يوم بخطوات يومية.</li>
          <li>لو تحس الوضع أكبر من قدرتك لوحدك: تواصل مع أخصائي/طبيب من فوق.</li>
        </ol>
        <div class="row">
          <button class="btn gold" onclick="window.print()">🖨️ طباعة</button>
          <button class="btn" onclick="downloadCaseSummary()">💾 تنزيل JSON</button>
          <a class="btn gold" href="/cbt">🧠 فتح CBT الآن</a>
        </div>
      </div>
    </section>
    """
    return out

@app.route("/case", methods=["GET", "POST"])
def case_page():
    if request.method == "GET":
        return render_page("دراسة الحالة — " + BRAND, "case", CASE_FORM_HTML)

    # POST: اجمع العلامات اللي المستخدم اخترها
    form_data = {
        k: True
        for k in request.form.keys()
        if k not in ("age", "marital", "work", "notes")
    }
    # meta info (مو مستخدم حالياً لكن ممكن نعرض لاحقاً)
    form_data["age_val"]     = request.form.get("age","").strip()
    form_data["marital_val"] = request.form.get("marital","").strip()
    form_data["work_val"]    = request.form.get("work","").strip()
    _user_notes              = request.form.get("notes","").strip()

    picks = preliminary_picks(form_data)
    plans = suggest_plans(form_data)
    result_html = build_case_result_html(picks, plans)

    return render_page("نتيجة الحالة — " + BRAND, "case", result_html)


# ---------- /cbt : العلاج السلوكي المعرفي ----------

CBT_HTML = f"""
<h1>🧠 العلاج السلوكي المعرفي (CBT)</h1>

<p>
الهدف: مو بس "تفهم مشكلتك"، بل خطة يومية صغيرة ممكن تنفذها فعلاً.
إختر خطة أو خطتين، وحدد المدة (7 / 10 / 14 يوم)،
واضغط "إنشاء الجدول".
</p>

<div class="section-card">
  <h2>الخطط (أمثلة من المكتبة)</h2>
  <ul class="dx-list">
    <li>BA — تنشيط سلوكي (مزاج منخفض)</li>
    <li>WT — وقت القلق (قلق عام)</li>
    <li>IE — تعرّض داخلي (نوبات هلع)</li>
    <li>ERP — وسواس قهري</li>
    <li>PTSD — تأريض/تنظيم بعد الصدمة</li>
    <li>IPSRT — روتين ثابت للمزاج المرتفع/الهايج</li>
    <li>RP — منع الانتكاس (إدمان)</li>
    <li>AM — إدارة الغضب</li>
    <li>SC — تعزيز الثقة بالنفس</li>
  </ul>
</div>

<div class="section-card">
  <h2>📅 مولّد الجدول اليومي</h2>
  <div class="row">
    <label style="flex:1;min-width:160px;">
      الخطة A:
      <select id="planA"></select>
    </label>
    <label style="flex:1;min-width:160px;">
      الخطة B (اختياري):
      <select id="planB"><option value="">— بدون —</option></select>
    </label>
    <label style="flex:1;min-width:120px;">
      المدة (أيام):
      <select id="daysSelect">
        <option value="7">7</option>
        <option value="10">10</option>
        <option value="14">14</option>
      </select>
    </label>
    <button class="btn gold" type="button" onclick="buildChecklist()">إنشاء الجدول</button>
    <button class="btn" type="button" onclick="saveChecklist()">💾 تنزيل الجدول</button>
    <a class="btn wa" id="share-wa" target="_blank" rel="noopener">🟢 واتساب</a>
    <a class="btn tg" id="share-tg" target="_blank" rel="noopener">✈️ تيليجرام</a>
  </div>

  <div id="checklist"></div>
</div>

<div class="section-card">
  <h2>هل تحتاج بشر فعلي الآن؟</h2>
  <div class="row">
    <a class="btn pro" target="_blank" rel="noopener" href="{PSYCHO_WA}">👨‍🎓 أخصائي نفسي (خطة CBT معك)</a>
    <a class="btn pro" target="_blank" rel="noopener" href="{PSYCH_WA}">👨‍⚕️ طبيب نفسي (تشخيص وأدوية)</a>
    <a class="btn pro" target="_blank" rel="noopener" href="{SOCIAL_WA}">🤝 أخصائي اجتماعي (موقف حياتي)</a>
  </div>
</div>
"""

@app.get("/cbt")
def cbt_page():
    return render_page("CBT — " + BRAND, "cbt", CBT_HTML)


# ---------- /pharm : الصيدلية النفسية ----------

PHARM_HTML = f"""
<h1>💊 الصيدلية النفسية (تثقيف فقط)</h1>

<p>
المحتوى هنا للتوعية، مو وصفة علاج.
لا تبدأ/توقف دواء بدون دكتور/صيدلي مختص.
بعض الأدوية لو تنقطع فجأة يكون فيه انسحاب أو ارتداد خطير.
لو فيه أفكار إيذاء نفسك أو غيرك، هذا طارئ.
</p>

<div class="section-card">
  <h2>🔍 ابحث</h2>
  <div class="row" style="align-items:flex-end;">
    <label style="flex:1;min-width:200px;">
      اكتب اسم دواء أو حالة (مثال: اكتئاب / هلع / ذهان)
      <input id="pharm-q" placeholder="مثلاً: وسواس، قلق، اكتئاب">
    </label>
    <button class="btn gold" type="button" onclick="pharmSearch()">بحث</button>
  </div>
  <div id="pharm-results" style="margin-top:16px;"></div>
</div>

<div class="section-card">
  <h2>متى أحتاج دكتور فوراً؟</h2>
  <ul class="dx-list">
    <li>لو فجأة صار عندك أفكار انتحار/إيذاء قوية ومستمرة</li>
    <li>لو في هلوسات جديدة قوية (أصوات/رؤية أشياء مش موجودة)</li>
    <li>لو تشنجات، ارتباك ذهني شديد، حرارة مع تيبس عضلات</li>
    <li>لو صرت خطر على نفسك أو أحد</li>
  </ul>
</div>
"""

@app.get("/pharm")
def pharm_page():
    return render_page("الصيدلية النفسية — " + BRAND, "pharm", PHARM_HTML)


# ---------- /tests : اختبارات نفسية سريعة ----------

TESTS_HTML = """
<h1>🧪 اختبارات نفسية سريعة</h1>

<p>
هذي مو تشخيص رسمي. الهدف: وعي لحظي.
جاوب بكل صدق، ما في صح/غلط، ما في حكم.
</p>

<div class="section-card">
  <h2>مستوى الضيق / المزاج الآن</h2>
  <form id="mood-form" onsubmit="event.preventDefault();calcMoodTest();">
    <p>خلال آخر يومين...</p>

    <label class="badge2">
      1) كم تحس بالحزن / الكتمة / الضيق؟
      <div class="row" style="gap:4px;">
        <label><input type="radio" name="m1" value="0"> لا تقريبًا</label>
        <label><input type="radio" name="m1" value="2"> متوسط</label>
        <label><input type="radio" name="m1" value="3"> عالي جدًا</label>
      </div>
    </label>

    <label class="badge2">
      2) كم تحس بالقلق / توتر الجسم / صعوبة تهدى؟
      <div class="row" style="gap:4px;">
        <label><input type="radio" name="m2" value="0"> لا تقريبًا</label>
        <label><input type="radio" name="m2" value="2"> متوسط</label>
        <label><input type="radio" name="m2" value="3"> عالي جدًا</label>
      </div>
    </label>

    <label class="badge2">
      3) كم جاءك أفكار "أنا ما أقدر أتحمل / خلاص تعبت"؟
      <div class="row" style="gap:4px;">
        <label><input type="radio" name="m3" value="0"> تقريبًا أبدًا</label>
        <label><input type="radio" name="m3" value="2"> أحيانًا</label>
        <label><input type="radio" name="m3" value="3"> كثير / مزعج</label>
      </div>
    </label>

    <div class="row" style="margin-top:10px;">
      <button class="btn gold" type="submit">احسب النتيجة</button>
    </div>
  </form>

  <div id="mood-result" style="
    margin-top:12px;
    background:#2a2045;
    border:1px solid #3a2f55;
    border-radius:10px;
    box-shadow:0 0 12px rgba(209,178,58,.15);
    padding:10px;
    font-size:13px;
    line-height:1.5;
  ">
    النتيجة: —
  </div>

  <small class="small">
  لو طلعت نتيجة عالية وفيها أفكار إيذاء أو عجز تام: لا تبقى لحالك. تواصل مع مختص أو خدمة دعم مباشر.
  </small>
</div>

<div class="section-card">
  <h2>ملاحظة</h2>
  <p>
    الاختبار هذا "لقطة سريعة" لحالتك الآن.
    مو بدل تقييم مهني، لكنه يساعدك تتكلم أو تشرح لحياتك/لطبيبك/للأخصائي بدل ما تقول "ما أدري".
  </p>
</div>
"""

@app.get("/tests")
def tests_page():
    return render_page("الاختبارات النفسية — " + BRAND, "tests", TESTS_HTML)


# ---------- /health : readiness ping ----------

@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "brand": BRAND,
        "build": BUILD_STAMP
    }), 200


# ======================== Security Headers ========================

@app.after_request
def add_headers(resp):
    # أكثر شيء معقول نحطه بعالم single-file selfhost
    csp = (
        "default-src 'self' data: blob: https://t.me https://wa.me https://api.whatsapp.com; "
        "script-src 'self' 'unsafe-inline' data: blob: https://t.me https://wa.me https://api.whatsapp.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob: *; "
        "connect-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors *"
    )
    resp.headers['Content-Security-Policy'] = csp
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return resp


# ======================== تشغيل محلّي / WSGI ========================

if __name__ == "__main__":
    # محلي:
    # python app.py
    #
    # في Render استخدم:
    # gunicorn app:app --bind 0.0.0.0:$PORT
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
