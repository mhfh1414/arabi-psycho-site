# DSM.py — موسّع (تعليمي) لتوليد ترشيحات تشخيصية مبدئية
# يقرأ الأعراض من /case ويرجع قائمة [(name, why, score)]
# ⚠️ للاستخدام التعليمي/الإرشادي فقط — ليس تشخيصًا طبيًا

from typing import Dict, List, Tuple

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

def diagnose(symptoms: Dict) -> List[Tuple[str, str, float]]:
    Y = lambda k: _yes(symptoms.get(k))
    V = lambda k, d=0.0: _num(symptoms.get(k, d), d)

    results: List[Tuple[str, str, float]] = []
    distress = V("distress", 0)

    # ===== اكتئاب جسيم =====
    reasons = []
    score = 0; max_score = 8
    _reason(Y("low_mood"), "مزاج منخفض", reasons); score += 2 if Y("low_mood") else 0
    _reason(Y("anhedonia"), "فقدان المتعة", reasons); score += 2 if Y("anhedonia") else 0
    _reason(Y("sleep_issue"), "اضطراب نوم", reasons); score += 1 if Y("sleep_issue") else 0
    _reason(Y("appetite_change"), "تغير شهية", reasons); score += 1 if Y("appetite_change") else 0
    _reason(Y("fatigue"), "إرهاق", reasons); score += 1 if Y("fatigue") else 0
    if distress >= 6:
        _reason(True, f"شدّة {int(distress)}/10", reasons); score += 1
    if score >= 4:
        pct = round(100*score/max_score)
        results.append(("اكتئاب جسيم (MDD)", f"{'، '.join(reasons)} — تقدير {pct}%", float(score)))

    # ===== القلق العام =====
    reasons = []
    score = 0; max_score = 6
    _reason(Y("worry"), "قلق مستمر", reasons); score += 2 if Y("worry") else 0
    _reason(Y("tension"), "توتر جسدي", reasons); score += 1 if Y("tension") else 0
    _reason(Y("focus_issue"), "تشتت", reasons); score += 1 if Y("focus_issue") else 0
    _reason(Y("restlessness"), "تململ", reasons); score += 1 if Y("restlessness") else 0
    if distress >= 6:
        _reason(True, f"ضيق {int(distress)}/10", reasons); score += 1
    if score >= 4:
        pct = round(100*score/max_score)
        results.append(("اضطراب القلق العام (GAD)", f"{'، '.join(reasons)} — تقدير {pct}%", float(score)))

    # ===== الهلع =====
    reasons = []
    score = 0; max_score = 4
    _reason(Y("panic_attacks"), "نوبات هلع", reasons); score += 2 if Y("panic_attacks") else 0
    _reason(Y("fear_of_attacks"), "خوف من النوبات", reasons); score += 1 if Y("fear_of_attacks") else 0
    _reason(Y("panic_avoidance"), "سلوك تجنبي", reasons); score += 1 if Y("panic_avoidance") else 0
    if score >= 3:
        pct = round(100*score/max_score)
        results.append(("اضطراب الهلع", f"{'، '.join(reasons)} — تقدير {pct}%", float(score)))

    # ===== قلق/رهاب اجتماعي =====
    reasons = []
    score = 0; max_score = 4
    _reason(Y("social_avoid"), "تجنب اجتماعي", reasons); score += 2 if Y("social_avoid") else 0
    _reason(Y("fear_judgment"), "خوف من تقييم الآخرين", reasons); score += 1 if Y("fear_judgment") else 0
    if distress >= 5:
        _reason(True, f"ضيق {int(distress)}/10", reasons); score += 1
    if score >= 3:
        pct = round(100*score/max_score)
        results.append(("رهاب اجتماعي", f"{'، '.join(reasons)} — تقدير {pct}%", float(score)))

    # ===== وسواس قهري =====
    reasons = []
    score = 0; max_score = 5
    _reason(Y("obsessions"), "أفكار ملحّة", reasons); score += 2 if Y("obsessions") else 0
    _reason(Y("compulsions"), "أفعال قهرية", reasons); score += 2 if Y("compulsions") else 0
    if distress >= 5:
        _reason(True, f"ضيق {int(distress)}/10", reasons); score += 1
    if score >= 4:
        pct = round(100*score/max_score)
        results.append(("وسواس قهري (OCD)", f"{'، '.join(reasons)} — تقدير {pct}%", float(score)))

    # ===== PTSD =====
    reasons = []
    score = 0; max_score = 5
    _reason(Y("trauma_event"), "حدث صادمي", reasons); score += 2 if Y("trauma_event") else 0
    _reason(Y("flashbacks") or Y("nightmares"), "استرجاع/كوابيس", reasons); score += 1 if (Y("flashbacks") or Y("nightmares")) else 0
    _reason(Y("trauma_avoid"), "تجنب", reasons); score += 1 if Y("trauma_avoid") else 0
    _reason(Y("hypervigilance"), "يقظة مفرطة", reasons); score += 1 if Y("hypervigilance") else 0
    if score >= 4:
        pct = round(100*score/max_score)
        results.append(("اضطراب ما بعد الصدمة (PTSD)", f"{'، '.join(reasons)} — تقدير {pct}%", float(score)))

    # ===== ثنائي القطب =====
    reasons = []
    score = 0; max_score = 5
    _reason(Y("elevated_mood"), "مزاج مرتفع", reasons); score += 2 if Y("elevated_mood") else 0
    _reason(Y("impulsivity"), "اندفاع", reasons); score += 1 if Y("impulsivity") else 0
    _reason(Y("grandiosity"), "شعور بالعظمة", reasons); score += 1 if Y("grandiosity") else 0
    _reason(Y("decreased_sleep_need"), "قلة نوم", reasons); score += 1 if Y("decreased_sleep_need") else 0
    if score >= 3:
        pct = round(100*score/max_score)
        results.append(("ثنائي القطب", f"{'، '.join(reasons)} — تقدير {pct}%", float(score)))

    # ===== فصام/ذهان =====
    reasons = []
    score = 0; max_score = 6
    _reason(Y("hallucinations"), "هلوسات", reasons); score += 2 if Y("hallucinations") else 0
    _reason(Y("delusions"), "أوهام", reasons); score += 2 if Y("delusions") else 0
    _reason(Y("disorganized_speech"), "اضطراب تفكير", reasons); score += 1 if Y("disorganized_speech") else 0
    _reason(Y("functional_decline"), "تدهور وظيفي", reasons); score += 1 if Y("functional_decline") else 0
    if score >= 4:
        pct = round(100*score/max_score)
        results.append(("ذهان/فصام", f"{'، '.join(reasons)} — تقدير {pct}%", float(score)))

    # ===== ADHD =====
    reasons = []
    score = 0; max_score = 5
    _reason(Y("inattention"), "عدم انتباه", reasons); score += 1 if Y("inattention") else 0
    _reason(Y("hyperactivity"), "فرط حركة", reasons); score += 1 if Y("hyperactivity") else 0
    _reason(Y("impulsivity_symp"), "اندفاعية", reasons); score += 1 if Y("impulsivity_symp") else 0
    _reason(Y("since_childhood"), "منذ الطفولة", reasons); score += 1 if Y("since_childhood") else 0
    _reason(Y("functional_impair"), "تأثير وظيفي", reasons); score += 1 if Y("functional_impair") else 0
    if score >= 3:
        pct = round(100*score/max_score)
        results.append(("ADHD", f"{'، '.join(reasons)} — تقدير {pct}%", float(score)))

    # ===== تعاطي مواد =====
    reasons = []
    score = 0; max_score = 4
    _reason(Y("craving"), "اشتهاء", reasons); score += 1 if Y("craving") else 0
    _reason(Y("tolerance"), "تحمّل", reasons); score += 1 if Y("tolerance") else 0
    _reason(Y("withdrawal"), "انسحاب", reasons); score += 1 if Y("withdrawal") else 0
    _reason(Y("use_despite_harm"), "استخدام رغم الضرر", reasons); score += 1 if Y("use_despite_harm") else 0
    if score >= 3:
        pct = round(100*score/max_score)
        results.append(("اضطراب تعاطي مواد", f"{'، '.join(reasons)} — تقدير {pct}%", float(score)))

    if not results:
        results.append(("لا ترشيحات", "الأعراض غير كافية — راجع مختص", 0.0))

    results.sort(key=lambda x: x[2], reverse=True)
    return results

def main():
    return """
    <h1>الدليل التشخيصي DSM-5 — نسخة مبسطة</h1>
    <p>هذه النسخة للتعليم والإرشاد فقط. للاستخدام السريري راجع النسخة الكاملة.</p>
    """
