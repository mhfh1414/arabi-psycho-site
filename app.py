# -*- coding: utf-8 -*-
"""
عربي سايكو — ملف واحد كامل (Purple × Gold) v7.2

الصفحات:
    /        الرئيسية
    /case    دراسة الحالة (DSM + إدمان مدمج)
    /cbt     خطط CBT + مولد الجدول
    /pharm   دليل الأدوية النفسية (تثقيف فقط، بدون جرعات)
    /health  فحص جاهزية السيرفر (لـ Render)

⚠ أمان مهم:
- هذه أداة تثقيفية/تنظيمية وليست تشخيص طبي ولا وصف علاج.
- لا تبدأ أو توقف دواء بدون طبيب/صيدلي مختص.
- إذا عندك أفكار انتحار أو إيذاء: لازم تتواصل مع دعم بشري فوري.

تشغيل محلّي:
    python app.py

تشغيل على Render / Railway / أي استضافة WSGI:
    gunicorn app:app --bind 0.0.0.0:$PORT
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# ======================== إعدادات عامة ========================

BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO = os.environ.get(
    "LOGO_URL",
    "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg"
)

TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696")
WA_BASE = WA_URL.split("?")[0]

PSYCHO_WA = os.environ.get("PSYCHOLOGIST_WA", "https://wa.me/966530565696")
PSYCH_WA = os.environ.get("PSYCHIATRIST_WA", "https://wa.me/966530565696")
SOCIAL_WA = os.environ.get("SOCIAL_WORKER_WA", "https://wa.me/966530565696")

CACHE_BUST = os.environ.get(
    "CACHE_BUST",
    datetime.utcnow().strftime("%Y%m%d%H%M%S")
)

SLOGAN = "«نراك بعين الاحترام، ونسير معك بخطوات عملية.»"


# ======================== أدوات تحليل الأعراض ========================

def _cnt(flags, *keys):
    return sum(1 for k in keys if flags.get(k))

def preliminary_picks(flags):
    picks = []

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

    if _cnt(flags, "worry", "tension", "restlessness", "irritability",
            "mind_blank", "sleep_anxiety", "concentration_anxiety") >= 3:
        picks.append((
            "قلق معمّم / توتر مستمر",
            "قلق زائد صعب التحكم مع توتر جسدي أو صعوبة نوم أو تشوش التركيز",
            "درجة 65"
        ))

    if flags.get("panic_attacks") or flags.get("panic_fear"):
        picks.append((
            "نوبات هلع",
            "نوبات مفاجئة قوية مع خوف من تكرارها أو تجنّب أماكن",
            "درجة 70"
        ))

    if flags.get("agoraphobia") or flags.get("specific_phobia"):
        picks.append((
            "رُهاب/رهبة مواقف",
            "خوف محدد (أماكن/مواقف/أشياء) مع تجنّب وطلب أمان",
            "درجة 65"
        ))

    if flags.get("social_fear"):
        picks.append((
            "قلق اجتماعي",
            "خشية التقييم من الآخرين/الإحراج مع تجنّب المواقف الاجتماعية",
            "درجة 65"
        ))

    if flags.get("obsessions") and flags.get("compulsions"):
        picks.append((
            "وسواس قهري (OCD)",
            "وساوس ملحّة + أفعال قهرية (غسل/تفقد/ترتيب/طمأنة...)",
            "درجة 80"
        ))

    if _cnt(flags, "flashbacks", "hypervigilance", "startle",
            "numbing", "trauma_avoid", "guilt_trauma") >= 2:
        picks.append((
            "آثار صدمة / يقظة مفرطة",
            "استرجاعات/كوابيس/توتر شديد/تجنّب مرتبط بحدث مؤلم",
            "درجة 70"
        ))

    if _cnt(flags, "insomnia", "hypersomnia", "nightmares",
            "irregular_sleep") >= 1:
        picks.append((
            "صعوبات نوم",
            "مشاكل بدء/استمرار النوم أو نوم زائد/كوابيس",
            "درجة 55"
        ))

    if _cnt(flags, "adhd_inattention", "adhd_hyper",
            "disorganization", "time_blindness") >= 2:
        picks.append((
            "سمات تشتت/اندفاع (ADHD سمات)",
            "تشتت/نسيان/اندفاع/ضعف التنظيم ممكن يأثر على العمل أو الدراسة",
            "درجة 60"
        ))

    if _cnt(flags, "elevated_mood", "decreased_sleep_need", "grandiosity",
            "racing_thoughts", "pressured_speech", "risk_spending") >= 3:
        picks.append((
            "سمات مزاج مرتفع / اندفاع عالي",
            "طاقة عالية جدًا + نوم قليل + سلوك متهور ممكن يشير لسمات هوس/ثنائي القطب",
            "درجة 70"
        ))

    if _cnt(flags, "hallucinations", "delusions",
            "disorganized_speech", "negative_symptoms",
            "catatonia") >= 2 and flags.get("decline_function"):
        picks.append((
            "سمات ذهانية / فصامية",
            "وجود هلوسات/أوهام/تفكك تفكير مع تأثير واضح على الأداء اليومي",
            "درجة 80"
        ))

    if _cnt(flags, "binge_eating", "restrict_eating", "body_image",
            "purging") >= 2:
        picks.append((
            "صعوبات أكل/صورة الجسد",
            "نوبات أكل أو تقييد أو قلق عالي حول الجسم/الوزن",
            "درجة 60"
        ))

    if _cnt(flags, "craving", "withdrawal", "use_harm",
            "loss_control", "relapse_history") >= 2:
        picks.append((
            "تعاطي مواد / سلوك إدماني",
            "اشتهاء قوي، انسحاب، أو استمرار رغم الضرر",
            "درجة 80"
        ))

    if _cnt(flags, "emotion_instability", "impulsivity", "anger_issues",
            "perfectionism", "dependence", "social_withdrawal") >= 3:
        picks.append((
            "تنظيم عاطفي / غضب / علاقات",
            "تقلب عاطفي، اندفاع، انفجارات غضب أو تمسك زائد يضغط العلاقات",
            "درجة 60"
        ))

    if flags.get("self_conf_low"):
        picks.append((
            "ثقة بالنفس منخفضة",
            "نظرة ذاتية سلبية / تردد عالي / إحساس بعدم الكفاية",
            "درجة 50"
        ))

    if _cnt(flags, "asd_social", "sensory", "rigidity") >= 2:
        picks.append((
            "سمات تواصل/حسّية (طيف توحد)",
            "صعوبة قراءة الإشارات الاجتماعية، حساسية حسّية، أو تمسّك روتيني عالي",
            "درجة 55"
        ))

    if flags.get("suicidal"):
        picks.insert(0, (
            "تنبيه أمان",
            "وجود أفكار إيذاء أو انتحار — نوصي بالتواصل الفوري مع مختص أو دعم طارئ.",
            "درجة 99"
        ))

    return picks

def suggest_plans(flags):
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

    final = []
    seen = set()
    for k in sug:
        if k not in seen:
            seen.add(k)
            final.append(k)

    return final[:10]

def build_case_result_html(picks, plan_keys):
    PLAN_TITLES = {
        "ba": "BA — تنشيط سلوكي",
        "thought_record": "TR — سجل أفكار",
        "sleep_hygiene": "SH — نظافة النوم",
        "interoceptive_exposure": "IE — تعرّض داخلي (هلع)",
        "graded_exposure": "GE — تعرّض تدرّجي (رهاب/اجتماعي)",
        "ocd_erp": "ERP — وسواس قهري",
        "ptsd_grounding": "PTSD — تأريض/تنظيم",
        "problem_solving": "PS — حلّ المشكلات",
        "worry_time": "WT — وقت القلق",
        "mindfulness": "MB — يقظة ذهنية",
        "behavioral_experiments": "BE — تجارب سلوكية",
        "safety_behaviors": "SA — إيقاف سلوكيات آمنة/طمأنة",
        "bipolar_routine": "IPSRT — روتين ثنائي القطب",
        "relapse_prevention": "RP — منع الانتكاس (إدمان)",
        "social_skills": "SS — مهارات اجتماعية",
        "anger_management": "AM — إدارة الغضب",
        "self_confidence": "SC — تعزيز الثقة"
    }

    if picks:
        lis = "".join([
            f"<li><b>{t}</b> — {desc} "
            f"<span class='small'>({score})</span></li>"
            for (t, desc, score) in picks
        ])
    else:
        lis = (
            "<li>لا توجد مؤشرات كافية حالياً. "
            "استمر بالملاحظة الذاتية 👀</li>"
        )

    if plan_keys:
        cbt_badges = "".join([
            f"<span class='badge2 plan' data-key='{k}'>🔧 "
            f"{PLAN_TITLES.get(k, k)}</span>"
            for k in plan_keys
        ])
    else:
        cbt_badges = "<span class='small'>لا توجد توصيات محددة الآن.</span>"

    praise_line = (
        "أحسنت 👏 — كل خطوة وعي تقرّبك من التعافي. "
        "هذه ليست تشخيص نهائي طبي، لكنها خريطة أولية لمساعدتك على اختيار الخطة السلوكية."
    )

    html = f"""
    <section class="case-result">
      <div class="header-box">
        <img src="{LOGO}" class="logo-sm" alt="logo"/>
        <div>
          <div class="brand-name">{BRAND}</div>
          <div class="sub">نتيجة دراسة الحالة — ملخص جاهز للطباعة والمشاركة</div>
        </div>
      </div>

      <p class="praise">{praise_line}</p>

      <h2>📌 الترشيحات المبدئية</h2>
      <ul class="dx-list">{lis}</ul>

      <h3>🔧 أدوات CBT المقترحة حسب حالتك</h3>
      <div class="plans-wrap">{cbt_badges}</div>

      <h3>🚀 ماذا بعد؟</h3>
      <ol class="next-steps">
        <li>اطبع أو خزّن هذه النتائج.</li>
        <li>اضغط "فتح CBT" لتوليد جدول 7 / 10 / 14 يوم بخطوات يومية واضحة.</li>
        <li>إذا حسّيت أنك تحتاج دعم بشري مباشر: تواصل من الأزرار تحت.</li>
      </ol>

      <div class="share-row">
        <button class="btn gold" onclick="window.print()">🖨️ طباعة</button>
        <button class="btn" onclick="downloadJSON()">💾 تنزيل JSON</button>
        <a class="btn wa" target="_blank" rel="noopener"
           href="{WA_BASE}">🟢 مشاركة واتساب</a>
        <a class="btn tg" target="_blank" rel="noopener"
           href="{TG_URL}">✈️ تيليجرام</a>
        <a class="btn gold" href="/cbt">🧠 فتح CBT (مخصّص لحالتك)</a>
      </div>

      <div class="help-row">
        <a class="btn pro" target="_blank" rel="noopener" href="{PSYCHO_WA}">👨‍🎓 أخصائي نفسي الآن</a>
        <a class="btn pro" target="_blank" rel="noopener" href="{PSYCH_WA}">👨‍⚕️ طبيب نفسي</a>
        <a class="btn pro" target="_blank" rel="noopener" href="{SOCIAL_WA}">🤝 أخصائي اجتماعي</a>
      </div>
    </section>
    """
    return html


# ======================== shell() آمن بدون f-string داخل سكربت ========================

def shell(page_title, content_html, active="home"):
    """
    نبني الصفحة عن طريق قالب فيه [[PLACEHOLDER]] ثم replace()
    عشان ما ينفجر بسبب أقواس الجافاسكربت.
    """

    template = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>[[PAGE_TITLE]]</title>
<style>
/* نفس الستايل */
body {
    background-color:#0a0612;
    color:#f7f3d6;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    margin:0;
    padding:0 12px 80px;
    line-height:1.6;
}
header {
    text-align:center;
    padding:16px 8px 8px;
}
header .brand-row {
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:8px;
}
.logo {
    width:64px;
    height:64px;
    border-radius:50%;
    border:2px solid #d1b23a;
    background-color:#1a132b;
    object-fit:contain;
}
.brand-name-big {
    font-size:20px;
    font-weight:600;
    color:#f7f3d6;
}
.slogan {
    font-size:14px;
    color:#d1b23a;
    font-weight:500;
}
.subline {
    font-size:12px;
    color:#888;
}
nav.nav {
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:8px;
    margin:16px auto 24px;
    max-width:800px;
}
nav.nav a {
    text-decoration:none;
    background-color:#1a132b;
    border:1px solid #3a2f55;
    border-radius:12px;
    padding:8px 12px;
    min-width:140px;
    flex:1;
    color:#f7f3d6;
    font-size:14px;
    line-height:1.4;
    box-shadow:0 0 10px rgba(209,178,58,0.2);
}
nav.nav a small {
    display:block;
    font-size:11px;
    color:#d1b23a;
}
nav.nav a.active {
    border:1px solid #d1b23a;
    box-shadow:0 0 12px rgba(209,178,58,0.6);
}
.ref-box {
    border:1px solid #3a2f55;
    background-color:#1a132b;
    border-radius:12px;
    padding:12px;
    max-width:800px;
    margin:0 auto 24px;
    box-shadow:0 0 20px rgba(209,178,58,0.15);
}
.ref-box h4 {
    margin:0 0 8px;
    font-size:15px;
    color:#d1b23a;
    font-weight:600;
}
.ref-links {
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    font-size:13px;
    line-height:1.4;
}
.ref-links a {
    display:flex;
    flex-direction:column;
    flex:1;
    min-width:140px;
    text-decoration:none;
    color:#f7f3d6;
    background-color:#241a3c;
    border-radius:10px;
    border:1px solid #3a2f55;
    padding:8px;
}
.ref-links a span {
    font-size:12px;
    color:#d1b23a;
}

.main-wrap {
    max-width:900px;
    margin:0 auto;
    background-color:#1a132b;
    border:1px solid #3a2f55;
    border-radius:16px;
    padding:16px;
    box-shadow:0 0 30px rgba(209,178,58,0.15);
}

h1,h2,h3,h4,h5 {
    color:#f7f3d6;
    font-weight:600;
    line-height:1.4;
}
h1 {font-size:20px; margin:0 0 12px;}
h2 {font-size:18px; margin:16px 0 8px;}
h3 {font-size:16px; margin:16px 0 8px;}

p,li,label,small,div {
    font-size:14px;
}
small.small {
    font-size:11px;
    color:#aaa;
}
.dx-list {
    margin:0;
    padding:0 16px;
}
.badge2 {
    display:inline-flex;
    align-items:center;
    gap:6px;
    background-color:#2a2045;
    border:1px solid #3a2f55;
    border-radius:10px;
    padding:6px 8px;
    margin:4px 4px 0 0;
    font-size:13px;
    line-height:1.4;
    color:#f7f3d6;
    box-shadow:0 0 12px rgba(209,178,58,0.15);
}
.badge2 input[type=checkbox] {
    accent-color:#d1b23a;
    transform:scale(1.2);
}
.grid {
    display:flex;
    flex-wrap:wrap;
    gap:12px;
}
.tile {
    background-color:#1f1634;
    border-radius:12px;
    padding:10px;
    flex:1;
    min-width:260px;
    box-shadow:0 0 20px rgba(209,178,58,0.08);
}
.tile h3 {
    color:#d1b23a;
    font-size:14px;
    margin:0 0 8px;
    font-weight:600;
}
.tile label {
    display:flex;
    flex-wrap:wrap;
    font-size:13px;
}

input,select,textarea {
    width:100%;
    background-color:#2a2045;
    border:1px solid #3a2f55;
    color:#f7f3d6;
    border-radius:8px;
    font-size:14px;
    padding:8px;
    margin-top:4px;
    font-family:inherit;
}
textarea {
    min-height:80px;
    resize:vertical;
}

.divider {
    border-top:1px solid #3a2f55;
    margin:16px 0;
}

.row {
    display:flex;
    flex-wrap:wrap;
    gap:10px;
}

.btn {
    background-color:#2a2045;
    border:1px solid #3a2f55;
    border-radius:10px;
    color:#f7f3d6;
    font-size:14px;
    padding:8px 12px;
    text-decoration:none;
    cursor:pointer;
    line-height:1.4;
    text-align:center;
    min-width:120px;
    box-shadow:0 0 12px rgba(209,178,58,0.15);
}
.btn.gold {
    background-color:#3b2a00;
    border:1px solid #d1b23a;
    color:#f7f3d6;
    box-shadow:0 0 16px rgba(209,178,58,0.45);
    font-weight:600;
}
.btn.alt {
    background-color:#1f1634;
}
.btn.wa {
    background-color:#1a2f1a;
    border:1px solid #2d5f2d;
}
.btn.tg {
    background-color:#1a2538;
    border:1px solid #2d4b7a;
}
.btn.pro {
    flex:1;
    min-width:140px;
    background-color:#241a3c;
    border:1px solid #3a2f55;
}

.share-row,.help-row {
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    margin-top:16px;
}

.case-result .header-box {
    display:flex;
    flex-wrap:nowrap;
    align-items:center;
    gap:10px;
    background-color:#241a3c;
    border:1px solid #3a2f55;
    border-radius:12px;
    padding:10px;
    box-shadow:0 0 20px rgba(209,178,58,0.15);
}
.logo-sm {
    width:44px;
    height:44px;
    border-radius:50%;
    border:2px solid #d1b23a;
    object-fit:contain;
    background-color:#0a0612;
}
.brand-name {
    font-weight:600;
    font-size:14px;
    color:#f7f3d6;
}
.case-result .sub {
    font-size:12px;
    color:#d1b23a;
    line-height:1.4;
}
.case-result .praise {
    font-size:14px;
    color:#f7f3d6;
    background-color:#1f1634;
    border:1px solid #3a2f55;
    border-radius:10px;
    padding:10px;
    margin-top:12px;
    box-shadow:0 0 20px rgba(209,178,58,0.15);
}
.plans-wrap {
    display:flex;
    flex-wrap:wrap;
    gap:6px;
    margin-bottom:8px;
}
.next-steps {
    padding-right:20px;
    font-size:14px;
    line-height:1.6;
}

footer {
    text-align:center;
    color:#888;
    font-size:12px;
    margin:32px auto 12px;
    max-width:900px;
    line-height:1.5;
}
footer .legal {
    color:#d1b23a;
    font-size:12px;
    margin-top:8px;
}

#print-note {
    font-size:11px;
    color:#777;
    text-align:center;
    margin-top:8px;
}

#checklist {
    margin-top:16px;
    background-color:#1f1634;
    border:1px solid #3a2f55;
    border-radius:12px;
    box-shadow:0 0 20px rgba(209,178,58,0.15);
    padding:12px;
    font-size:14px;
    line-height:1.6;
    overflow-x:auto;
}
.check-day {
    border-bottom:1px solid #3a2f55;
    padding:8px 0;
}
.check-day:last-child {
    border-bottom:none;
}
.check-day h4 {
    margin:0 0 6px;
    font-size:14px;
    color:#d1b23a;
}
.todo-item {
    display:flex;
    align-items:flex-start;
    gap:6px;
    font-size:14px;
    line-height:1.5;
}
.todo-item input[type=checkbox] {
    accent-color:#d1b23a;
    transform:scale(1.2);
    margin-top:2px;
}

.search-bar {
    display:flex;
    gap:8px;
    flex-wrap:wrap;
    margin:12px 0 16px;
}
.search-bar input {
    flex:1;
    min-width:200px;
}
.search-bar button {
    min-width:100px;
}

.drug-card {
    background-color:#241a3c;
    border:1px solid #3a2f55;
    border-radius:12px;
    padding:12px;
    margin-bottom:12px;
    box-shadow:0 0 20px rgba(209,178,58,0.15);
}
.drug-card h3 {
    margin:0 0 8px;
    font-size:15px;
    color:#d1b23a;
}
.drug-card .sec {
    font-size:13px;
    line-height:1.5;
    color:#f7f3d6;
}
.drug-card .warn {
    color:#ff7676;
    font-size:12px;
    margin-top:6px;
    line-height:1.5;
}
</style>

<script>
// مكتبة CBT
const CBT_LIBRARY = {
  "ba": {
    "title": "BA — تنشيط سلوكي",
    "tasks": [
      "اخرج من الغرفة ولو 10 دقائق مشي خفيف.",
      "نشاط بسيط كنت تسويه قبل (قهوة مع نفسك / هواية).",
      "تواصل مع شخص واحد تثق فيه برسالة قصيرة ودودة."
    ]
  },
  "thought_record": {
    "title": "TR — سجل أفكار",
    "tasks": [
      "أكتب الموقف اللي ضايقك.",
      "ما هو الفكرة السلبية اللي طلعت في بالك؟",
      "ما هو الدليل أنها 100% صحيحة؟ ما هو الدليل ضدها؟",
      "اكتب نسخة فكرية أهدأ وأكثر توازن."
    ]
  },
  "sleep_hygiene": {
    "title": "SH — نظافة النوم",
    "tasks": [
      "نام واستيقظ تقريبًا نفس الوقت اليوم.",
      "لا قهوة ثقيلة قبل النوم بـ 6 ساعات.",
      "سريرك للنوم فقط، لا للجوال 60 دقيقة قبل النوم."
    ]
  },
  "problem_solving": {
    "title": "PS — حلّ المشكلات",
    "tasks": [
      "حدّد مشكلة محددة بصيغة سؤال.",
      "اكتب 3 حلول ممكنة بدون تقييم.",
      "اختر حل واحد صغير وجرّبه اليوم.",
      "قيّم النتيجة آخر اليوم."
    ]
  },
  "worry_time": {
    "title": "WT — وقت القلق",
    "tasks": [
      "لو جاءك قلق طول اليوم: قل له (مو وقته الآن).",
      "حدد 15 دقيقة ثابتة لاحقًا للقلق فقط.",
      "في الوقت المحدد اكتب كل المخاوف على ورق."
    ]
  },
  "mindfulness": {
    "title": "MB — يقظة ذهنية",
    "tasks": [
      "تمرين تنفس 4-4-6: شهيق 4 / ثبات 4 / زفير 6.",
      "ركّز على إحساس القدم بالأرض 60 ثانية.",
      "لاحظ الفكرة بدون تصديقها، فقط لاحظها وعد."
    ]
  },
  "interoceptive_exposure": {
    "title": "IE — تعرّض داخلي (هلع)",
    "tasks": [
      "راقب خفقان القلب بدون محاولة تهدئة فورية.",
      "ذكّر نفسك: (الأعراض مزعجة لكن مو خطيرة).",
      "دوّن شدة القلق من 0 إلى 10 بعد دقيقتين."
    ]
  },
  "graded_exposure": {
    "title": "GE — تعرّض تدرّجي",
    "tasks": [
      "حدد موقف يخوفك بدرجة 3/10 مو 10/10.",
      "ادخل الموقف مدة قصيرة بدون هروب مباشر.",
      "دوّن النتيجة الحقيقية اللي حصلت مو التوقع الكارثي."
    ]
  },
  "social_skills": {
    "title": "SS — مهارات اجتماعية",
    "tasks": [
      "ابدأ تحية قصيرة مع شخص (السلام عليكم + سؤال بسيط).",
      "تدرب تقول (عفوًا، أحتاج دقيقة أرتب فكرتي).",
      "تسمية شعورك بصوت واضح: (أنا قلق شوي الآن)."
    ]
  },
  "self_confidence": {
    "title": "SC — تعزيز الثقة",
    "tasks": [
      "اكتب إنجاز بسيط عملته اليوم حتى لو شكلك تقليل من قيمته.",
      "قل لنفسك بصوت مسموع (أنا أتحرك، حتى لو خطوة صغيرة).",
      "توقف عن جملة جلد ذاتي وحدة اليوم (بدلها بجملة ألطف وواقعية)."
    ]
  },
  "safety_behaviors": {
    "title": "SA — إيقاف سلوكيات الطمأنة",
    "tasks": [
      "قلل سؤال (هل أنا بخير؟) للناس من 10 مرات إلى 5.",
      "جرّب تبقى في الموقف المقلق بدون رسائل طمأنة فورية.",
      "لاحظ: هل القلق فعلاً يطلع للسماء أو ينزل بعد كم دقيقة؟"
    ]
  },
  "ocd_erp": {
    "title": "ERP — وسواس قهري",
    "tasks": [
      "اختر فكرة وسواسية متوسطة القوة (مو أقوى شي).",
      "امنع الطقس القهري (غسل/تفقد) فقط لدقيقة إضافية.",
      "دوّن مستوى الضيق بعد دقيقة وبعد 5 دقائق."
    ]
  },
  "ptsd_grounding": {
    "title": "PTSD — تأريض/تنظيم",
    "tasks": [
      "تمرين 5-4-3-2-1: سمِّ 5 أشياء تشوفها الآن، 4 تلمسها، 3 تسمعها...",
      "ذكر النفس: (أنت الآن في بيئة آمنة، مو في الحدث القديم).",
      "تنفس بطيء من البطن 2 دقيقة."
    ]
  },
  "bipolar_routine": {
    "title": "IPSRT — روتين ثابت",
    "tasks": [
      "نوم/استيقاظ تقريبًا نفس الساعة.",
      "وجبات في أوقات شبه ثابتة.",
      "سجل التقلب المزاجي رقمياً (0 هادي / 10 متهور)."
    ]
  },
  "relapse_prevention": {
    "title": "RP — منع الانتكاس (إدمان)",
    "tasks": [
      "اكتب أقوى مُحفّز اليوم (شخص / مكان / إحساس).",
      "اكتب خطة استبدال (بديل سليم تُسويه بدل التعاطي).",
      "راسل دعمك البشري ولو (سلام أنا صامد معك)."
    ]
  },
  "anger_management": {
    "title": "AM — إدارة الغضب",
    "tasks": [
      "إذا حسّيت الغضب يطلع فوق 6/10: خذ انسحاب هادئ دقيقة.",
      "اكتب ما هو الشيء اللي تحت الغضب؟ (جرح؟ إحساس عدم احترام؟).",
      "ارجع وتكلم بصيغة (أنا أحس...) بدل (إنت دايم...)."
    ]
  }
};

// يبني القوائم المنسدلة للخطط
function initPlanSelectors() {
  const selA = document.getElementById("planA");
  const selB = document.getElementById("planB");
  if (!selA || !selB) return;
  Object.keys(CBT_LIBRARY).forEach(key => {
    const optA = document.createElement("option");
    optA.value = key;
    optA.textContent = CBT_LIBRARY[key].title;
    selA.appendChild(optA);

    const optB = document.createElement("option");
    optB.value = key;
    optB.textContent = CBT_LIBRARY[key].title;
    selB.appendChild(optB);
  });
}

// يبني الجدول اليومي
function buildChecklist() {
  const days = parseInt(document.getElementById("daysSelect").value || "7");
  const planA = document.getElementById("planA").value;
  const planB = document.getElementById("planB").value || null;

  const out = [];
  for (let d=1; d<=days; d++) {
    out.push({
      day: d,
      tasks: []
    });
  }

  function pushTasks(planKey) {
    if (!planKey) return;
    const lib = CBT_LIBRARY[planKey];
    if (!lib) return;
    lib.tasks.forEach(t => {
      out.forEach(dayObj => {
        dayObj.tasks.push({ text: t, done:false, plan: planKey });
      });
    });
  }

  pushTasks(planA);
  pushTasks(planB);

  const wrap = document.getElementById("checklist");
  wrap.innerHTML = "";
  out.forEach(dayObj => {
    const div = document.createElement("div");
    div.className = "check-day";
    div.innerHTML = "<h4>اليوم " + dayObj.day + "</h4>";
    dayObj.tasks.forEach(task => {
      const row = document.createElement("div");
      row.className = "todo-item";
      row.innerHTML = `
        <input type="checkbox">
        <div>
          <div>${task.text}</div>
          <small class="small">خطة: ${CBT_LIBRARY[task.plan]?.title || task.plan}</small>
        </div>
      `;
      div.appendChild(row);
    });
    wrap.appendChild(div);
  });

  // share links
  const waLink = document.getElementById("share-wa");
  const tgLink = document.getElementById("share-tg");
  if (waLink) {
    waLink.href = "[[WA_BASE]]?text=" + encodeURIComponent("جدول CBT ✔");
  }
  if (tgLink) {
    tgLink.href = "[[TG_URL]]";
  }
}

// يحفظ الجدول كـ JSON
function saveChecklist() {
  const wrap = document.getElementById("checklist");
  const txt = wrap.innerText || wrap.textContent || "";
  const blob = new Blob([txt], {type:"application/json"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "cbt-plan-[[CACHE_BUST]].json";
  a.click();
}

// تنزيل نتيجة دراسة الحالة
function downloadJSON() {
  const sec = document.querySelector(".case-result");
  if (!sec) return;
  const data = {
    brand: "[[BRAND]]",
    ts: "[[CACHE_BUST]]",
    summaryText: sec.innerText
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], {type:"application/json"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "case-summary-[[CACHE_BUST]].json";
  a.click();
}

// بحث الأدوية
const DRUGS = [
  {
    name: "مثبطات السيروتونين الانتقائية (SSRI)",
    use: "غالباً للقلق والاكتئاب وأحيانًا الوسواس القهري",
    common: "غثيان خفيف، صداع، تغير نوم/شهية، أحيانًا برود جنسي",
    urgent: "أفكار انتحارية جديدة أو أسوأ بشكل مفاجئ، تهيج شديد، هوس/اندفاع غير طبيعي"
  },
  {
    name: "مثبتات المزاج",
    use: "لتقلب المزاج الشديد أو نوبات المزاج المرتفع",
    common: "عطش، رجفة خفيفة، زيادة وزن محتملة",
    urgent: "تقيؤ شديد، رعشة قوية، تشوش وعي، خمول مفاجئ غير طبيعي"
  },
  {
    name: "مضادات الذهان الحديثة",
    use: "تُصرف للهلاوس/الأوهام أو الاضطراب الشديد أو التهيج العالي",
    common: "نعاس، زيادة شهية، جفاف فم",
    urgent: "تيبس شديد بالعضلات، حرارة، ارتباك ذهني قوي"
  },
  {
    name: "أدوية النوم/القلق المهدئة (قصيرة المدى فقط)",
    use: "أرق حاد قصير المدى أو قلق شديد مؤقت",
    common: "نعاس، تباطؤ تركيز، بطء رد فعل",
    urgent: "نعاس مفرط جدًا، تداخل كلام، تنفس بطيء أو ضعيف"
  },
  {
    name: "أدوية دعم الإدمان / منع الانتكاس",
    use: "تقلل الرغبة أو تساعد تثبيت السلوك بعد الإيقاف",
    common: "غثيان بسيط، صداع، دوخة خفيفة",
    urgent: "اصفرار عين/جلد، ألم بطن قوي، تشنج، هلاوس"
  }
];

function pharmSearch() {
  const q = (document.getElementById("pharm-q").value || "").trim().toLowerCase();
  const zone = document.getElementById("pharm-results");
  zone.innerHTML = "";
  DRUGS.filter(d => (
    d.name.toLowerCase().includes(q) ||
    d.use.toLowerCase().includes(q)
  )).forEach(d => {
    const card = document.createElement("div");
    card.className = "drug-card";
    card.innerHTML = `
      <h3>${d.name}</h3>
      <div class="sec"><b>لماذا يُصرف؟</b> ${d.use}</div>
      <div class="sec"><b>أعراض جانبية شائعة:</b> ${d.common}</div>
      <div class="warn"><b>مراجعة طبية فورية إذا:</b> ${d.urgent}</div>
      <div class="warn"><b>تحذير:</b> لا تبدأ/توقف الدواء بدون إشراف طبي مباشر.</div>
    `;
    zone.appendChild(card);
  });
}
</script>

</head>
<body onload="initPlanSelectors()">

<header>
  <div class="brand-row">
    <img src="[[LOGO]]" class="logo" alt="logo"/>
    <div class="brand-name-big">[[BRAND]]</div>
    <div class="slogan">[[SLOGAN]]</div>
    <div class="subline">بنفسجي × ذهبي — @[[BRAND_NO_SPACE]]</div>
  </div>
</header>

<nav class="nav">
  <a href="/" class="[[ACTIVE_HOME]]">
    <span>🏠 الرئيسية</span>
    <small>الصفحة الأولى</small>
  </a>
  <a href="/case" class="[[ACTIVE_CASE]]">
    <span>📝 دراسة الحالة</span>
    <small>أعراضك وتشخيص مبدئي</small>
  </a>
  <a href="/cbt" class="[[ACTIVE_CBT]]">
    <span>🧠 CBT</span>
    <small>الخطط + الجدول</small>
  </a>
  <a href="/pharm" class="[[ACTIVE_PHARM]]">
    <span>💊 دليل الأدوية النفسية</span>
    <small>متى يُصرف / التحذيرات</small>
  </a>
</nav>

<div class="ref-box">
  <h4>📞 دعم مباشر الآن</h4>
  <div class="ref-links">
    <a href="[[PSYCHO_WA]]" target="_blank" rel="noopener">
      👨‍🎓 أخصائي نفسي
      <span>خطة سلوكية/سلوكية معرفية</span>
    </a>
    <a href="[[PSYCH_WA]]" target="_blank" rel="noopener">
      👨‍⚕️ طبيب نفسي
      <span>تشخيص طبي / أدوية</span>
    </a>
    <a href="[[SOCIAL_WA]]" target="_blank" rel="noopener">
      🤝 أخصائي اجتماعي
      <span>دعم أسري / مواقف حياتية</span>
    </a>
  </div>
</div>

<main class="main-wrap">
[[CONTENT]]
</main>

<footer>
  © جميع الحقوق محفوظة لـ [[BRAND]] — [[SLOGAN]]<br/>
  تيليجرام الدعم: [[TG_URL]] · واتساب: [[WA_URL]]<br/>
  الإصدار البنفسجي × الذهبي — BUILD [[BUILD]]
  <div class="legal">
    هذه الأداة ليست بديلاً عن رعاية صحية طارئة أو طبيب نفسي مرخّص.
  </div>
  <div id="print-note">اطبع أو خزّن النتيجة بشفرة خاصة في جهازك فقط.</div>
</footer>

</body>
</html>
"""

    html_out = (
        template
        .replace("[[PAGE_TITLE]]", page_title)
        .replace("[[LOGO]]", LOGO)
        .replace("[[BRAND]]", BRAND)
        .replace("[[BRAND_NO_SPACE]]", BRAND.replace(" ", ""))
        .replace("[[SLOGAN]]", SLOGAN)
        .replace("[[TG_URL]]", TG_URL)
        .replace("[[WA_URL]]", WA_URL)
        .replace("[[WA_BASE]]", WA_BASE)
        .replace("[[CACHE_BUST]]", CACHE_BUST)
        .replace("[[BUILD]]", CACHE_BUST)
        .replace("[[PSYCHO_WA]]", PSYCHO_WA)
        .replace("[[PSYCH_WA]]", PSYCH_WA)
        .replace("[[SOCIAL_WA]]", SOCIAL_WA)
        .replace("[[ACTIVE_HOME]]", "active" if active == "home" else "")
        .replace("[[ACTIVE_CASE]]", "active" if active == "case" else "")
        .replace("[[ACTIVE_CBT]]", "active" if active == "cbt" else "")
        .replace("[[ACTIVE_PHARM]]", "active" if active == "pharm" else "")
        .replace("[[CONTENT]]", content_html)
    )

    return html_out


