# -*- coding: utf-8 -*-
"""
عربي سايكو – واجهة فاخرة مبهجة
- خلفيات متحركة + جزيئات + شِمِر + رِبل + Scroll-Reveal
- أقسام: DSM-5 / CBT / اختبارات / علاج الإدمان / تواصل
- أزرار وأيقونات SVG بدون أي مكتبات خارجية
- متوافق مع Render (app = Flask(__name__), وبدون مسارات ستاتيكية معقدة)
"""

from flask import Flask, render_template_string, url_for

app = Flask(__name__)

HOME_HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>عربي سايكو | الراحة النفسية تبدأ هنا</title>
<style>
/* ====== أساسيات ====== */
:root{
  --bg1:#6EE7B7; --bg2:#3B82F6; --bg3:#9333EA;
  --glass: rgba(255,255,255,.14);
  --stroke: rgba(255,255,255,.5);
  --text:#FFFFFF; --text-dim:#F3F4F6;
  --primary:#8B5CF6; --primary-2:#6366F1; --accent:#22D3EE;
  --ok:#34D399; --warn:#FBBF24; --bad:#F87171;
  --shadow: 0 10px 30px rgba(0,0,0,.30);
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; color:var(--text); font-family: "Tahoma", system-ui, -apple-system, "Segoe UI", Arial;
  background: linear-gradient(135deg,var(--bg1),var(--bg2),var(--bg3));
  background-size: 300% 300%; animation:bgMove 18s ease-in-out infinite;
  overflow-x:hidden;
}
@keyframes bgMove{
  0%{background-position:0% 50%}
  50%{background-position:100% 50%}
  100%{background-position:0% 50%}
}

