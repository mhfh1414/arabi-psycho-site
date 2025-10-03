# DSM.py — مرجع مُوسَّع + تشخيص ترشيحي أدق
from typing import Dict, List, Tuple

HTML = """
<h1>📘 DSM — مرجع مُوسَّع (تعليمي)</h1>
<p class="muted">مختصر منظَّم للفئات الشائعة (للمراجعة فقط).</p>

<h2>1) اضطرابات القلق</h2>
<ul>
  <li><b>قلق عام (GAD):</b> قلق مفرط أغلب الأيام ≥6 أشهر + توتر/تعب/صعوبة تركيز/أرق.</li>
  <li><b>نوبات هلع:</b> نوبات فجائية + أعراض جسدية + قلق من التكرار وتجنّب.</li>
  <li><b>رهاب اجتماعي:</b> خوف من تقييم الآخرين + تجنب.</li>
</ul>

<h2>2) الاضطرابات المزاجية</h2>
<ul>
  <li><b>اكتئاب جسيم:</b> مزاج منخفض أو فقدان متعة مع نوم/شهية/طاقة/تركيز/ذنب.</li>
  <li><b>ثنائي القطب:</b> نوبات هوس/هوس خفيف (مزاج مرتفع، قلة نوم، اندفاع/عظمة) ± اكتئاب.</li>
</ul>

<h2>3) الوسواس القهري (OCD)</h2>
<ul>
  <li>أفكار ملحّة + أفعال قهرية مؤثرة وظيفياً.</li>
</ul>

<h2>4) الصدمة والضغوط (PTSD)</h2>
<ul>
  <li>تعرض لحدث صادمي + استرجاع/كوابيس/تجنب/يقظة مفرطة.</li>
</ul>

<h2>5) طيف الفُصام</h2>
<ul>
  <li>هلاوس/أوهام/اضطراب كلام/سلوك + تدهور وظيفي.</li>
</ul>

<h2>6) اضطرابات الأكل</h2>
<ul>
  <li><b>فقدان الشهية:</b> تقييد شديد + نقص وزن + صورة جسد مشوّهة.</li>
  <li><b>الشره:</b> نوبات أكل مع سلوكات تعويضية.</li>
</ul>

<h2>7) ADHD</h2>
<ul>
  <li>عدم انتباه و/أو فرط حركة واندفاعية منذ الطفولة مع أثر وظيفي.</li>
</ul>

<h2>8) تعاطي المواد (SUD)</h2>
<ul>
  <li>اشتهاء، تحمّل، انسحاب، استخدام رغم الضرر، فشل أدوار.</li>
</ul>
"""

def main() -> str:
    return HTML

def diagnose(data: Dict[str, str]) -> List[Tuple[str, str, float]]:
    Y = lambda k: k in data

    picks: List[Tuple[str,str,float]] = []

    # اكتئاب
    dep = sum(Y(k) for k in ["low_mood","anhedonia","sleep_issue","appetite_change","fatigue"])
    if dep >= 2:
        score = 60 + 8*max(0, dep-2)
        why = f"أعراض مزاجية متعددة ({dep}/5)"
        picks.append(("اكتئاب جسيم — ترشيح", why, min(score, 85)))

    # قلق عام
    gad = sum(Y(k) for k in ["worry","tension","focus_issue","restlessness"])
    if gad >= 2:
        score = 55 + 7*max(0, gad-2)
        picks.append(("قلق عام — ترشيح", f"قلق مستمر مع توتر/تركيز ({gad}/4)", min(score, 80)))

    # هلع
    if Y("panic_attacks"):
        subs = sum(Y(k) for k in ["fear_of_attacks","panic_avoidance"])
        picks.append(("اضطراب هلع — ترشيح", "نوبات + " + ("خوف/تجنّب" if subs else "أعراض نوبات واضحة"), 65 + 7*subs))

    # رهاب اجتماعي
    if Y("social_avoid") and Y("fear_judgment"):
        picks.append(("رهاب اجتماعي — ترشيح","خوف من التقييم + تجنّب", 62))

    # OCD
    if Y("obsessions") or Y("compulsions"):
        both = int(Y("obsessions") and Y("compulsions"))
        picks.append(("وسواس قهري — ترشيح","أفكار ملحّة/أفعال قهرية", 60 + 8*both))

    # PTSD
    pts = Y("trauma_event") and (Y("flashbacks") or Y("nightmares") or Y("trauma_avoid") or Y("hypervigilance"))
    if pts:
        n = sum(Y(k) for k in ["flashbacks","nightmares","trauma_avoid","hypervigilance"])
        picks.append(("اضطراب ما بعد الصدمة — ترشيح","حدث صادمي + أعراض لاحقة", 65 + 5*min(3,n)))

    # ثنائي القطب
    mania_n = sum(Y(k) for k in ["elevated_mood","decreased_sleep_need","impulsivity","grandiosity"])
    if Y("elevated_mood") and mania_n >= 2:
        picks.append(("ثنائي القطب — ترشيح","مزاج مرتفع + (قلة نوم/اندفاع/عظمة)", 58 + 6*(mania_n-1)))

    # ذهانيات
    psych_n = sum(Y(k) for k in ["hallucinations","delusions","disorganized_speech","functional_decline"])
    if psych_n >= 2:
        picks.append(("طيف فُصام/ذهاني — ترشيح","أعراض ذهانية متعددة", 57 + 6*min(4, psych_n)))

    # أكل
    eat_n = sum(Y(k) for k in ["restriction","underweight","body_image_distort","binges","compensatory"])
    if eat_n >= 2:
        picks.append(("اضطراب أكل — ترشيح","تقييد/نوبات/صورة جسد", 56 + 5*min(3,eat_n)))

    # ADHD
    adhd_n = sum(Y(k) for k in ["inattention","hyperactivity","impulsivity_symp","since_childhood","functional_impair"])
    if adhd_n >= 3 and Y("since_childhood"):
        picks.append(("ADHD — ترشيح","استمرارية منذ الطفولة مع أثر", 60 + 5*min(3, adhd_n-2)))

    # SUD
    sud_n = sum(Y(k) for k in ["craving","tolerance","withdrawal","use_despite_harm"])
    if sud_n >= 2:
        picks.append(("تعاطي مواد — ترشيح","اشتهاء/انسحاب/تحمّل/رغم الضرر", 62 + 5*min(3,sud_n)))

    picks.sort(key=lambda x: x[2], reverse=True)
    return picks[:8] if picks else [("لا توجد ترشيحات قوية","البيانات المدخلة غير كافية",0.0)]
