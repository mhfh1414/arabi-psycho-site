# -*- coding: utf-8 -*-
# dsm.py — ملف واحد: تشغيل + واجهة رئيسية + DSM موسّع جدًا + دراسة حالة + نتيجة

from flask import Flask, render_template_string, request, redirect, url_for
import re
from collections import defaultdict

app = Flask(__name__)

# ============================= أدوات لغوية متقدمة =============================
_AR_DIAC  = r"[ًٌٍَُِّْـ]"
_AR_PUNCT = r"[.,،;؛!?؟()\[\]{}\"\'<>]"

def normalize(s: str) -> str:
    if not s: return ""
    s = s.strip()
    s = re.sub(_AR_DIAC, "", s)
    s = re.sub(_AR_PUNCT, " ", s)
    s = (s.replace("أ","ا").replace("إ","ا").replace("آ","ا")
           .replace("ة","ه").replace("ى","ي").replace("ؤ","و").replace("ئ","ي")
           .replace("ـ","").replace("ﻻ","لا").replace("ﻷ","لا"))
    s = re.sub(r"\s+", " ", s)
    return s.lower()

def tokenize(s: str):
    return normalize(s).split()

def calculate_similarity(text: str, phrase: str) -> float:
    t = set(tokenize(text)); p = set(tokenize(phrase))
    if not p: return 0.0
    return len(t & p)/len(p)

# ============================= مرادفات موسّعة =============================
SYNONYMS = {
    "حزن": ["زعل","غم","ضيقه","طفش","كآبه","تعاسه","نفسية سيئه"],
    "انعدام المتعة": ["فقدان المتعه","مافي متعه","لا استمتع","فقدان الاهتمام","ما عاد يفرحني شي"],
    "طاقة منخفضة": ["خمول","كسل","ارهاق","تعب","فقدان حافز","وهن"],
    "اضطراب نوم": ["قلة نوم","كثرة نوم","ارق","نوم متقطع","استيقاظ مبكر","كابوس"],
    "شهية منخفضة": ["قلة اكل","سدت نفسي","فقدان شهية"],
    "انسحاب اجتماعي": ["انعزال","انطواء","ما اطلع","ابتعاد عن الناس"],
    "تفكير انتحاري": ["افكار انتحار","تمني الموت","رغبة بالموت"],
    "قلق": ["توتر","توجس","خوف مستمر","على اعصابي","ترقب"],
    "نوبة هلع": ["هجوم هلع","خفقان","ضيقه تنفس","اختناق","ذعر"],
    "خوف الموت": ["حاس بموت","بموت","خايف اموت"],
    "وسواس": ["افكار متسلطه","افكار مزعجه","اقتحاميه","هواجس"],
    "سلوك قهري": ["طقوس","تفقد متكرر","عد قهري","غسل متكرر","تنظيم مفرط","ترتيب"],
    "حدث صادم": ["حادث شديد","اعتداء","كارثه","حرب","تجربة مؤلمة"],
    "استرجاع الحدث": ["فلاش باك","ذكريات مؤلمه","كوابيس"],
    "هلوسة": ["هلاوس سمعيه","هلاوس بصريه","اسمع اصوات","اشوف اشياء"],
    "اوهام": ["ضلالات","اعتقادات وهميه","شك مرضي","اضطهاد","عظمه"],
    "تشتت": ["عدم تركيز","سهو","شرود","نسيان"],
    "فرط حركة": ["نشاط زائد","اندفاع","مقاطعه","ملل سريع"],
    "تواصل اجتماعي ضعيف": ["صعوبه تواصل","نظره عيون ضعيفه","صعوبات علاقات"],
    "اهتمامات مقيدة": ["روتين صارم","تكرار حركات","حساسيات صوت/ضوء","سلوك نمطي"],
    "نهم": ["شراهه","اكل بكثره","نوبات اكل","ما اقدر اوقف اكل"],
    "تطهير": ["استفراغ متعمد","ملينات","صيام تعويضي"],
    "تعاطي": ["استخدام","ادمان","اعتماد","اسراف"],
    "انسحاب": ["رجفه","تعرق","ارق","قلق","رغبه ملحه"],
}

