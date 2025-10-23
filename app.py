# -*- coding: utf-8 -*-
# Arabi Psycho — One-File (Purple × Gold) v5.0
# Pages: Home / Case+DSM (one page, 70+ symptoms) / CBT
# Features:
# - Case page (DSM merged) with 70+ symptoms, smart preliminary suggestions
# - Result page: print, share, referrals, and "Open CBT" passes suggested plans
# - CBT: 15 plans + generator 7/10/14 days, suggestions preselected from Case
# - Purple × Gold theme, RTL Arabic, CSP headers

import os, json, urllib.parse
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# ====== Settings (change via env) ======
BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO  = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
TG_URL = os.environ.get("TELEGRAM_URL", "https://t.me/arabipsycho")
WA_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/966530565696")
CACHE_BUST = os.environ.get("CACHE_BUST", datetime.utcnow().strftime("%Y%m%d%H%M%S"))

# Referrals (can be same number):
PSYCHO_WA = os.environ.get("PSYCHOLOGIST_WA", "https://wa.me/966530565696")
PSYCH_WA  = os.environ.get("PSYCHIATRIST_WA", "https://wa.me/966530565696")
SOCIAL_WA = os.environ.get("SOCIAL_WORKER_WA", "https://wa.me/966530565696")

# ====== HTML Shell ======
def shell(title, content, active="home"):
    html = r"""
<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>[[TITLE]]</title>
<link rel="icon" href="[[LOGO]]"/>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>
<meta http-equiv="Pragma" content="no-cache"/><meta http-equiv="Expires" content="0"/>
<style>
:root{--p:#4B0082;--g:#FFD700;--bg:#f8f6ff;--ink:#2b1a4c}
*{box-sizing:border-box} html,body{height:100%}
body{margin:0;background:var(--bg);font-family:"Tajawal","Segoe UI",system-ui,sans-serif;color:var(--ink);font-size:16.5px;line-height:1.7}
.layout{display:grid;grid-template-columns:280px 1fr;min-height:100vh}
.side{background:linear-gradient(180deg,#4b0082,#3a0d72);color:#fff;padding:18px;position:sticky;top:0;height:100vh}
.logo{display:flex;align-items:center;gap:10px;margin-bottom:18px}
.logo img{width:48px;height:48px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.25)}
.brand{font-weight:900;letter-spacing:.3px;font-size:20px}
.nav a{display:block;color:#fff;text-decoration:none;padding:10px 12px;border-radius:12px;margin:6px 0;font-weight:700;opacity:.9}
.nav a.active{background:rgba(255,255,255,.18)}
.nav a:hover{opacity:1;background:rgba(255,255,255,.12)}
.badge{display:inline-block;background:var(--g);color:#4b0082;border-radius:999px;padding:2px 10px;font-weight:900;font-size:.8rem}
.content{padding:26px}
.card{background:#fff;border:1px solid #eee;border-radius:16px;padding:22px;box-shadow:0 10px 24px rgba(0,0,0,.06)}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.tile{background:#fff;border:1px solid #eee;border-radius:14px;padding:14px}
h1{font-weight:900;font-size:28px} h2{font-weight:800;margin:.2rem 0 .6rem} h3{font-weight:800;margin:.2rem 0 .6rem}
.btn{display:inline-block;background:var(--p);color:#fff;text-decoration:none;padding:11px 16px;border-radius:12px;font-weight:800;cursor:pointer}
.btn.alt{background:#5b22a6} .btn.gold{background:var(--g);color:#4b0082}
.btn.wa{background:#25D366} .btn.tg{background:#229ED9}
.small{font-size:.95rem;opacity:.85}
.table{width:100%;border-collapse:collapse}
.table th,.table td{border:1px solid #eee;padding:8px;text-align:center}
.row{display:flex;gap:10px;flex-wrap:wrap}
.badge2{display:inline-block;border:1px solid #eee;background:#fafafa;padding:6px 10px;border-radius:999px;margin:4px 4px 0 0;font-weight:700}
.note{background:#fff7d1;border:1px dashed #e5c100;border-radius:12px;padding:10px 12px;margin:10px 0}
.header-result{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.header-result img{width:44px;height:44px;border-radius:10px}
.footer{color:#fff;margin-top:24px;padding:14px;background:#3a0d72;text-align:center}
@media print { @page { size: A4; margin: 16mm 14mm; }
  .side, .footer, .screen-only { display:none !important; }
  body { background:#fff; font-size:18px; line-height:1.8; }
  .content { padding:0 !important; }
  .card { box-shadow:none; border:none; padding:0; }
  h1{font-size:26px} h2{font-size:22px} h3{font-size:18px}
}
</style></head><body>
<script>window.__BUILD__='[[BUILD]]';</script>
<div class="layout">
  <aside class="side">
    <div class="logo"><img src="[[LOGO]]" alt="شعار"/><div>
      <div class="brand">[[BRAND]]</div>
      <div class="small">«نراك بعين الاحترام، ونسير معك بخطوات عملية.»</div>
      <div class="badge">بنفسجي × ذهبي</div>
    </div></div>
    <nav class="nav">
      <a href="/" class="[[A_HOME]]">🏠 الرئيسية</a>
      <a href="/case" class="[[A_CASE]]">📝 دراسة الحالة</a>
      <a href="/cbt" class="[[A_CBT]]">🧠 CBT</a>
      <a href="[[TG_URL]]" target="_blank" rel="noopener">✈️ تيليجرام</a>
      <a href="[[WA_URL]]" target="_blank" rel="noopener">🟢 واتساب</a>
    </nav>
  </aside>
  <main class="content">[[CONTENT]]</main>
</div>
<div class="footer"><small>© جميع الحقوق محفوظة لـ [[BRAND]]</small></div>
</body></html>
""".replace("[[TITLE]]", title)\
     .replace("[[LOGO]]", LOGO)\
     .replace("[[BUILD]]", CACHE_BUST)\
     .replace("[[BRAND]]", BRAND)\
     .replace("[[TG_URL]]", TG_URL)\
     .replace("[[WA_URL]]", WA_URL)\
     .replace("[[A_HOME]]", "active" if active=="home" else "")\
     .replace("[[A_CASE]]", "active" if active=="case" else "")\
     .replace("[[A_CBT]]", "active" if active=="cbt" else "")\
     .replace("[[CONTENT]]", content)
    return html

