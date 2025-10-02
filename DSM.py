# DSM.py — مرجع + تشخيص مبدئي موسّع (تعليمي)

from typing import Dict, List, Tuple

# -------- أدوات مساعدة --------
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

# -------- دالة التشخيص --------
def diagnose(symptoms: Dict) -> List[Tuple[str, str, float]]:
    """
    ترجع قائمة [(اسم التشخيص، السبب المختصر، درجة)] — تعليمية وليست تشخيصًا طبيًا.
    """
    Y = lambda k: _yes(symptoms.get(k))
    V = lambda k, d=0.0: _num(symptoms.get(k, d), d)

    results: List[Tuple[str,str,float]] = []
    distress = V("distress", 0)

    # ==== مزاجية ====
    # MDD
    score_mdd = (2*Y("low_mood")) + (2*Y("anhedonia")) + Y("sleep_issue") + Y("appetite_change") + Y("fatigue") + (1 if distress>=6 else 0)
    if score_mdd >= 4:
        results.append(("اكتئاب جسيم (MDD)", "مزاج منخفض/فقد متعة مع اضطراب نوم/شهية وضيق ملحوظ", float(score_mdd)))

    # Bipolar (احتمال)
    score_bip = (2*Y("elevated_mood")) + Y("impulsivity") + Y("grandiosity") + Y("decreased_sleep_need")
    if score_bip >= 3:
        results.append(("ثنائي القطب (احتمال)", "مزاج مرتفع + اندفاع/عظمة + قلة حاجة للنوم", float(score_bip)))

    # ==== قلق ====
    # GAD
    score_gad = (2*Y("worry")) + Y("tension") + Y("focus_issue") + Y("restlessness") + (1 if distress>=6 else 0)
    if score_gad >= 4:
        results.append(("اضطراب القلق العام (GAD)", "قلق متواصل مع توتر/تشتت وتأثير وظيفي", float(score_gad)))

    # Panic
    score_panic = (2*Y("panic_attacks")) + Y("fear_of_attacks") + Y("panic_avoidance")
    if score_panic >= 3:
        results.append(("اضطراب الهلع", "نوبات مفاجئة + قلق من تكرارها + تجنّب", float(score_panic)))

    # Social Anxiety
    score_social = (2*Y("social_avoid")) + Y("fear_judgment") + (1 if distress>=5 else 0)
    if score_social >= 3:
        results.append(("قلق/رهاب اجتماعي", "تجنب اجتماعي وخوف من تقييم الآخرين مع ضيق", float(score_social)))

    # ==== وسواس/صدمات ====
    # OCD
    score_ocd = (2*Y("obsessions")) + (2*Y("compulsions")) + (1 if distress>=5 else 0)
    if score_ocd >= 4:
        results.append(("وسواس قهري (OCD)", "أفكار ملحّة مع أفعال قهرية وضيق", float(score_ocd)))

    # PTSD
    score_ptsd = (2*Y("trauma_event")) + (1 if (Y("flashbacks") or Y("nightmares")) else 0) + Y("trauma_avoid") + Y("hypervigilance")
    if score_ptsd >= 4:
        results.append(("اضطراب ما بعد الصدمة (PTSD)", "حدث صادمي + استرجاع/كوابيس + تجنّب + يقظة", float(score_ptsd)))

    # ==== ذهانات/طيف الفصام ====
    score_psych = (2*Y("hallucinations")) + (2*Y("delusions")) + Y("disorganized_speech") + Y("functional_decline")
    if score_psych >= 4:
        results.append(("ذهاني/طيف الفصام (احتمال)", "هلاوس/أوهام مع اضطراب تفكير/تدهور وظيفي", float(score_psych)))

    # ==== أكل ====
    score_an = (2*Y("restriction")) + Y("body_image_distort") + Y("underweight")
    if score_an >= 3:
        results.append(("فقدان الشهية (احتمال)", "تقييد أكل + صورة جسد مشوهة + نقص وزن", float(score_an)))

    score_bn = (2*Y("binges")) + Y("compensatory")
    if score_bn >= 3:
        results.append(("نهام عصبي (احتمال)", "نوبات أكل كبيرة مع سلوك تعويضي", float(score_bn)))

    # ==== ADHD (مختصر) ====
    score_adhd = Y("inattention") + Y("hyperactivity") + Y("impulsivity_symp") + Y("since_childhood") + Y("functional_impair")
    if score_adhd >= 3:
        results.append(("ADHD (احتمال)", "عدم انتباه/فرط حركة منذ الطفولة وتأثير وظيفي", float(score_adhd)))

    # ==== تعاطي مواد ====
    score_sud = Y("craving") + Y("tolerance") + Y("withdrawal") + Y("use_despite_harm")
    if score_sud >= 3:
        results.append(("اضطراب تعاطي مواد (احتمال)", "اشتهاء/تحمّل/انسحاب أو استمرار رغم الضرر", float(score_sud)))

    # لا شيء واضح
    if not results:
        results.append(("لا توجد ترشيحات واضحة", "البيانات غير كافية — يُفضّل مراجعة مختص", 0.0))

    # ترتيب تنازلي بالدرجة
    results.sort(key=lambda x: x[2], reverse=True)
    return results

