# DSM.py — موسّع (تعليمي) لتوليد ترشيحات تشخيصية مبدئية
# يقرأ حقول الفورم في /case ويُرجع [(name, why, score)] مرتبة تنازليًا.
# ملاحظة: هذا للاستخدام التعليمي/الإرشادي فقط وليس تشخيصًا طبيًا.

from typing import Dict, List, Tuple

# ========== Helpers ==========
def _yes(v) -> bool:
    if v is True: 
        return True
    s = str(v or "").strip().lower()
    return s in ["1","y","yes","on","true","صح","نعم"]

def _num(v, default=0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default

def _reason(flag: bool, text: str, bag: list):
    if flag: bag.append(text)

# ========== Core DX ==========
def diagnose(symptoms: Dict) -> List[Tuple[str, str, float]]:
    """
    يأخذ dict من الأعراض (كما ترسلها صفحة /case) ويُرجع قائمة:
      (اسم التشخيص، سبب مختصر + نسبة تقديرية، درجة خام)
    يتم ترتيب النتائج تنازليًا حسب الدرجة.
    """

    Y = lambda k: _yes(symptoms.get(k))
    V = lambda k, d=0.0: _num(symptoms.get(k, d), d)

    results: List[Tuple[str, str, float]] = []
    distress = V("distress", 0)  # 0..10

    # نستخدم نفس مفاتيح الفورم في app.py

    # ====== 1) الاكتئاب الجسيم (MDD) ======
    mdd_reasons = []
    score_mdd = 0; max_mdd = 8
    _reason(Y("low_mood"), "مزاج منخفض", mdd_reasons);           score_mdd += 2 if Y("low_mood") else 0
    _reason(Y("anhedonia"), "فقدان المتعة", mdd_reasons);         score_mdd += 2 if Y("anhedonia") else 0
    _reason(Y("sleep_issue"), "اضطراب نوم", mdd_reasons);         score_mdd += 1 if Y("sleep_issue") else 0
    _reason(Y("appetite_change"), "تغيّر شهية", mdd_reasons);     score_mdd += 1 if Y("appetite_change") else 0
    _reason(Y("fatigue"), "إرهاق/خمول", mdd_reasons);             score_mdd += 1 if Y("fatigue") else 0
    if distress >= 6:
        _reason(True, f"شدّة مرتفعة ({int(distress)}/10)", mdd_reasons); score_mdd += 1
    if score_mdd >= 4:
        pct = round(100*score_mdd/max_mdd)
        results.append(("اكتئاب جسيم (MDD)", f"{'، '.join(mdd_reasons)} — تقدير {pct}%", float(score_mdd)))

    # ====== 2) اضطراب القلق العام (GAD) ======
    gad_reasons = []
    score_gad = 0; max_gad = 6
    _reason(Y("worry"), "قلق مستمر", gad_reasons);                 score_gad += 2 if Y("worry") else 0
    _reason(Y("tension"), "توتر جسدي", gad_reasons);               score_gad += 1 if Y("tension") else 0
    _reason(Y("focus_issue"), "تشتت/صعوبة تركيز", gad_reasons);    score_gad += 1 if Y("focus_issue") else 0
    _reason(Y("restlessness"), "تململ", gad_reasons);              score_gad += 1 if Y("restlessness") else 0
    if distress >= 6:
        _reason(True, f"شدّة مرتفعة ({int(distress)}/10)", gad_reasons); score_gad += 1
    if score_gad >= 4:
        pct = round(100*score_gad/max_gad)
        results.append(("اضطراب القلق العام (GAD)", f"{'، '.join(gad_reasons)} — تقدير {pct}%", float(score_gad)))

    # ====== 3) الهلع ======
    panic_reasons = []
    score_panic = 0; max_panic = 4
    _reason(Y("panic_attacks"), "نوبات هلع", panic_reasons);       score_panic += 2 if Y("panic_attacks") else 0
    _reason(Y("fear_of_attacks"), "خوف من تكرار النوبات", panic_reasons); score_panic += 1 if Y("fear_of_attacks") else 0
    _reason(Y("panic_avoidance"), "سلوك تجنّبي", panic_reasons);   score_panic += 1 if Y("panic_avoidance") else 0
    if score_panic >= 3:
        pct = round(100*score_panic/max_panic)
        results.append(("اضطراب الهلع", f"{'، '.join(panic_reasons)} — تقدير {pct}%", float(score_panic)))

    # ====== 4) القلق/الرهاب الاجتماعي ======
    sa_reasons = []
    score_sa = 0; max_sa = 4
    _reason(Y("social_avoid"), "تجنّب اجتماعي", sa_reasons);       score_sa += 2 if Y("social_avoid") else 0
    _reason(Y("fear_judgment"), "خوف من تقييم الآخرين", sa_reasons); score_sa += 1 if Y("fear_judgment") else 0
    if distress >= 5:
        _reason(True, f"ضيق واضح ({int(distress)}/10)", sa_reasons); score_sa += 1
    if score_sa >= 3:
        pct = round(100*score_sa/max_sa)
        results.append(("قلق/رهاب اجتماعي", f"{'، '.join(sa_reasons)} — تقدير {pct}%", float(score_sa)))

    # ====== 5) الوسواس القهري (OCD) ======
    ocd_reasons = []
    score_ocd = 0; max_ocd = 5
    _reason(Y("obsessions"), "أفكار ملحّة", ocd_reasons);          score_ocd += 2 if Y("obsessions") else 0
    _reason(Y("compulsions"), "أفعال قهرية", ocd_reasons);         score_ocd += 2 if Y("compulsions") else 0
    if distress >= 5:
        _reason(True, f"ضيق ملحوظ ({int(distress)}/10)", ocd_reasons); score_ocd += 1
    if score_ocd >= 4:
        pct = round(100*score_ocd/max_ocd)
        results.append(("وسواس قهري (OCD)", f"{'، '.join(ocd_reasons)} — تقدير {pct}%", float(score_ocd)))

    # ====== 6) اضطراب ما بعد الصدمة (PTSD) ======
    ptsd_reasons = []
    score_ptsd = 0; max_ptsd = 5
    _reason(Y("trauma_event"), "تعرض لحدث صادمي", ptsd_reasons);   score_ptsd += 2 if Y("trauma_event") else 0
    _reason(Y("flashbacks") or Y("nightmares"), "استرجاع/كوابيس", ptsd_reasons); score_ptsd += 1 if (Y("flashbacks") or Y("nightmares")) else 0
    _reason(Y("trauma_avoid"), "تجنّب مرتبط بالحدث", ptsd_reasons); score_ptsd += 1 if Y("trauma_avoid") else 0
    _reason(Y("hypervigilance"), "يقظة مفرطة", ptsd_reasons);      score_ptsd += 1 if Y("hypervigilance") else 0
    if score_ptsd >= 4:
        pct = round(100*score_ptsd/max_ptsd)
        results.append(("اضطراب ما بعد الصدمة (PTSD)", f"{'، '.join(ptsd_reasons)} — تقدير {pct}%", float(score_ptsd)))

    # ====== 7) ثنائي القطب (احتمال) ======
    bp_reasons = []
    score_bp = 0; max_bp = 5
    _reason(Y("elevated_mood"), "نوبات مزاج مرتفع/مبالغ", bp_reasons); score_bp += 2 if Y("elevated_mood") else 0
    _reason(Y("impulsivity"), "اندفاع/تهوّر", bp_reasons);         score_bp += 1 if Y("impulsivity") else 0
    _reason(Y("grandiosity"), "شعور بالعظمة", bp_reasons);         score_bp += 1 if Y("grandiosity") else 0
    _reason(Y("decreased_sleep_need"), "قلة الحاجة للنوم", bp_reasons); score_bp += 1 if Y("decreased_sleep_need") else 0
    if score_bp >= 3:
        pct = round(100*score_bp/max_bp)
        results.append(("ثنائي القطب (احتمال)", f"{'، '.join(bp_reasons)} — تقدير {pct}%", float(score_bp)))

    # ====== 8) طيف الذهان/الفصام ======
    psych_reasons = []
    score_psy = 0; max_psy = 6
    _reason(Y("hallucinations"), "هلوسات", psych_reasons);         score_psy += 2 if Y("hallucinations") else 0
    _reason(Y("delusions"), "أوهام ثابتة", psych_reasons);         score_psy += 2 if Y("delusions") else 0
    _reason(Y("disorganized_speech"), "اضطراب تفكير/كلام", psych_reasons); score_psy += 1 if Y("disorganized_speech") else 0
    _reason(Y("functional_decline"), "تدهور وظيفي", psych_reasons); score_psy += 1 if Y("functional_decline") else 0
    if score_psy >= 4:
        pct = round(100*score_psy/max_psy)
        results.append(("ذهاني/طيف الفصام (احتمال)", f"{'، '.join(psych_reasons)} — تقدير {pct}%", float(score_psy)))

    # ====== 9) اضطرابات الأكل ======
    # فقدان الشهية
    an_reasons = []
    score_an = 0; max_an = 4
    _reason(Y("restriction"), "تقييد الأكل", an_reasons);          score_an += 2 if Y("restriction") else 0
    _reason(Y("body_image_distort"), "صورة جسد مشوّهة", an_reasons); score_an += 1 if Y("body_image_distort") else 0
    _reason(Y("underweight"), "نقص وزن", an_reasons);               score_an += 1 if Y("underweight") else 0
    if score_an >= 3:
        pct = round(100*score_an/max_an)
        results.append(("فقدان الشهية (احتمال)", f"{'، '.join(an_reasons)} — تقدير {pct}%", float(score_an)))

    # النهام العصبي
    bn_reasons = []
    score_bn = 0; max_bn = 4
    _reason(Y("binges"), "نوبات أكل كبيرة متكررة", bn_reasons);    score_bn += 2 if Y("binges") else 0
    _reason(Y("compensatory"), "سلوك تعويضي (تقيؤ/مسهلات/رياضة)", bn_reasons); score_bn += 2 if Y("compensatory") else 0
    if score_bn >= 3:
        pct = round(100*score_bn/max_bn)
        results.append(("نهام عصبي (احتمال)", f"{'، '.join(bn_reasons)} — تقدير {pct}%", float(score_bn)))

    # ====== 10) ADHD (مختصر للبالغين) ======
    adhd_reasons = []
    score_adhd = 0; max_adhd = 5
    _reason(Y("inattention"), "عدم انتباه", adhd_reasons);         score_adhd += 1 if Y("inattention") else 0
    _reason(Y("hyperactivity"), "فرط حركة", adhd_reasons);         score_adhd += 1 if Y("hyperactivity") else 0
    _reason(Y("impulsivity_symp"), "اندفاعية", adhd_reasons);      score_adhd += 1 if Y("impulsivity_symp") else 0
    _reason(Y("since_childhood"), "منذ الطفولة", adhd_reasons);     score_adhd += 1 if Y("since_childhood") else 0
    _reason(Y("functional_impair"), "تأثير وظيفي", adhd_reasons);   score_adhd += 1 if Y("functional_impair") else 0
    if score_adhd >= 3:
        pct = round(100*score_adhd/max_adhd)
        results.append(("ADHD (احتمال)", f"{'، '.join(adhd_reasons)} — تقدير {pct}%", float(score_adhd)))

    # ====== 11) تعاطي مواد ======
    sud_reasons = []
    score_sud = 0; max_sud = 4
    _reason(Y("craving"), "اشتهاء", sud_reasons);                   score_sud += 1 if Y("craving") else 0
    _reason(Y("tolerance"), "تحمّل", sud_reasons);                  score_sud += 1 if Y("tolerance") else 0
    _reason(Y("withdrawal"), "انسحاب", sud_reasons);                score_sud += 1 if Y("withdrawal") else 0
    _reason(Y("use_despite_harm"), "استمرار رغم الضرر", sud_reasons); score_sud += 1 if Y("use_despite_harm") else 0
    if score_sud >= 3:
        pct = round(100*score_sud/max_sud)
        results.append(("اضطراب تعاطي مواد (احتمال)", f"{'، '.join(sud_reasons)} — تقدير {pct}%", float(score_sud)))

    # لا توجد ترشيحات
    if not results:
        results.append(("لا توجد ترشيحات واضحة", "البيانات غير كافية — يُفضّل مراجعة مختص", 0.0))

    # ترتيب حسب الدرجة
    results.sort(key=lambda x: x[2], reverse=True)
    return results


def main():
    # تُستخدم هذه الصفحة كمرجع (كما أرسلت سابقًا من عندك).
    return """
    <h1>الدليل التشخيصي DSM-5 — نظرة منظمة</h1>
    <p>هذه نسخة مرجعية تعليمية. للاقتراح المبدئي استخدم "دراسة الحالة".</p>
    """