# ====== Home ======
@app.get("/")
def home():
    content = """
    <div class="card" style="margin-bottom:14px">
      <h1>مرحبًا بك في [[BRAND]]</h1>
      <div class="small">ابدأ من «دراسة الحالة» لتحديد الأعراض، ثم انتقل لـ «CBT» بخطة جاهزة حسب حالتك.</div>
    </div>
    <div class="grid">
      <div class="tile"><h3>📝 دراسة الحالة (DSM مدمج)</h3><p class="small">أكثر من 70 عرض — نتيجة قابلة للطباعة والمشاركة والتحويل.</p><a class="btn gold" href="/case">ابدأ الآن</a></div>
      <div class="tile"><h3>🧠 CBT</h3><p class="small">15 خطة + جدول 7/10/14 يوم — تُحفظ محليًا وتشارك بلمسة.</p><a class="btn" href="/cbt">افتح CBT</a></div>
      <div class="tile"><h3>تواصل سريع</h3><a class="btn tg" href="[[TG_URL]]" target="_blank" rel="noopener">تيليجرام</a> <a class="btn wa" href="[[WA_URL]]" target="_blank" rel="noopener">واتساب</a></div>
    </div>
    """.replace("[[BRAND]]", BRAND).replace("[[TG_URL]]", TG_URL).replace("[[WA_URL]]", WA_URL)
    return shell("الرئيسية — " + BRAND, content, "home")