# -------- صفحة مرجعية (HTML) --------
def main():
    return """
    <h1>الدليل التشخيصي DSM-5 — نظرة منظمة</h1>
    <p>هذه نسخة مرجعية تعليمية. للاقتراح المبدئي استخدم "دراسة الحالة".</p>

    <style>
      details{background:#fff; border:1px solid #ddd; border-radius:10px; margin:10px 0; padding:10px}
      summary{cursor:pointer; font-weight:700; color:#4B0082}
      .note{width:100%; min-height:70px}
      .action{margin:12px 6px 0 0; padding:8px 12px; border-radius:10px; border:0; background:#4B0082; color:#fff; font-weight:700}
      .action.gold{background:#FFD700; color:#4B0082}
      .grid{display:grid; gap:8px; grid-template-columns: repeat(auto-fit, minmax(220px,1fr));}
      label{display:block; background:#fafafa; border:1px solid #eee; border-radius:8px; padding:8px}
    </style>

    <div id="dsm">
      <details open>
        <summary>الاضطرابات العصابية/القلقية</summary>
        <div class="grid">
          <label><input type="checkbox" name="anxiety_gad"> اضطراب القلق العام (GAD)</label>
          <label><input type="checkbox" name="panic"> اضطراب الهلع</label>
          <label><input type="checkbox" name="phobia"> الرهاب المحدد</label>
          <label><input type="checkbox" name="social"> قلق/رهاب اجتماعي</label>
          <label><input type="checkbox" name="ocd"> الوسواس القهري (OCD)</label>
          <label><input type="checkbox" name="ptsd"> اضطراب ما بعد الصدمة (PTSD)</label>
        </div>
      </details>

      <details>
        <summary>الاضطرابات المزاجية</summary>
        <div class="grid">
          <label><input type="checkbox" name="mdd"> اكتئاب جسيم (MDD)</label>
          <label><input type="checkbox" name="pdd"> عسر المزاج (PDD)</label>
          <label><input type="checkbox" name="bipolar1"> ثنائي القطب I</label>
          <label><input type="checkbox" name="bipolar2"> ثنائي القطب II</label>
          <label><input type="checkbox" name="cyclothymic"> دوروية المزاج</label>
        </div>
      </details>

      <details>
        <summary>اضطرابات الشخصية</summary>
        <div class="grid">
          <label><input type="checkbox" name="paranoid"> شخصية زورانية</label>
          <label><input type="checkbox" name="schizoid"> انعزالية</label>
          <label><input type="checkbox" name="schizotypal"> فصامية نمط</label>
          <label><input type="checkbox" name="antisocial"> معادية للمجتمع</label>
          <label><input type="checkbox" name="borderline"> حدّية</label>
          <label><input type="checkbox" name="histrionic"> هستيرية</label>
          <label><input type="checkbox" name="narcissistic"> نرجسية</label>
          <label><input type="checkbox" name="avoidant"> تجنبية</label>
          <label><input type="checkbox" name="dependent"> اعتمادية</label>
          <label><input type="checkbox" name="ocpd"> قسرية-قهريّة شخصية</label>
        </div>
      </details>

      <details>
        <summary>اضطرابات طيف الفصام</summary>
        <div class="grid">
          <label><input type="checkbox" name="schizophrenia"> فصام</label>
          <label><input type="checkbox" name="schizoaffective"> فصامي وجداني</label>
          <label><input type="checkbox" name="brief_psychotic"> ذهان وجيز</label>
          <label><input type="checkbox" name="delusional"> وهامي</label>
        </div>
      </details>

      <details>
        <summary>اضطرابات عصبية نمائية</summary>
        <div class="grid">
          <label><input type="checkbox" name="adhd"> فرط الحركة وتشتت الانتباه (ADHD)</label>
          <label><input type="checkbox" name="asd"> طيف التوحد (ASD)</label>
          <label><input type="checkbox" name="learning"> صعوبات تعلّم</label>
          <label><input type="checkbox" name="tic"> اضطرابات العرات/تورات</label>
        </div>
      </details>

      <details>
        <summary>تعاطي المواد والإدمان</summary>
        <div class="grid">
          <label><input type="checkbox" name="alcohol"> اضطراب تعاطي الكحول</label>
          <label><input type="checkbox" name="opioid"> أفيونات</label>
          <label><input type="checkbox" name="stimulant"> منبهات</label>
          <label><input type="checkbox" name="cannabis"> قنّب</label>
          <label><input type="checkbox" name="sedative"> مهدئات/منومات</label>
        </div>
      </details>

      <h3>ملاحظات تشخيصية</h3>
      <textarea class="note" name="notes" placeholder="ضع المبررات ودليل الأعراض والمدة والاستبعاد التفريقي..."></textarea><br>
      <button class="action" onclick="window.print()">طباعة</button>
      <button class="action gold" onclick="saveDSM()">حفظ JSON</button>
    </div>

    <script>
      function saveDSM(){
        const root = document.getElementById('dsm');
        const data = {};
        root.querySelectorAll('input[type=checkbox]').forEach(cb=>{
          data[cb.name] = cb.checked;
        });
        data['notes'] = root.querySelector('textarea[name=notes]').value || '';
        const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'dsm_selection.json';
        a.click();
        URL.revokeObjectURL(a.href);
      }
    </script>
    """
