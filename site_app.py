# -*- coding: utf-8 -*-
"""
site_app.py
واجهة عربية فاخرة (كحلي + ذهبي) + تشخيص مبسّط يعتمد على قاعدة DSM من ملف JSON.
يتوقع وجود الملف: data/dsm_rules_extended.json

تشغيل محلي:
    pip install -r requirements.txt
    python site_app.py

تشغيل على Render:
    Procfile => web: gunicorn site_app:app
"""

from __future__ import annotations
from flask import Flask, request, render_template_string, redirect, url_for, jsonify
import json, os, re
from datetime import datetime

# ---------------------------------------
# تحميل قاعدة DSM من الملف
# ---------------------------------------
DATA_PATH = os.environ.get("DSM_JSON_PATH", "data/dsm_rules_extended.json")

def load_dsm_rules(path: str = DATA_PATH) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"لم يتم العثور على ملف DSM: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("صيغة ملف DSM غير صحيحة، يجب أن تكون كائن JSON (dict).")
    return data

try:
    DSM_RULES = load_dsm_rules()
except Exception as e:
    # نحمل نسخة فاضية مع رسالة خطأ داخل الواجهة
    DSM_RULES = {"_meta": {"error": str(e)}}

# ---------------------------------------
# أدوات مساعدة للتطبيع اللغوي
# ---------------------------------------
_AR_DIAC = re.compile(r"[\u0617-\u061A\u064B-\u0652\u0670]")
_AR_PUNCT = re.compile(r"[^\w\s\u0600-\u06FF]+")

def normalize_text(s: str) -> str:
    if not s:
        return ""
    s = s.strip()
    s = _AR_DIAC.sub("", s)           # إزالة التشكيل
    s = _AR_PUNCT.sub(" ", s)         # إزالة علامات غير عربية/حروف
    s = re.sub(r"\s+", " ", s)
    return s

def tokenize(s: str) -> set[str]:
    s = normalize_text(s)
    # تفتيت مبسّط إلى كلمات/عبارات قصيرة
    toks = set()
    for w in s.split():
        if len(w) >= 2:
            toks.add(w)
    return toks