# ====== Case + DSM (70+ symptoms) ======
CASE_FORM = r"""
<div class="card">
  <h1>📝 دراسة الحالة — (DSM مدمج)</h1>
  <p class="small">اختر ما ينطبق عليك بدقة، ثم اضغط «عرض النتيجة». يتم <b>حفظ</b> اختياراتك محليًا في جهازك.</p>

  <form method="post" action="/case" oninput="persistCase()">
    <h3>1) بيانات عامة</h3>
    <div class="grid">
      <div class="tile"><label>العمر<input name="age" type="number" min="5" max="120" placeholder="28"></label></div>
      <div class="tile"><label>الحالة الاجتماعية
        <select name="marital"><option value="">—</option><option>أعزب/عزباء</option><option>متزوج/ة</option><option>منفصل/ة</option></select>
      </label></div>
      <div class="tile"><label>العمل/الدراسة<input name="work" placeholder="طالب/موظف/باحث..."></label></div>
    </div>

    <h3>2) الأعراض (اختر ما ينطبق)</h3>
    <div class="grid">

      <div class="tile"><h3>🟣 المزاج والاكتئاب</h3>
        <label class="badge2"><input type="checkbox" name="low_mood"> مزاج منخفض أكثر اليوم</label>
        <label class="badge2"><input type="checkbox" name="anhedonia"> فقد المتعة</label>
        <label class="badge2"><input type="checkbox" name="fatigue"> إرهاق/طاقة منخفضة</label>
        <label class="badge2"><input type="checkbox" name="sleep_issue"> نوم مضطرب</label>
        <label class="badge2"><input type="checkbox" name="appetite_change"> تغيّر الشهية/الوزن</label>
        <label class="badge2"><input type="checkbox" name="worthlessness"> ذنب/عدم قيمة</label>
        <label class="badge2"><input type="checkbox" name="poor_concentration"> تركيز ضعيف</label>
        <label class="badge2"><input type="checkbox" name="psychomotor"> تباطؤ/تهيج حركي</label>
        <label class="badge2"><input type="checkbox" name="hopeless"> تشاؤم/يأس</label>
        <label class="badge2"><input type="checkbox" name="somatic_pain"> آلام جسدية مرتبطة بالمزاج</label>
        <label class="badge2"><input type="checkbox" name="suicidal"> أفكار إيذاء/انتحار</label>
      </div>

      <div class="tile"><h3>🟣 القلق العام</h3>
        <label class="badge2"><input type="checkbox" name="worry"> قلق زائد صعب التحكم</label>
        <label class="badge2"><input type="checkbox" name="tension"> توتر/شد عضلي</label>
        <label class="badge2"><input type="checkbox" name="restlessness"> أرق/تململ</label>
        <label class="badge2"><input type="checkbox" name="irritability"> سرعة انفعال</label>
        <label class="badge2"><input type="checkbox" name="mind_blank"> فراغ ذهني</label>
        <label class="badge2"><input type="checkbox" name="sleep_anxiety"> صعوبة النوم بسبب القلق</label>
        <label class="badge2"><input type="checkbox" name="concentration_anxiety"> تشوش تركيز مع القلق</label>
      </div>

      <div class="tile"><h3>🟣 الهلع/الرهاب</h3>
        <label class="badge2"><input type="checkbox" name="panic_attacks"> نوبات هلع متكررة</label>
        <label class="badge2"><input type="checkbox" name="panic_fear"> خشية تكرار النوبة</label>
        <label class="badge2"><input type="checkbox" name="agoraphobia"> رهبة الأماكن المفتوحة/المزدحمة</label>
        <label class="badge2"><input type="checkbox" name="specific_phobia"> رُهاب محدد (حيوان/طيران/ارتفاعات...)</label>
        <label class="badge2"><input type="checkbox" name="social_fear"> قلق اجتماعي/خشية تقييم</label>
        <label class="badge2"><input type="checkbox" name="avoidance"> تجنّب مواقف خوفًا من الأعراض</label>
        <label class="badge2"><input type="checkbox" name="safety_behaviors"> الاعتماد على طمأنة/مرافق</label>
      </div>

      <div class="tile"><h3>🟣 الوسواس القهري</h3>
        <label class="badge2"><input type="checkbox" name="obsessions"> وساوس مُلحة</label>
        <label class="badge2"><input type="checkbox" name="compulsions"> أفعال قهرية متكررة</label>
        <label class="badge2"><input type="checkbox" name="contamination"> تلوّث/غسل مفرط</label>
        <label class="badge2"><input type="checkbox" name="checking"> فحص وتفقد متكرر</label>
        <label class="badge2"><input type="checkbox" name="ordering"> ترتيب/تماثل</label>
        <label class="badge2"><input type="checkbox" name="harm_obs"> وساوس أذى</label>
        <label class="badge2"><input type="checkbox" name="scrupulosity"> تدقيق ديني/أخلاقي قهري</label>
      </div>

      <div class="tile"><h3>🟣 الصدمات (PTSD/ASD)</h3>
        <label class="badge2"><input type="checkbox" name="flashbacks"> استرجاعات/كوابيس</label>
        <label class="badge2"><input type="checkbox" name="hypervigilance"> يقظة مفرطة</label>
        <label class="badge2"><input type="checkbox" name="startle"> فزع مفرط</label>
        <label class="badge2"><input type="checkbox" name="numbing"> خدر عاطفي</label>
        <label class="badge2"><input type="checkbox" name="trauma_avoid"> تجنب تذكارات الحدث</label>
        <label class="badge2"><input type="checkbox" name="guilt_trauma"> ذنب مرتبط بالحدث</label>
      </div>

      <div class="tile"><h3>🟣 النوم</h3>
        <label class="badge2"><input type="checkbox" name="insomnia"> أرق</label>
        <label class="badge2"><input type="checkbox" name="hypersomnia"> نوم زائد</label>
        <label class="badge2"><input type="checkbox" name="nightmares"> كوابيس متكررة</label>
        <label class="badge2"><input type="checkbox" name="irregular_sleep"> مواعيد نوم غير منتظمة</label>
      </div>

      <div class="tile"><h3>🟣 الانتباه/فرط الحركة</h3>
        <label class="badge2"><input type="checkbox" name="adhd_inattention"> تشتت/نسيان واضح</label>
        <label class="badge2"><input type="checkbox" name="adhd_hyper"> فرط حركة/اندفاع</label>
        <label class="badge2"><input type="checkbox" name="disorganization"> ضعف تنظيم/تأجيل</label>
        <label class="badge2"><input type="checkbox" name="time_blindness"> خلل ضبط الوقت</label>
      </div>

      <div class="tile"><h3>🟣 ثنائي القطب (الهوس/الخفة)</h3>
        <label class="badge2"><input type="checkbox" name="elevated_mood"> مزاج مرتفع/متهوّر</label>
        <label class="badge2"><input type="checkbox" name="decreased_sleep_need"> قلة الحاجة للنوم</label>
        <label class="badge2"><input type="checkbox" name="grandiosity"> شعور بالعظمة</label>
        <label class="badge2"><input type="checkbox" name="racing_thoughts"> أفكار متسارعة</label>
        <label class="badge2"><input type="checkbox" name="pressured_speech"> كلام ضاغط</label>
        <label class="badge2"><input type="checkbox" name="risk_spending"> صرف/مخاطر عالية</label>
      </div>

      <div class="tile"><h3>🟣 ذهانية/فصام</h3>
        <label class="badge2"><input type="checkbox" name="hallucinations"> هلوسات</label>
        <label class="badge2"><input type="checkbox" name="delusions"> أوهام ثابتة</label>
        <label class="badge2"><input type="checkbox" name="disorganized_speech"> تفكك خطاب/تفكير</label>
        <label class="badge2"><input type="checkbox" name="negative_symptoms"> أعراض سلبية (انسحاب/سطحية انفعال)</label>
        <label class="badge2"><input type="checkbox" name="catatonia"> سمات كاتاتونية</label>
        <label class="badge2"><input type="checkbox" name="decline_function"> تدهور وظيفي واضح</label>
      </div>

      <div class="tile"><h3>🟣 الأكل/الجسم</h3>
        <label class="badge2"><input type="checkbox" name="binge_eating"> نوبات أكل شره</label>
        <label class="badge2"><input type="checkbox" name="restrict_eating"> تقييد/تجويع</label>
        <label class="badge2"><input type="checkbox" name="body_image"> انشغال بالشكل/الوزن</label>
        <label class="badge2"><input type="checkbox" name="purging"> تطهير/إقياء قهري</label>
      </div>

      <div class="tile"><h3>🟣 الإدمان/المواد</h3>
        <label class="badge2"><input type="checkbox" name="craving"> اشتهاء قوي</label>
        <label class="badge2"><input type="checkbox" name="withdrawal"> أعراض انسحاب</label>
        <label class="badge2"><input type="checkbox" name="use_harm"> استمرار رغم الضرر</label>
        <label class="badge2"><input type="checkbox" name="loss_control"> فقدان السيطرة/زيادة الجرعة</label>
        <label class="badge2"><input type="checkbox" name="relapse_history"> سوابق انتكاس</label>
      </div>

      <div class="tile"><h3>🟣 سمات شخصية/تنظيم</h3>
        <label class="badge2"><input type="checkbox" name="emotion_instability"> تقلب عاطفي شديد</label>
        <label class="badge2"><input type="checkbox" name="impulsivity"> اندفاعية</label>
        <label class="badge2"><input type="checkbox" name="anger_issues"> غضب/انفجارات</label>
        <label class="badge2"><input type="checkbox" name="perfectionism"> كمالية مع تعطيل</label>
        <label class="badge2"><input type="checkbox" name="dependence"> اتكالية/تعلق عالي</label>
        <label class="badge2"><input type="checkbox" name="social_withdrawal"> انسحاب اجتماعي</label>
      </div>

      <div class="tile"><h3>🟣 تواصل/طيف توحد</h3>
        <label class="badge2"><input type="checkbox" name="asd_social"> صعوبات تواصل/إشارات اجتماعية</label>
        <label class="badge2"><input type="checkbox" name="sensory"> حساسية حسّية (أصوات/روائح/ملمس)</label>
        <label class="badge2"><input type="checkbox" name="rigidity"> صلابة روتين/اهتمامات ضيقة</label>
      </div>

    </div>

    <div class="tile" style="margin-top:10px"><label>ملاحظات<textarea name="notes" rows="4" placeholder="أي تفاصيل إضافية مهمة لك"></textarea></label></div>
    <div class="row">
      <button class="btn gold" type="submit">عرض النتيجة</button>
      <a class="btn" href="/cbt">🧠 فتح CBT</a>
    </div>
  </form>

  <script>
    const KEY='case_state_v2';
    function persistCase(){
      const f=document.querySelector('form[action="/case"]'); const data={};
      f.querySelectorAll('input[type=checkbox]').forEach(ch=>{ if(ch.checked) data[ch.name]=true; });
      ["age","marital","work","notes"].forEach(n=>{ const el=f.querySelector('[name="'+n+'"]'); if(el) data[n]=el.value||''; });
      localStorage.setItem(KEY, JSON.stringify(data));
    }
    (function restore(){
      try{
        const d=JSON.parse(localStorage.getItem(KEY)||'{}');
        Object.keys(d).forEach(k=>{
          const el=document.querySelector('[name="'+k+'"]');
          if(!el) return;
          if(el.type==='checkbox' && d[k]) el.checked=true;
          else if(el.tagName==='INPUT' || el.tagName==='TEXTAREA' || el.tagName==='SELECT') el.value=d[k];
        });
      }catch(e){}
    })();
  </script>
</div>
"""

