# --- أعلى الملف ---
import os, json, re
from collections import defaultdict
from flask import Flask, request, render_template_string

# لو تستخدم openai الرسمي:
# from openai import OpenAI
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(APP_DIR, "data", "dsm_rules.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    DSM_RULES = json.load(f)

def normalize_ar(text: str) -> str:
    if not text: return ""
    t = text.strip()
    t = re.sub(r"[^\u0600-\u06FF\s]", " ", t)  # إبقاء العربية والمسافات
    t = re.sub(r"\s+", " ", t)
    # تطبيع بسيط
    t = t.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    t = t.replace("ة", "ه").replace("ى", "ي")
    return t

def score_by_rules(text: str):
    txt = normalize_ar(text)
    tokens = set(txt.split())
    reports = []
    for code, spec in DSM_RULES.items():
        required = [normalize_ar(w) for w in spec.get("required", [])]
        optional = [normalize_ar(w) for w in spec.get("optional", [])]
        min_req = spec.get("min_required", max(1, len(required)//2))
        weights = spec.get("weights", {})

        req_hits = [w for w in required if any(w in token for token in tokens)]
        opt_hits = [w for w in optional if any(w in token for token in tokens)]

        if len(req_hits) >= min_req:
            score = 0
            details = []
            for w in req_hits + opt_hits:
                w_norm = normalize_ar(w)
                w_score = weights.get(w, 1)
                score += w_score
                details.append((w, w_score))
            reports.append({
                "code": code,
                "name_ar": spec.get("name_ar", code),
                "score": score,
                "required_hits": req_hits,
                "optional_hits": opt_hits,
                "details": details
            })
    # ترتيب أفضل 3
    reports.sort(key=lambda d: d["score"], reverse=True)
    return reports[:3]

def llm_opinion(user_text: str, top3):
    """اختياري: تعليق تفسيري من نموذج لغوي—يتطلب مفتاح OPENAI_API_KEY.
       لو المفتاح غير متوفر نرجّع None.
    """
    api = os.getenv("OPENAI_API_KEY")
    if not api:
        return None

    # prompt مختصر وواضح (بدون تعهدات طبية)
    summary = "\n".join([f"- {r['name_ar']} (درجة: {r['score']})" for r in top3]) or "لا ترشيحات قوية."
    system_msg = (
        "أنت مساعد دعم نفسي غير علاجي. قدّم ترشيحاً تفسيرياً غير تشخيصي "
        "استناداً إلى الشكوى وترشيحات النظام القاعدي. اذكر لماذا قد تنطبق "
        "هذه الترشيحات، واقترح خطوات مبدئية آمنة للرعاية الذاتية أو طلب المساعدة المختصة. "
        "أضف تنبيهاً واضحاً أن هذا ليس تشخيصاً طبياً."
    )
    user_msg = f"الشكوى:\n{user_text}\n\nترشيحات القواعد:\n{summary}"

    # مثال باستخدام Chat Completions القديم/المشابه. عدّل بحسب مكتبتك:
    # resp = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role":"system","content":system_msg},
    #               {"role":"user","content":user_msg}],
    #     temperature=0.2,
    # )
    # return resp.choices[0].message.content.strip()

    return None  # لو ما تبغى LLM الآن

# -------- واجهة DSM-AI --------

DSM_AI_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>تشخيص مساعد (DSM-AI) | عربي سايكو</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  :root{
    --navy:#0b1b3a;        /* كحلي عميق */
    --navy-2:#0e254f;      /* تدرّج أدكن */
    --gold:#f5c242;        /* ذهبي لامع */
    --gold-2:#ffd773;      /* إضاءة ذهبية */
    --text:#e9eef7;
    --ok:#49d17c;
    --bad:#ff6b6b;
  }
  *{box-sizing:border-box}
  body{
    margin:0; font-family:'Cairo', system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    background: radial-gradient(1200px 600px at 80% -100px, rgba(245,194,66,0.08), transparent 70%),
                linear-gradient(180deg, var(--navy), var(--navy-2));
    color:var(--text);
    min-height:100vh;
    display:flex; align-items:center; justify-content:center; padding:32px;
  }
  .shell{
    width:min(1100px,100%);
    background: rgba(14,37,79,0.65);
    border:1px solid rgba(245,194,66,0.22);
    box-shadow: 0 20px 60px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.06);
    border-radius:24px; padding:28px;
    backdrop-filter: blur(8px);
  }
  .hero{
    display:flex; gap:18px; align-items:center; justify-content:space-between; flex-wrap:wrap;
    margin-bottom:18px;
  }
  .brand{
    font-weight:800; letter-spacing:.5px; font-size:26px;
    color:var(--gold);
    text-shadow:0 0 18px rgba(245,194,66,.35);
  }
  .badge{
    background: linear-gradient(140deg, var(--gold), var(--gold-2));
    color:#141b2d; font-weight:800; padding:8px 14px; border-radius:9999px; font-size:14px;
    box-shadow:0 10px 30px rgba(245,194,66,.25);
  }
  .panel{background:rgba(9,18,40,.55); border:1px solid rgba(245,194,66,.18); border-radius:18px; padding:18px}
  .title{font-size:20px; font-weight:800; color:#fff; margin:0 0 12px}
  textarea{
    width:100%; min-height:140px; resize:vertical;
    background:rgba(255,255,255,.04);
    color:var(--text); border:1px solid rgba(245,194,66,.18);
    border-radius:14px; padding:14px; outline:none;
  }
  textarea:focus{border-color:var(--gold); box-shadow:0 0 0 4px rgba(245,194,66,.15)}
  .row{display:flex; gap:14px; flex-wrap:wrap}
  .btn{
    background: linear-gradient(180deg, var(--gold), #f0b226);
    color:#171c2c; font-weight:800; border:none; border-radius:14px; padding:12px 18px;
    cursor:pointer; box-shadow: 0 8px 28px rgba(245,194,66,.3);
  }
  .btn:hover{transform:translateY(-1px)}
  .ghost{
    background:transparent; color:var(--gold); border:1px solid var(--gold); box-shadow:none
  }
  .chips{display:flex; gap:10px; flex-wrap:wrap}
  .chip{
    border:1px dashed rgba(245,194,66,.35);
    color:var(--gold-2); border-radius:999px; padding:6px 10px; font-size:12px
  }
  .card{
    background:rgba(255,255,255,.03);
    border:1px solid rgba(245,194,66,.16);
    border-radius:16px; padding:14px;
  }
  .score{font-weight:800; color:var(--gold)}
  .muted{opacity:.8; font-size:13px}
  .warn{
    background:rgba(255,107,107,.12); border:1px solid rgba(255,107,107,.35);
    color:#ffdede; border-radius:12px; padding:10px 12px; font-size:13px;
  }
</style>
</head>
<body>
  <div class="shell">
    <div class="hero">
      <div class="brand">عربي سايكو — DSM-AI</div>
      <div class="badge">تجريبي • غير تشخيصي</div>
    </div>

    <form method="post" class="panel" style="margin-bottom:14px">
      <div class="title">احكِ لنا باختصار، ما الذي يزعجك هذه الفترة؟</div>
      <textarea name="complaint" placeholder="مثال: أشعر بقلق مستمر وصعوبة بالنوم وتركيزي ضعيف في العمل...">{{complaint or ""}}</textarea>
      <div class="row" style="margin-top:12px">
        <button class="btn" type="submit">تحليل الشكوى</button>
        <button class="btn ghost" type="reset">مسح</button>
      </div>
      <div class="chips" style="margin-top:10px">
        <div class="chip">التحليل يعتمد على الكلمات الدالة</div>
        <div class="chip">يمكن أن يخطئ • ليس بديلاً للطبيب</div>
      </div>
    </form>

    {% if results %}
    <div class="panel" style="margin-bottom:14px">
      <div class="title">الترشيحات الأقرب استناداً إلى الأعراض</div>
      <div class="row">
        {% for r in results %}
        <div class="card" style="flex:1 1 260px">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div style="font-weight:800">{{r.name_ar}}</div>
            <div class="score">درجة: {{r.score}}</div>
          </div>
          <div class="muted" style="margin-top:6px">رمز: {{r.code}}</div>
          <div class="muted" style="margin-top:8px">أصابت: {{ ", ".join(r.required_hits + r.optional_hits) if (r.required_hits or r.optional_hits) else "—" }}</div>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}

    {% if llm %}
    <div class="panel">
      <div class="title">ملاحظات توضيحية من المساعد</div>
      <div class="card">{{llm|safe}}</div>
    </div>
    {% endif %}

    <div class="warn" style="margin-top:14px">
      هذا المحتوى لأغراض تثقيفية ودعم أولي فقط، ولا يُعد تشخيصاً طبياً. إذا كانت الأعراض شديدة
      أو لديك أفكار بإيذاء النفس، فضلاً تواصل فوراً مع جهات الطوارئ أو مختص مرخّص.
    </div>
  </div>
</body>
</html>
"""

@app.route("/dsm-ai", methods=["GET", "POST"])
def dsm_ai():
    complaint = ""
    results = []
    llm = None
    if request.method == "POST":
        complaint = request.form.get("complaint", "")
        if complaint.strip():
            results = score_by_rules(complaint)
            llm = llm_opinion(complaint, results)  # قد تكون None
    return render_template_string(DSM_AI_HTML, complaint=complaint, results=results, llm=llm)
