# app.py — Flask web (Render-ready) — Purple/Gold + Shake
import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>عربي سايكو — واجهة بنفسجي وذهبي</title>
  <style>
    :root{
      --purple:#4B0082;   /* البنفسجي */
      --gold:#FFD700;     /* الذهبي */
      --white:#ffffff;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      min-height:100%;
      display:flex;
      align-items:center;
      justify-content:center;
      background:var(--purple);
      font-family:"Tajawal","Segoe UI",system-ui,sans-serif;
      color:var(--white);
      overflow:hidden;
    }
    /* شريط علوي بسيط */
    .topbar{
      position:fixed; inset:16px 16px auto 16px;
      display:flex; gap:12px; align-items:center; justify-content:space-between;
    }
    .brand{
      padding:10px 16px; border-radius:14px;
      background:linear-gradient(135deg,var(--gold), #fff0bf);
      color:var(--purple); font-weight:700;
      box-shadow:0 6px 20px rgba(0,0,0,.25);
      animation:shake 1.1s infinite;
    }
    /* بطاقة وسط الصفحة */
    .card{
      background:linear-gradient(180deg,#fff8d1,var(--gold));
      color:var(--purple);
      padding:42px 56px;
      border-radius:22px;
      box-shadow:0 20px 60px rgba(0,0,0,.35);
      text-align:center;
      animation:shake 1s infinite;
    }
    .card h1{margin:0 0 10px; font-size:2rem}
    .btn{
      display:inline-block; margin-top:14px; padding:12px 18px;
      border-radius:14px; background:var(--purple); color:var(--white);
      text-decoration:none; font-weight:700;
      box-shadow:0 8px 25px rgba(0,0,0,.3);
      transition:transform .15s ease, filter .15s ease;
      animation:shake 1.25s infinite;
    }
    .btn:hover{ transform:translateY(-2px); filter:brightness(1.08); }

    /* حركة يهز هز */
    @keyframes shake {
      0%{transform:translate(1px, 1px) rotate(0deg);}
      10%{transform:translate(-1px, -2px) rotate(-1deg);}
      20%{transform:translate(-3px, 0px) rotate(1deg);}
      30%{transform:translate(3px, 2px) rotate(0deg);}
      40%{transform:translate(1px, -1px) rotate(1deg);}
      50%{transform:translate(-1px, 2px) rotate(-1deg);}
      60%{transform:translate(-3px, 1px) rotate(0deg);}
      70%{transform:translate(3px, 1px) rotate(-1deg);}
      80%{transform:translate(-1px, -1px) rotate(1deg);}
      90%{transform:translate(1px, 2px) rotate(0deg);}
      100%{transform:translate(1px, -2px) rotate(-1deg);}
    }
    /* زخرفة ذهبية خلفية */
    .glow{
      position:fixed; width:70vmax; height:70vmax; border-radius:50%;
      background:radial-gradient(circle at 30% 30%, rgba(255,215,0,.35), transparent 60%);
      right:-20vmax; bottom:-20vmax; pointer-events:none; filter:blur(8px);
    }
  </style>
</head>
<body>
  <div class="topbar">
    <div class="brand">عربي سايكو</div>
  </div>

  <main class="card">
    <h1>مرحباً يا بطل ✨</h1>
    <p>واجهة بنفسجي × ذهبي مع حركة يهز هز — جاهزة لموقعك.</p>
    <a class="btn" href="/">ابدأ الآن</a>
  </main>

  <div class="glow"></div>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(HTML)

# لمراقبة الصحة على Render
@app.get("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