def _cnt(d,*keys): return sum(1 for k in keys if d.get(k))

# Map: symptom-driven suggestion to CBT plans (keys used by CBT page)
# plan keys: ba, thought_record, sleep_hygiene, interoceptive_exposure, graded_exposure,
# ocd_erp, ptsd_grounding, problem_solving, worry_time, mindfulness, behavioral_experiments,
# safety_behaviors, bipolar_routine, relapse_prevention, social_skills
def suggest_plans(d):
    sug=[]
    # Depression
    dep_core=_cnt(d,"low_mood","anhedonia"); dep_more=_cnt(d,"fatigue","sleep_issue","appetite_change","worthlessness","poor_concentration","psychomotor","hopeless","somatic_pain")
    if dep_core>=1 and (dep_core+dep_more)>=5: sug+=["ba","thought_record","sleep_hygiene","problem_solving"]
    elif dep_core>=1 and (dep_core+dep_more)>=3: sug+=["ba","thought_record","sleep_hygiene"]
    # Safety
    if d.get("suicidal"): pass  # يظهر تنبيه لكن لا نضيف خطة خاصة
    # GAD
    if _cnt(d,"worry","tension","restlessness","irritability","mind_blank","sleep_anxiety","concentration_anxiety")>=3:
        sug+=["worry_time","mindfulness","problem_solving"]
    # Panic/Agoraphobia
    if d.get("panic_attacks") or d.get("panic_fear"): sug+=["interoceptive_exposure","safety_behaviors"]
    if d.get("agoraphobia") or d.get("specific_phobia"): sug+=["graded_exposure"]
    if d.get("social_fear"): sug+=["graded_exposure","social_skills","thought_record"]
    # OCD
    if d.get("obsessions") and d.get("compulsions"): sug+=["ocd_erp","safety_behaviors","mindfulness"]
    # Trauma
    if _cnt(d,"flashbacks","hypervigilance","startle","numbing","trauma_avoid","guilt_trauma")>=2:
        sug+=["ptsd_grounding","mindfulness","sleep_hygiene"]
    # Sleep
    if _cnt(d,"insomnia","hypersomnia","nightmares","irregular_sleep")>=1: sug+=["sleep_hygiene","mindfulness"]
    # ADHD
    if _cnt(d,"adhd_inattention","adhd_hyper","disorganization","time_blindness")>=2: sug+=["problem_solving","ba"]
    # Bipolar (psychoeducation + routine)
    if _cnt(d,"elevated_mood","decreased_sleep_need","grandiosity","racing_thoughts","pressured_speech","risk_spending")>=3:
        sug+=["bipolar_routine","sleep_hygiene"]
    # Substance
    if _cnt(d,"craving","withdrawal","use_harm","loss_control","relapse_history")>=2:
        sug+=["relapse_prevention","problem_solving","mindfulness"]
    # Personality/anger
    if _cnt(d,"emotion_instability","impulsivity","anger_issues","perfectionism","dependence","social_withdrawal")>=2:
        sug+=["mindfulness","problem_solving","social_skills"]
    # ASD supportive
    if _cnt(d,"asd_social","sensory","rigidity")>=2:
        sug+=["social_skills","problem_solving"]
    # Dedup & order
    seen=set(); ordered=[]
    for k in sug:
        if k not in seen: seen.add(k); ordered.append(k)
    return ordered[:8]  # نعرض الأهم 8 كحد أعلى

