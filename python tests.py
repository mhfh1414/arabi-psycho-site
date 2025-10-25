# -*- coding: utf-8 -*-
# ======================================================================
# عربي سايكو — tests.py
#
# صفحة اختبارات نفسية/شخصية سريعة (تثقيف فقط، ليست تشخيص رسمي)
#
# المقصود:
# - ملف مستقل (ما يلمس ppp / main app)
# - يعطي /tests صفحة HTML كاملة تحسب النتيجة بالمتصفح (JS فقط)
#
# النشر:
#   محلي: python tests.py  (يفتح على http://0.0.0.0:11000/tests)
#   Render/Railway: شغّله كسيرفر ثاني بـ gunicorn tests:app --bind 0.0.0.0:$PORT
#
# مهم قانونياً:
# - النتائج إرشادية فقط، لا تغني عن تقييم مختص ولا خطة علاج بدون إشراف.
# ======================================================================

import os
from datetime import datetime
from flask import Flask

app = Flask(__name__)

BRAND = os.environ.get("BRAND_NAME", "عربي سايكو")
LOGO  = os.environ.get("LOGO_URL", "https://upload.wikimedia.org/wikipedia/commons/3/36/Emoji_u1f985.svg")
SLOGAN = "«نراك بعين الاحترام، ونسير معك بخطوات عملية.»"
CACHE_BUST = os.environ.get("CACHE_BUST", datetime.utcnow().strftime("%Y%m%d%H%M%S"))