/* ====== جزيئات عائمة ====== */
.particles {position:fixed; inset:0; pointer-events:none; overflow:hidden; z-index:0}
.p {position:absolute; width:10px; height:10px; border-radius:50%;
    background: radial-gradient(circle at 30% 30%, #fff, rgba(255,255,255,.2));
    filter:blur(.2px); opacity:.7; animation:floatY var(--d) linear infinite;
}
@keyframes floatY{
  from{ transform: translate(var(--x), 110vh) scale(var(--s)); }
  to  { transform: translate(calc(var(--x) + 20px), -10vh) scale(var(--s)); }
}

/* ====== تخطيط ====== */
.wrapper{position:relative; z-index:1; padding:28px}
.header{
  display:flex; align-items:center; justify-content:space-between;
  gap:16px; padding:16px 20px; border:1px solid var(--stroke);
  background:var(--glass); backdrop-filter: blur(10px);
  border-radius:18px; box-shadow:var(--shadow);
}
.brand{display:flex; align-items:center; gap:14px}
.logo{width:46px; height:46px; border-radius:14px;
      background:linear-gradient(135deg,#fff, #e5e7eb);
      display:grid; place-items:center; color:#1f2937; font-weight:900}
.brand h1{margin:0; font-size:24px}
.brand small{display:block; color:var(--text-dim); font-size:12px}

.nav{display:flex; gap:10px; flex-wrap:wrap}
.btn{
  --h:56px; --pad:24px; --r:16px;
  min-height:var(--h); padding:12px var(--pad);
  display:inline-flex; align-items:center; gap:12px;
  background:linear-gradient(135deg,var(--primary-2),var(--primary));
  border:none; color:#fff; font-weight:700; border-radius:var(--r);
  cursor:pointer; box-shadow:var(--shadow); position:relative; overflow:hidden;
  transition: transform .2s ease, box-shadow .2s ease;
}
.btn:before{
  content:""; position:absolute; inset:0; background:
  linear-gradient(115deg, rgba(255,255,255,.35) 0%, rgba(255,255,255,0) 35%);
  opacity:.0; transition:opacity .25s;
}
.btn:hover{ transform:translateY(-3px); box-shadow:0 16px 36px rgba(0,0,0,.35); }
.btn:hover:before{opacity:.3}
.btn--ghost{
  background:transparent; border:1.5px solid var(--stroke);
  color:#fff;
}

/* تموج (Ripple) */
.btn .ripple{
  position:absolute; border-radius:50%; transform:scale(0); animation:ripple .6s linear; background:rgba(255,255,255,.5);
}
@keyframes ripple{
  to{transform:scale(12); opacity:0}
}

/* ====== بطل الصفحة ====== */
.hero{
  margin:26px 0; padding:36px; border-radius:22px;
  border:1px solid var(--stroke); background:var(--glass);
  backdrop-filter: blur(12px); box-shadow:var(--shadow);
  display:grid; gap:18px;
}
.hero h2{margin:6px 0 0; font-size:40px; line-height:1.2; text-shadow:2px 2px 6px rgba(0,0,0,.28)}
.hero p{margin:0; font-size:18px; color:var(--text-dim)}

/* وميض النص */
.shimmer{
  background: linear-gradient(90deg, rgba(255,255,255,.1), rgba(255,255,255,.8), rgba(255,255,255,.1));
  background-size: 200% 100%;
  -webkit-background-clip: text; background-clip:text; color: transparent;
  animation:sh 2.6s infinite;
}
@keyframes sh{
  0%{background-position:200% 0}
  100%{background-position:-200% 0}
}

/* ====== الشبكة ====== */
.grid{
  display:grid; gap:18px;
  grid-template-columns:repeat(12,minmax(0,1fr));
}
.col-12{grid-column: span 12}
.col-6{grid-column: span 6}
.col-4{grid-column: span 4}
.col-3{grid-column: span 3}
@media (max-width:1100px){ .col-3{grid-column: span 4} }
@media (max-width:900px) { .col-6{grid-column: span 12} .col-4{grid-column: span 6} .col-3{grid-column: span 6} }

/* ====== الكروت ====== */
.card{
  background:var(--glass); border:1px solid var(--stroke); border-radius:20px;
  padding:22px; box-shadow:var(--shadow); position:relative; overflow:hidden;
  transform:translateY(0); transition:transform .25s ease, box-shadow .25s ease;
}
.card:hover{ transform:translateY(-5px); box-shadow:0 18px 36px rgba(0,0,0,.35) }
.card h3{margin:2px 0 10px; font-size:22px}
.card p{margin:0; color:var(--text-dim); line-height:1.8}
.badge{display:inline-flex; align-items:center; gap:8px; padding:6px 12px; border-radius:999px;
       background:rgba(255,255,255,.14); border:1px solid var(--stroke); font-size:13px;}
.tag{display:inline-block; padding:6px 10px; border-radius:10px; background:rgba(255,255,255,.12); border:1px solid var(--stroke); font-size:12px; margin-inline:4px}

.icon{
  width:26px; height:26px; display:inline-flex; align-items:center; justify-content:center;
  border-radius:8px; background:linear-gradient(135deg,var(--accent),#60A5FA);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.6);
}

/* ====== اقتباسات ====== */
.quotes{display:flex; gap:12px; flex-wrap:wrap}
.quote{
  padding:10px 16px; border-radius:14px; background:rgba(255,255,255,.1);
  border:1px solid var(--stroke); font-size:14px; color:#fff
}

/* ====== فوتر ====== */
footer{
  margin:34px 0 8px; padding:18px; border-radius:18px; border:1px solid var(--stroke);
  background:var(--glass); text-align:center; color:var(--text-dim)
}

/* ====== ظهور عند التمرير ====== */
.reveal{ opacity:0; transform: translateY(14px) scale(.98); transition: all .6s cubic-bezier(.2,.6,.2,1)}
.reveal.in{ opacity:1; transform: translateY(0) scale(1)}

/* ====== أزرار ثانوية ====== */
.actions{display:flex; flex-wrap:wrap; gap:10px}
.small{
  background:transparent; border:1.5px solid var(--stroke); color:#fff; border-radius:12px;
  padding:10px 14px; font-weight:700
}

/* ====== روابط ====== */
a{color:#fff; text-decoration:none}
a.underline{text-decoration:underline}
</style>
</head>
<body>

<!-- جزيئات -->
<div class="particles" aria-hidden="true">
  <!-- 24 نقطة عشوائية -->
  <script>
    (function(){
      const root=document.currentScript.parentElement;
      for(let i=0;i<24;i++){
        const e=document.createElement('div'); e.className='p';
        const x=Math.random()*100; const s=.4+Math.random()*1.4;
        const d=8+Math.random()*14; e.style.setProperty('--x', x+'vw');
        e.style.setProperty('--s', s); e.style.setProperty('--d', d+'s');
        root.appendChild(e);
      }
    })();
  </script>
</div>

<div class="wrapper">

  <!-- الهيدر -->
  <header class="header reveal">
    <div class="brand">
      <div class="logo">AS</div>
      <div>
        <h1>عربي سايكو</h1>
        <small>الوعي بداية التغيير ✨</small>
      </div>
    </div>

    <nav class="nav">
      <a href="#dsm"   class="btn btn--ghost" data-ripple>📘 DSM-5</a>
      <a href="#cbt"   class="btn btn--ghost" data-ripple>🧠 CBT</a>
      <a href="#tests" class="btn btn--ghost" data-ripple>📝 اختبارات</a>
      <a href="#add"   class="btn btn--ghost" data-ripple>🚭 الإدمان</a>
      <a href="#contact" class="btn" data-ripple>📞 تواصل</a>
    </nav>
  </header>

  <!-- البانر -->
  <section class="hero reveal">
    <span class="badge"><span class="icon">✓</span>مساحتك الآمنة</span>
    <h2 class="shimmer">الراحة النفسية تبدأ من هنا 🌿</h2>
    <p>نقدّم أدوات عملية وعلمية تُسهِّل عليك فهم نفسك والتعامل مع مشاعرك.  
      هنا ستجد دليل <b>DSM-5</b> المبسّط، وتمارين <b>CBT</b>، واختبارات شخصية، ومسارات دعم للتعافي من الإدمان.</p>

    <div class="quotes">
      <div class="quote">✨ أنت تستحق السكينة.</div>
      <div class="quote">🌸 كل يوم فرصة جديدة.</div>
      <div class="quote">💡 الوعي بداية التحرّر.</div>
      <div class="quote">🤝 لست وحدك.. نحن معك.</div>
      <div class="quote">🕊️ خُطوة صغيرة تصنع فرقًا كبيرًا.</div>
    </div>

    <div class="actions" style="margin-top:12px">
      <a href="#start" class="small" data-ripple>ابدأ الآن</a>
      <a href="#contact" class="small" data-ripple>طلب استشارة</a>
      <a href="https://t.me/Mhfh1414" target="_blank" class="small underline">قناة تيليجرام</a>
    </div>
  </section>

  <!-- الشبكة الرئيسية -->
  <section id="start" class="grid">

    <!-- DSM -->
    <article id="dsm" class="card col-6 reveal">
      <span class="badge"><span class="icon">📘</span> DSM-5</span>
      <h3>دليل الاضطرابات النفسية – مبسّط</h3>
      <p>ملخّصات واضحة لأهم التصنيفات مع مؤشرات وماذا-تفعل-الآن:  
         اكتئاب، قلق، وسواس، اضطرابات النوم، الصدمة، وغير ذلك.  
         الهدف ليس التشخيص الذاتي، بل الوعي والاتجاه للمتخصص عند الحاجة.</p>
      <div style="margin-top:12px">
        <span class="tag">ملخّصات</span><span class="tag">خطط أوليّة</span><span class="tag">تثقيفي</span>
      </div>
      <div style="margin-top:14px">
        <a class="small" href="/dsm" data-ripple>افتح قسم DSM-5</a>
      </div>
    </article>

    <!-- CBT -->
    <article id="cbt" class="card col-6 reveal">
      <span class="badge"><span class="icon">🧠</span> CBT</span>
      <h3>العلاج السلوكي المعرفي – تمارين عملية</h3>
      <p>دفتر أفكار، إعادة هيكلة الأفكار، الموازنة، التعرض المتدرّج،  
         جدول المتعة/الإنجاز، وأوراق عمل أسبوعية قابلة للطباعة.</p>
      <div style="margin-top:12px">
        <span class="tag">أوراق عمل</span><span class="tag">خطوات صغيرة</span><span class="tag">نتائج ملموسة</span>
      </div>
      <div style="margin-top:14px">
        <a class="small" href="/cbt" data-ripple>ابدأ تمارين CBT</a>
      </div>
    </article>

    <!-- اختبارات -->
    <article id="tests" class="card col-4 reveal">
      <span class="badge"><span class="icon">📝</span> اختبارات</span>
      <h3>اختبارات نفسية وشخصية</h3>
      <p>مستوى المزاج، القلق، أفكار الوسواس، نمط الشخصيّة،  
         نتائج فورية مع نصائح لتحسين العافية.</p>
      <div style="margin-top:12px">
        <span class="tag">نتائج فورية</span><span class="tag">بدون تسجيل</span>
      </div>
      <div style="margin-top:14px">
        <a class="small" href="/tests" data-ripple>جرّب الآن</a>
      </div>
    </article>

    <!-- الإدمان -->
    <article id="add" class="card col-4 reveal">
      <span class="badge"><span class="icon">🚭</span> الإدمان</span>
      <h3>مسار تعافٍ إنساني وواقعي</h3>
      <p>فهم الدوافع، إدارة المثيرات، خطط النجاة، دوائر الدعم،  
         والمتابعة اليومية بلغة تقدّر إنسانيتك بلا جلد.</p>
      <div style="margin-top:12px">
        <span class="tag">تعافٍ</span><span class="tag">مجتمع داعم</span>
      </div>
      <div style="margin-top:14px">
        <a class="small" href="/addiction" data-ripple>ابدأ المسار</a>
      </div>
    </article>

    <!-- تواصل -->
    <article id="contact" class="card col-4 reveal">
      <span class="badge"><span class="icon">📞</span> تواصل</span>
      <h3>نسمعك بكل ود</h3>
      <p>لدعم سريع، شراكات، أو استفسارات:  
         تيليجرام: <a class="underline" href="https://t.me/Mhfh1414" target="_blank">@Mhfh1414</a></p>
      <div style="margin-top:14px">
        <a class="small" href="https://t.me/Mhfh1414" target="_blank" data-ripple>راسلنا على تيليجرام</a>
      </div>
    </article>

  </section>

  <footer class="reveal">
    © 2025 عربي سايكو — بإشراف موسى وأبو فارس 💙 | كل يوم أخفّ من اللي قبله
  </footer>

</div>

<script>
/* ====== Ripple على كل زر يحمل data-ripple ====== */
document.addEventListener('click', function(e){
  const t = e.target.closest('[data-ripple]');
  if(!t) return;
  const rect=t.getBoundingClientRect();
  const span=document.createElement('span');
  span.className='ripple';
  const size=Math.max(rect.width, rect.height);
  span.style.width=span.style.height=size+'px';
  span.style.left=(e.clientX-rect.left - size/2)+'px';
  span.style.top =(e.clientY-rect.top  - size/2)+'px';
  t.appendChild(span);
  span.addEventListener('animationend', ()=>span.remove());
}, false);

/* ====== Scroll-Reveal ====== */
const revealEls=[...document.querySelectorAll('.reveal')];
const io=new IntersectionObserver((entries)=>{
  entries.forEach(en=>{ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target);} });
},{threshold:.15});
revealEls.forEach(el=>io.observe(el));

</script>
</body>
</html>
"""

# صفحات ثانوية بسيطة – جاهزة للتبديل لاحقًا بصفحات كاملة
DSM_HTML = """
<h2 style="font-family:Tahoma; text-align:center; color:#0f172a">📘 قسم DSM-5</h2>
<p style="text-align:center; color:#334155">ملخّصات مبسّطة للتصنيفات + مؤشرات + ماذا تفعل الآن.</p>
"""

CBT_HTML = """
<h2 style="font-family:Tahoma; text-align:center; color:#0f172a">🧠 قسم CBT</h2>
<p style="text-align:center; color:#334155">دفتر أفكار، إعادة هيكلة، جداول متعة/إنجاز، وتعرّض متدرّج.</p>
"""

TESTS_HTML = """
<h2 style="font-family:Tahoma; text-align:center; color:#0f172a">📝 الاختبارات</h2>
<p style="text-align:center; color:#334155">اختبارات سريعة بنتائج فورية وإرشادات صحية.</p>
"""

ADD_HTML = """
<h2 style="font-family:Tahoma; text-align:center; color:#0f172a">🚭 التعافي من الإدمان</h2>
<p style="text-align:center; color:#334155">خُطة إنسانية واقعية لإدارة المثيرات والدوافع وبناء دعم.</p>
"""

CONTACT_HTML = """
<h2 style="font-family:Tahoma; text-align:center; color:#0f172a">📞 تواصل معنا</h2>
<p style="text-align:center; color:#334155">تيليجرام: <a href="https://t.me/Mhfh1414" target="_blank">@Mhfh1414</a></p>
"""

# ====== Routes ======
@app.route("/")
def home(): return render_template_string(HOME_HTML)

@app.route("/dsm")
def dsm(): return render_template_string(DSM_HTML)

@app.route("/cbt")
def cbt(): return render_template_string(CBT_HTML)

@app.route("/tests")
def tests(): return render_template_string(TESTS_HTML)

@app.route("/addiction")
def addiction(): return render_template_string(ADD_HTML)

@app.route("/contact")
def contact(): return render_template_string(CONTACT_HTML)

# ====== Local run (ignored by gunicorn) ======
if __name__ == "__main__":
    # Render يمر عبر gunicorn, لكن local dev يشتغل هكذا:
    app.run(host="0.0.0.0", port=5000, debug=True)