def preliminary_picks(d):
    picks=[]
    # Depression
    dep_core=_cnt(d,"low_mood","anhedonia")
    dep_more=_cnt(d,"fatigue","sleep_issue","appetite_change","worthlessness","poor_concentration","psychomotor","hopeless","somatic_pain")
    if dep_core>=1 and (dep_core+dep_more)>=5: picks.append(("نوبة اكتئابية جسيمة","≥5 أعراض مزاجية مع أثر وظيفي","درجة 80"))
    elif dep_core>=1 and (dep_core+dep_more)>=3: picks.append(("اكتئاب خفيف/متوسط","مجموعة أعراض مزاجية مستمرة","درجة 60"))
    elif dep_core>=1: picks.append(("مزاج منخفض/فتور","كتلة أعراض مزاجية جزئية","درجة 50"))
    # Anxiety
    if _cnt(d,"worry","tension","restlessness","irritability","mind_blank","sleep_anxiety","concentration_anxiety")>=3:
        picks.append(("قلق معمّم","قلق زائد صعب التحكم + توتر/نوم/تركيز","درجة 70"))
    # Panic & phobias
    if d.get("panic_attacks") or d.get("panic_fear"): picks.append(("نوبات هلع","نوبات مفاجئة وخشية/تجنّب لاحق","درجة 70"))
    if d.get("agoraphobia") or d.get("specific_phobia"): picks.append(("رُهاب/رهبة مواقف","خوف محدد/رهبة أماكن مع تجنّب","درجة 65"))
    if d.get("social_fear"): picks.append(("قلق اجتماعي","خشية تقييم الآخرين وتجنّب","درجة 65"))
    # OCD
    if d.get("obsessions") and d.get("compulsions"): picks.append(("وسواس قهري (OCD)","وساوس + أفعال قهرية مؤثرة","درجة 80"))
    # Trauma
    if _cnt(d,"flashbacks","hypervigilance","startle","numbing","trauma_avoid","guilt_trauma")>=2:
        picks.append(("آثار صدمة (PTSD/ASD)","استرجاعات/يقظة/تجنّب","درجة 70"))
    # Sleep
    if _cnt(d,"insomnia","hypersomnia","nightmares","irregular_sleep")>=1:
        picks.append(("اضطراب نوم","صعوبات في بدء/استمرار النوم/كوابيس","درجة 55"))
    # ADHD
    if _cnt(d,"adhd_inattention","adhd_hyper","disorganization","time_blindness")>=2:
        picks.append(("سمات ADHD","تشتت/اندفاعية مع أثر وظيفي","درجة 60"))
    # Bipolar
    if _cnt(d,"elevated_mood","decreased_sleep_need","grandiosity","racing_thoughts","pressured_speech","risk_spending")>=3:
        picks.append(("سمات هوس/ثنائي القطب","مزاج مرتفع/نوم قليل/اندفاع","درجة 70"))
    # Psychotic spectrum
    if _cnt(d,"hallucinations","delusions","disorganized_speech","negative_symptoms","catatonia")>=2 and d.get("decline_function"):
        picks.append(("فصام/طيف ذهاني","ذهانية مع أثر وظيفي ملحوظ","درجة 80"))
    # Eating/body
    if _cnt(d,"binge_eating","restrict_eating","body_image","purging")>=2:
        picks.append(("اضطراب الأكل","شراهة/تقييد/انشغال بالشكل","درجة 60"))
    # Substance
    if _cnt(d,"craving","withdrawal","use_harm","loss_control","relapse_history")>=2:
        picks.append(("تعاطي مواد","اشتهاء/انسحاب/استمرار رغم الضرر","درجة 80"))
    # Personality/anger
    if _cnt(d,"emotion_instability","impulsivity","anger_issues","perfectionism","dependence","social_withdrawal")>=3:
        picks.append(("صعوبات تنظيم عاطفي/سمات شخصية","تقلب/اندفاع/غضب/كمالية","درجة 60"))
    # ASD supportive
    if _cnt(d,"asd_social","sensory","rigidity")>=2:
        picks.append(("سمات طيف توحّد","تواصل/حساسية/صلابة روتين","درجة 55"))
    # Safety
    if d.get("suicidal"):
        picks.insert(0,("تنبيه أمان","وجود أفكار إيذاء — يُفضّل تواصلًا فوريًا مع مختص/الطوارئ","درجة 99"))
    return picks

RESULT_JS = r"""
<script>
  function saveJSON(){
    const data={
      items:[...document.querySelectorAll('#diag-items li')].map(li=>li.innerText),
      cbt:[...document.querySelectorAll('.badge2')].map(b=>b.innerText.replace('🔧 ','')),
      notes:[[NOTES_JSON]],
      created_at:new Date().toISOString(), build: window.__BUILD__
    };
    const a=document.createElement('a');
    a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
    a.download='case_result.json'; a.click(); URL.revokeObjectURL(a.href);
  }
  function buildShare(){
    const items=[...document.querySelectorAll('#diag-items li')].map(li=>'- '+li.innerText).join('\n');
    const msg='نتيجة دراسة الحالة — [[BRAND]]\n\n'+items+( [[NOTES_JSON]] ? '\n\nملاحظات: '+[[NOTES_JSON]]:'' )+'\n'+location.origin+'/case';
    const text=encodeURIComponent(msg);
    document.getElementById('share-wa').href='[[WA_BASE]]'+'?text='+text;
    document.getElementById('share-tg').href='https://t.me/share/url?url='+encodeURIComponent(location.origin+'/case')+'&text='+text;
  }
  buildShare();

  // نقل الاقتراحات للـCBT
  function openCBTWithSuggestions(keys){
    try{
      // نخزن اقتراحات الخطط محليًا ليقرأها /cbt
      localStorage.setItem('cbt_suggested', JSON.stringify(keys||[]));
    }catch(e){}
    const qp = keys && keys.length ? ('?suggest='+encodeURIComponent(keys.join(','))) : '';
    location.href = '/cbt'+qp;
  }
</script>
"""

