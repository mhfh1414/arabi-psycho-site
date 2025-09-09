# ------------------------ إعدادات القرار الدقيق ------------------------
CRITICAL_SYM = { normalize("هلوسة"), normalize("اوهام"), normalize("نوبة هلع"), normalize("تفكير انتحاري") }
MIN_OK   = 2.2    # أقل درجة نقبل عندها تشخيص واحد
MARGIN   = 0.60   # الفارق الأدنى بين الأول والثاني لاعتباره “حاسمًا”

PSYCHOSIS_HINTS = { normalize("هلوسة"), normalize("اوهام"), normalize("ضلالات") }
PANIC_HINTS     = { normalize("نوبة هلع"), normalize("خفقان"), normalize("اختناق") }
OCD_HINTS       = { normalize("وسواس"), normalize("سلوك قهري"), normalize("تفقد متكرر"), normalize("غسل متكرر") }

def _gate_candidates(text_norm: str):
    """تصفية مبكرة: تحديد مجموعة التشاخيص المحتملة لتسريع ودقة المطابقة."""
    has_psy  = any(h in text_norm for h in PSYCHOSIS_HINTS)
    has_panic= any(h in text_norm for h in PANIC_HINTS)
    has_ocd  = any(h in text_norm for h in OCD_HINTS)
    if has_psy:
        allow = {"فصام","اضطراب فصامي عاطفي","اضطراب وهامي","ذُهان وجيز","فُصام شكلي"}
        return {k:v for k,v in DSM.items() if k in allow}
    if has_panic:
        allow = {"اضطراب الهلع","رهاب الساحة","اضطراب القلق العام","رهاب اجتماعي","رهاب محدد"}
        return {k:v for k,v in DSM.items() if k in allow}
    if has_ocd:
        allow = {"اضطراب الوسواس القهري","تشوه صورة الجسد","اكتناز","اضطراب نتف الشعر","اضطراب قشط الجلد"}
        return {k:v for k,v in DSM.items() if k in allow}
    # لا مؤشرات بوابة: ابقِ الكل
    return DSM

def _boost_text_with_synonyms(text_norm: str) -> str:
    """تعزيز النص بمرادفات عند ظهور أي مفتاح أساسي."""
    out = [text_norm]
    for base, syns in SYNONYMS.items():
        norm_base = normalize(base)
        if norm_base in text_norm or any(normalize(s) in text_norm for s in syns):
            out.append(" ".join(normalize(s) for s in ([base] + syns)))
    return " ".join(out)

def _severity_multipliers(duration_days: str, history: str):
    try: dur = float(duration_days or 0)
    except: dur = 0.0
    durB = 1.25 if dur>=365 else 1.15 if dur>=90 else 1.08 if dur>=30 else 1.0
    hist = normalize(history or "")
    fxB  = 1.10 if any(k in hist for k in ["مشاكل عمل","مشاكل زواج","طلاق","تعثر دراسي","غياب متكرر","قضيه"]) else 1.0
    return durB, fxB

def _contradiction_penalty(text_norm: str, dx_name: str) -> float:
    """خصم بسيط عند تعارضات شائعة (اختياري)."""
    # مثال: قهم عصبي دون أي ذكر لنقص وزن/خوف من زيادة الوزن
    if dx_name == "قهم عصبي":
        if normalize("نقص وزن شديد") not in text_norm and normalize("خوف من زياده الوزن") not in text_norm:
            return 0.85
    return 1.0

