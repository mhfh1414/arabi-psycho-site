# DSM.py — مرجع مختصر منظم + diagnose(data) للترشيح القائم على الأعراض

def main():
    return """
    <h1>DSM-5 — مرجع منظم</h1>
    <p>قوائم مختصرة لأشيع الاضطرابات لتكون دليلاً سريعًا أثناء دراسة الحالة.</p>
    <style>
      details{background:#fff;border:1px solid #eee;border-radius:12px;margin:10px 0;padding:10px}
      summary{cursor:pointer;font-weight:800;color:#4B0082}
      .grid{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
      label{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:8px}
    </style>

    <details open><summary>اضطرابات المزاج</summary>
      <div class="grid">
        <label>الاكتئاب الجسيم (MDD)</label>
        <label>عسر المزاج (PDD)</label>
        <label>ثنائي القطب I/II</label>
        <label>دورية المزاج</label>
      </div>
    </details>

    <details><summary>القلق وما يتعلّق به</summary>
      <div class="grid">
        <label>اضطراب القلق العام (GAD)</label>
        <label>نوبات الهلع/رهاب الساح</label>
        <label>قلق/رهاب اجتماعي</label>
        <label>وسواس قهري (OCD)</label>
        <label>ما بعد الصدمة (PTSD)</label>
        <label>رهاب محدد</label>
      </div>
    </details>

    <details><summary>الذهانية</summary>
      <div class="grid">
        <label>فصام</label><label>ذهان وجيز</label><label>وهامي</label><label>فصامي وجداني</label>
      </div>
    </details>

    <details><summary>عصبية نمائية/أكل</summary>
      <div class="grid">
        <label>ADHD</label><label>طيف التوحد (مختصر)</label>
        <label>قهم عصبي (Anorexia)</label>
        <label>نهام عصبي (Bulimia)</label>
        <label>نهم الطعام (BED)</label>
      </div>
    </details>

    <details><summary>تعاطي مواد</summary>
      <div class="grid">
        <label>الكحول</label><label>أفيونات</label><label>منبهات</label><label>قنب</label><label>مهدئات</label>
      </div>
    </details>
    """

def diagnose(form):
    """
    form: dict من app.py (checkboxes = 'on' إذا تم اختيارها)
    تعيد قائمة [(اسم, سبب موجز, درجة 0-100)]
    """
    f = lambda k: form.get(k) in ("on","true","True","1")
    score = {}

    # --- اكتئاب جسيم MDD ---
    mdd_sym = sum([f("low_mood"), f("anhedonia"), f("sleep_issue"), f("appetite_change"),
                   f("fatigue"), f("guilt"), f("concentration"), f("slow_psychomotor"), f("suicidal")])
    if mdd_sym >= 5:
        score["اكتئاب جسيم (MDD)"] = (70 + 3*mdd_sym,
            "≥5 أعراض بينها مزاج منخفض/فقدان المتعة مع تأثير وظيفي")

    # عسر مزاج PDD (أخف لكن مزمن)
    if f("low_mood") and (f("sleep_issue") or f("appetite_change") or f("fatigue") or f("concentration")) and mdd_sym>=2:
        score["عُسر المزاج (PDD)"] = (55, "مزاج منخفض مزمن مع بعض الأعراض المرافقة")

    # --- قلق عام GAD ---
    gad = sum([f("worry"), f("restlessness"), f("tension"), f("concentration"), f("sleep_issue"), f("fatigue")])
    if f("worry") and gad >= 3:
        score["اضطراب القلق العام (GAD)"] = (60 + 4*min(gad,5), "قلق مفرط مع ≥3 أعراض جسدية/معرفية")

    # --- هلع / رهاب الساح ---
    panic = sum([f("panic_attacks"), f("panic_avoidance")])
    if f("panic_attacks") and panic >= 1:
        score["نوبات هلع ± رهاب الساح"] = (60 + 10*panic, "نوبات مفاجئة مع تجنّب/خوف مستمر")

    # --- قلق/رهاب اجتماعي ---
    soc = sum([f("social_avoid"), f("fear_judgment")])
    if soc >= 2:
        score["قلق/رهاب اجتماعي"] = (60, "تجنب اجتماعي وخوف من تقييم الآخرين")

    # --- OCD ---
    if f("obsessions") and f("compulsions"):
        score["وسواس قهري (OCD)"] = (70, "أفكار ملحّة وسلوكيات قهرية لتخفيف القلق")

    # --- PTSD ---
    ptsd = sum([f("trauma_event"), f("flashbacks"), f("nightmares"), f("trauma_avoid"), f("hypervigilance")])
    if f("trauma_event") and ptsd >= 3:
        score["ما بعد الصدمة (PTSD)"] = (65 + 3*min(ptsd,5), "تعرض صادمي مع إعادة خبرة وتجنّب ويقظة")

    # --- ثنائي القطب ---
    mania = sum([f("elevated_mood"), f("grandiosity"), f("decreased_sleep_need"),
                 f("pressured_speech"), f("impulsivity")])
    if f("elevated_mood") and mania >= 3:
        score["ثنائي القطب (نوبة هوس/هيبو)"] = (65 + 3*mania, "مزاج مرتفع + أعراض نشاط/اندفاع واضحة")

    # --- ذهان/فصام ---
    psych = sum([f("hallucinations"), f("delusions"), f("disorganized_speech"), f("functional_decline")])
    if psych >= 2 and f("functional_decline"):
        score["طيف الفصام/اضطراب ذهاني"] = (70, "ذهانية مع تدهور وظيفي")

    # --- ADHD ---
    adhd = sum([f("inattention"), f("hyperactivity"), f("impulsivity"), f("since_childhood"), f("functional_impair")])
    if (f("inattention") or f("hyperactivity")) and f("since_childhood") and f("functional_impair"):
        score["اضطراب فرط الحركة وتشتّت الانتباه (ADHD)"] = (60 + 4*min(adhd,5), "نمط منذ الطفولة مع تأثير وظيفي")

    # --- اضطرابات الأكل ---
    if f("restriction") and f("underweight") and f("body_image_distort"):
        score["قُهم عصبي (Anorexia)"] = (70, "تقييد + وزن منخفض + تشوّه صورة الجسد")
    if f("binges") and f("compensatory"):
        score["نُهام عصبي (Bulimia)"] = (65, "نوبات أكل كبيرة مع سلوك تعويضي")
    if f("binges") and not f("compensatory"):
        score["نهم الطعام (BED)"] = (55, "نوبات أكل دون تعويض")

    # --- تعاطي مواد ---
    substance = sum([f("craving"), f("tolerance"), f("withdrawal"), f("use_despite_harm")])
    if substance >= 2:
        sev = "خفيف" if substance==2 else ("متوسط" if substance==3 else "شديد")
        score[f"اضطراب تعاطي مواد ({sev})"] = (60 + 5*substance, "≥2 معايير (اشتهاء/تحمّل/انسحاب/استمرار رغم الضرر)")

    # تعديل الدرجة بحسب الشدة العامة
    try:
        distress = int(form.get("distress","5"))
    except: distress = 5
    mul = 0.9 + (distress/10)*0.3  # 0.9..1.2
    items = []
    for name,(s,why) in score.items():
        items.append((name, why, max(0,min(100, round(s*mul)))))
    # ترتيب تنازلي
    items.sort(key=lambda x: x[2], reverse=True)
    # إذا فارغة
    if not items:
        items=[("لا يظهر نمط محدد","الأعراض المختارة لا تكوّن متلازمة واضحة؛ جرّب تفاصيل أكثر أو راجع مختص.",0)]
    return items