def _render_case_result(picks, plan_keys, notes):
    # Human titles for badges (map will be re-labeled on CBT page anyway)
    PLAN_TITLES = {
      "ba":"BA — تنشيط سلوكي","thought_record":"TR — سجل أفكار","sleep_hygiene":"SH — نظافة النوم",
      "interoceptive_exposure":"IE — تعرّض داخلي","graded_exposure":"GE — تعرّض تدرّجي","ocd_erp":"ERP — وسواس قهري",
      "ptsd_grounding":"PTSD — تأريض/تنظيم","problem_solving":"PS — حلّ المشكلات","worry_time":"WT — وقت القلق",
      "mindfulness":"MB — يقظة ذهنية","behavioral_experiments":"BE — تجارب سلوكية","safety_behaviors":"SA — إيقاف سلوكيات آمنة",
      "bipolar_routine":"IPSRT — روتين ثنائي القطب","relapse_prevention":"RP — منع الانتكاس (إدمان)",
      "social_skills":"SS — مهارات اجتماعية"
    }
    lis = "".join([f"<li><b>{t}</b> — {w} <span class='small'>({s})</span></li>" for (t,w,s) in picks]) or "<li>لا توجد مؤشرات كافية.</li>"
    cbt_badges = "".join([f"<span class='badge2'>🔧 {PLAN_TITLES.get(k,k)}</span>" for k in plan_keys]) or "<span class='small'>—</span>"
    js = RESULT_JS.replace('[[NOTES_JSON]]', repr((notes or "").replace("\n"," ").strip()))\
                  .replace('[[BRAND]]', BRAND)\
                  .replace('[[WA_BASE]]', WA_URL.split("?")[0])

    # Motivational phrases
    praise = "أحسنت 👏 — كل خطوة وعي تقرّبك من التعافي. ثبّت هذا التقدم 🌿"

    # Build the final HTML
    html = f"""
    <div class="card">
      <div class='header-result'>
        <img src='{LOGO}' alt='logo' onerror="this.style.display='none'">
        <div><div style='font-weight:900;font-size:22px'>{BRAND}</div>
        <div class='small'>نتيجة دراسة الحالة — ملخص جاهز للطباعة والمشاركة</div></div>
      </div>

      <div class="note">{praise}</div>

      <h2>📌 الترشيحات</h2>
      <ol id="diag-items" style="line-height:1.95; padding-inline-start: 20px">{lis}</ol>

      <h3>🔧 أدوات CBT المقترحة</h3>
      <div>{cbt_badges}</div>

      {"<div class='tile' style='margin-top:10px'><b>ملاحظاتك:</b><br/>"+notes+"</div>" if notes else ""}

      <div class="row screen-only" style="margin-top:12px">
        <button class="btn alt" onclick="window.print()">🖨️ طباعة</button>
        <button class="btn" onclick="saveJSON()">💾 تنزيل JSON</button>
        <a class="btn wa" id="share-wa" target="_blank" rel="noopener">🟢 مشاركة واتساب</a>
        <a class="btn tg" id="share-tg" target="_blank" rel="noopener">✈️ مشاركة تيليجرام</a>
        <a class="btn gold" onclick="openCBTWithSuggestions({json.dumps(plan_keys)})">🧠 فتح CBT (منسّق حسب حالتك)</a>
      </div>

      <div class="row screen-only" style="margin-top:10px">
        <a class="btn" href="{PSYCHO_WA}" target="_blank" rel="noopener">👨‍🎓 تحويل لأخصائي نفسي</a>
        <a class="btn" href="{PSYCH_WA}"  target="_blank" rel="noopener">👨‍⚕️ تحويل لطبيب نفسي</a>
        <a class="btn" href="{SOCIAL_WA}" target="_blank" rel="noopener">🤝 تحويل لأخصائي اجتماعي</a>
      </div>

      {js}
    </div>
    """
    return html

@app.route("/case", methods=["GET","POST"])
def case():
    if request.method == "GET":
        return shell("دراسة الحالة — DSM مدمج", CASE_FORM, "case")
    # POST: collect checked boxes as True
    data = {k: True for k in request.form.keys()}
    notes = request.form.get("notes","").strip()
    picks = preliminary_picks(data)
    plans = suggest_plans(data)
    html = _render_case_result(picks, plans, notes)
    return shell("نتيجة دراسة الحالة", html, "case")