def diagnose_one(symptoms: str, age: str="", gender: str="", duration_days: str="", history: str=""):
    """ترجع تشخيصًا واحدًا إن كان واثقًا، وإلا ترجع None مع أسباب/تلميحات."""
    base_text = normalize(symptoms or "")
    if not base_text or len(base_text) < 3:
        return None, {"reason":"النص فارغ أو قصير جدًا","hints":["اكتب أعراضًا صريحة مثل: هلوسة/نوبة هلع/وسواس/أرق/نهم..."]}

    text = _boost_text_with_synonyms(base_text)
    durB, fxB = _severity_multipliers(duration_days, history)

    # تصفية مبكرة
    candidates = _gate_candidates(text)

    scored = []
    for dx, meta in candidates.items():
        req = meta["req"]
        # تحقق المطلوبات بدقة/تقارب
        if req and not all((r in text) or (similarity(text, r)>=0.65) for r in req):
            continue

        s = 0.0; hits=[]
        for raw_kw, kw in zip(meta["kwr"], meta["kwn"]):
            if kw in text:
                w = 1.0
                if kw in CRITICAL_SYM:
                    w = 1.9
                s += w; hits.append(raw_kw)
            else:
                sim = similarity(text, kw)
                if sim >= 0.70:
                    s += 0.85; hits.append(raw_kw+"~")
                elif sim >= 0.45:
                    s += 0.45

        if s == 0: 
            continue

        # أوزان التشخيص نفسه + المدة/الأثر + خصم التعارض
        s *= meta["w"]
        s *= durB * fxB
        s *= _contradiction_penalty(text, dx)

        # ملاحظة: استبعاد تضادات مذكورة في الداتا (إن وجدت)
        # (إذا أضفت "exclusions" في DSM_DB، طبّقها هنا)

        scored.append({"name": dx, "score": round(s,3), "hits": hits[:14]})

    if not scored:
        return None, {"reason":"لا توجد مطابقة كافية","hints":["أدخل مفردات أوضح، ومدة الأعراض، وأثرها على العمل/الدراسة.","أمثلة: هلوسة/أوهام (للذهان)، نوبة هلع، وسواس + طقوس، انعدام المتعة + حزن (للاكتئاب)."]}

    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0]
    second = scored[1]["score"] if len(scored)>1 else 0.0

    if best["score"] >= MIN_OK and (best["score"] - second) >= MARGIN:
        # قرار حاسم
        conf = min(0.99, 0.55 + 0.15*(best["score"]-MIN_OK))  # تقريب ثقة مبسّط
        return {"name":best["name"],"confidence":round(conf,2),"score":best["score"],"hits":best["hits"]}, None

    # غير حاسم: أعرض أقرب اثنين كتغذية راجعة، بدون تعدد تشخيص نهائي
    tips = [f"اقترب من: {scored[0]['name']} (درجة {scored[0]['score']})",
            f"والثاني: {scored[1]['name'] if len(scored)>1 else '—'}"]
    return None, {"reason":"الفارق بين الاحتمالات صغير","hints":tips}

# ---------- صفحة النتيجة الواحدة (استبدل دالة dsm_result_page القديمة بهذا الإصدار) ----------
def dsm_result_page(form):
    name     = (form.get("name","") or "").strip()
    age      = (form.get("age","") or "").strip()
    gender   = (form.get("gender","") or "").strip()
    duration = (form.get("duration","") or "").strip()
    symptoms = (form.get("symptoms","") or "").strip()
    history  = (form.get("history","") or "").strip()

    win, why = diagnose_one(symptoms, age=age, gender=gender, duration_days=duration, history=history)

    if win:
        res_html = f"""
        <div class="result">
          <h3>✅ التشخيص المرجّح (نهائي واحد)</h3>
          <div style="margin:.5rem 0">
            <span class="badge ok">ثقة: {int(win['confidence']*100)}%</span>
            <span class="badge" style="background:#2563eb;color:#fff">درجة داخلية: {win['score']}</span>
          </div>
          <p><b>{win['name']}</b></p>
          <details style="margin-top:.5rem"><summary>المؤشرات التي دعمت القرار</summary>
            <div style="opacity:.9;margin-top:.5rem">{", ".join(win['hits'])}</div>
          </details>
          <p style="opacity:.8;margin-top:.6rem">⚠️ ناتج مساعد مبني على الأعراض المدخلة، لا يغني عن تقييم متخصص.</p>
        </div>
        """
    else:
        # why يحتوي سببًا وتلميحات دقيقة
        hints = "".join(f"<li>{h}</li>" for h in why.get("hints",[]))
        res_html = f"""
        <div class="result">
          <h3>🚧 لا يمكن إخراج تشخيص واحد بثقة</h3>
          <p><span class="badge warn">{why.get('reason','')}</span></p>
          <ul>{hints}</ul>
          <p style="opacity:.85">جرّب إضافة كلمات سريرية أدق، أو تحديد المدة، أو الأثر الوظيفي.</p>
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
            <button class="btn" type="submit">تشخيص نهائي واحد</button>
            <a class="btn" href="/">الواجهة</a>
          </div>
        </form>
      </section>
      {res_html}
    </div>
    """
    return render_template_string(DSM_PAGE, body=body)
