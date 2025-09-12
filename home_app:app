# -*- coding: utf-8 -*-
# home_app.py — الواجهة الرئيسية "عربي سايكو"

from flask import Flask, render_template_string

app = Flask(__name__)

HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>عربي سايكو | المنصّة النفسية</title>
<meta name="description" content="عربي سايكو: منصّة نفسية عربية تقدم تشخيصًا مبدئيًا وفق DSM وأدوات CBT وبرنامج التعافي من الإدمان. سرية وخصوصية تامة.">
<style>
  :root{
    --bg1:#0b1530; --bg2:#0f2b6b; --acc:#ffd166; --mint:#00d4aa; --rose:#ff5d7a; --sky:#62b0ff;
    --card: rgba(255,255,255,.10); --card-b: rgba(255,255,255,.18); --txt:#eef3ff
  }
  *{box-sizing:border-box}
  body{
    margin:0; font-family: "Tajawal", "Segoe UI", Tahoma, sans-serif; color:var(--txt);
    background: radial-gradient(80% 120% at 100% 0%, #153067 0%, #091225 55%),
                linear-gradient(135deg, var(--bg1), var(--bg2));
    min-height:100vh;
  }
  .wrap{max-width:1150px;margin:0 auto;padding:22px}
  /* ====== Nav ====== */
  .nav{
    display:flex; align-items:center; justify-content:space-between; gap:12px;
    padding:10px 14px; border-radius:16px; background:var(--card); border:1px solid var(--card-b);
    backdrop-filter: blur(8px);
  }
  .brand{display:flex; align-items:center; gap:10px; font-weight:900; letter-spacing:.3px}
  .logo{
    width:44px;height:44px;border-radius:12px;
    background: conic-gradient(from 220deg, #ffd166, #9b5cff, #00d4aa, #ffd166);
    display:grid; place-items:center; font-size:22px; color:#14203c; font-weight:900;
    box-shadow: 0 6px 24px rgba(0,0,0,.25);
  }
  .badge{
    display:inline-flex; align-items:center; gap:6px; padding:6px 10px; border-radius:999px;
    background:rgba(0,0,0,.35); border:1px solid rgba(255,255,255,.18); font-size:.92rem
  }
  .badge .dot{width:8px;height:8px;background:#22c55e;border-radius:50%}

  /* ====== Hero ====== */
  .hero{
    margin:28px 0 18px; padding:30px; border-radius:20px; background:var(--card);
    border:1px solid var(--card-b); backdrop-filter: blur(10px);
    display:grid; grid-template-columns: 1.05fr .95fr; gap:20px;
  }
  .hero h1{margin:0 0 10px; font-size:clamp(28px,4.5vw,44px)}
  .hero p{margin:0; opacity:.92; line-height:1.8}
  .stats{display:flex; flex-wrap:wrap; gap:12px; margin-top:14px}
  .chip{padding:8px 12px; border-radius:12px; background:rgba(255,255,255,.08); border:1px solid var(--card-b)}
  .cta{
    display:flex; flex-wrap:wrap; gap:12px; margin-top:18px
  }
  .btn{
    text-decoration:none; display:inline-flex; align-items:center; gap:10px; font-weight:800;
    padding:12px 16px; border-radius:14px; border:1px solid rgba(255,255,255,.15);
    background: linear-gradient(180deg, #ffe59e, var(--acc)); color:#1a1500;
    box-shadow: 0 8px 22px rgba(0,0,0,.22); transition: transform .15s ease, filter .15s ease;
  }
  .btn:hover{ transform: translateY(-1px); filter: brightness(1.03) }
  .btn.alt{ background: linear-gradient(180deg, var(--mint), #07bd98); color:#041a15 }
  .btn.ghost{ background:rgba(255,255,255,.05); color:var(--txt) }

  /* ====== Grid Cards ====== */
  .grid{display:grid; grid-template-columns: repeat(3,1fr); gap:16px; margin:26px 0}
  .card{
    background:var(--card); border:1px solid var(--card-b); border-radius:18px; padding:18px; min-height:182px;
    position:relative; overflow:hidden
  }
  .card h3{margin:0 0 8px}
  .card p{margin:0; opacity:.9; line-height:1.7}
  .ic{
    width:46px;height:46px;border-radius:14px; display:grid; place-items:center; font-size:22px; font-weight:900;
    margin-bottom:10px; color:#0c152e; box-shadow:0 6px 18px rgba(0,0,0,.25)
  }
  .ic.gold{background:linear-gradient(180deg,#fff0bd,#ffd166)}
  .ic.sky{background:linear-gradient(180deg,#bfe0ff,#62b0ff)}
  .ic.rose{background:linear-gradient(180deg,#ff9fb1,#ff5d7a)}
  .go{ position:absolute; bottom:14px; right:14px }
  .go a{ text-decoration:none; font-weight:800; color:#0c152e; background:#ffe59e; padding:8px 12px; border-radius:12px }

  /* ====== Footer ====== */
  footer{opacity:.85; margin:22px 0 10px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px}
  .links{display:flex; gap:10px; flex-wrap:wrap}
  .links a{color:#d8e7ff; text-decoration:none; padding:6px 10px; border-radius:10px; background:rgba(255,255,255,.06); border:1px solid var(--card-b)}
  @media(max-width:1024px){ .hero{grid-template-columns:1fr} .grid{grid-template-columns:1fr 1fr} }
  @media(max-width:680px){ .grid{grid-template-columns:1fr} }
</style>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800;900&display=swap" rel="stylesheet">
</head>
<body>
  <div class="wrap">

    <!-- NAV -->
    <nav class="nav">
      <div class="brand">
        <div class="logo">ع س</div>
        <div>
          <div style="font-size:1.15rem">عربي سايكو</div>
          <small style="opacity:.8">منصّة نفسية عربية تخدم الجميع</small>
        </div>
      </div>
      <div class="badge" title="نحترم السرية والخصوصية">
        <span class="dot"></span>
        السرية والخصوصية
      </div>
    </nav>

    <!-- HERO -->
    <section class="hero">
      <div>
        <h1>رعاية نفسية موثوقة… بلغة قريبة لقلبك</h1>
        <p>
          نقيس الأعراض بمقاييس معتمدة، ونوفّر أدوات العلاج السلوكي المعرفي (CBT)،
          مع تشخيص مبدئي وفق أحدث معايير <b>DSM-5/DSM-5-TR</b>—كل ذلك بسرية تامة.
        </p>
        <div class="stats">
          <span class="chip">معايير مقننة</span>
          <span class="chip">دليل جلسات مختصر</span>
          <span class="chip">أدوات عملية يومية</span>
        </div>
        <div class="cta">
          <a class="btn" href="/dsm">📘 بدء التشخيص (DSM)</a>
          <a class="btn alt" href="/cbt">🧠 أدوات CBT</a>
          <a class="btn ghost" href="/addiction">🚭 برنامج التعافي من الإدمان</a>
        </div>
      </div>
      <div>
        <div class="card" style="height:100%">
          <div class="ic sky">🧪</div>
          <h3>مقاييس قياسية</h3>
          <p>PHQ-9 للاكتئاب، GAD-7 للقلق، PCL-5 لاضطراب ما بعد الصدمة، و DASS-21.</p>
          <div class="go"><a href="/cbt">ابدأ القياس</a></div>
        </div>
      </div>
    </section>

    <!-- GRID -->
    <section class="grid">
      <article class="card">
        <div class="ic gold">📘</div>
        <h3>تشخيص مبدئي (DSM)</h3>
        <p>إدخال ذكي للأعراض والمدة + عوامل وظيفية لإخراج تشخيص مرجَّح (مبدئي).</p>
        <div class="go"><a href="/dsm">الدخول</a></div>
      </article>

      <article class="card">
        <div class="ic sky">🧠</div>
        <h3>العلاج السلوكي المعرفي (CBT)</h3>
        <p>سجلّ الأفكار REBT/CBT، التنشيط السلوكي، سُلّم التعرض، وخطة جلسات أولية.</p>
        <div class="go"><a href="/cbt">لوحة CBT</a></div>
      </article>

      <article class="card">
        <div class="ic rose">🚭</div>
        <h3>التعافي من الإدمان</h3>
        <p>خطة مدروسة للمحفزات والرغبات والانتكاسة، مع واجبات يومية واقعية.</p>
        <div class="go"><a href="/addiction">ابدأ الآن</a></div>
      </article>
    </section>

    <!-- FOOTER -->
    <footer>
      <div>© {{year}} عربي سايكو — دعم نفسي بلغة عربية واضحة</div>
      <div class="links">
        <a href="/dsm">DSM</a>
        <a href="/cbt">CBT</a>
        <a href="/addiction">الإدمان</a>
        <a href="#">سياسة الخصوصية</a>
      </div>
    </footer>

  </div>
</body>
</html>
"""

@app.route("/")
def home():
    from datetime import datetime
    return render_template_string(HOME_HTML, year=datetime.now().year)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