# ======================== صفحات Flask ========================

@app.get("/")
def home():
    content = f"""
    <h1>مرحبًا بك في {BRAND}</h1>

    <p>
    هذه مساحة آمنة تساعدك تحلل وضعك بصراحة، بدون حُكم.
    الخطوات عندنا واضحة:
    </p>

    <ol>
      <li>📝 قيّم نفسك في «دراسة الحالة»</li>
      <li>🧠 ننشئ لك خطة CBT يومية عملية (7 / 10 / 14 يوم)</li>
      <li>🤝 لو احتجت دعم بشري مباشر: أخصائي نفسي / طبيب نفسي / أخصائي اجتماعي — بزر واحد تكلمهم.</li>
      <li>💊 تبغى تعرف عن الأدوية النفسية والآثار الجانبية وليش تنصرف؟ افتح «دليل الأدوية».</li>
    </ol>

    <div class="divider"></div>

    <section>
      <h2>📝 دراسة الحالة (DSM + الإدمان مدمج)</h2>
      <p>
        أكثر من 70 عرض (مزاج، قلق، وسواس، صدمة، نوم، تركيز، ثقة، غضب، تعاطي مواد...).
        بعدها يطلع لك ملخص مبدئي + توصيات CBT + زر تحويل مباشر للدعم.
      </p>
      <a class="btn gold" href="/case">ابدأ الآن</a>
    </section>

    <section>
      <h2>🧠 CBT العلاج السلوكي المعرفي</h2>
      <p>
        خطط واضحة (تنشيط سلوكي، إدارة الغضب، تعزيز الثقة بالنفس، نوم، هلع، وسواس...).
        الموقع يبني لك جدول يومي قابل للطباعة والمشاركة.
      </p>
      <a class="btn gold" href="/cbt">افتح CBT</a>
    </section>

    <section>
      <h2>💊 دليل الأدوية النفسية</h2>
      <p>
        SSRIs, مثبت مزاج, أدوية الذهان, القلق, الإدمان...
        ليش ينصرف الدواء؟ أهم الأعراض الجانبية؟ متى لازم دكتور فورًا؟
      </p>
      <a class="btn gold" href="/pharm">استعرض الأدوية</a>
    </section>

    <section>
      <h2>📞 تواصل سريع</h2>
      <p>تحتاج تتكلم مع بشر حقيقي؟ نوصلك مباشرة.</p>
      <div class="row">
        <a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">✈️ تيليجرام</a>
        <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">🟢 واتساب</a>
      </div>
    </section>
    """

    return shell("الرئيسية — " + BRAND, content, "home")


