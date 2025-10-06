# DSM.py — مرجع مُنظَّم + مُشخِّص أولي متوافق مع app.py (diagnose)

def main():
    return """
    <div class='card'>
      <h1>📘 مرجع DSM — منظم حسب الفئات</h1>
      <p class='small'>علاج نفسي افتراضي — قوائم مختصرة تساعدك على تنظيم الأعراض. يمكنك الطباعة أو حفظ الاختيارات كملف JSON.</p>

      <style>
        details{background:#fff;border:1px solid #eee;border-radius:12px;padding:10px;margin:10px 0}
        summary{cursor:pointer;font-weight:900;color:#4B0082}
        .grid{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
        label{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:8px}
        .note{margin-top:10px}
      </style>

      <div id="dsm">
        <details open>
          <summary>الاضطرابات المزاجية</summary>
          <div class="grid">
            <label><input type="checkbox" name="mdd"> نوبة اكتئابية جسيمة (MDD)</label>
            <label><input type="checkbox" name="pdd"> عسر المزاج (PDD)</label>
            <label><input type="checkbox" name="bipolar1"> ثنائي القطب I</label>
            <label><input type="checkbox" name="bipolar2"> ثنائي القطب II</label>
            <label><input type="checkbox" name="cyclothymic"> دوروية المزاج</label>
          </div>
        </details>

        <details>
          <summary>القلق والهلع والرهاب</summary>
          <div class="grid">
            <label><input type="checkbox" name="gad"> قلق معمّم (GAD)</label>
            <label><input type="checkbox" name="panic"> نوبات هلع</label>
            <label><input type="checkbox" name="social_anxiety"> قلق/رهاب اجتماعي</label>
            <label><input type="checkbox" name="specific_phobia"> رهاب محدد</label>
            <label><input type="checkbox" name="agoraphobia"> رهاب الأماكن المفتوحة/المزدحمة</label>
          </div>
        </details>

        <details>
          <summary>الوسواس القهري والصدمات</summary>
          <div class="grid">
            <label><input type="checkbox" name="ocd"> وسواس قهري (OCD)</label>
            <label><input type="checkbox" name="ptsd"> اضطراب ما بعد الصدمة (PTSD)</label>
            <label><input type="checkbox" name="asd"> اضطراب الكرب الحاد (ASD)</label>
          </div>
        </details>

        <details>
          <summary>طيف الفُصام والذهانات</summary>
          <div class="grid">
            <label><input type="checkbox" name="schizophrenia"> فُصام</label>
            <label><input type="checkbox" name="schizoaffective"> فصامي وجداني</label>
            <label><input type="checkbox" name="brief_psychotic"> ذهاني وجيز</label>
            <label><input type="checkbox" name="delusional"> اضطراب وهامي</label>
          </div>
        </details>

        <details>
          <summary>اضطرابات عصبية نمائية</summary>
          <div class="grid">
            <label><input type="checkbox" name="adhd"> فرط الحركة وتشتت الانتباه (ADHD)</label>
            <label><input type="checkbox" name="asd"> طيف التوحد (ASD)</label>
            <label><input type="checkbox" name="learning"> صعوبات تعلّم</label>
            <label><input type="checkbox" name="tic"> اضطرابات العرّات</label>
          </div>
        </details>

        <details>
          <summary>تعاطي المواد والإدمان</summary>
          <div class="grid">
            <label><input type="checkbox" name="alcohol"> كحول</label>
            <label><input type="checkbox" name="opioid"> أفيونات</label>
            <label><input type="checkbox" name="stimulant"> منبّهات</label>
            <label><input type="checkbox" name="cannabis"> قنّب</label>
            <label><input type="checkbox" name="sedative"> مهدئات/منوّمات</label>
          </div>
        </details>

        <div class="note">
          <button class="btn" onclick="window.print()">🖨️ طباعة</button>
          <button class="btn gold" onclick="saveDSM()">💾 حفظ JSON</button>
        </div>
      </div>

      <script>
        function saveDSM(){
          const root=document.getElementById('dsm'); const data={};
          root.querySelectorAll('input[type=checkbox]').forEach(cb=>data[cb.name]=cb.checked);
          const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
          const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='dsm_selection.json'; a.click();
          URL.revokeObjectURL(a.href);
        }
      </script>
    </div>
    """

