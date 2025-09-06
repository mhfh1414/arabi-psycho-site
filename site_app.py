def _precompute_dsm():
    """نحضّر نسخة مطبّعة من القاموس لتسريع المطابقة."""
    prepared = {}
    for dx, meta in DSM_DB.items():
        kws = meta.get("keywords", [])
        prepared[dx] = {
            "keywords_raw": kws,
            "keywords_norm": [normalize(k) for k in kws],
            "required_norm": [normalize(k) for k in meta.get("required", [])],
            "exclusions_norm": [normalize(k) for k in meta.get("exclusions", [])],
            "weight": float(meta.get("weight", 1.0)),
            "prev": meta.get("prevalence", {"male":1.0,"female":1.0}),
            "onset_age": meta.get("onset_age", "أي عمر")
        }
    return prepared

_DSM_PREP = _precompute_dsm()

def _gender_key(gender: str) -> str:
    g = normalize(gender)
    if "انثى" in g or "female" in g or "f" == g:
        return "female"
    return "male"

def _age_factor(age_str: str, onset_age: str) -> float:
    try: age = int(age_str)
    except: return 1.0
    # تبسيط: قرب العمر من نافذة الظهور يعطي +10%، بعيد جدًا -10%
    onset = normalize(onset_age)
    if "طفول" in onset: 
        if age <= 12: return 1.1
        if age >= 30: return 0.9
    if "مراهق" in onset:
        if 12 <= age <= 19: return 1.1
    if "بلوغ مبكر" in onset or "البُلوع" in onset:
        if 18 <= age <= 30: return 1.1
    if "منتصف العمر" in onset:
        if 35 <= age <= 55: return 1.1
    return 1.0

def score_diagnoses(symptoms_text: str, age: str="", gender: str="", duration_days: str="", history: str=""):
    """
    تعطي أفضل 5 تشخيصات مع درجات وسبب الترشيح.
    تحترم required/exclusions/weight/المدّة/العمر/النوع + تشابه ناعم.
    """
    # نص المستخدم + توسيع بالمرادفات
    text_raw = symptoms_text or ""
    text_norm = normalize(text_raw)
    # وسّع التوكنات بالمرادفات إذا النص يلمّح لفئة
    for base, syns in SYNONYMS.items():
        if any(normalize(t) in text_norm for t in [base] + syns):
            text_norm += " " + " ".join(set(normalize(s) for s in ([base] + syns)))

    toks = set(tokenize(text_norm))

    # بوستات عامة
    def _duration_boost(d):
        try: d = float(d)
        except: return 1.0
        if d >= 365: return 1.25
        if d >= 90:  return 1.15
        if d >= 30:  return 1.08
        return 1.0

    def _impairment_boost(h):
        if not h: return 1.0
        t = normalize(h)
        keys = ["مشاكل عمل","فصل","انذار","مشاكل زواج","طلاق","خلافات","قضيه","مشاكل ماليه","تعثر دراسي","غياب متكرر"]
        return 1.1 if any(normalize(k) in t for k in keys) else 1.0

    gkey = _gender_key(gender)
    durB = _duration_boost(duration_days)
    impB = _impairment_boost(history)

    results = []
    for dx, meta in _DSM_PREP.items():
        req = meta["required_norm"]
        exc = meta["exclusions_norm"]
        kws_norm = meta["keywords_norm"]

        # استبعاد واضح
        if any(x in text_norm for x in exc):
            continue

        # تحقق المطلوب (required) — إذا ما تحقق نخفض الدرجة بشدة أو نتخطى
        if req and not all(r in text_norm for r in req):
            # نعطي فرصة عبر تشابه ناعم: إذا التشابه > 0.6 لكل required نقبل
            soft_ok = True
            for r in req:
                if calculate_similarity(text_norm, r) < 0.6:
                    soft_ok = False
                    break
            if not soft_ok:
                continue

        # نقاط المطابقة
        score = 0.0
        hits = []
        for kw_raw, kw in zip(meta["keywords_raw"], kws_norm):
            # مطابقة صارمة
            if kw in text_norm:
                w = 1.0
                # أعراض محورية عالية الخطورة
                if kw in (normalize("انتحار"), normalize("افكار انتحارية"), normalize("نوبة هلع"),
                          normalize("هلوسة"), normalize("اوهام"), normalize("ضلالات")):
                    w = 1.8
                score += w
                hits.append(kw_raw)
            else:
                # تشابه ناعم
                sim = calculate_similarity(text_norm, kw)
                if sim >= 0.66:
                    score += 0.8
                    hits.append(kw_raw + "~")
                elif sim >= 0.4:
                    score += 0.4

        if score <= 0:
            continue

        # أوزان التشخيص + العمر + النوع + المدة + الأثر
        score *= meta["weight"]
        score *= _age_factor(age, meta["onset_age"])
        score *= (meta["prev"].get(gkey, 1.0) or 1.0)
        score *= durB
        score *= impB

        results.append({
            "name": dx,
            "score": round(score, 2),
            "hits": hits[:12],  # نعرض أول 12 سبب
        })

    if not results:
        return [], {"suggestion": "أضف كلمات أوضح عن الأعراض/المدة/الأثر الوظيفي. جرّب: هلوسة، ضلالات، وسواس، نوبة هلع، نهم، أرق ...", "buckets": []}

    # ترتيب ونخبة أعلى 5
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5], None