# ---------------- /case ----------------

CASE_FORM_HTML = f"""
<h1>📝 دراسة الحالة — (DSM + الإدمان مدمج)</h1>

<p>
اختر الأعراض اللي تحس إنها <b>عندك فعلاً</b> بالفترة الحالية. بعدها اضغط «عرض النتيجة».<br/>
مهم: هذا مو تشخيص طبي نهائي. هذا مسار مبدئي يساعدك تبني خطة سلوكية محترمة.
</p>

<p class="small">تنبيه خصوصية: يتم حفظ اختياراتك محليًا في جهازك (localStorage) وليس في السيرفر.</p>

<form method="POST" action="/case">

<h2>1) معلومات أساسية</h2>
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
    <label>العمل / الدراسة
      <input name="work" placeholder="طالب / موظف / باحث عن عمل / غير ذلك">
    </label>
  </div>
</div>

<div class="divider"></div>

<h2>2) الأعراض الحالية (اختر ما ينطبق فعلاً)</h2>

<div class="grid">

  <div class="tile">
    <h3>🟣 المزاج / الاكتئاب</h3>
    <label class="badge2"><input type="checkbox" name="low_mood"> مزاج منخفض أكثر من العادة</label>
    <label class="badge2"><input type="checkbox" name="anhedonia"> فقدان المتعة بالأشياء</label>
    <label class="badge2"><input type="checkbox" name="hopeless"> إحساس بالتشاؤم / اليأس</label>
    <label class="badge2"><input type="checkbox" name="fatigue"> إرهاق / طاقة منخفضة</label>
    <label class="badge2"><input type="checkbox" name="sleep_issue"> نوم مضطرب أو متقطع</label>
    <label class="badge2"><input type="checkbox" name="appetite_change"> تغيّر واضح بالشّهية / الوزن</label>
    <label class="badge2"><input type="checkbox" name="somatic_pain"> آلام جسدية مرتبطة بالمزاج</label>
    <label class="badge2"><input type="checkbox" name="worthlessness"> شعور بالذنب / عدم القيمة</label>
    <label class="badge2"><input type="checkbox" name="poor_concentration"> تركيز ضعيف / بطء تفكير</label>
    <label class="badge2"><input type="checkbox" name="psychomotor"> تباطؤ أو تهيّج حركي</label>
    <label class="badge2"><input type="checkbox" name="suicidal"> أفكار إيذاء أو انتحار</label>
  </div>

  <div class="tile">
    <h3>🟣 القلق / الهلع / الرهاب</h3>
    <label class="badge2"><input type="checkbox" name="worry"> قلق زائد صعب السيطرة</label>
    <label class="badge2"><input type="checkbox" name="tension"> توتر عضلي / شد جسدي</label>
    <label class="badge2"><input type="checkbox" name="restlessness"> تململ / أرق / عصبية</label>
    <label class="badge2"><input type="checkbox" name="irritability"> سرعة انفعال / عصبية سريعة</label>
    <label class="badge2"><input type="checkbox" name="mind_blank"> فراغ ذهني تحت الضغط</label>
    <label class="badge2"><input type="checkbox" name="sleep_anxiety"> صعوبة نوم بسبب القلق</label>
    <label class="badge2"><input type="checkbox" name="concentration_anxiety"> تشوش تركيز مع القلق</label>
    <label class="badge2"><input type="checkbox" name="panic_attacks"> نوبات هلع متكررة</label>
    <label class="badge2"><input type="checkbox" name="panic_fear"> خوف من تكرار نوبة هلع</label>
    <label class="badge2"><input type="checkbox" name="agoraphobia"> رهبة الأماكن المزدحمة / المفتوحة</label>
    <label class="badge2"><input type="checkbox" name="specific_phobia"> رُهاب محدد (حيوان/قيادة/طيران..)</label>
    <label class="badge2"><input type="checkbox" name="social_fear"> خوف من تقييم الآخرين / إحراج اجتماعي</label>
    <label class="badge2"><input type="checkbox" name="safety_need"> أحتاج طمأنة أو مرافقة عشان أهدى</label>
  </div>

  <div class="tile">
    <h3>🟣 وسواس قهري (OCD)</h3>
    <label class="badge2"><input type="checkbox" name="obsessions"> أفكار/صور مُلِحّة ما أقدر أوقفها</label>
    <label class="badge2"><input type="checkbox" name="compulsions"> أفعال قهرية (غسل/تفقد/ترتيب...)</label>
    <label class="badge2"><input type="checkbox" name="contamination"> هوس تلوّث / غسل مفرط</label>
    <label class="badge2"><input type="checkbox" name="checking"> تفقد الأبواب/القفل/الأشياء كثير</label>
    <label class="badge2"><input type="checkbox" name="ordering"> لازم ترتيب/تماثل كامل</label>
    <label class="badge2"><input type="checkbox" name="harm_obs"> وساوس أذى (أخاف أضر نفسي/غيري)</label>
    <label class="badge2"><input type="checkbox" name="scrupulosity"> تدقيق ديني/أخلاقي قهري</label>
  </div>

  <div class="tile">
    <h3>🟣 الصدمة / ما بعد الصدمة</h3>
    <label class="badge2"><input type="checkbox" name="flashbacks"> استرجاعات / كوابيس عن حدث صعب</label>
    <label class="badge2"><input type="checkbox" name="hypervigilance"> يقظة مفرطة / دائمًا على أهبة الاستعداد</label>
    <label class="badge2"><input type="checkbox" name="startle"> فزع مفرط من الأصوات/المفاجآت</label>
    <label class="badge2"><input type="checkbox" name="numbing"> خدر عاطفي / كأني مو موجود</label>
    <label class="badge2"><input type="checkbox" name="trauma_avoid"> أتجنب أي تذكير بالحدث (أماكن/كلام)</label>
    <label class="badge2"><input type="checkbox" name="guilt_trauma"> شعور بالذنب تجاه الحدث</label>
  </div>

  <div class="tile">
    <h3>🟣 النوم</h3>
    <label class="badge2"><input type="checkbox" name="insomnia"> صعوبة بداية/استمرار النوم (أرق)</label>
    <label class="badge2"><input type="checkbox" name="hypersomnia"> نوم مفرط / صعوبة القيام</label>
    <label class="badge2"><input type="checkbox" name="nightmares"> كوابيس متكررة</label>
    <label class="badge2"><input type="checkbox" name="irregular_sleep"> مواعيد نوم فوضوية جدًا</label>
  </div>

  <div class="tile">
    <h3>🟣 تركيز / حركة / تنظيم الوقت</h3>
    <label class="badge2"><input type="checkbox" name="adhd_inattention"> تشتت / نسيان أشياء أساسية</label>
    <label class="badge2"><input type="checkbox" name="adhd_hyper"> فرط حركة / اندفاع / صعوبة الجلوس</label>
    <label class="badge2"><input type="checkbox" name="disorganization"> فوضى تنظيم / تأجيل مزمن</label>
    <label class="badge2"><input type="checkbox" name="time_blindness"> ضياع الإحساس بالوقت / التأخير الدائم</label>
  </div>

  <div class="tile">
    <h3>🟣 مزاج مرتفع / طاقة مفرطة</h3>
    <label class="badge2"><input type="checkbox" name="elevated_mood"> مزاج مرتفع جدًا / تهوّر</label>
    <label class="badge2"><input type="checkbox" name="decreased_sleep_need"> أحتاج نوم قليل جدًا وأحس طبيعي</label>
    <label class="badge2"><input type="checkbox" name="grandiosity"> إحساس بالعظمة / قدرات خارقة</label>
    <label class="badge2"><input type="checkbox" name="racing_thoughts"> أفكار سريعة جدًا / ما ألحقها</label>
    <label class="badge2"><input type="checkbox" name="pressured_speech"> كلام سريع/متدفق جدًا</label>
    <label class="badge2"><input type="checkbox" name="risk_spending"> صرف فلوس/مخاطرة عالية بدون تفكير</label>
  </div>

  <div class="tile">
    <h3>🟣 إدراك/تفكير (ذهاني/فصام)</h3>
    <label class="badge2"><input type="checkbox" name="hallucinations"> هلوسات (أسمع/أشوف شي غير طبيعي)</label>
    <label class="badge2"><input type="checkbox" name="delusions"> أفكار مراقبة / مؤامرة / يقين غريب</label>
    <label class="badge2"><input type="checkbox" name="disorganized_speech"> كلام/تفكير متشتت أو غير مفهوم</label>
    <label class="badge2"><input type="checkbox" name="negative_symptoms"> انسحاب / برود عاطفي</label>
    <label class="badge2"><input type="checkbox" name="catatonia"> تجمّد حركي / سلوك غير متجاوب</label>
    <label class="badge2"><input type="checkbox" name="decline_function"> تدهور واضح بالدراسة/العمل/العلاقات</label>
  </div>

  <div class="tile">
    <h3>🟣 الأكل / صورة الجسد</h3>
    <label class="badge2"><input type="checkbox" name="binge_eating"> نوبات أكل شره / فقدان التحكم</label>
    <label class="badge2"><input type="checkbox" name="restrict_eating"> تقييد قوي / تجويع نفسي</label>
    <label class="badge2"><input type="checkbox" name="body_image"> انشغال قوي بالشكل/الوزن</label>
    <label class="badge2"><input type="checkbox" name="purging"> تطهير/إقياء قهري بعد الأكل</label>
  </div>

  <div class="tile">
    <h3>🟣 تعاطي مواد / إدمان</h3>
    <label class="badge2"><input type="checkbox" name="craving"> اشتهاء قوي / أحتاج أستخدم الآن</label>
    <label class="badge2"><input type="checkbox" name="withdrawal"> انسحاب جسدي/نفسي إذا ما استخدمت</label>
    <label class="badge2"><input type="checkbox" name="use_harm"> أستمر رغم ضرر واضح</label>
    <label class="badge2"><input type="checkbox" name="loss_control"> صعوبة إيقاف / فقدان السيطرة</label>
    <label class="badge2"><input type="checkbox" name="relapse_history"> انتكاسات بعد محاولات الإيقاف</label>
  </div>

  <div class="tile">
    <h3>🟣 تنظيم العاطفة / العلاقات / الغضب</h3>
    <label class="badge2"><input type="checkbox" name="emotion_instability"> تقلب مزاج حاد / مشاعر قوية فجأة</label>
    <label class="badge2"><input type="checkbox" name="impulsivity"> اندفاعية / أتصرف قبل ما أفكر</label>
    <label class="badge2"><input type="checkbox" name="anger_issues"> نوبات غضب / صراخ / انفجار سريع</label>
    <label class="badge2"><input type="checkbox" name="perfectionism"> كمالية تعطلني (كل شيء لازم مثالي)</label>
    <label class="badge2"><input type="checkbox" name="dependence"> تعلق عالي / خوف قوي من الهجر</label>
    <label class="badge2"><input type="checkbox" name="social_withdrawal"> انسحاب اجتماعي / صعوبة تواصل</label>
    <label class="badge2"><input type="checkbox" name="self_conf_low"> ثقة بالنفس منخفضة / جلد ذاتي</label>
  </div>

  <div class="tile">
    <h3>🟣 تواصل / حساسية حسّية</h3>
    <label class="badge2"><input type="checkbox" name="asd_social"> صعوبة قراءة الإشارات الاجتماعية</label>
    <label class="badge2"><input type="checkbox" name="sensory"> حساسية حسّية (أصوات/إضاءة/ملمس)</label>
    <label class="badge2"><input type="checkbox" name="rigidity"> تمسّك عالي بروتين/ترتيب (أتضايق لو تغيّر)</label>
  </div>

</div>

<div class="divider"></div>

<label>ملاحظاتك (اختياري)
  <textarea name="notes" placeholder="شي تبغى تشرحه بوضوح؟ موقف صار؟ شيء يخوّفك؟"></textarea>
</label>

<div class="row" style="margin-top:14px">
  <button class="btn gold" type="submit">عرض النتيجة</button>
  <a class="btn" href="/cbt">🧠 فتح CBT الآن</a>
</div>

</form>
"""