def diagnose(form_data: dict):
    """
    تُعيد قائمة من ثلاثيات: (الاسم، السبب، درجة/100)
    تتوافق مع استدعاء app.py -> DSM.diagnose(data)
    """
    def has(*keys): return any(k in form_data for k in keys)
    def cnt(*keys): return sum(1 for k in keys if k in form_data)

    picks=[]

    # اكتئاب (مُراعاة PHQ-9 مبسّط)
    dep_core = cnt("low_mood","anhedonia")
    dep_more = cnt("fatigue","sleep_issue","appetite_change","psychomotor","worthlessness","poor_concentration","suicidal")
    dep_total = dep_core + dep_more
    dep_2w = "dep_2w" in form_data
    dep_fx = "dep_function" in form_data

    if dep_total >= 5 and dep_2w and dep_core >= 1:
        picks.append(("نوبة اكتئابية جسيمة (MDD)","≥5 أعراض لمدة ≥ أسبوعين مع تأثير وظيفي", 90 if dep_fx else 80))
    elif dep_total >= 3 and dep_2w:
        picks.append(("نوبة اكتئابية خفيفة/متوسطة","مجموعة أعراض مستمرة أسبوعين", 70))
    elif dep_core >=1 and dep_total >=2:
        picks.append(("مزاج منخفض/فتور","مجموعة أعراض مزاجية جزئية", 55))

    if "suicidal" in form_data:
        picks.append(("تنبيه أمان","وجود أفكار إيذاء/انتحار — يُفضّل تواصلًا فوريًا مع مختص", 99))

    # قلق
    if cnt("worry","tension")>=2:
        picks.append(("قلق معمّم","قلق مفرط مع توتر جسدي",75))
    if "panic_attacks" in form_data:
        picks.append(("نوبات هلع","نوبات مفاجئة مع خشية التكرار",70))
    if "social_fear" in form_data:
        picks.append(("قلق اجتماعي","خشية تقييم الآخرين وتجنّب",70))

    # وسواس/صدمات
    if "obsessions" in form_data and "compulsions" in form_data:
        picks.append(("وسواس قهري (OCD)","وساوس مع أفعال قهرية",80))
    if cnt("flashbacks","hypervigilance")>=2:
        picks.append(("آثار صدمة (PTSD/ASD)","استرجاعات ويقظة مفرطة",70))

    # مواد
    if cnt("craving","withdrawal","use_harm")>=2:
        picks.append(("تعاطي مواد","اشتهاء/انسحاب/استمرار رغم الضرر",80))

    # ذهانية/طيف الفصام
    psych_count = cnt("hallucinations","delusions","disorganized_speech","negative_symptoms","catatonia")
    dur_lt_1m  = "duration_lt_1m" in form_data
    dur_ge_1m  = "duration_ge_1m" in form_data
    dur_ge_6m  = "duration_ge_6m" in form_data
    decline    = "decline_function" in form_data

    if psych_count>=2 and (dur_ge_6m or (dur_ge_1m and decline)):
        picks.append(("فُصام","ذهانية أساسية مع استمرار/تدهور وظيفي",85))
    elif psych_count>=2 and dep_total>=3:
        picks.append(("فصامي وجداني","ذهانية مع كتلة مزاجية واضحة",75))
    elif psych_count>=2 and dur_lt_1m:
        picks.append(("اضطراب ذهاني وجيز","ذهانية قصيرة المدة",65))
    elif "delusions" in form_data and psych_count==1 and dur_ge_1m and not decline:
        picks.append(("اضطراب وهامي","أوهام ثابتة مع أداء وظيفي مقبول",60))

    return picks