# ============================= قاعدة DSM موسّعة (قابلة للتوسيع) =============================
DSM_DB = {
    # نمائي/عصبي
    "اضطراب طيف التوحد": {
        "keywords": ["تواصل اجتماعي ضعيف","نظره عين ضعيفه","سلوك نمطي","روتين","حساسيات حسيه","اهتمامات مقيده","لغة متأخره","حركات نمطيه"],
        "required": ["تواصل اجتماعي ضعيف","سلوك نمطي"], "exclusions": [], "weight": 1.2,
        "prevalence": {"male":2.5,"female":1.0}, "onset_age":"الطفوله المبكره"
    },
    "اضطراب نقص الانتباه وفرط الحركة": {
        "keywords": ["تشتت","عدم تركيز","فرط حركة","اندفاع","نسيان","تنظيم ضعيف","مقاطعه","ملل سريع"],
        "required": ["تشتت","فرط حركة"], "exclusions": [], "weight": 1.1,
        "prevalence": {"male":2.0,"female":1.0}, "onset_age":"الطفوله"
    },
    "اضطرابات التعلّم النوعية": {
        "keywords": ["صعوبه قراءه","ديسلكسيا","صعوبه حساب","تهجئه ضعيفه","بطء تعلم","صعوبه كتابة"],
        "required": ["صعوبه قراءه"], "exclusions": [], "weight": 1.0,
        "prevalence": {"male":1.5,"female":1.0}, "onset_age":"الطفوله"
    },

    # ذهاني
    "فصام": {
        "keywords": ["هلوسة","اوهام","ضلالات","تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني","انعدام اراده","تدهور اداء"],
        "required": ["هلوسة","اوهام"], "exclusions": [], "weight": 1.8,
        "prevalence": {"male":1.4,"female":1.0}, "onset_age":"البلوغ المبكر"
    },
    "اضطراب فصامي عاطفي": {
        "keywords": ["اعراض ذهانيه","اكتئاب شديد","هوس","تذبذب مزاج"],
        "required": ["اعراض ذهانيه"], "exclusions": [], "weight": 1.6,
        "prevalence":{"male":1.0,"female":1.0}, "onset_age":"البلوغ"
    },
    "اضطراب وهامي": {
        "keywords": ["ضلالات ثابته","غيرة وهامية","اضطهاد","عظمة","شك مرضي"],
        "required": ["ضلالات ثابته"], "exclusions": [], "weight": 1.5,
        "prevalence":{"male":1.0,"female":1.5}, "onset_age":"منتصف العمر"
    },

    # مزاج
    "اضطراب اكتئابي جسيم": {
        "keywords": ["حزن","مزاج منخفض","انعدام المتعة","فقدان المتعة","تشاؤم","تفكير سلبي","بكاء","انسحاب اجتماعي",
                     "طاقة منخفضة","ارهاق","تعب","خمول","كسل","بطء نفسي حركي",
                     "اضطراب نوم","قلة نوم","كثرة نوم","ارق","نوم متقطع","استيقاظ مبكر",
                     "شهية منخفضة","قلة اكل","فقدان شهية","فقدان وزن","زيادة وزن",
                     "تركيز ضعيف","احتقار الذات","شعور بالذنب","يأس","تفكير انتحاري"],
        "required": ["حزن","انعدام المتعة"], "exclusions": [], "weight": 1.8,
        "prevalence":{"male":1.0,"female":2.0}, "onset_age":"أي عمر (ذروه بالعشرينات)"
    },
    "اكتئاب مستمر (عسر المزاج)": {
        "keywords": ["مزاج مكتئب مزمن","تشاؤم مزمن","طاقة قليلة","نوم ضعيف","شهية قليلة","ثقه منخفضه","انتاجية ضعيفه"],
        "required": ["مزاج مكتئب مزمن"], "exclusions": [], "weight": 1.5,
        "prevalence":{"male":1.0,"female":2.0}, "onset_age":"المراهقه/البلوغ المبكر"
    },
    "اضطراب ثنائي القطب": {
        "keywords": ["نوبة هوس","هوس","طاقة عالية","قليل نوم","اندفاع","تهور","افكار سباق","طلاقة الكلام","عظمة","نوبات اكتئاب","تذبذب المزاج"],
        "required": ["نوبة هوس"], "exclusions": [], "weight": 1.7,
        "prevalence":{"male":1.0,"female":1.0}, "onset_age":"البلوغ المبكر"
    },
    "اضطراب ما قبل الطمث المزعج": {
        "keywords": ["تقلب مزاج قبل الدوره","تهيج","حساسيه","انتفاخ","شهية","حزن قبل الحيض"],
        "required": ["تقلب مزاج قبل الدوره"], "exclusions": [], "weight":1.3,
        "prevalence":{"male":0.0,"female":1.0}, "onset_age":"سن الانجاب"
    },
    "اكتئاب ما حول الولادة": {
        "keywords": ["بعد الولاده","حزن ما بعد الولاده","بكاء","قلق طفل","نوم مضطرب"],
        "required": ["بعد الولاده"], "exclusions": [], "weight":1.4,
        "prevalence":{"male":0.0,"female":1.0}, "onset_age":"بعد الولاده"
    },

    # قلق/رهاب/هلع
    "اضطراب القلق العام": {
        "keywords": ["قلق","قلق مفرط","توتر","توجس","افكار سلبية","شد عضلي","صعوبة تركيز","قابلية استفزاز","ارق","تعب"],
        "required": ["قلق مفرط"], "exclusions": [], "weight":1.4,
        "prevalence":{"male":1.0,"female":2.0}, "onset_age":"المراهقه/البلوغ"
    },
    "اضطراب الهلع": {
        "keywords": ["نوبة هلع","خفقان","اختناق","ضيق نفس","تعرق","رجفه","دوار","خوف الموت","خوف فقدان السيطره","غثيان","خدر"],
        "required": ["نوبة هلع"], "exclusions": [], "weight":1.6,
        "prevalence":{"male":1.0,"female":2.5}, "onset_age":"البلوغ المبكر"
    },
    "رهاب اجتماعي": {
        "keywords": ["خوف اجتماعي","خوف التقييم","خجل شديد","تجنب اجتماعي","قلق اداء","احمرار","رجفه","رهبه مواجهه"],
        "required": ["خوف اجتماعي"], "exclusions": [], "weight":1.4,
        "prevalence":{"male":1.0,"female":1.5}, "onset_age":"المراهقه"
    },
    "رهاب الساحة": {
        "keywords": ["خوف من الاماكن المفتوحه","خوف من الازدحام","تجنب مواصلات","صعوبه الخروج وحيدا","رهبه اماكن عامه"],
        "required": ["خوف من الاماكن المفتوحه"], "exclusions": [], "weight":1.4,
        "prevalence":{"male":1.0,"female":2.0}, "onset_age":"المراهقه/البلوغ"
    },
    "رهاب محدد": {
        "keywords": ["خوف شديد","فوبيا","تجنب مواقف","خوف طيران","خوف حشرات","خوف المرتفعات","خوف الظلام","خوف حقن","خوف دم"],
        "required": ["خوف شديد"], "exclusions": [], "weight":1.3,
        "prevalence":{"male":1.0,"female":2.0}, "onset_age":"الطفوله"
    },

    # وسواس وما يرتبط به
    "اضطراب الوسواس القهري": {
        "keywords": ["وسواس","افكار اقتحاميه","سلوك قهري","طقوس","تفقد متكرر","غسل متكرر","تنظيم مفرط","عد قهري","خوف تلوث"],
        "required": ["وسواس","سلوك قهري"], "exclusions": [], "weight":1.7,
        "prevalence":{"male":1.0,"female":1.0}, "onset_age":"المراهقه/البلوغ المبكر"
    },
    "تشوه صورة الجسد": {
        "keywords": ["انشغال بالمظهر","عيوب متخيله","تفقد المرآه","تعديل مظهر مفرط"],
        "required": ["انشغال بالمظهر"], "exclusions": [], "weight":1.5,
        "prevalence":{"male":1.0,"female":1.5}, "onset_age":"المراهقه"
    },
    "اكتناز": {
        "keywords": ["اكتناز","صعوبة رمي","تكديس","فوضى منزل","رفض التخلص"],
        "required": ["اكتناز"], "exclusions": [], "weight":1.4,
        "prevalence":{"male":1.0,"female":1.5}, "onset_age":"المراهقه/البلوغ"
    },
    "نتف الشعر": {
        "keywords": ["شد شعر","سحب شعر","فراغات شعر","توتر ثم ارتياح"],
        "required": ["شد شعر"], "exclusions": [], "weight":1.4,
        "prevalence":{"male":1.0,"female":2.0}, "onset_age":"المراهقه"
    },
    "قشط الجلد": {
        "keywords": ["قشط جلد","خدش متكرر","جروح صغيرة","تقشير الجلد"],
        "required": ["قشط جلد"], "exclusions": [], "weight":1.3,
        "prevalence":{"male":1.0,"female":2.0}, "onset_age":"المراهقه"
    },

    # صدمة/ضغوط
    "اضطراب ما بعد الصدمة": {
        "keywords": ["حدث صادم","استرجاع الحدث","فلاش باك","كابوس","تجنب","خدر عاطفي","يقظه مفرطه","حساسيه صوت","ذنب الناجي"],
        "required": ["حدث صادم","استرجاع الحدث"], "exclusions": [], "weight":1.8,
        "prevalence":{"male":1.0,"female":2.0}, "onset_age":"أي عمر"
    },
    "اضطراب كرب حاد": {
        "keywords": ["اعراض صدمة قصيرة","خلال اسابيع","قلق عالي","تجنب","يقظه"],
        "required": ["اعراض صدمة قصيرة"], "exclusions": [], "weight":1.5,
        "prevalence":{"male":1.0,"female":1.5}, "onset_age":"أي عمر"
    },
    "اضطراب تكيف": {
        "keywords": ["توتر موقف","حزن بعد حدث","قلق ظرفي","تراجع اداء بعد ضغط","مشاكل عمل","مشاكل دراسة"],
        "required": ["توتر موقف"], "exclusions": [], "weight":1.3,
        "prevalence":{"male":1.0,"female":1.5}, "onset_age":"أي عمر"
    },

    # أعراض جسدية/قلق المرض
    "اعراض جسدية": {
        "keywords": ["الم غير مفسر","اعراض جسدية متعدده","انشغال صحي","زياره اطباء كثيره"],
        "required": ["الم غير مفسر"], "exclusions": [], "weight":1.5,
        "prevalence":{"male":1.0,"female":2.0}, "onset_age":"المراهقه/البلوغ"
    },
    "قلق المرض": {
        "keywords": ["خوف مرض خطير","تفقد جسد","طمأنه متكرره","بحث طبي مستمر","توهم المرض"],
        "required": ["خوف مرض خطير"], "exclusions": [], "weight":1.5,
        "prevalence":{"male":1.0,"female":1.0}, "onset_age":"البلوغ"
    },
    "اضطراب تحولي": {
        "keywords": ["اعراض عصبية بدون سبب عضوي","شلل وظيفي","نوبات غير صرعية","فقدان احساس"],
        "required": ["اعراض عصبية بدون سبب عضوي"], "exclusions": [], "weight":1.5,
        "prevalence":{"male":1.0,"female":2.0}, "onset_age":"المراهقه/البلوغ"
    },

    # أكل
    "قهم عصبي": {
        "keywords": ["نقص وزن شديد","خوف من زياده الوزن","صورة جسد سلبيه","تقييد طعام"],
        "required": ["نقص وزن شديد","خوف من زياده الوزن"], "exclusions": [], "weight":1.7,
        "prevalence":{"male":1.0,"female":10.0}, "onset_age":"المراهقه"
    },
    "نهام عصبي": {
        "keywords": ["نهم متكرر","تطهير","استفراغ","ملينات","ذنب بعد الاكل"],
        "required": ["نهم متكرر","تطهير"], "exclusions": [], "weight":1.6,
        "prevalence":{"male":1.0,"female":3.0}, "onset_age":"المراهقه/البلوغ المبكر"
    },
    "اضطراب نهم الطعام": {
        "keywords": ["نهم","اكل بشراهه","فقدان تحكم","اكل سرا","زيادة وزن"],
        "required": ["نهم","فقدان تحكم"], "exclusions": [], "weight":1.5,
        "prevalence":{"male":1.0,"female":1.5}, "onset_age":"البلوغ"
    },

    # نوم/يقظة
    "أرق مزمن": {
        "keywords": ["صعوبه نوم","استيقاظ مبكر","نوم متقطع","عدم راحه","اجهاد نهاري","تفكير ليلي"],
        "required": ["صعوبه نوم"], "exclusions": [], "weight":1.4,
        "prevalence":{"male":1.0,"female":1.5}, "onset_age":"البلوغ"
    },
    "فرط نعاس/ناركوليبسي": {
        "keywords": ["نعاس نهاري","غفوات مفاجئة","شلل نوم","هلوسات نعاس"],
        "required": ["نعاس نهاري"], "exclusions": [], "weight":1.3,
        "prevalence":{"male":1.0,"female":1.5}, "onset_age":"المراهقه/البلوغ"
    },
    "انقطاع نفس اثناء النوم": {
        "keywords": ["شخير","توقف تنفس","اختناق ليلي","نعاس نهاري"],
        "required": ["شخير","توقف تنفس"], "exclusions": [], "weight":1.3,
        "prevalence":{"male":2.0,"female":1.0}, "onset_age":"البلوغ"
    },

    # إدمان
    "اضطراب تعاطي الكحول": {
        "keywords": ["كحول","سكر متكرر","تحمل","اعراض انسحاب","فقدان سيطرة","مشاكل عمل","مشاكل علاقات"],
        "required": ["كحول"], "exclusions": [], "weight":1.6,
        "prevalence":{"male":2.0,"female":1.0}, "onset_age":"البلوغ"
    },
    "اضطراب تعاطي القنب": {
        "keywords": ["حشيش","قنب","استخدام يومي","تسامح","انسحاب","قلق بعد الايقاف","ذهان مرتبط بالقنب"],
        "required": ["حشيش","قنب"], "exclusions": [], "weight":1.4,
        "prevalence":{"male":2.0,"female":1.0}, "onset_age":"المراهقه/البلوغ"
    },
    "اضطراب تعاطي المنبهات": {
        "keywords": ["منشطات","امفيتامين","كوكايين","سهر","فقدان شهيه","بارانويا","استخدام قهري"],
        "required": ["منشطات"], "exclusions": [], "weight":1.6,
        "prevalence":{"male":2.0,"female":1.0}, "onset_age":"البلوغ"
    },
    "اضطراب تعاطي الأفيونات": {
        "keywords": ["هيروين","مورفين","اوكسيدودون","انسحاب افيوتي","رغبه ملحه","تحمل"],
        "required": ["هيروين","مورفين","اوكسيدودون"], "exclusions": [], "weight":1.7,
        "prevalence":{"male":2.0,"female":1.0}, "onset_age":"البلوغ"
    },

    # معرفي/خرف
    "اضطراب معرفي خفيف": {
        "keywords": ["نسيان جديد","بطء معالجه","تراجع تنفيذي","ضياع اشياء","تشتت"],
        "required": ["نسيان جديد"], "exclusions": [], "weight":1.3,
        "prevalence":{"male":1.0,"female":1.0}, "onset_age":"منتصف العمر/كبار السن"
    },
    "خرف مبكر/متوسط": {
        "keywords": ["تدهور ذاكره","ارتباك","تيه","تراجع اداء يومي","تغير شخصيه"],
        "required": ["تدهور ذاكره"], "exclusions": [], "weight":1.6,
        "prevalence":{"male":1.0,"female":1.0}, "onset_age":"الكهوله"
    },

    # الشخصية
    "شخصية حدّية": {
        "keywords": ["اندفاع","تقلب عاطفي","خوف هجر","ايذاء ذاتي","فراغ مزمن","علاقات غير مستقرة","غضب شديد"],
        "required": ["تقلب عاطفي"], "exclusions": [], "weight":1.4,
        "prevalence":{"male":1.0,"female":1.5}, "onset_age":"البدايات الرشيده"
    },
    "شخصية نرجسية": {
        "keywords": ["عظمه","حاجه اعجاب","تعاطف قليل","استغلالي","حساس للنقد"],
        "required": ["عظمه"], "exclusions": [], "weight":1.2,
        "prevalence":{"male":1.5,"female":1.0}, "onset_age":"البلوغ"
    },
    "شخصية وسواسيه قهريه": {
        "keywords": ["انشغال بالتفاصيل","كماليه","صرامه","عناد","قواعد","قائمة مهام لا تنتهي"],
        "required": ["انشغال بالتفاصيل"], "exclusions": [], "weight":1.2,
        "prevalence":{"male":1.2,"female":1.0}, "onset_age":"البلوغ"
    }
}