@app.route("/case", methods=["GET", "POST"])
def case():
    if request.method == "GET":
        return shell("دراسة الحالة — " + BRAND, CASE_FORM_HTML, "case")

    # POST
    form_data = {
        k: True
        for k in request.form.keys()
        if k not in ("age", "marital", "work", "notes")
    }

    form_data["age_val"] = request.form.get("age", "").strip()
    form_data["marital_val"] = request.form.get("marital", "").strip()
    form_data["work_val"] = request.form.get("work", "").strip()
    _user_notes = request.form.get("notes", "").strip()

    picks = preliminary_picks(form_data)
    plans = suggest_plans(form_data)
    html = build_case_result_html(picks, plans)

    return shell("نتيجة دراسة الحالة — " + BRAND, html, "case")


# ---------------- /cbt ----------------

CBT_PAGE_HTML = f"""
<h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>

<p>
الهدف: تحويل الأعراض إلى خطوات يومية قابلة للتنفيذ.
اختَر خطة (أو خطتين مع بعض)، حدّد عدد الأيام (7 / 10 / 14)، واضغط "إنشاء الجدول" 👇
</p>

<p class="small">
لو جيت من «دراسة الحالة»، بنوسّط لك الخطط المقترحة بخط ذهبي.
إذا ما جيت من هناك، عادي؛ تقدر تختار يدوي.
</p>

<h2>الخطط المتاحة (بعض الأمثلة)</h2>
<ul class="dx-list">
  <li>BA — تنشيط سلوكي (مزاج منخفض / اكتئاب)</li>
  <li>WT — وقت القلق (قلق عام)</li>
  <li>IE — تعرّض داخلي (نوبات هلع)</li>
  <li>ERP — وسواس قهري</li>
  <li>PTSD — تأريض / تنظيم بعد الصدمة</li>
  <li>IPSRT — روتين ثابت لثنائي القطب</li>
  <li>RP — منع الانتكاس (إدمان)</li>
  <li>AM — إدارة الغضب</li>
  <li>SC — تعزيز الثقة بالنفس</li>
</ul>

<div class="divider"></div>

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
  <button class="btn alt" type="button" onclick="window.print()">🖨️ طباعة</button>
  <button class="btn" type="button" onclick="saveChecklist()">💾 تنزيل JSON</button>
  <a class="btn wa" id="share-wa" target="_blank" rel="noopener">🟢 واتساب</a>
  <a class="btn tg" id="share-tg" target="_blank" rel="noopener">✈️ تيليجرام</a>
</div>

<div id="checklist"></div>

<div class="divider"></div>

<h2>هل تحتاج بشري الآن؟</h2>
<div class="help-row">
  <a class="btn pro" target="_blank" rel="noopener" href="{PSYCHO_WA}">👨‍🎓 أخصائي نفسي</a>
  <a class="btn pro" target="_blank" rel="noopener" href="{PSYCH_WA}">👨‍⚕️ طبيب نفسي</a>
  <a class="btn pro" target="_blank" rel="noopener" href="{SOCIAL_WA}">🤝 أخصائي اجتماعي</a>
</div>
"""

