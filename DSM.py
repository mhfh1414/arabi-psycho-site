# DSM.py — مرجع مختصر + خوارزمية ترشيح diagnose()

from typing import Dict, List, Tuple

HTML = """
<h1>📘 DSM — مرجع مختصر</h1>
<p class="muted">محتوى تعليمي مبسّط للمراجعة فقط.</p>

<h2>اضطرابات القلق</h2>
<ul>
  <li><b>قلق عام (GAD):</b> قلق مفرط أغلب الأيام ≥ 6 أشهر مع توتر/تعب/صعوبة تركيز.</li>
  <li><b>نوبات هلع:</b> نوبات مفاجئة من الخوف الشديد + أعراض جسدية، يعقبها قلق من التكرار وتجنّب.</li>
  <li><b>رهاب اجتماعي:</b> خوف من تقييم الآخرين، تجنّب مواقف اجتماعية.</li>
</ul>

<h2>الاضطرابات المزاجية</h2>
<ul>
  <li><b>اكتئاب جسيم:</b> مزاج منخفض/فقدان متعة + أعراض نوم/شهية/طاقة/تركيز.</li>
  <li><b>ثنائي القطب:</b> نوبات مزاج مرتفع (هوس/هوس خفيف) ± اكتئاب.</li>
</ul>

<h2>الوسواس القهري (OCD)</h2>
<ul>
  <li>أفكار ملحّة متكررة + أفعال قهرية لتخفيف القلق، مع أثر وظيفي.</li>
</ul>

<h2>اضطرابات الصدمة (PTSD)</h2>
<ul>
  <li>تعرّض لحدث صادمي + استرجاع/كوابيس/تجنّب/يقظة مفرطة.</li>
</ul>

<h2>اضطرابات طيف الفُصام</h2>
<ul>
  <li>هلاوس/أوهام/اضطراب كلام أو سلوك + تدهور وظيفي.</li>
</ul>

<h2>اضطرابات الأكل</h2>
<ul>
  <li><b>فقدان الشهية:</b> تقييد شديد ونقص وزن وصورة جسد مشوّهة.</li>
  <li><b>الشره:</b> نوبات أكل مع سلوك تعويضي (قيء/مسهل/صيام/تمارين مفرطة).</li>
</ul>

<h2>فرط الحركة وتشتّت الانتباه (ADHD)</h2>
<ul>
  <li>عدم انتباه/فرط حركة/اندفاعية منذ الطفولة مع أثر وظيفي.</li>
</ul>

<h2>اضطرابات تعاطي المواد</h2>
<ul>
  <li>نمط مشكلات: اشتهاء، تحمّل، انسحاب، استخدام رغم الضرر.</li>
</ul>
"""

def main() -> str:
    return HTML

# تستقبل قاموس request.form من /case
# وتُرجِع قائمة [(اسم, سبب, درجة)]
def diagnose(data: Dict[str, str]) -> List[Tuple[str, str, float]]:
    yes = lambda k: k in data  # وجود المربع يعني True

    picks: List[Tuple[str,str,float]] = []

    # اكتئاب
    dep_keys = ["low_mood","anhedonia","sleep_issue","appetite_change","fatigue"]
    dep_score = sum(1 for k in dep_keys if yes(k))
    if dep_score >= 2:
        picks.append((
            "اكتئاب — ترشيح",
            f"أعراض مزاجية متعددة ({dep_score}/{len(dep_keys)})",
            60 + 5*max(0, dep_score-2)
        ))

    # قلق عام
    gad_keys = ["worry","tension","focus_issue","restlessness"]
    gad_score = sum(1 for k in gad_keys if yes(k))
    if gad_score >= 2:
        picks.append((
            "قلق عام — ترشيح",
            f"قلق مستمر مع توتر/تركيز ({gad_score}/{len(gad_keys)})",
            55 + 5*max(0, gad_score-2)
        ))

    # هلع
    if yes("panic_attacks"):
        sub = int(yes("fear_of_attacks")) + int(yes("panic_avoidance"))
        picks.append((
            "اضطراب هلع — ترشيح",
            "نوبات + " + ("خوف من التكرار" if yes("fear_of_attacks") else "") + (" وتجنّب" if yes("panic_avoidance") else ""),
            60 + 5*sub
        ))

    # رهاب اجتماعي
    soc = int(yes("social_avoid")) + int(yes("fear_judgment"))
    if soc >= 2:
        picks.append(("رهاب اجتماعي — ترشيح","تجنّب اجتماعي وخوف من التقييم",60))

    # وسواس قهري
    if yes("obsessions") or yes("compulsions"):
        both = int(yes("obsessions") and yes("compulsions"))
        picks.append(("وسواس قهري — ترشيح","أفكار ملحّة/أفعال قهرية",60 + 5*both))

    # PTSD
    if yes("trauma_event") and (yes("flashbacks") or yes("nightmares") or yes("trauma_avoid") or yes("hypervigilance")):
        pts = int(yes("flashbacks")) + int(yes("nightmares")) + int(yes("trauma_avoid")) + int(yes("hypervigilance"))
        picks.append(("اضطراب ما بعد الصدمة — ترشيح","حدث صادمي + أعراض لاحقة",60 + 5*min(3, pts)))

    # ثنائي القطب
    if yes("elevated_mood") and (yes("decreased_sleep_need") or yes("impulsivity") or yes("grandiosity")):
        mania = int(yes("decreased_sleep_need")) + int(yes("impulsivity")) + int(yes("grandiosity"))
        picks.append(("ثنائي القطب — ترشيح","مزاج مرتفع + مؤشرات هوس",55 + 5*mania))

    # فُصام/ذهان
    psych = int(yes("hallucinations")) + int(yes("delusions")) + int(yes("disorganized_speech")) + int(yes("functional_decline"))
    if psych >= 2:
        picks.append(("ذهانيات — ترشيح","أعراض ذهانية متعددة",55 + 5*min(4, psych)))

    # اضطرابات الأكل
    eat = int(yes("restriction")) + int(yes("underweight")) + int(yes("body_image_distort")) + int(yes("binges")) + int(yes("compensatory"))
    if eat >= 2:
        picks.append(("اضطراب أكل — ترشيح","نمط تقييد/نوبات/صورة جسد",55 + 5*min(3, eat)))

    # ADHD
    adhd = int(yes("inattention")) + int(yes("hyperactivity")) + int(yes("impulsivity_symp")) + int(yes("since_childhood")) + int(yes("functional_impair"))
    if adhd >= 3 and yes("since_childhood"):
        picks.append(("ADHD — ترشيح","أعراض مستمرة منذ الطفولة مع أثر وظيفي",60 + 5*min(3, adhd-2)))

    # تعاطي مواد
    sud = int(yes("craving")) + int(yes("tolerance")) + int(yes("withdrawal")) + int(yes("use_despite_harm"))
    if sud >= 2:
        picks.append(("تعاطي مواد — ترشيح","اشتهاء/انسحاب/تحمّل/استخدام رغم الضرر",60 + 5*min(3, sud)))

    # ترتيب ونرجع أعلى 6
    picks.sort(key=lambda x: x[2], reverse=True)
    return picks[:6] if picks else [("لا توجد ترشيحات قوية","البيانات المدخلة غير كافية",0.0)]