# ============================= تهيئة للقاموس =============================
def _precompute_dsm():
    prepared = {}
    for dx, meta in DSM_DB.items():
        kws = meta.get("keywords", [])
        prepared[dx] = {
            "keywords_raw": kws,
            "keywords_norm": [normalize(k) for k in kws],
            "required_norm": [normalize(k) for k in meta.get("required", [])],
            "exclusions_norm": [normalize(k) for k in meta.get("exclusions", [])],
            "weight": float(meta.get("weight", 1.0)),
            "prev": meta.get("prevalence", {"male":1.0,"female":1.0}),
            "onset_age": meta.get("onset_age","أي عمر")
        }
    return prepared

_DSM_PREP = _precompute_dsm()

def _gender_key(gender: str) -> str:
    g = normalize(gender)
    if "انثى" in g or "female" in g or g == "f": return "female"
    return "male"

def _age_factor(age_str: str, onset_age: str) -> float:
    try: age = int(age_str)
    except: return 1.0
    o = normalize(onset_age)
    if "طفول" in o and age <= 12: return 1.1
    if ("مراهق" in o) and (12 <= age <= 19): return 1.1
    if ("بلوغ" in o) and (18 <= age <= 30): return 1.08
    if ("منتصف" in o) and (35 <= age <= 55): return 1.08
    if ("كهل" in o or "كهوله" in o) and (age >= 60): return 1.1
    return 1.0