def page_tests():
    html = r"""
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>الاختبارات النفسية — عربي سايكو</title>
<link rel="icon" href="[[LOGO]]"/>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>
<meta http-equiv="Pragma" content="no-cache"/>
<meta http-equiv="Expires" content="0"/>

<style>
:root{
  --p:#4B0082;
  --p-dark:#3a0d72;
  --g:#FFD700;
  --bg:#f8f6ff;
  --ink:#2b1a4c;
  --line:#000000;
  --soft-shadow:0 10px 24px rgba(0,0,0,.06);
  --radius-xl:16px;
  --radius-md:12px;
  --radius-sm:10px;
  --card-border:#eee;
  --section-bg:#fff;
  --note-bg:#fff7d1;
  --note-border:#e5c100;
}
*{box-sizing:border-box}
body{
  margin:0;
  background:var(--bg);
  font-family:"Tajawal","Segoe UI",system-ui,sans-serif;
  color:var(--ink);
  font-size:16.5px;
  line-height:1.7;
  direction:rtl;
  text-align:right;
}
.wrap{
  max-width:1100px;
  margin:0 auto;
  padding:24px;
}
.headerbox{
  background:linear-gradient(180deg,var(--p),var(--p-dark));
  color:#fff;
  border:1px solid #000;
  border-radius:var(--radius-xl);
  box-shadow:0 10px 24px rgba(0,0,0,.4);
  padding:18px 20px;
  display:flex;
  flex-wrap:wrap;
  gap:16px;
  align-items:flex-start;
}
.header-left{
  display:flex;
  gap:12px;
  align-items:flex-start;
  color:#fff;
}
.header-left img{
  width:60px;
  height:60px;
  border-radius:14px;
  background:#fff;
  border:2px solid var(--g);
  box-shadow:0 4px 12px rgba(0,0,0,.6);
  object-fit:cover;
}
.brand-block{
  line-height:1.4;
  color:#fff;
  text-shadow:0 2px 4px rgba(0,0,0,.6);
}
.brand-main{
  font-weight:900;
  font-size:22px;
  color:#fff;
}
.brand-handle{
  display:inline-block;
  background:rgba(0,0,0,.35);
  border:1px solid #000;
  color:var(--g);
  font-size:.8rem;
  font-weight:700;
  line-height:1.4;
  padding:2px 8px;
  border-radius:999px;
  box-shadow:0 2px 4px rgba(0,0,0,.7);
}
.slogan{
  font-size:.9rem;
  font-weight:500;
  color:#fff;
  margin-top:6px;
}
.badge-style{
  display:inline-block;
  background:var(--g);
  color:#4b0082;
  border-radius:999px;
  padding:2px 10px;
  font-weight:900;
  font-size:.8rem;
  border:1px solid #000;
  box-shadow:0 2px 4px rgba(0,0,0,.7);
  margin-top:6px;
}

.header-note{
  flex:1;
  min-width:240px;
  background:rgba(0,0,0,.2);
  border:1px solid #000;
  border-radius:var(--radius-md);
  padding:12px;
  color:#fff;
  font-size:.9rem;
  font-weight:600;
  line-height:1.6;
  box-shadow:0 4px 12px rgba(0,0,0,.6);
}
.header-note ul{
  margin:0;
  padding-right:20px;
}
.header-note li{
  margin-bottom:6px;
}

.grid{
  display:grid;
  gap:18px;
  margin-top:24px;
}
@media(min-width:900px){
  .grid{
    grid-template-columns:repeat(2,minmax(0,1fr));
  }
}
.card{
  background:var(--section-bg);
  border:2px solid #000;
  border-radius:var(--radius-xl);
  box-shadow:var(--soft-shadow);
  padding:18px 20px;
}
.card h2{
  margin-top:0;
  font-size:20px;
  font-weight:800;
  color:var(--p);
}
.card p.small{
  font-size:.95rem;
  color:var(--ink);
  line-height:1.7;
  margin-top:0;
}
.q-block{
  background:#fff;
  border:1px solid var(--card-border);
  border-radius:var(--radius-md);
  box-shadow:0 6px 12px rgba(0,0,0,.04);
  padding:12px 14px;
  margin-bottom:10px;
  font-size:.9rem;
  line-height:1.6;
  color:#2b1a4c;
}
.q-head{
  font-weight:700;
  color:var(--p);
  margin-bottom:8px;
  font-size:.9rem;
}
.opts{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
}
.optbtn{
  flex:1;
  min-width:90px;
  background:#fafafa;
  color:#000;
  text-align:center;
  font-size:.8rem;
  line-height:1.4;
  font-weight:700;
  border-radius:var(--radius-md);
  border:1px solid #ddd;
  box-shadow:0 4px 10px rgba(0,0,0,.03);
  padding:8px;
  cursor:pointer;
  user-select:none;
}
.optbtn.active{
  background:var(--g);
  color:#4b0082;
  border:1px solid #000;
  box-shadow:0 4px 10px rgba(255,215,0,.4);
}

.result-box{
  background:var(--note-bg);
  border:1px dashed var(--note-border);
  border-radius:var(--radius-md);
  color:#5c4a00;
  box-shadow:0 4px 10px rgba(0,0,0,.05);
  padding:12px;
  font-size:.9rem;
  font-weight:600;
  line-height:1.6;
  margin-top:14px;
  white-space:pre-line;
}
.btn-row{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  margin-top:10px;
}
.btn{
  display:inline-block;
  background:var(--p);
  color:#fff;
  text-decoration:none;
  padding:10px 14px;
  border-radius:var(--radius-md);
  font-weight:800;
  cursor:pointer;
  border:1px solid #000;
  box-shadow:0 4px 12px rgba(0,0,0,.25);
  font-size:.8rem;
  line-height:1.4;
  text-align:center;
  min-width:fit-content;
}
.btn.alt{
  background:#5b22a6;
}
.footer{
  margin-top:32px;
  text-align:center;
  background:var(--p-dark);
  border-top:1px solid #000;
  border-bottom:1px solid #000;
  color:#fff;
  font-size:.75rem;
  font-weight:600;
  line-height:1.6;
  padding:16px;
  text-shadow:0 2px 4px rgba(0,0,0,.7);
}
.footer .build{
  color:var(--g);
  font-size:.7rem;
  font-weight:700;
  margin-top:4px;
}
</style>

<script>
window.__BUILD__="[[BUILD]]";

/*
 أربع مقاييس مبسطة:
 - PHQ-9 mood (اكتئاب)
 - GAD-7 anxiety (قلق عام)
 - PCL-5 style (توتر/صدمة): بروح مختص لو عالي
 - Self-esteem ثقة بالنفس مبسطة

 كل سؤال ياخذ درجة 0..3
*/

const TESTS = {
  phq9: {
    title: "مزاج واكتئاب (مؤشرات اكتئابية)",
    info: "هذا يساعدك تقيس المزاج المنخفض وفقدان المتعة. مو تشخيص رسمي.",
    questions: [
      "قلة الاهتمام / قلة المتعة بالأشياء؟",
      "شعور بالحزن أو الإحباط أو اليأس؟",
      "مشاكل نوم (صعوبة/كثرة)؟",
      "إرهاق أو طاقة منخفضة؟",
      "شهية قليلة أو أكل أكثر من المعتاد؟",
      "إحساس بأنك سيئ عن نفسك / فاشل؟",
      "صعوبة تركيز (قراءة/تلفزيون/شغل)؟",
      "بطء بالحركة أو تململ وعصبية واضحة للناس؟",
      "أفكار أنك تود إلحاق الأذى بنفسك أو أنك أفضل بدون حياة؟"
    ],
    scale:[
      "أبدًا (0)",
      "عدة أيام (1)",
      "أغلب الأيام (2)",
      "تقريبًا كل يوم (3)"
    ],
    interpret: score=>{
      if(score<=4) return "مؤشرات اكتئابية منخفضة.\nاستمر على الروتين الصحي والدعم الاجتماعي.";
      if(score<=9) return "درجة خفيفة. جرّب خطة تنشيط سلوكي / نوم / دعم قريب.";
      if(score<=14) return "درجة متوسطة. يفضّل استشارة مختص (أخصائي نفسي أو طبيب نفسي).";
      if(score<=19) return "درجة متوسطة-عالية. يوصى تقييم علاجي مهني قريب.";
      return "درجة عالية جدًا. لو معك أفكار أذى لنفسك، اطلب مساعدة طبية/طارئة فورًا.";
    }
  },

  gad7: {
    title: "توتر وقلق عام (مؤشرات قلق)",
    info: "هل القلق مسيطر عليك؟ هذا الاختبار شائع للقلق المعمم.",
    questions: [
      "عصبية / توتر / قلق مستمر؟",
      "ما تقدر توقف القلق أو تتحكم فيه؟",
      "قلق مفرط على أشياء كثيرة؟",
      "صعوبة استرخاء الجسم؟",
      "أرق أو صعوبة الجلوس بهدوء بسبب القلق؟",
      "انفعال / عصبية بسرعة؟",
      "خوف كأن شي سيئ بيصير؟"
    ],
    scale:[
      "أبدًا (0)",
      "أيام قليلة (1)",
      "أغلب الأيام (2)",
      "تقريبًا كل يوم (3)"
    ],
    interpret: score=>{
      if(score<=4) return "قلق منخفض. ممتاز 👌 استمر بتنظيم النوم والتنفس البطيء.";
      if(score<=9) return "قلق خفيف. جرّب يقظة ذهنية وتمارين تهدئة (تنفس 4-6-8).";
      if(score<=14) return "قلق متوسط. استشارة مختص سلوكي/نفسي بتفيدك.";
      return "قلق شديد. يفضّل تقييم مهني (علاج سلوكي وأحيانًا دواء بإشراف طبيب).";
    }
  },

  trauma: {
    title: "توتر ما بعد حدث صعب (مؤشرات صدمة)",
    info: "لو مريت بحدث صعب/مؤلم، هل ما زال يأثر عليك يوميًا؟",
    questions: [
      "كوابيس / تذكّر مزعج للحدث؟",
      "تحاول تتجنّب أشياء تذكّرك بالحدث؟",
      "صعوبة تهدئة جسمك (تيقظ مفرط)؟",
      "تقلّب مزاج قوي أو عصبية/انفجار غضب سريع؟",
      "إحساس بالخطر أو الحذر طول الوقت؟",
      "إحساس بالانفصال / برود عاطفي / كأنك مو موجود؟"
    ],
    scale:[
      "لا / تقريبًا أبدًا (0)",
      "أحيانًا (1)",
      "غالبًا (2)",
      "باستمرار تقريبًا (3)"
    ],
    interpret: score=>{
      if(score<=5) return "مؤشرات صدمة منخفضة حاليًا.";
      if(score<=10) return "قد يكون في ضغط/توتر بعد الحدث. مفيد تحكي مع مختص دعم نفسي/اجتماعي.";
      if(score<=15) return "إجهاد صدمة ملحوظ. يُنصح بعلاج مختص بالصدمة (تنظيم وتهدئة جسدية).";
      return "مستوى عالٍ من أعراض الصدمة. يوصى تقييم علاجي متخصص بشكل قريب.";
    }
  },

  esteem: {
    title: "نظرة الذات / الثقة بالنفس",
    info: "كيف تشوف نفسك وقيمتك؟ (هذا يؤثر على العلاقات والمزاج)",
    questions: [
      "أحس أني أقل من الناس حولي؟",
      "أجلد نفسي بسرعة إذا غلطت؟",
      "صعب أطلب احتياجي بصوت واضح؟",
      "أخاف أزعّل أحد لو قلت 'لا'؟",
      "أحس إني ما أستحق معاملة محترمة؟"
    ],
    scale:[
      "أبدًا (0)",
      "أحيانًا (1)",
      "غالبًا (2)",
      "تقريبًا دائم (3)"
    ],
    interpret: score=>{
      if(score<=3) return "ثقتك بنفسك جيدة عمومًا 👏 استمر.";
      if(score<=6) return "في بعض مناطق ضعف تقدير الذات. تمارين تعزيز الثقة (كتابة إنجازات صغيرة يوميًا) تفيد.";
      if(score<=10) return "تقدير ذات منخفض. مفيد تدريب مهارات حدود صحية و'أنا أستحق احترام'.";
      return "تقدير ذات ضعيف جدًا. دعم علاجي (علاج سلوكي معرفي / علاج علاقات) قد يكون مهم لك.";
    }
  }
};

function renderTest(key){
  const t = TESTS[key];
  let html = "";
  html += "<div class='card' id='test-"+key+"'>";
  html += "<h2>"+t.title+"</h2>";
  html += "<p class='small'>"+t.info+"</p>";

  t.questions.forEach((q,qi)=>{
    html += "<div class='q-block'>";
    html += "<div class='q-head'>س"+(qi+1)+". "+q+"</div>";
    html += "<div class='opts'>";
    t.scale.forEach((label,si)=>{
      html += "<div class='optbtn' data-test='"+key+"' data-q='"+qi+"' data-score='"+si+"' onclick='pickOption(this)'>"+label+"</div>";
    });
    html += "</div></div>";
  });

  html += "<div class='btn-row'>";
  html += "<div class='btn' onclick='calcScore(\""+key+"\")'>احسب النتيجة 📊</div>";
  html += "<div class='btn alt' onclick='resetTest(\""+key+"\")'>إعادة ضبط ↺</div>";
  html += "</div>";

  html += "<div class='result-box' id='res-"+key+"' style='display:none;'></div>";

  html += "</div>";
  return html;
}

function pickOption(el){
  const test = el.getAttribute("data-test");
  const q    = el.getAttribute("data-q");
  document.querySelectorAll('.optbtn[data-test="'+test+'"][data-q="'+q+'"]').forEach(b=>{
    b.classList.remove("active");
  });
  el.classList.add("active");
}

function calcScore(key){
  let score = 0;
  let answered = 0;
  document.querySelectorAll('.optbtn[data-test="'+key+'"]').forEach(btn=>{
    if(btn.classList.contains("active")){
      score += parseInt(btn.getAttribute("data-score"),10)||0;
      answered += 1;
    }
  });
  const totalQ = TESTS[key].questions.length;
  const box = document.getElementById("res-"+key);
  if(answered < totalQ){
    box.style.display="block";
    box.textContent="جاوب كل الأسئلة أول 🙏 ("+answered+"/"+totalQ+")";
    return;
  }
  const txt = "مجموعك = "+score+"\n\n"+TESTS[key].interpret(score)+"\n\nتنبيه: هذه أداة وعي ذاتي فقط. ما تغني عن تقييم مختص.";
  box.style.display="block";
  box.textContent=txt;
}

function resetTest(key){
  document.querySelectorAll('.optbtn[data-test="'+key+'"]').forEach(btn=>{
    btn.classList.remove("active");
  });
  const box = document.getElementById("res-"+key);
  box.style.display="none";
  box.textContent="";
}

window.addEventListener("DOMContentLoaded",()=>{
  const container = document.getElementById("tests-container");
  container.innerHTML =
      renderTest("phq9")
    + renderTest("gad7")
    + renderTest("trauma")
    + renderTest("esteem");
});
</script>
</head>

<body>
<div class="wrap">

  <section class="headerbox">
    <div class="header-left">
      <img src="[[LOGO]]" alt="logo" onerror="this.style.display='none'">
      <div class="brand-block">
        <div class="brand-main">[[BRAND]]</div>
        <div class="brand-handle">@ArabiPsycho</div>
        <div class="slogan">[[SLOGAN]]</div>
        <div class="badge-style">اختبارات نفسية / شخصية</div>
      </div>
    </div>

    <div class="header-note">
      <ul>
        <li>هذه النتائج <b>مو تشخيص رسمي</b> ولا وصفة علاج.</li>
        <li>الهدف: وعي ذاتي مبدئي يساعدك تعرف "وين أنا تقريبًا؟".</li>
        <li>لو فيه خطر على سلامتك أو أفكار أذى لنفسك أو لغيرك ⇦ تدخل طبي/إسعافي مباشر.</li>
        <li>حاول تطبع النتيجة أو تحفظ سكرين، وتناقشها مع مختص محترم يتعامل معك بكرامة 🙏</li>
      </ul>
    </div>
  </section>

  <div class="grid" id="tests-container"></div>

  <footer class="footer">
    <div>© جميع الحقوق محفوظة لـ [[BRAND]] — [[SLOGAN]]</div>
    <div class="build">BUILD [[BUILD]] — ملف الاختبارات (tests.py)</div>
  </footer>

</div>
</body>
</html>
"""
    return (
        html
        .replace("[[LOGO]]", LOGO)
        .replace("[[BRAND]]", BRAND)
        .replace("[[SLOGAN]]", SLOGAN)
        .replace("[[BUILD]]", CACHE_BUST)
    )


@app.get("/tests")
def tests():
    return page_tests()


if __name__ == "__main__":
    # تشغيل محلي:
    #   python tests.py
    #
    # تشغيل production (مثلاً Render):
    #   gunicorn tests:app --bind 0.0.0.0:$PORT
    #
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "11000")))