def render_cbt_page():
    return CBT_PAGE_HTML

@app.get("/cbt")
def cbt():
    return shell("CBT — خطط وتمارين", render_cbt_page(), "cbt")


# ---------------- /pharm ----------------

PHARM_PAGE_HTML = f"""
<h1>💊 دليل الأدوية النفسية (تثقيف فقط)</h1>

<p>
مهم جدًا:
</p>
<ul class="dx-list">
  <li>هذه الصفحة تثقيف فقط — مو وصفة علاج.</li>
  <li>لا تبدأ ولا توقف دواء بدون طبيب/صيدلي مختص.</li>
  <li>بعض الأدوية إيقافها فجأة خطر (انسحاب، هلع، تشنجات، انتكاس شديد).</li>
  <li>لو فيه أفكار إيذاء نفسك أو غيرك لازم دعم طبي عاجل.</li>
</ul>

<div class="search-bar">
  <input id="pharm-q" placeholder="ابحث باسم الدواء أو الحالة (مثال: اكتئاب / هلع / ذهان)">
  <button class="btn gold" type="button" onclick="pharmSearch()">بحث</button>
</div>

<div id="pharm-results"></div>

<div class="divider"></div>

<h2>أحتاج مختص الآن؟</h2>
<div class="help-row">
  <a class="btn pro" target="_blank" rel="noopener" href="{PSYCHO_WA}">👨‍🎓 أخصائي نفسي (سلوكي)</a>
  <a class="btn pro" target="_blank" rel="noopener" href="{PSYCH_WA}">👨‍⚕️ طبيب نفسي (دوائي)</a>
  <a class="btn pro" target="_blank" rel="noopener" href="{SOCIAL_WA}">🤝 أخصائي اجتماعي (دعم حياتي)</a>
</div>
"""

def render_pharm_page():
    return PHARM_PAGE_HTML

@app.get("/pharm")
def pharm():
    return shell("دليل الأدوية النفسية — " + BRAND, render_pharm_page(), "pharm")


# ---------------- /health ----------------

@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "brand": BRAND,
        "build": CACHE_BUST
    }), 200


# ======================== Security headers ========================

@app.after_request
def add_headers(resp):
    # سياسة حماية محتوى
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


# ======================== Run ========================

if __name__ == "__main__":
    # محلي:
    #   python app.py
    #
    # على Render / Railway:
    #   gunicorn app:app --bind 0.0.0.0:$PORT
    #
    # ملاحظة: Render يعطي env PORT تلقائي
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
