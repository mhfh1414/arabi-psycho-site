# -*- coding: utf-8 -*-
# site_app.py — ملف واحد: واجهة + DSM موسّع جدًا + دراسة حالة + نتيجة

from flask import Flask, request, render_template_string, redirect, url_for
import re
from collections import defaultdict

app = Flask(__name__)

# ============================= أدوات لغوية =============================
_AR_DIAC = r"[ًٌٍَُِّْـ]"
def normalize(s: str) -> str:
    if not s: return ""
    s = s.strip()
    s = re.sub(_AR_DIAC, "", s)
    s = (s.replace("أ","ا").replace("إ","ا").replace("آ","ا")
           .replace("ة","ه").replace("ى","ي").replace("ؤ","و").replace("ئ","ي"))
    s = re.sub(r"(.)\1{2,}", r"\1\1", s)
    s = re.sub(r"\s+", " ", s)
    return s

def tokenize(s: str):
    s = normalize(s)
    s = re.sub(r"[^\w\s\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.split()

def contains_phrase(text_norm: str, phrase: str) -> bool:
    return normalize(phrase) in text_norm

# ============================= مرادفات (تعزيز) =============================
SYNONYMS = {
    # مزاج/اكتئاب
    "حزن": ["زعل","كدر","طفش","غم","ضيقه","هم","اكتئاب","نكد","نفسية سيئة"],
    "انعدام المتعة": ["فقدان المتعه","مافي متعه","عدم استمتاع","لا استمتع","ما عاد يفرحني شي"],
    "طاقة منخفضة": ["خمول","كسل","ارهاق","تعب","مافي طاقه","فقدان حافز"],
    "اضطراب نوم": ["قلة نوم","كثرة نوم","ارق","نوم متقطع","استيقاظ مبكر","كابوس","تقلّب نوم"],
    "شهية منخفضة": ["قلة اكل","ما اقدر اكل","فقدان شهية","سدت نفسي"],
    "زيادة وزن": ["سمنت","سمنه","وزني زاد","شهية مفتوحة"],

    # قلق/هلع
    "قلق": ["توتر","توجس","خوف مستمر","على اعصابي","قلق عام","قلق زائد"],
    "نوبة هلع": ["هجوم هلع","تسارع قلب","خفقان","ضيقه تنفس","اختناق","دوخه"],
    "خوف الموت": ["حاس بموت","بموت","خايف اموت","خوف فقدان السيطره"],

    # وسواس قهري
    "وسواس": ["افكار مزعجه","افكار متسلطه","ملحاحه","اقتحاميه"],
    "سلوك قهري": ["طقوس","تكرار غسيل","تفقد مكرر","عد قهري","تنظيف شديد","ترتيب مفرط"],
    "خوف تلوث": ["قذاره","وساوس نظافه","جراثيم"],

    # صدمة/ضغوط
    "حدث صادم": ["حادث شديد","اعتداء","حرب","كارثه","فقد شخص","مشاهدة عنف"],
    "استرجاع الحدث": ["فلاش باك","ذكريات مؤلمه","كوابيس","حساسيه صوت"],

    # ذهان
    "هلوسة": ["اسمع اصوات","اشوف اشياء","هلاوس سمعيه","هلاوس بصريه","هلاوس شميه"],
    "اوهام": ["ضلالات","افكار غير واقعيه","شك مرضي","اضطهاد","غيرة وهاميه","عظمه"],

    # ADHD
    "تشتت": ["عدم تركيز","سهو","نسيان","ما اركز","شرود"],
    "فرط حركة": ["كثرة حركه","اندفاع","مقاطعه","ملل سريع","قلق حركي"],

    # توحد
    "تواصل اجتماعي ضعيف": ["صعوبه تواصل","نظره عيون ضعيفه","علاقات محدوده","صعوبات علاقات"],
    "اهتمامات مقيدة": ["روتين صارم","تكرار حركات","حساسيات صوت/ضوء","سلوك نمطي"],

    # أكل/نوم
    "نهم": ["شراهه","اكل بكثره","نوبات اكل","ما اقدر اوقف اكل"],
    "تطهير": ["ترجيع متعمد","استفراغ بعد الاكل","ملينات","صيام تعويضي"],

    # ادمان
    "تعاطي": ["استخدام","ادمان","اعتماد","شراهه استخدام","اسراف"],
    "انسحاب": ["رجفه","تعرق","ارق","قلق","دوخه","رغبه ملحه"],
}

def expand_with_synonyms(text: str) -> str:
    text_norm = normalize(text)
    extra = []
    for base, syns in SYNONYMS.items():
        if any(normalize(s) in text_norm for s in [base] + syns):
            extra.extend([base] + syns)
    if extra:
        text_norm += " " + " ".join(set(normalize(w) for w in extra))
    return text_norm

# ============================= DSM موسّع جدًا =============================
# تم تكبير القاعدة بشكل كبير. أضفنا فئات DSM-5 مع مفردات غزيرة (طبية + عامية).
DSM_DB = {
    # --- نمائي/عصبي ---
    "اضطراب طيف التوحد": ["تواصل اجتماعي ضعيف","نظره عين ضعيفه","سلوك نمطي","روتين","حساسيات حسيه","اهتمامات مقيده","لغة متأخره","قله تواصل بصري","حركات نمطيه","تأخر نمائي"],
    "اضطراب نقص الانتباه وفرط الحركة": ["تشتت","عدم تركيز","فرط حركة","اندفاع","نسيان","تأجيل","تنظيم ضعيف","كثرة حركة","مقاطعه","ملل سريع","سهو","شرود"],
    "اضطرابات التعلّم النوعية": ["صعوبه قراءه","ديسلكسيا","صعوبه حساب","تهجئه ضعيفه","بطء تعلم"],
    "اضطرابات التشنجات/العرات": ["عرات","حركات لا إراديه","اصوات لا إراديه","تفريغ توتر","توريت"],

    # --- ذهاني ---
    "فصام": ["هلوسة","هلاوس سمعيه","هلاوس بصريه","اوهام","ضلالات","تفكير غير منظم","انسحاب اجتماعي","تسطح وجداني","انعدام اراده","تدهور اداء"],
    "اضطراب فصامي عاطفي": ["اعراض ذهانيه","اكتئاب شديد","هوس","تذبذب مزاج"],
    "اضطراب وهامي": ["ضلالات ثابته","غيرة وهامية","اضطهاد","عظمة","شك مرضي"],

    # --- مزاج ---
    "اضطراب اكتئابي جسيم": [
        "حزن","مزاج منخفض","انعدام المتعة","فقدان المتعة","تشاؤم","تفكير سلبي","بكاء","انسحاب اجتماعي",
        "طاقة منخفضة","ارهاق","تعب","خمول","كسل","بطء نفسي حركي",
        "اضطراب نوم","قلة نوم","كثرة نوم","ارق","نوم متقطع","استيقاظ مبكر",
        "شهية منخفضة","قلة اكل","فقدان شهية","فقدان وزن","زيادة وزن",
        "تركيز ضعيف","احتقار الذات","شعور بالذنب","يأس","افكار انتحارية","انتحار","فقدان حافز"
    ],
    "اكتئاب مستمر (عسر المزاج)": ["مزاج مكتئب مزمن","تشاؤم مزمن","طاقة قليلة","نوم ضعيف","شهية قليلة","ثقة منخفضة","انتاجية ضعيفه","احباط مزمن"],
    "اضطراب ثنائي القطب": ["نوبة هوس","هوس","نشاط زائد","طاقة عالية","قليل نوم","اندفاع","تهور","افكار سباق","طلاقة الكلام","عظمة","نوبات اكتئاب","تذبذب المزاج","تقلب شديد"],
    "اضطراب ما قبل الطمث المزعج": ["تقلب مزاج قبل الدوره","تهيج","حساسيه","انتفاخ","شهية","غضب","حزن قبل الحيض"],
    "اكتئاب ما حول الولادة": ["بعد الولاده","حزن ما بعد الولاده","بكاء","قلق طفل","نوم مضطرب"],

    # --- قلق/رهاب/هلع ---
    "اضطراب القلق العام": ["قلق","قلق مفرط","توتر","توجس","افكار سلبية","شد عضلي","صعوبة تركيز","قابلية استفزاز","ارق","تعب","وساوس قلق"],
    "اضطراب الهلع": ["نوبة هلع","خفقان","اختناق","ضيق نفس","تعرق","رجفة","دوار","خوف الموت","خوف فقدان السيطرة","غثيان","خدر","ارتعاش","خوف مكان نوبه"],
    "رهاب الساحة": ["خوف من الاماكن المفتوحه","خوف من الازدحام","تجنب مواصلات","صعوبه الخروج وحيدا","تجنب اسواق","رهبه اماكن عامة"],
    "رهاب اجتماعي": ["خوف اجتماعي","خوف التقييم","خجل شديد","تجنب اجتماعي","قلق اداء","احمرار","رجفه","رهبه مواجهه","خوف كلام امام ناس"],
    "رهاب محدد": ["خوف شديد","تجنب مواقف","خوف طيران","خوف حشرات","خوف المرتفعات","خوف الظلام","خوف حقن","خوف دم"],
    "قلق انفصالي (بالغ)": ["قلق انفصال","صعوبة ابتعاد","كابوس فقد","اعراض جسدية عند الفراق"],
    "خرس اختياري": ["سكوت انتقائي","لا يتكلم بمواقف اجتماعية","قلق كلام"],

    # --- وسواس وما يرتبط به ---
    "اضطراب الوسواس القهري": ["وسواس","افكار اقتحاميه","سلوك قهري","طقوس","تفقد متكرر","غسل متكرر","تنظيم مفرط","عد قهري","خوف تلوث","صلوات قهرية","تحقق الاقفال"],
    "تشوه صورة الجسد": ["انشغال بالمظهر","عيوب متخيله","تفقد المرآه","تعديل مظهر مفرط","جلد غير متساو"],
    "اكتناز": ["اكتناز","صعوبة رمي","تكديس","فوضى منزل","رفض التخلص"],
    "نتف الشعر": ["شد شعر","سحب شعر","فراغات شعر","توتر ثم ارتياح"],
    "قشط الجلد": ["قشط جلد","خدش متكرر","جروح صغيرة","حفر"],

    # --- صدمة/ضغوط ---
    "اضطراب ما بعد الصدمة": ["حدث صادم","استرجاع الحدث","فلاش باك","كابوس","تجنب","خدر عاطفي","يقظه مفرطه","حساسيه صوت","فرط يقظه","ذنب الناجي"],
    "اضطراب كرب حاد": ["اعراض صدمة قصيرة","خلال اسابيع","قلق عالي","تجنب","يقظه"],
    "اضطراب تكيف": ["توتر موقف","حزن بعد حدث","قلق ظرفي","تراجع اداء بعد ضغط","مشاكل عمل","مشاكل دراسة"],

    # --- انفصامية ---
    "اضطراب الهوية الانفصامي": ["هويات متعددة","فقدان ذاكرة فواصل","ضياع وقت","اصوات داخليه"],
    "تبدد الشخصية/الواقع": ["شعور باللاتواقعية","انفصال عن الذات","غربة الواقع","ضبابية"],
    "فقدان ذاكرة انفصالي": ["نوبات نسيان احداث صادمة","ثقوب ذاكرة","نسيان اسماء/اماكن"],

    # --- أعراض جسدية/قلق المرض ---
    "اعراض جسدية": ["الم غير مفسر","اعراض جسدية متعدده","انشغال صحي","زياره اطباء كثيره","رحلات طبية"],
    "قلق المرض": ["خوف مرض خطير","تفقد جسد","طمأنه متكرره","بحث طبي مستمر","قراءة امراض بكثرة"],
    "اضطراب تحولي": ["اعراض عصبية بدون سبب عضوي","شلل وظيفي","نوبات غير صرعية","فقدان احساس"],

    # --- أكل ---
    "قهم عصبي": ["نقص وزن شديد","خوف من زياده الوزن","صورة جسد سلبيه","تقييد طعام","حساب سعرات"],
    "نهام عصبي": ["نهم متكرر","تطهير","استفراغ","ملينات","ذنب بعد الاكل","نوبات اكل"],
    "اضطراب نهم الطعام": ["نهم","اكل بشراهه","فقدان تحكم","اكل سرا","زيادة وزن","اختباء اكل"],
    "اضطراب تجنّبي/مقيّد": ["انتقائيه طعام","تجنب قوام/روائح","نقص تغذيه","قلق من الاختناق"],

    # --- نوم ويقظة ---
    "أرق مزمن": ["صعوبه نوم","استيقاظ مبكر","نوم متقطع","عدم راحه","اجهاد نهاري","تفكير ليلي"],
    "فرط نعاس/ناركوليبسي": ["نعاس نهاري","غفوات مفاجئة","شلل نوم","هلوسات نعاس"],
    "انقطاع نفس اثناء النوم": ["شخير","توقف تنفس","نعاس نهاري","اختناق ليلي"],
    "اضطراب ايقاع يومي": ["سهر مزمن","نوم نهاري","دوام متأخر","Jet lag"],

    # --- جنسي/جندري ---
    "ضعف انتصاب": ["صعوبه انتصاب","عدم ثبات","قلق اداء"],
    "سرعة قذف": ["قذف مبكر","سيطرة ضعيفة","توتر اثناء الجماع"],
    "انخفاض الرغبة": ["رغبه جنسية منخفضه","فتور","عدم اهتمام جنسي"],
    "عسر جماع/تشنج مهبلي": ["الم جماع","تشنج مهبلي","رهبه جماع"],
    "اضطراب الهوية الجندرية": ["ضيق من الجنس المحدد","رغبه بتغيير الجنس","رفض السمات الجسدية"],

    # --- سلوكي/اندفاعي ---
    "نوبات غضب تفجيرية": ["نوبات غضب","عدوان مفاجئ","تهشيم","ندم لاحق","اندفاع غضبي"],
    "اضطراب معارض متحدي": ["جدال مع الكبار","تحدي قواعد","استفزاز","حساسيه مفرطة","عناد"],
    "اضطراب سلوكي": ["اعتداء","سرقه","هروب","تخريب","انتهاك حقوق"],
    "هوس سرقه": ["سرقة اندفاعية","توتر قبل الفعل","ارتياح بعده"],
    "هوس اشعال": ["ولع بالنار","اشعال متكرر","فضول بالنار"],

    # --- إدمان مواد (موسّع) ---
    "اضطراب تعاطي الكحول": ["كحول","سكر متكرر","تحمل","اعراض انسحاب","فقدان سيطرة","مشاكل عمل","مشاكل علاقات","سُكر","اعادة استخدام"],
    "اضطراب تعاطي القنب": ["حشيش","قنب","استخدام يومي","تسامح","انسحاب","قلق بعد الايقاف","ذهان مرتبط بالقنب"],
    "اضطراب تعاطي المنبهات": ["منشطات","امفيتامين","كوكايين","سهر","فقدان شهيه","بارانويا","استخدام قهري","نوبات نشاط"],
    "اضطراب تعاطي الأفيونات": ["هيروين","مورفين","اوكسيدودون","انسحاب افيوتي","رغبه ملحه","تحمل","حقن"],
    "تعاطي المهدئات/المنومات": ["بنزوديازبين","زاناكس","فاليوم","انسحاب قلق ورجفه","اعتماد"],
    "تعاطي النيكوتين": ["سجائر","شيشه","تبغ","انسحاب عصبيه واشتهاء","محاولات فاشلة"],
    "تعاطي الاستنشاق/المذيبات": ["شم مواد","دوخه","تلف عصبي","سلوك خطر"],
    "تعاطي متعدد": ["اكثر من ماده","خلط","خطر مرتفع","تناوب مواد"],

    # --- معرفي/خرف ---
    "اضطراب معرفي خفيف": ["نسيان جديد","بطء معالجه","تراجع تنفيذي","ضياع اشياء","تشتت"],
    "خرف مبكر/متوسط": ["تدهور ذاكره","ارتباك","تيه","تراجع اداء يومي","تغير شخصيه"],

    # --- الشخصية (موسّع) ---
    "شخصية بارانوية": ["ارتياب","سوء ظن","تاويل عدائي","حساسيه مفرطه","شك بلا دليل"],
    "شخصية فصامية": ["انعزال","برود عاطفي","قلة متعه","انسحاب"],
    "شخصية فُصامية النمط": ["افكار غريبة","اعتقادات سحرية","ريبة اجتماعية","ادراك غير اعتيادي","بدائية التفكير"],
    "شخصية معادية للمجتمع": ["خرق قواعد","عدوانيه","خداع","لامسؤوليه","اندفاع مؤذي"],
    "شخصية حدّية": ["اندفاع","تقلب عاطفي","خوف هجر","ايذاء ذاتي","فراغ مزمن","علاقات غير مستقرة","غضب شديد"],
    "شخصية هستيرية": ["بحث انتباه","انفعال سطحي","اغواء","درامية"],
    "شخصية نرجسية": ["عظمه","حاجه اعجاب","تعاطف قليل","استغلالي","حساس للنقد"],
    "شخصية اجتنابية": ["خجل شديد","تجنب نقد","حساسية رفض","شعور بالنقص","انعزال خوفا من الاحراج"],
    "شخصية اتكالية": ["اتكاليه","صعوبه قرار","خوف فراق","حاجة دعم","تجنب مسؤولية"],
    "شخصية وسواسية قهرية": ["انشغال بالتفاصيل","كماليه","صرامه","عناد","قواعد","قائمة مهام لا تنتهي"],
}

# ============================= تعزيزات الترجيح =============================
def duration_boost(duration_days: str) -> float:
    try: d = float(duration_days)
    except: return 0.0
    if d >= 365: return 2.0
    if d >= 90:  return 1.0
    if d >= 30:  return 0.5
    return 0.0

def gender_bias(gender: str, disorder: str) -> float:
    g = normalize(gender)
    if "انثى" in g:
        if any(k in disorder for k in ["ما قبل الطمث","ما حول الولادة"]):
            return 1.0
    return 0.0

def age_bias(age: str, disorder: str) -> float:
    try: a = int(age)
    except: return 0.0
    if a < 16 and ("فرط الحركة" in disorder or "سلوكي" in disorder):
        return 1.0
    if a >= 50 and ("معرفي" in disorder or "خرف" in disorder):
        return 1.0
    return 0.0

def impairment_boost(history_text: str) -> float:
    if not history_text: return 0.0
    t = normalize(history_text)
    keys = ["مشاكل عمل","فصل","انذار","مشاكل زواج","طلاق","خلافات","قضيه","مشاكل ماليه","تعثر دراسي","غياب متكرر"]
    if any(normalize(k) in t for k in keys):
        return 0.5
    return 0.0

# ============================= تشخيص =============================
def score_diagnoses(symptoms_text: str, age: str="", gender: str="", duration: str="", history: str=""):
    text_raw = symptoms_text or ""
    text_norm = expand_with_synonyms(text_raw)

    scores = defaultdict(float)
    hits_by_disorder = {}

    for disorder, keywords in DSM_DB.items():
        local_hits = []
        sc = 0.0
        toks = set(tokenize(text_norm))
        for kw in keywords:
            kw_n = normalize(kw)
            if contains_phrase(text_norm, kw):
                w = 1.0
                if kw_n in ("انتحار","افكار انتحارية","نوبة هلع","هلوسة","اوهام","ضلالات"):
                    w = 1.8
                sc += w
                local_hits.append(kw)
            elif kw_n in toks:
                sc += 0.6
                local_hits.append(kw)
        sc += duration_boost(duration)
        sc += gender_bias(gender, disorder)
        sc += age_bias(age, disorder)
        sc += impairment_boost(history)
        if sc > 0:
            scores[disorder] = sc
            hits_by_disorder[disorder] = local_hits

    if not scores:
        buckets = {
            "مزاج/اكتئاب": ["حزن","مزاج","متعه","يأس","نوم","طاقه","ذنب"],
            "قلق/هلع": ["قلق","توتر","نوبه","خفقان","اختناق","خوف"],
            "وسواس قهري": ["وسواس","طقوس","غسل","تفقد","تلوث"],
            "صدمة": ["حدث","فلاش","كوابيس","تجنب"],
            "ذهان": ["هلوسه","اوهام","ضلالات"],
            "انتباه/حركه": ["تشتت","تركيز","فرط","اندفاع"],
            "توحد": ["تواصل","روتين","حساسيات"],
            "نوم/أكل": ["نوم","شهية","نهم","تطهير"],
            "ادمان": ["تعاطي","انسحاب","تحمل"]
        }
        txt = normalize(text_raw)
        hints = [label for label, kws in buckets.items() if any(normalize(k) in txt for k in kws)]
        return [], {"suggestion": "أضف مفردات أدق (المدة/الشدة/السياق) لرفع الدقة.", "buckets": hints[:3]}

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    details = []
    for d, sc in ranked[:5]:
        hits = hits_by_disorder.get(d, [])
        details.append({"name": d, "score": round(sc, 2), "hits": ", ".join(hits[:10]) + ("..." if len(hits) > 10 else "")})
    return details, None

# ============================= واجهة رئيسية (هوم) =============================
HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | الرئيسية</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root{--bg1:#0b3a75; --bg2:#0a65b0; --gold:#f4b400; --white:#fff}
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
    .btn--alt{background:linear-gradient(180deg,#9cc5ff,#63a4ff);color:#04122c;box-shadow:0 6px 18px rgba(60,130,255,.28)}
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
      <div style="display:flex;flex-wrap:wrap;gap:12px">
        <a class="btn" href="{{ url_for('dsm') }}">🗂️ دراسة الحالة + التشخيص (DSM)</a>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h3>📖 DSM-5</h3>
        <p>قاعدة اضطرابات موسّعة + مطابقة كلمات لنتيجة تقديرية فورية عبر دراسة حالة.</p>
        <a class="btn" href="{{ url_for('dsm') }}">ابدأ الآن</a>
      </div>
      <div class="card">
        <h3>🧪 الاختبارات + CBT</h3>
        <p>سيُربط لاحقًا بلوحة اختبارات كاملة توجّه خطة CBT.</p>
        <a class="btn btn--alt" href="{{ url_for('dsm') }}">مؤقتًا إلى DSM</a>
      </div>
      <div class="card">
        <h3>🚭 علاج الإدمان</h3>
        <p>تقييم أولي وخطط علاج — سنضيفه كقسم مستقل لاحقًا.</p>
        <a class="btn" href="{{ url_for('dsm') }}">مؤقتًا إلى DSM</a>
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
    name = (form.get("name","") or "").strip()
    age = (form.get("age","") or "").strip()
    gender = (form.get("gender","") or "").strip()
    duration = (form.get("duration","") or "").strip()
    symptoms = (form.get("symptoms","") or "").strip()
    history = (form.get("history","") or "").strip()

    details, fallback = score_diagnoses(symptoms, age=age, gender=gender, duration=duration, history=history)

    if fallback is not None:
        result_html = f"""
        <div class="result">
          <h3>📋 النتيجة</h3>
          <p><span class="badge warn">لا تطابقات مباشرة كافية</span> — أضف كلمات أوضح (مثل: وسواس/نهم/هلع/هلوسة/رهاب...)</p>
          {"<p><strong>أقرب فئات:</strong> " + ", ".join(fallback.get("buckets", [])) + "</p>" if fallback.get("buckets") else ""}
          <p>اذكر <strong>المدة</strong> بدقّة، ووجود <strong>أثر وظيفي</strong> (عمل/دراسة/علاقات) وأي <strong>أدوية</strong>.</p>
        </div>
        """
    else:
        rows = [f"<tr><td>{d['name']}</td><td>{d['score']}</td><td>{d['hits']}</td></tr>" for d in details]
        table = "<table><thead><tr><th>التشخيص المقترح</th><th>الدرجة</th><th>كلمات مطابقة</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
        result_html = f"""
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
      {result_html}
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

# روابط تواصل (تحويل مؤقت)
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
