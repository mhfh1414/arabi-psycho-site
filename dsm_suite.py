# ------------------------ إعدادات القرار الدقيق (تحديث) ------------------------
CRITICAL_SYM = { normalize("هلوسة"), normalize("اوهام"), normalize("نوبة هلع"), normalize("تفكير انتحاري") }

# عتبات أخف عشان نحسم أسرع عند وضوح الصورة
MIN_OK   = 1.90   # كان 2.2
MARGIN   = 0.35   # كان 0.60

# مرادفات إضافية (الهذيان يُستعمل عاميًّا كـ"ضلالات")
SYNONYMS["اوهام"] = list(set(SYNONYMS.get("اوهام", []) + ["هذيان"]))

PSYCHOSIS_HINTS = { normalize("هلوسة"), normalize("اوهام"), normalize("ضلالات"), normalize("هذيان") }
PANIC_HINTS     = { normalize("نوبة هلع"), normalize("خفقان"), normalize("اختناق") }
OCD_HINTS       = { normalize("وسواس"), normalize("سلوك قهري"), normalize("تفقد متكرر"), normalize("غسل متكرر") }
MOOD_HINTS      = { normalize("اكتئاب"), normalize("حزن"), normalize("نوبة هوس"), normalize("هوس"),
                    normalize("طاقة عالية"), normalize("اندفاع"), normalize("قلة نوم") }

def _gate_candidates(text_norm: str):
    has_psy   = any(h in text_norm for h in PSYCHOSIS_HINTS)
    has_panic = any(h in text_norm for h in PANIC_HINTS)
    has_ocd   = any(h in text_norm for h in OCD_HINTS)

    if has_psy:
        # مبدئيًا نسمح بالذهانيات الأساسية فقط — ونستثني الفصامي-العاطفي إذا ما فيه دلائل مزاجية
        allow = {"فصام", "اضطراب فصامي عاطفي"}
        return {k:v for k,v in DSM.items() if k in allow}

    if has_panic:
        allow = {"اضطراب الهلع","رهاب الساحة","اضطراب القلق العام","رهاب اجتماعي","رهاب محدد"}
        return {k:v for k,v in DSM.items() if k in allow}

    if has_ocd:
        allow = {"اضطراب الوسواس القهري","تشوه صورة الجسد","اكتناز"}
        return {k:v for k,v in DSM.items() if k in allow}

    return DSM

def _boost_text_with_synonyms(text_norm: str) -> str:
    out = [text_norm]
    for base, syns in SYNONYMS.items():
        nb = normalize(base)
        if nb in text_norm or any(normalize(s) in text_norm for s in syns):
            out.append(" ".join(normalize(s) for s in ([base] + syns)))
    return " ".join(out)

def _severity_multipliers(duration_days: str, history: str):
    try: dur = float(duration_days or 0)
    except: dur = 0.0
    durB = 1.25 if dur>=365 else 1.15 if dur>=90 else 1.08 if dur>=30 else 1.0
    fxB  = 1.10 if any(k in normalize(history or "") for k in
            ["مشاكل عمل","مشاكل زواج","طلاق","تعثر دراسي","غياب متكرر","قضيه"]) else 1.0
    return durB, fxB

def _contradiction_penalty(text_norm: str, dx_name: str) -> float:
    if dx_name == "قهم عصبي":
        if normalize("نقص وزن شديد") not in text_norm and normalize("خوف من زياده الوزن") not in text_norm:
            return 0.85
    return 1.0

def diagnose_one(symptoms: str, age: str="", gender: str="", duration_days: str="", history: str=""):
    base_text = normalize(symptoms or "")
    if not base_text or len(base_text) < 3:
        return None, {"reason":"النص فارغ أو قصير جدًا","hints":["اكتب أعراضًا صريحة مثل: هلوسة/ضلالات/نوبة هلع/وسواس/أرق/نهم..."]}

    text = _boost_text_with_synonyms(base_text)
    durB, fxB = _severity_multipliers(duration_days, history)

    # 1) قاعدة حسم مبكرة للفصام:
    has_hall = normalize("هلوسة") in text or "هلاوس" in text
    has_del  = normalize("اوهام") in text or normalize("ضلالات") in text or normalize("هذيان") in text
    has_mood = any(h in text for h in MOOD_HINTS)
    try: dur = float(duration_days or 0)
    except: dur = 0.0

    if has_hall and has_del and dur >= 30 and not has_mood:
        return {
            "name":"فصام",
            "confidence":0.92,
            "score":3.10,
            "hits":["هلوسة","أوهام/ضلالات","مدة ≥ 30 يوم","لا دلائل مزاجية واضحة"]
        }, None

    # 2) باقي الحالات: نمر عبر التسجيل + البوابة
    candidates = _gate_candidates(text)

    scored = []
    for dx, meta in candidates.items():
        # لو الذهان حاضر بدون مزاج، امنع الفصامي-العاطفي
        if dx == "اضطراب فصامي عاطفي" and (has_hall or has_del) and not has_mood:
            continue

        req = meta["req"]
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

        s *= meta["w"]
        s *= durB * fxB
        s *= _contradiction_penalty(text, dx)

        scored.append({"name": dx, "score": round(s,3), "hits": hits[:14]})

    if not scored:
        return None, {"reason":"لا توجد مطابقة كافية","hints":["زد مفردات حاسمة (هلوسة/أوهام/نوبة هلع/وسواس...) + المدة + الأثر الوظيفي."]}

    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0]
    second = scored[1]["score"] if len(scored)>1 else 0.0

    if best["score"] >= MIN_OK and (best["score"] - second) >= MARGIN:
        conf = min(0.99, 0.55 + 0.15*(best["score"]-MIN_OK))
        return {"name":best["name"],"confidence":round(conf,2),"score":best["score"],"hits":best["hits"]}, None

    tips = [f"اقترب من: {scored[0]['name']} (درجة {scored[0]['score']})",
            f"والثاني: {scored[1]['name'] if len(scored)>1 else '—'}"]
    return None, {"reason":"الفارق بين الاحتمالات صغير","hints":tips}