# ====== CBT (15 plans + suggestions via suggest param or localStorage) ======
CBT_HTML = r"""
<div class="card">
  <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
  <p class="small">اختر خطة/خطة+خطة ثم أنشئ جدول 7/10/14 يوم. <b>إذا جئت من «دراسة الحالة» سنقترح لك خططًا تلقائيًا.</b></p>

  <h2>خطط جاهزة (15 خطة)</h2>
  <div class="grid">

    <div class="tile"><h3 id="t-ba">BA — تنشيط سلوكي</h3><ol>
      <li>3 نشاطات مُجزية يوميًا.</li><li>قياس مزاج قبل/بعد.</li><li>رفع الصعوبة تدريجيًا.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ba')">اختيار</button><button class="btn" onclick="dl('ba')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-thought_record">TR — سجل أفكار</h3><ol>
      <li>موقف→فكرة.</li><li>دلائل مع/ضد.</li><li>بديل متوازن + تجربة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('thought_record')">اختيار</button><button class="btn" onclick="dl('thought_record')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-sleep_hygiene">SH — نظافة النوم</h3><ol>
      <li>أوقات ثابتة.</li><li>إيقاف الشاشات 60د.</li><li>لا كافيين قبل 6س.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('sleep_hygiene')">اختيار</button><button class="btn" onclick="dl('sleep_hygiene')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-interoceptive_exposure">IE — تعرّض داخلي</h3><ol>
      <li>إحداث إحساس آمن.</li><li>منع الطمأنة.</li><li>تكرار حتى الانطفاء.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('interoceptive_exposure')">اختيار</button><button class="btn" onclick="dl('interoceptive_exposure')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-graded_exposure">GE — تعرّض تدرّجي</h3><ol>
      <li>سُلّم 0→100.</li><li>تعرّض تصاعدي.</li><li>منع التجنّب/الطمأنة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('graded_exposure')">اختيار</button><button class="btn" onclick="dl('graded_exposure')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-ocd_erp">ERP — وسواس قهري</h3><ol>
      <li>قائمة وساوس/طقوس.</li><li>ERP 3× أسبوع.</li><li>قياس القلق.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ocd_erp')">اختيار</button><button class="btn" onclick="dl('ocd_erp')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-ptsd_grounding">PTSD — تأريض/تنظيم</h3><ol>
      <li>5-4-3-2-1.</li><li>تنفّس هادئ ×10.</li><li>روتين أمان.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('ptsd_grounding')">اختيار</button><button class="btn" onclick="dl('ptsd_grounding')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-problem_solving">PS — حل المشكلات</h3><ol>
      <li>تعريف دقيق.</li><li>عصف وتقييم.</li><li>خطة ومراجعة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('problem_solving')">اختيار</button><button class="btn" onclick="dl('problem_solving')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-worry_time">WT — وقت القلق</h3><ol>
      <li>تأجيل القلق.</li><li>تدوين وسياق.</li><li>عودة للنشاط.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('worry_time')">اختيار</button><button class="btn" onclick="dl('worry_time')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-mindfulness">MB — يقظة ذهنية</h3><ol>
      <li>تنفّس 5د.</li><li>فحص جسدي.</li><li>وعي غير حاكم.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('mindfulness')">اختيار</button><button class="btn" onclick="dl('mindfulness')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-behavioral_experiments">BE — تجارب سلوكية</h3><ol>
      <li>فرضية.</li><li>تجربة صغيرة.</li><li>مراجعة دلائل.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('behavioral_experiments')">اختيار</button><button class="btn" onclick="dl('behavioral_experiments')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-safety_behaviors">SA — إيقاف سلوكيات آمنة</h3><ol>
      <li>حصر السلوكيات.</li><li>تقليل تدريجي.</li><li>بدائل تكيفية.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('safety_behaviors')">اختيار</button><button class="btn" onclick="dl('safety_behaviors')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-bipolar_routine">IPSRT — روتين ثنائي القطب</h3><ol>
      <li>ثبات نوم/طعام/نشاط.</li><li>مراقبة مزاج.</li><li>إنذارات مبكرة.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('bipolar_routine')">اختيار</button><button class="btn" onclick="dl('bipolar_routine')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-relapse_prevention">RP — منع الانتكاس</h3><ol>
      <li>مثيرات شخصية.</li><li>بدائل فورية.</li><li>شبكة تواصل.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('relapse_prevention')">اختيار</button><button class="btn" onclick="dl('relapse_prevention')">تنزيل JSON</button></div></div>

    <div class="tile"><h3 id="t-social_skills">SS — مهارات اجتماعية</h3><ol>
      <li>رسائل حازمة.</li><li>تواصل بصري/نبرة.</li><li>تعرّض اجتماعي.</li></ol>
      <div class="row"><button class="btn alt" onclick="pick('social_skills')">اختيار</button><button class="btn" onclick="dl('social_skills')">تنزيل JSON</button></div></div>

  </div>

  <h2 style="margin-top:18px">📅 مولّد جدول الأيام (يدعم دمج خطتين)</h2>
  <div class="tile">
    <div class="row">
      <label>الخطة A: <select id="planA"></select></label>
      <label>الخطة B (اختياري): <select id="planB"><option value="">— بدون —</option></select></label>
      <label>المدة:
        <select id="daysSelect"><option value="7">7</option><option value="10">10</option><option value="14">14</option></select>
      </label>
      <button class="btn gold" onclick="buildChecklist()">إنشاء الجدول</button>
      <button class="btn alt" onclick="window.print()">طباعة</button>
      <button class="btn" onclick="saveChecklist()">تنزيل JSON</button>
      <a class="btn wa" id="share-wa" target="_blank" rel="noopener">واتساب</a>
      <a class="btn tg" id="share-tg" target="_blank" rel="noopener">تيليجرام</a>
    </div>
    <div id="checklist" style="margin-top:12px"></div>
  </div>

  <script>
    const PLANS = {
      ba:{title:"BA — تنشيط سلوكي",steps:["3 نشاطات مجزية","قياس مزاج قبل/بعد","رفع الصعوبة تدريجيًا"]},
      thought_record:{title:"TR — سجل أفكار",steps:["موقف→فكرة","دلائل مع/ضد","بديل متوازن/تجربة"]},
      sleep_hygiene:{title:"SH — نظافة النوم",steps:["مواعيد ثابتة","قطع الشاشات 60د","لا كافيين 6س قبل"]},
      interoceptive_exposure:{title:"IE — تعرّض داخلي",steps:["إحداث إحساس آمن","منع الطمأنة","تكرار حتى الانطفاء"]},
      graded_exposure:{title:"GE — تعرّض تدرّجي",steps:["سُلّم 0→100","تعرّض تصاعدي","منع التجنّب/الطمأنة"]},
      ocd_erp:{title:"ERP — وسواس قهري",steps:["قائمة وساوس/طقوس","ERP 3× أسبوع","قياس القلق"]},
      ptsd_grounding:{title:"PTSD — تأريض/تنظيم",steps:["5-4-3-2-1","تنفّس هادئ ×10","روتين أمان"]},
      problem_solving:{title:"PS — حل المشكلات",steps:["تعريف دقيق","عصف وتقييم","خطة ومراجعة"]},
      worry_time:{title:"WT — وقت القلق",steps:["تأجيل القلق","تدوين وسياق","عودة للنشاط"]},
      mindfulness:{title:"MB — يقظة ذهنية",steps:["تنفّس 5د","فحص جسدي","وعي غير حاكم"]},
      behavioral_experiments:{title:"BE — تجارب سلوكية",steps:["فرضية","تجربة صغيرة","مراجعة دلائل"]},
      safety_behaviors:{title:"SA — إيقاف سلوكيات آمنة",steps:["حصر السلوكيات","تقليل تدريجي","بدائل تكيفية"]},
      bipolar_routine:{title:"IPSRT — روتين ثنائي القطب",steps:["ثبات نوم/طعام/نشاط","مراقبة مزاج يومي","إشارات مبكرة"]},
      relapse_prevention:{title:"RP — منع الانتكاس (إدمان)",steps:["مثيرات شخصية","بدائل فورية","شبكة تواصل"]},
      social_skills:{title:"SS — مهارات اجتماعية",steps:["رسائل حازمة","تواصل بصري/نبرة","تعرّض اجتماعي"]}
    };

    const selectA=document.getElementById('planA');
    const selectB=document.getElementById('planB');

    (function fill(){
      for(const k in PLANS){
        const o=document.createElement('option'); o.value=k; o.textContent=PLANS[k].title; selectA.appendChild(o);
        const o2=document.createElement('option'); o2.value=k; o2.textContent=PLANS[k].title; selectB.appendChild(o2);
      }
      const saved=JSON.parse(localStorage.getItem('cbt_state')||'{}');
      selectA.value=saved.planA||'ba';
      if(saved.planB) selectB.value=saved.planB;
      if(saved.days) document.getElementById('daysSelect').value=String(saved.days);

      // التمايز من دراسة الحالة: نقرأ suggest من query أو من localStorage
      const qp=new URLSearchParams(location.search); let suggest=qp.get('suggest');
      if(!suggest){
        try{ suggest = (JSON.parse(localStorage.getItem('cbt_suggested')||'[]')||[]).join(','); }catch(e){}
      }
      if(suggest){
        const keys = suggest.split(',').map(s=>s.trim()).filter(Boolean);
        // نبرز الكروت المقترحة ونضبط الخطة A تلقائيًا
        if(keys.length){
          selectA.value = PLANS[keys[0]] ? keys[0] : (saved.planA||'ba');
        }
        keys.forEach(k=>{
          const h=document.getElementById('t-'+k);
          if(h){ h.style.outline='3px solid var(--g)'; h.style.boxShadow='0 0 0 4px rgba(255,215,0,.25)'; }
        });
      }
    })();

    function persist(){
      const state={planA:selectA.value, planB:selectB.value||'', days:parseInt(document.getElementById('daysSelect').value,10)||7};
      localStorage.setItem('cbt_state', JSON.stringify(state));
    }

    function pick(key){ selectA.value=key; persist(); window.scrollTo({top:document.getElementById('daysSelect').offsetTop-60,behavior:'smooth'}); }

    function dl(key){
      const data=PLANS[key]||{};
      const a=document.createElement('a');
      a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
      a.download= key + ".json"; a.click(); URL.revokeObjectURL(a.href);
    }

    function buildChecklist(){
      persist();
      const a = selectA.value; const b = selectB.value; const days = parseInt(document.getElementById('daysSelect').value,10);
      const A = PLANS[a]; const B = PLANS[b] || null;
      const steps = [...A.steps, ...(B?B.steps:[])];
      const titles = [A.title].concat(B?[B.title]:[]).join(" + ");

      let html="<h3 style='margin:6px 0'>"+titles+" — جدول "+days+" يوم</h3>";
      html += "<table class='table'><thead><tr><th>اليوم</th>";
      steps.forEach((s,i)=> html += "<th>"+(i+1)+". "+s+"</th>");
      html += "</tr></thead><tbody>";
      for(let d=1; d<=days; d++) {
        html+="<tr><td><b>"+d+"</b></td>";
        for(let i=0;i<steps.length;i++) html+="<td><input type='checkbox' /></td>";
        html+="</tr>";
      }
      html+="</tbody></table>";
      document.getElementById('checklist').innerHTML=html;
      updateShareLinks(titles, days);
    }

    function saveChecklist(){
      const rows = document.querySelectorAll('#checklist tbody tr');
      if(!rows.length) return;
      const head = document.querySelector('#checklist h3')?.innerText || '';
      const parts = head.split(' — جدول ');
      const days = parseInt((parts[1]||'7').split(' ')[0],10);
      const headerCells = [...document.querySelectorAll('#checklist thead th')].slice(1).map(th=>th.innerText);
      const progress = [];
      rows.forEach((tr, idx)=>{
        const done=[...tr.querySelectorAll('input[type=checkbox]')].map(ch=>ch.checked);
        progress.push({day:(idx+1), done});
      });
      const data = { title:parts[0]||'', steps:headerCells, days, progress, created_at:new Date().toISOString(), build: window.__BUILD__ };
      const a=document.createElement('a');
      a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
      a.download='cbt_checklist.json'; a.click(); URL.revokeObjectURL(a.href);
    }

    function updateShareLinks(title, days){
      const url = location.origin + '/cbt';
      const msg = "خطة CBT: "+title+"\\nمدة: "+days+" يوم\\n— من [[BRAND]]\\n"+url;
      const text = encodeURIComponent(msg);
      document.getElementById('share-wa').href='[[WA_BASE]]'+'?text='+text;
      document.getElementById('share-tg').href='https://t.me/share/url?url='+encodeURIComponent(url)+'&text='+text;
    }
  </script>
</div>
"""

@app.get("/cbt")
def cbt():
    wa_base = WA_URL.split("?")[0]
    html = CBT_HTML.replace("[[BRAND]]", BRAND).replace("[[WA_BASE]]", wa_base)
    return shell("CBT — خطط وتمارين", html, "cbt")

# ====== Health & Headers ======
@app.get("/health")
def health():
    return jsonify({"ok": True, "brand": BRAND, "build": CACHE_BUST}), 200

@app.after_request
def add_headers(resp):
    csp = (
        "default-src 'self' data: blob: https://t.me https://wa.me https://api.whatsapp.com; "
        "script-src 'self' 'unsafe-inline' data: blob: https://t.me https://wa.me https://api.whatsapp.com; "
        "style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: *; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors *"
    )
    resp.headers['Content-Security-Policy'] = csp
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return resp

if __name__ == "__main__":
    # تشغيل محليًا: python app.py
    # على Render: gunicorn app:app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