def _duration_boost(days: str) -> float:
    try: d = float(days)
    except: return 1.0
    if d >= 365: return 1.25
    if d >= 90:  return 1.15
    if d >= 30:  return 1.08
    return 1.0

def _impairment_boost(h: str) -> float:
    if not h: return 1.0
    t = normalize(h)
    keys = ["مشاكل عمل","فصل","انذار","مشاكل زواج","طلاق","خلافات","قضيه","مشاكل ماليه","تعثر دراسي","غياب متكرر"]
    return 1.1 if any(normalize(k) in t for k in keys) else 1.0

# ============================= محرك التشخيص =============================
def score_diagnoses(symptoms_text: str, age: str="", gender: str="", duration_days: str="", history: str=""):
    text_norm = normalize(symptoms_text or "")
    for base, syns in SYNONYMS.items():
        if any(normalize(w) in text_norm for w in [base] + syns):
            text_norm += " " + " ".join(set(normalize(s) for s in ([base] + syns)))

    gkey = _gender_key(gender)
    durB = _duration_boost(duration_days)
    impB = _impairment_boost(history)

    out = []
    for dx, meta in _DSM_PREP.items():
        if any(ex in text_norm for ex in meta["exclusions_norm"]):
            continue
        req = meta["required_norm"]
        if req and not all((r in text_norm) or (calculate_similarity(text_norm, r) >= 0.6) for r in req):
            continue

        score = 0.0
        hits = []
        for raw_kw, kw in zip(meta["keywords_raw"], meta["keywords_norm"]):
            if kw in text_norm:
                w = 1.0
                if kw in (normalize("تفكير انتحاري"), normalize("نوبة هلع"),
                          normalize("هلوسة"), normalize("اوهام"), normalize("ضلالات")):
                    w = 1.8
                score += w; hits.append(raw_kw)
            else:
                sim = calculate_similarity(text_norm, kw)
                if sim >= 0.66:
                    score += 0.8; hits.append(raw_kw + "~")
                elif sim >= 0.4:
                    score += 0.4

        if score <= 0: 
            continue

        score *= meta["weight"]
        score *= (meta["prev"].get(gkey, 1.0) or 1.0)
        score *= _age_factor(age, meta["onset_age"])
        score *= durB
        score *= impB

        out.append({"name": dx, "score": round(score, 2), "hits": hits[:12]})

    if not out:
        return [], {"suggestion": "أضف كلمات أدق عن الأعراض/المدة/الأثر الوظيفي (مثال: وسواس، نهم، نوبة هلع، هلوسة، رهاب، أرق).", "buckets": []}

    out.sort(key=lambda x: x["score"], reverse=True)
    return out[:5], None