# ---------------------------------------
# منطق التشخيص المبسّط
# يتوقع في كل تشخيص داخل JSON:
# {
#   "name_ar": "الاكتئاب...",
#   "required": ["حزن", "فقدان المتعة"],
#   "optional": ["أرق","شهية"],
#   "weights": {"حزن": 3, "فقدان المتعة": 3, "أرق": 1}
# }
# ---------------------------------------
def diagnose_from_rules(user_text: str, top_k: int = 3):
    if not user_text or not DSM_RULES:
        return []

    # تحويل الشكوى إلى مجموعة رموز/كلمات
    words = tokenize(user_text)

    results = []
    for code, rule in DSM_RULES.items():
        if code.startswith("_"):
            continue

        name = rule.get("name_ar", code)
        required = rule.get("required", [])
        optional = rule.get("optional", [])
        weights = rule.get("weights", {})

        # نحاول المطابقة: required يمكن تكون كلمات مفردة أو عبارات قصيرة
        missing = []
        matched_required = []
        score = 0

        for r in required:
            r_norm = normalize_text(r)
            # إذا كانت عبارة متعددة كلمات، نبحث substring طبيعي في النص الموحَّد
            if " " in r_norm:
                if r_norm in normalize_text(user_text):
                    matched_required.append(r)
                    score += int(weights.get(r, 2))
                else:
                    missing.append(r)
            else:
                # كلمة مفردة: نطابق بالـ tokens
                if r_norm in words:
                    matched_required.append(r)
                    score += int(weights.get(r, 2))
                else:
                    missing.append(r)

        # إذا بقي مطلوب ناقص، ننقص نقاط كبيرة
        if missing:
            # خصم بسيط بدلاً من استبعاد كامل حتى نعرض احتمالات قريبة
            score -= len(missing) * 2

        matched_optional = []
        for o in optional:
            o_norm = normalize_text(o)
            in_text = (o_norm in normalize_text(user_text)) if " " in o_norm else (o_norm in words)
            if in_text:
                matched_optional.append(o)
                score += int(weights.get(o, 1))

        # مقياس ثانوي: طول النص وعدد الكلمات يساعد قليلاً
        score += min(len(words), 50) * 0.02

        results.append({
            "code": code,
            "name": name,
            "score": round(score, 2),
            "matched_required": matched_required,
            "missing_required": missing,
            "matched_optional": matched_optional
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

# ---------------------------------------
# الواجهة (HTML قالب Jinja داخل الملف)
# ---------------------------------------
BASE_TMPL = r"""
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>عربي سايكو | الراحة النفسية تبدأ من هنا</title>
  <style>
    :root{
      --blue:#0B1E39;     /* كحلي عميق */
      --blue-2:#10294F;
      --gold:#E4B000;     /* ذهبي لامع */
      --gold-2:#F5CF3B;
      --ink:#E9EDF6;
      --muted:#9db0d1;
      --ok:#47d18c;
      --warn:#ffb74d;
      --danger:#ff6b6b;
      --radius:18px;
      --shadow:0 12px 30px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.04);
      --shadow-soft:0 8px 18px rgba(0,0,0,.20);
      --gloss:linear-gradient(180deg, rgba(255,255,255,.14), rgba(255,255,255,0) 40%);
      --gold-grad:linear-gradient(135deg, #FBE084, #F3C949 30%, #E4B000 60%, #C89A00);
      --blue-grad:linear-gradient(180deg, #112752, #0B1E39 60%);
    }
    *{box-sizing:border-box}
    body{
      font-family: "Tajawal", system-ui, -apple-system, Segoe UI, Roboto, "Noto Kufi Arabic", Arial, sans-serif;
      background: radial-gradient(1000px 600px at 80% -10%, #1A366B, transparent),
                  radial-gradient(800px 500px at -10% 110%, #0f2244, transparent),
                  var(--blue-grad);
      color: var(--ink);
      margin:0; padding:0;
      min-height:100vh;
      display:flex; align-items:stretch; justify-content:center;
    }
    .container{
      width:min(1100px, 96vw);
      margin: 32px auto 40px;
      background: linear-gradient(180deg, rgba(17,39,82,.9), rgba(11,30,57,.85));
      border:1px solid rgba(255,255,255,.06);
      border-radius: calc(var(--radius) + 6px);
      box-shadow: var(--shadow);
      overflow:hidden;
      position:relative;
    }
    .header{
      padding: 28px 28px 16px;
      border-bottom:1px solid rgba(255,255,255,.06);
      background:
        radial-gradient(700px 180px at 50% -80px, rgba(255,255,255,.10), transparent),
        linear-gradient(180deg, rgba(255,255,255,.08), rgba(255,255,255,0));
    }
    .brand{
      display:flex; align-items:center; gap:14px;
    }
    .brand .logo{
      width:46px; height:46px; border-radius:50%;
      background: var(--gold-grad);
      box-shadow: 0 6px 16px rgba(228,176,0,.45), inset 0 0 8px rgba(255,255,255,.35);
      position:relative;
    }
    .brand .logo:after{
      content:"AS"; font-weight:800; font-size:16px; color:#1a1300;
      position:absolute; inset:0; display:grid; place-items:center;
      text-shadow:0 1px 0 rgba(255,255,255,.25);
    }
    .brand h1{
      margin:0; font-size:22px; letter-spacing:.5px;
    }
    .brand .badge{
      margin-inline-start:auto;
      background: rgba(228,176,0,.12);
      border:1px solid rgba(228,176,0,.35);
      color:#ffe69a; padding:6px 12px; border-radius:999px; font-size:12px;
    }

    .hero{
      padding: 24px 28px 30px;
      display:flex; gap:22px; flex-wrap:wrap;
    }
    .card{
      background: linear-gradient(180deg, rgba(20,48,96,.65), rgba(10,25,48,.85));
      border:1px solid rgba(255,255,255,.06);
      border-radius: var(--radius);
      box-shadow: var(--shadow-soft);
      position:relative; overflow:hidden;
    }
    .card:before{content:""; position:absolute; inset:0; background: var(--gloss); pointer-events:none}
    .card.head{
      flex: 1 1 560px; padding:22px 22px 18px;
    }
    .card.side{
      flex: 1 1 320px; padding:18px;
      max-width: 340px;
    }

    .title{
      font-size:28px; margin:2px 0 10px; font-weight:800;
      background: var(--gold-grad); -webkit-background-clip:text; background-clip:text; color:transparent;
      text-shadow: 0 2px 10px rgba(228,176,0,.25);
    }
    .subtitle{ color: var(--muted); line-height:1.9; margin:0 0 8px }
    .row{ display:flex; gap:12px; flex-wrap:wrap; margin-top:10px }
    .chip{
      background: rgba(255,255,255,.06);
      color: var(--ink); border:1px solid rgba(255,255,255,.1);
      border-radius:999px; padding:8px 12px; font-size:13px;
    }

    /* زر ذهبي */
    .btn{
      appearance:none; border:0; outline:0; cursor:pointer;
      border-radius:999px; padding:12px 18px; font-weight:700; letter-spacing:.25px;
      color:#1F1600; text-decoration:none; display:inline-flex; align-items:center; gap:10px;
      background: var(--gold-grad);
      box-shadow: 0 8px 20px rgba(228,176,0,.35), inset 0 1px 0 rgba(255,255,255,.45);
      transition: transform .08s ease, filter .2s ease;
    }
    .btn:hover{ filter:saturate(1.1) brightness(1.02) }
    .btn:active{ transform: translateY(1px) }

    .section{
      padding: 12px 28px 26px;
      display:grid; grid-template-columns: minmax(260px, 360px) 1fr; gap:18px;
    }
    .panel{
      background: linear-gradient(180deg, rgba(17,39,82,.65), rgba(10,25,48,.8));
      border:1px solid rgba(255,255,255,.06);
      border-radius: var(--radius);
      padding:18px;
      box-shadow: var(--shadow-soft);
      position:relative; overflow:hidden;
    }
    .panel h3{ margin:0 0 12px; font-size:16px; color:#EBD889; letter-spacing:.3px }
    .panel small{ color:var(--muted) }

    textarea, input[type="text"]{
      width:100%; border:1px solid rgba(255,255,255,.1); background:rgba(255,255,255,.04);
      color: var(--ink); border-radius:14px; padding:12px 14px; font-size:15px;
      outline:none; box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
    }
    textarea{ min-height:130px; resize:vertical }
    .form-row{ display:flex; gap:10px; align-items:center; justify-content:flex-end; margin-top:10px }

    .result{
      display:grid; gap:12px;
    }
    .diag{
      background: linear-gradient(180deg, rgba(19,50,101,.6), rgba(11,30,57,.75));
      border:1px solid rgba(255,255,255,.06);
      border-radius: 14px; padding:12px 14px;
    }
    .diag .name{ font-weight:800; color:#FFE28A }
    .diag .score{ color:#C8D9FF; font-size:13px }
    .diag .tags{ margin-top:6px; display:flex; gap:6px; flex-wrap:wrap }
    .tag{
      background: rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.08);
      color:var(--ink); font-size:12px; padding:4px 8px; border-radius:999px;
    }

    .footer{
      padding: 14px 22px 20px; color: var(--muted); font-size:13px; text-align:center;
      border-top:1px solid rgba(255,255,255,.06);
      background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,0));
    }
    .copy{
      display:flex; gap:8px; align-items:center;
    }
    .copy input{
      flex:1; min-width:140px;
      background: rgba(255,255,255,.05); color:var(--ink);
      border:1px dashed rgba(255,255,255,.12); border-radius:12px; padding:8px 10px; font-size:13px;
    }
    .btn-ghost{
      background: rgba(255,255,255,.06); color:#FFE28A; border:1px solid rgba(255,255,255,.12);
      padding:8px 10px; border-radius:12px; cursor:pointer;
    }

    @media (max-width: 860px){
      .section{ grid-template-columns: 1fr }
      .card.side{ max-width: unset }
    }
  </style>
</head>
<body>
  <main class="container">
    <header class="header">
      <div class="brand">
        <div class="logo"></div>
        <h1>عربي سايكو</h1>
        <div class="badge">راحة نفسية • {{ now }}</div>
      </div>
    </header>

    <section class="hero">
      <div class="card head">
        <div class="title">الراحة النفسية تبدأ من هنا ✨</div>
        <p class="subtitle">
          منصة عربية تقدم أدوات تقييم مبسطة، وتمارين CBT، ومسارات دعم عاطفي مبنية على دليل <b>DSM</b>.
          سجّل شكواك النفسية بلغة بسيطة وسنقترح عليك أقرب التشخيصات المحتملة.
        </p>
        <div class="row">
          <span class="chip">CBT</span>
          <span class="chip">اختبارات</span>
          <span class="chip">DSM-5</span>
          <span class="chip">سرية تامة</span>
        </div>
        <div style="margin-top:14px">
          <a class="btn" href="#diag">ابدأ التشخيص الآن</a>
        </div>
      </div>

      <div class="card side">
        <h3 style="margin-top:2px">ملفات النظام</h3>
        <div class="copy" style="margin:10px 0 8px">
          <input id="fname" value="{{ dsm_filename }}" readonly>
          <button class="btn-ghost" onclick="copyFile()">نسخ الاسم</button>
        </div>
        <small>هذا هو الملف الذي يضم القواعد. أي تعديل عليه سينعكس مباشرة في النتائج.</small>
        {% if meta_error %}
          <div class="diag" style="margin-top:10px; border-color: rgba(255,0,0,.3)">
            <div class="name">خطأ في تحميل DSM</div>
            <div class="score">{{ meta_error }}</div>
          </div>
        {% else %}
          <div class="diag" style="margin-top:10px">
            <div class="name">الإحصائيات</div>
            <div class="score">عدد الأكواد: {{ dsm_count }}</div>
            <div class="tags">
              <span class="tag">إصدار: {{ dsm_version }}</span>
              <span class="tag">آخر تحديث: {{ dsm_updated }}</span>
            </div>
          </div>
        {% endif %}
      </div>
    </section>

    <section class="section" id="diag">
      <div class="panel">
        <h3>📝 اكتب شكواك النفسية (سري)</h3>
        <form method="post" action="{{ url_for('diagnose') }}">
          <textarea name="complaint" placeholder="مثال: أشعر بحزن مستمر، نومي قليل، لا أستمتع بالأشياء التي كنت أحبها...">{{ q or "" }}</textarea>
          <div class="form-row">
            <button class="btn" type="submit">تشخيص فوري</button>
          </div>
        </form>
      </div>

      <div class="panel">
        <h3>📊 النتائج</h3>
        {% if results %}
          <div class="result">
            {% for r in results %}
              <div class="diag">
                <div class="name">{{ loop.index }}) {{ r.name }}</div>
                <div class="score">الدرجة: {{ r.score }}</div>
                <div class="tags">
                  {% if r.matched_required %}
                    <span class="tag">متطلبات متطابقة: {{ r.matched_required|length }}</span>
                  {% endif %}
                  {% if r.matched_optional %}
                    <span class="tag">أعراض إضافية: {{ r.matched_optional|length }}</span>
                  {% endif %}
                  {% if r.missing_required %}
                    <span class="tag" style="border-color: rgba(255,0,0,.25); color:#ffd5d5">نواقص: {{ r.missing_required|length }}</span>
                  {% endif %}
                </div>
                {% if r.matched_required %}
                  <div class="tags" style="margin-top:8px">
                    {% for t in r.matched_required %}
                      <span class="tag">{{ t }}</span>
                    {% endfor %}
                  </div>
                {% endif %}
              </div>
            {% endfor %}
          </div>
        {% else %}
          <small>لن تظهر نتائج حتى تكتب الشكوى وتضغط "تشخيص فوري".</small>
        {% endif %}
      </div>
    </section>

    <footer class="footer">
      © عربي سايكو — واجهة كحلي+ذهبي • لا تُعد النتائج تشخيصًا طبيًا نهائيًا. يُنصح بمراجعة مختص.
    </footer>
  </main>

  <script>
    function copyFile(){
      const el = document.getElementById('fname');
      el.select(); el.setSelectionRange(0, 99999);
      document.execCommand('copy');
      const old = el.value;
      el.value = '✅ تم النسخ: ' + old;
      setTimeout(()=>{ el.value = old; }, 1200);
    }
  </script>
</body>
</html>
"""

# ---------------------------------------
# Flask App
# ---------------------------------------
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    meta = DSM_RULES.get("_meta", {})
    return render_template_string(
        BASE_TMPL,
        now=datetime.now().strftime("%Y-%m-%d"),
        q="",
        results=None,
        dsm_filename=DATA_PATH,
        dsm_count=sum(1 for k in DSM_RULES.keys() if not str(k).startswith("_")),
        dsm_version=meta.get("version", "غير محدد"),
        dsm_updated=meta.get("updated", "غير محدد"),
        meta_error=meta.get("error")
    )

@app.route("/diagnose", methods=["POST"])
def diagnose():
    q = request.form.get("complaint", "", type=str)
    results = diagnose_from_rules(q, top_k=3)
    meta = DSM_RULES.get("_meta", {})
    return render_template_string(
        BASE_TMPL,
        now=datetime.now().strftime("%Y-%m-%d"),
        q=q,
        results=results,
        dsm_filename=DATA_PATH,
        dsm_count=sum(1 for k in DSM_RULES.keys() if not str(k).startswith("_")),
        dsm_version=meta.get("version", "غير محدد"),
        dsm_updated=meta.get("updated", "غير محدد"),
        meta_error=meta.get("error")
    )

# JSON API خفيف (اختياري)
@app.route("/api/diagnose", methods=["POST"])
def api_diagnose():
    data = request.get_json(silent=True) or {}
    q = data.get("complaint", "")
    top_k = int(data.get("k", 3))
    res = diagnose_from_rules(q, top_k=top_k)
    return jsonify({"ok": True, "results": res})

# صفحة صحّة
@app.route("/health")
def health():
    ok = "_meta" in DSM_RULES or len(DSM_RULES) > 0
    return jsonify({"ok": ok, "count": len(DSM_RULES)}), (200 if ok else 500)

# للتشغيل المحلي
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
