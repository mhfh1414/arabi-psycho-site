# DSM.py — موسّع (تعليمي) لتوليد ترشيحات تشخيصية مبدئية
# يقرأ الأعراض من /case ويرجع [(name, why, score)]
# ⚠️ للاستخدام التعليمي/الإرشادي فقط

from typing import Dict, List, Tuple

def _yes(v) -> bool:
    if v is True: return True
    s = str(v or "").strip().lower()
    return s in {"1","y","yes","on","true","صح","نعم"}

def _num(v, default=0.0) -> float:
    try: return float(v)
    except Exception: return default

def _add(flag: bool, text: str, bucket: list, w: int = 1):
    if flag:
        bucket.append(text)
        return w
    return 0

def diagnose(sym: Dict) -> List[Tuple[str, str, float]]:
    Y = lambda k: _yes(sym.get(k))
    N = lambda k, d=0.0: _num(sym.get(k, d), d)

    distress = N("distress", 0)
    results: List[Tuple[str, str, float]] = []

    # ========= اكتئاب جسيم =========
    r = []; s = 0; MAX = 10
    s += _add(Y("low_mood"), "مزاج منخفض", r, 3)
    s += _add(Y("anhedonia"), "فقدان المتعة", r, 3)
    s += _add(Y("sleep_issue"), "اضطراب نوم", r, 1)
    s += _add(Y("appetite_change"), "تغيّر شهية", r, 1)
    s += _add(Y("fatigue"), "إرهاق/خمول", r, 1)
    s += _add(distress >= 6, f"شدّة {int(distress)}/10", r, 1)
    if s >= 5:
        pct = round(100*s/MAX)
        results.append(("اكتئاب جسيم (MDD)", "، ".join(r) + f" — تقدير {pct}%", float(s)))

    # ========= القلق العام =========
    r = []; s = 0; MAX = 8
    s += _add(Y("worry"), "قلق مستمر/زائد", r, 3)
    s += _add(Y("tension"), "توتر جسدي", r, 1)
    s += _add(Y("focus_issue"), "تشتت/صعوبة تركيز", r, 1)
    s += _add(Y("restlessness"), "تململ", r, 1)
    s += _add(distress >= 6, f"ضيق {int(distress)}/10", r, 1)
    # ترجيح إذا لا توجد أعراض مزاج مرتفع أو ذهان
    if not (Y("elevated_mood") or Y("hallucinations") or Y("delusions")):
        s += _add(True, "لا دلائل على ذهان/هوس", r, 1)
    if s >= 4:
        pct = round(100*s/MAX)
        results.append(("اضطراب القلق العام (GAD)", "، ".join(r) + f" — تقدير {pct}%", float(s)))

    # ========= نوبات الهلع =========
    r = []; s = 0; MAX = 6
    s += _add(Y("panic_attacks"), "نوبات هلع متكررة", r, 3)
    s += _add(Y("fear_of_attacks"), "قلق توقعي بعد النوبات", r, 2)
    s += _add(Y("panic_avoidance"), "سلوك تجنبي مرتبط", r, 1)
    if s >= 4:
        pct = round(100*s/MAX)
        results.append(("اضطراب الهلع", "، ".join(r) + f" — تقدير {pct}%", float(s)))

    # ========= رهاب اجتماعي =========
    r = []; s = 0; MAX = 6
    s += _add(Y("social_avoid"), "تجنب اجتماعي", r, 2)
    s += _add(Y("fear_judgment"), "خوف من تقييم الآخرين", r, 2)
    s += _add(distress >= 5, f"ضيق {int(distress)}/10", r, 1)
    if s >= 4:
        pct = round(100*s/MAX)
        results.append(("رهاب اجتماعي", "، ".join(r) + f" — تقدير {pct}%", float(s)))

    # ========= وسواس قهري =========
    r = []; s = 0; MAX = 7
    s += _add(Y("obsessions"), "أفكار ملحّة/اجترار", r, 3)
    s += _add(Y("compulsions"), "أفعال قهرية", r, 3)
    s += _add(distress >= 5, f"ضيق {int(distress)}/10", r, 1)
    if s >= 5:
        pct = round(100*s/MAX)
        results.append(("وسواس قهري (OCD)", "، ".join(r) + f" — تقدير {pct}%", float(s)))

    # ========= PTSD =========
    r = []; s = 0; MAX = 7
    s += _add(Y("trauma_event"), "تعرّض لحدث صادمي", r, 3)
    s += _add(Y("flashbacks") or Y("nightmares"), "استرجاع/كوابيس", r, 2)
    s += _add(Y("trauma_avoid"), "تجنّب مرتبط بالحدث", r, 1)
    s += _add(Y("hypervigilance"), "يقظة مفرطة", r, 1)
    if s >= 5:
        pct = round(100*s/MAX)
        results.append(("اضطراب ما بعد الصدمة (PTSD)", "، ".join(r) + f" — تقدير {pct}%", float(s)))

    # ========= ثنائي القطب =========
    r = []; s = 0; MAX = 7
    s += _add(Y("elevated_mood"), "مزاج مرتفع/مبالغ", r, 3)
    s += _add(Y("grandiosity"), "شعور بالعظمة", r, 1)
    s += _add(Y("impulsivity"), "اندفاع/تهوّر", r, 1)
    s += _add(Y("decreased_sleep_need"), "قلة الحاجة للنوم", r, 1)
    # استبعاد: إذا اكتئاب شديد بدون علامات هوس، يقلل الترجيح
    if Y("low_mood") and Y("anhedonia") and not Y("elevated_mood"):
        s -= 1
    if s >= 4:
        pct = round(max(0, 100*s/MAX))
        results.append(("اضطراب ثنائي القطب", "، ".join(r) + f" — تقدير {pct}%", float(s)))

    # ========= ذهان/فصام =========
    r = []; s = 0; MAX = 8
    s += _add(Y("hallucinations"), "هلوسات", r, 3)
    s += _add(Y("delusions"), "أوهام ثابتة", r, 3)
    s += _add(Y("disorganized_speech"), "تفكير/كلام غير منظّم", r, 1)
    s += _add(Y("functional_decline"), "تدهور وظيفي", r, 1)
    if s >= 5:
        pct = round(100*s/MAX)
        results.append(("ذهان/طيف الفصام", "، ".join(r) + f" — تقدير {pct}%", float(s)))

    # ========= اضطرابات الأكل (مختصر) =========
    if ( _yes(sym.get("restriction")) and _yes(sym.get("underweight")) and _yes(sym.get("body_image_distort")) ):
        results.append(("اضطراب أكل (اتجاه فقدان/تقييد)", "تقييد + نقص وزن + صورة جسد مشوهة", 4.0))
    elif ( _yes(sym.get("binges")) and _yes(sym.get("compensatory")) ):
        results.append(("اضطراب أكل (نوبات أكل/تعويض)", "نوبات أكل مع سلوك تعويضي", 3.0))

    # ========= ADHD =========
    r = []; s = 0; MAX = 6
    s += _add(_yes(sym.get("inattention")), "عدم انتباه", r, 1)
    s += _add(_yes(sym.get("hyperactivity")), "فرط حركة", r, 1)
    s += _add(_yes(sym.get("impulsivity_symp")), "اندفاعية", r, 1)
    s += _add(_yes(sym.get("since_childhood")), "منذ الطفولة", r, 2)
    s += _add(_yes(sym.get("functional_impair")), "تأثير وظيفي", r, 1)
    if s >= 4:
        pct = round(100*s/MAX)
        results.append(("اضطراب فرط الحركة/تشتت الانتباه (ADHD)", "، ".join(r) + f" — تقدير {pct}%", float(s)))

    # ========= تعاطي مواد =========
    r = []; s = 0; MAX = 6
    s += _add(_yes(sym.get("craving")), "اشتهاء", r, 1)
    s += _add(_yes(sym.get("tolerance")), "تحمّل", r, 2)
    s += _add(_yes(sym.get("withdrawal")), "انسحاب", r, 2)
    s += _add(_yes(sym.get("use_despite_harm")), "استمرار رغم الضرر", r, 1)
    if s >= 4:
        pct = round(100*s/MAX)
        results.append(("اضطراب تعاطي مواد", "، ".join(r) + f" — تقدير {pct}%", float(s)))

    if not results:
        results.append(("لا ترشيحات كافية", "الأعراض الحالية غير كافية — يُنصح بمراجعة مختص", 0.0))

    results.sort(key=lambda x: x[2], reverse=True)
    return results