# ============================= واجهة رئيسية =============================
HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | الرئيسية</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400;--white:#fff}
    *{box-sizing:border-box}
    body{margin:0;font-family:"Tajawal",system-ui;background:
      radial-gradient(1000px 520px at 85% -10%, #1a4bbd22, transparent),
      linear-gradient(135deg,var(--bg1),var(--bg2)); color:var(--white)}
    .wrap{max-width:1240px;margin:auto;padding:28px 20px}
    header{display:flex;align-items:center;justify-content:space-between;gap:16px}
    .brand{display:flex;align-items:center;gap:14px}
    .badge{width:56px;height:56px;border-radius:16px;background:#0d2c54;border:1px solid #ffffff33;display:grid;place-items:center;font-weight:800;box-shadow:0 8px 24px rgba(0,0,0,.25)}
    .title{margin:0;font-size:32px}
    .subtitle{margin:.25rem 0 0;color:#cfe0ff}
    .actions{display:flex;gap:10px}
    .iconbtn{display:inline-flex;align-items:center;gap:8px;text-decoration:none;color:#fff;padding:10px 12px;border-radius:12px;border:1px solid #ffffff22;background:rgba(255,255,255,.08)}
    .iconbtn:hover{background:rgba(255,255,255,.14)}
    .ico{width:18px;height:18px}
    .hero{margin:22px 0 26px;padding:22px;background:rgba(255,255,255,.06);border:1px solid #ffffff22;border-radius:18px}
    .btn{display:inline-flex;align-items:center;gap:10px;text-decoration:none;font-weight:800;background:linear-gradient(180deg,#ffd86a,#f4b400);color:#2b1b02;padding:14px 18px;border-radius:14px;box-shadow:0 6px 18px rgba(244,180,0,.28)}
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
    @media(max-width:980px){.grid{grid-template-columns:1fr}}
    .card{background:rgba(255,255,255,.08);border:1px solid #ffffff22;border-radius:16px;padding:18px}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="brand" style="text-align:right">
        <div class="badge">AS</div>
        <div>
          <h1 class="title">عربي سايكو</h1>
          <p class="subtitle">مركز عربي سايكو يرحّب بكم — نخدمك أينما كنت</p>
        </div>
      </div>
      <nav class="actions">
        <a class="iconbtn" href="{{ url_for('contact_whatsapp') }}" title="واتساب">
          <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M20 3.9A10 10 0 0 0 3.5 17.4L3 21l3.7-.9A10 10 0 1 0 20 3.9ZM12 21a8.4 8.4 0 0 1-4.3-1.2l-.3-.2-2.5.6.5-2.4-.2-.3A8.5 8.5 0 1 1 12 21Zm4.7-6.3-.6-.3c-.3-.1-1.8-.9-2-.9s-.5-.1-.7.3-.8.9-.9 1-.3.2-.6.1a7 7 0 0 1-2-1.2 7.4 7.4 0 0 1-1.4-1.7c-.1-.2 0-.4.2-.5l.5-.6.2-.3v-.3l-.1-.3-1-2c-.2-.6-.5-.5-.7-.5h-.6l-.3.1a1.4 1.4 0 0 0-.4 1.1 4.9 4.9 0 0 0 1 2.4 11.2 11.2 0 0 0 4.3 4 4.8 4.8 0 0 0 2.8.9c.6 0 1.2 0 1.7-.3a3.8 3.8 0 0 0 1.3-1 .9.9 0 0 0 .2-1c-.1-.2-.5-.3-.8-.5Z"/></svg>
          <span>واتساب</span>
        </a>
        <a class="iconbtn" href="{{ url_for('contact_telegram') }}" title="تلجرام">
          <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M9.1 16.3 8.9 20c.4 0 .6-.2.9-.4l2.1-2 4.3 3.1c.8.5 1.4.3 1.6-.8l2.9-13.4c.3-1.2-.4-1.7-1.2-1.4L2.8 9.7c-1.1.4-1.1 1.1-.2 1.4l4.3 1.3 10-6.3c.5-.3.9-.1.5.2l-8.1 7Z"/></svg>
          <span>تلجرام</span>
        </a>
        <a class="iconbtn" href="{{ url_for('contact_email') }}" title="إيميل">
          <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5v2Z"/></svg>
          <span>إيميل</span>
        </a>
      </nav>
    </header>

    <section class="hero">
      <a class="btn" href="{{ url_for('dsm') }}">🗂️ دراسة الحالة + التشخيص (DSM)</a>
    </section>

    <section class="grid">
      <div class="card">
        <h3>📖 DSM-5</h3>
        <p>قاعدة اضطرابات موسّعة + مطابقة كلمات (صارمة + ناعمة) لنتيجة تقديرية فورية.</p>
        <a class="btn" href="{{ url_for('dsm') }}">ابدأ الآن</a>
      </div>
      <div class="card">
        <h3>🧪 الاختبارات + CBT</h3>
        <p>سنربطه لاحقًا بلوحة اختبارات PHQ-9 وGAD-7 وغيرها.</p>
        <a class="btn" href="{{ url_for('dsm') }}">(مؤقتًا) ادخل DSM</a>
      </div>
      <div class="card">
        <h3>🚭 علاج الإدمان</h3>
        <p>تقييم أولي وخطط علاج وإحالة عند الحاجة.</p>
        <a class="btn" href="{{ url_for('dsm') }}">(مؤقتًا) ادخل DSM</a>
      </div>
    </section>
  </div>
</body>
</html>
"""

# ============================= صفحة DSM (GET/POST) =============================
DSM_PAGE_BASE = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>DSM-5 | دراسة حالة وتشخيص</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{--bg1:#0b3a75;--bg2:#0a65b0;--gold:#f4b400}
    *{box-sizing:border-box}
    body{font-family:"Tajawal",system-ui;background:linear-gradient(135deg,var(--bg1),var(--bg2)) fixed;color:#fff;margin:0}
    .wrap{max-width:1180px;margin:28px auto;padding:16px}
    .bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
    .card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:18px}
    a.btn,button.btn{display:inline-block;background:var(--gold);color:#2b1b02;border-radius:14px;padding:12px 16px;text-decoration:none;font-weight:800;border:none;cursor:pointer}
    label{display:block;color:#ffe28a;margin:8px 2px 6px}
    input,select,textarea{width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.12);color:#fff;padding:12px 14px}
    textarea{min-height:130px;resize:vertical}
    .grid{display:grid;grid-template-columns:1.1fr .9fr;gap:16px}
    @media(max-width:1000px){.grid{grid-template-columns:1fr}}
    .result{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px}
    .badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:.85rem;margin:4px 0}
    .ok{background:#16a34a;color:#fff}
    .warn{background:#ef4444;color:#fff}
    table{width:100%;border-collapse:collapse;margin-top:8px}
    th,td{border-bottom:1px solid rgba(255,255,255,.15);padding:8px 6px;text-align:right}
    th{color:#ffe28a}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="bar">
      <h2 style="margin:0">🗂️ دراسة حالة + تشخيص (DSM-5)</h2>
      <a class="btn" href="{{ url_for('home') }}">الواجهة</a>
    </div>
    {{ body|safe }}
  </div>
</body>
</html>
"""

def render_dsm_get():
    body = """
    <div class="grid">
      <section class="card">
        <form method="post">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label>الاسم الكامل</label><input name="name" placeholder="مثال: مشرف العنزي"></div>
            <div><label>العمر</label><input name="age" placeholder="30"></div>
            <div><label>الجنس</label>
              <select name="gender"><option value="">— اختر —</option><option>ذكر</option><option>أنثى</option></select>
            </div>
            <div><label>مدة الأعراض (بالأيام)</label><input name="duration" placeholder="مثال: 90"></div>
          </div>
          <label>الأعراض (اذكر كلمات دقيقة + عامية إن وجدت)</label>
          <textarea name="symptoms" placeholder="مثال: حزن شديد، خمول، قلة نوم، فقدان شهية، انسحاب عن الناس..."></textarea>
          <label>التاريخ الطبي/الأثر الوظيفي (اختياري)</label>
          <textarea name="history" placeholder="أدوية، جلسات، مشاكل عمل/دراسة أو علاقات..."></textarea>
          <div style="margin-top:10px"><button class="btn" type="submit">تشخيص مبدئي</button></div>
        </form>
      </section>
      <aside class="result"><span class="badge warn">لا توجد نتيجة بعد</span><p>املأ الأعراض بدقة. سنعرض أفضل 5 دائمًا.</p></aside>
    </div>
    """
    return render_template_string(DSM_PAGE_BASE, body=body)

def render_dsm_post(form):
    name     = (form.get("name","") or "").strip()
    age      = (form.get("age","") or "").strip()
    gender   = (form.get("gender","") or "").strip()
    duration = (form.get("duration","") or "").strip()
    symptoms = (form.get("symptoms","") or "").strip()
    history  = (form.get("history","") or "").strip()

    details, fallback = score_diagnoses(symptoms, age=age, gender=gender, duration_days=duration, history=history)

    if fallback is not None:
        res = f"""
        <div class="result">
          <h3>📋 النتيجة</h3>
          <p><span class="badge warn">لا تطابقات مباشرة كافية</span> — زد مفردات مثل: وسواس/نهم/هلع/هلوسة/رهاب/أرق…</p>
          {"<p><strong>تلميحات:</strong> " + ", ".join(fallback.get("buckets", [])) + "</p>" if fallback.get("buckets") else ""}
          <p>اذكر <strong>المدة</strong> بدقّة، ووجود <strong>أثر وظيفي</strong> (عمل/دراسة/علاقات) وأي <strong>أدوية</strong>.</p>
        </div>
        """
    else:
        rows = [f"<tr><td>{d['name']}</td><td>{d['score']}</td><td>{', '.join(d['hits'])}</td></tr>" for d in details]
        table = "<table><thead><tr><th>التشخيص المقترح</th><th>الدرجة</th><th>أسباب/مطابقات</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
        res = f"""
        <div class="result">
          <h3>📋 أقرب التشخيصات (أفضل 5)</h3>
          {table}
          <p style="opacity:.85;margin-top:8px">⚠️ نتيجة تقديرية للمساعدة وليست تشخيصًا نهائيًا.</p>
        </div>
        """

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
          <label>الأعراض</label>
          <textarea name="symptoms">{symptoms}</textarea>
          <label>التاريخ الطبي/الأثر الوظيفي</label>
          <textarea name="history">{history}</textarea>
          <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap">
            <button class="btn" type="submit">إعادة التشخيص</button>
            <a class="btn" href="{{{{ url_for('home') }}}}">الواجهة</a>
          </div>
        </form>
      </section>
      {res}
    </div>
    """
    return render_template_string(DSM_PAGE_BASE, body=body)

# ============================= المسارات =============================
@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/dsm", methods=["GET","POST"])
def dsm():
    if request.method == "POST":
        return render_dsm_post(request.form)
    return render_dsm_get()

# روابط تواصل (تحويل)
@app.route("/contact/whatsapp")
def contact_whatsapp():
    return redirect("https://wa.me/9665XXXXXXXX", code=302)

@app.route("/contact/telegram")
def contact_telegram():
    return redirect("https://t.me/USERNAME", code=302)

@app.route("/contact/email")
def contact_email():
    return redirect("mailto:info@arabipsycho.com", code=302)

# ============================= تشغيل =============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