def main():
    # نسخة موجزة من المرجع (واجهة مرتبة قابلة للطباعة/الحفظ)
    return """
    <h1>الدليل التشخيصي DSM-5 — مرجع مبسط</h1>
    <p class="muted">هذه النسخة للتعليم والإرشاد فقط.</p>
    <style>
      details{background:#fff;border:1px solid #eee;border-radius:12px;margin:10px 0;padding:10px}
      summary{cursor:pointer;font-weight:800;color:#4B0082}
      .grid{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
      label{display:block;background:#fafafa;border:1px solid #f2f2f2;border-radius:8px;padding:8px}
      .btn{margin-top:10px;padding:8px 12px;border-radius:10px;border:0;background:#4B0082;color:#fff;font-weight:700}
      .btn.gold{background:#FFD700;color:#4B0082}
      textarea{width:100%;min-height:90px}
    </style>
    <div id="ref">
      <details open>
        <summary>الاضطرابات القلقية</summary>
        <div class="grid">
          <label><input type="checkbox"> قلق عام (GAD)</label>
          <label><input type="checkbox"> هلع</label>
          <label><input type="checkbox"> رهاب اجتماعي</label>
          <label><input type="checkbox"> وسواس قهري</label>
          <label><input type="checkbox"> ما بعد الصدمة</label>
        </div>
      </details>
      <details><summary>المزاجية/الذهانية</summary>
        <div class="grid">
          <label><input type="checkbox"> اكتئاب جسيم</label>
          <label><input type="checkbox"> ثنائي القطب</label>
          <label><input type="checkbox"> طيف الفصام</label>
        </div>
      </details>
      <details><summary>أخرى</summary>
        <div class="grid">
          <label><input type="checkbox"> ADHD</label>
          <label><input type="checkbox"> اضطرابات أكل</label>
          <label><input type="checkbox"> تعاطي مواد</label>
        </div>
      </details>

      <h3>ملاحظات</h3>
      <textarea placeholder="ملاحظات تشخيصية…"></textarea><br>
      <button class="btn" onclick="window.print()">طباعة</button>
      <button class="btn gold" onclick="save()">حفظ JSON</button>
    </div>
    <script>
      function save(){ const data={{}};
        document.querySelectorAll('#ref input[type=checkbox]').forEach((c,i)=>data['item'+i]=c.checked);
        const blob=new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}});
        const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='dsm_ref.json'; a.click(); URL.revokeObjectURL(a.href);
      }
    </script>
    """
