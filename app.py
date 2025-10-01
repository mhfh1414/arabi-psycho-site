# app.py — Flask web (Purple/Gold, DSM + CBT + Addiction + Case Study)
import os
from flask import Flask, render_template_string
import importlib

app = Flask(__name__)

# واجهة HTML
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>عربي سايكو — DSM / CBT / Addiction / Case Study</title>
  <style>
    :root{
      --purple:#4B0082;   /* البنفسجي */
      --gold:#FFD700;     /* الذهبي */
      --white:#ffffff;
    }
    body{
      margin:0;
      min-height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      background:var(--purple);
      font-family:"Tajawal","Segoe UI",system-ui,sans-serif;
      color:var(--white);
    }
    .card{
      background:var(--gold);
      color:var(--purple);
      padding:40px 60px;
      border-radius:20px;
      box-shadow:0 8px 25px rgba(0,0,0,0.3);
      text-align:center;
    }
    .card h1{margin:0 0 20px; font-size:2rem}
    .btn{
      display:block; margin:10px auto; padding:12px 18px;
      border-radius:14px; background:var(--purple); color:var(--white);
      text-decoration:none; font-weight:700; width:200px;
    }
    .btn:hover{opacity:0.85}
    pre{
      text-align:right;
      background:#f4f4f4;
      color:#000;
      padding:15px;
      border-radius:10px;
      overflow-x:auto;
      max-width:90%;
      margin:20px auto;
      direction:ltr;
    }
  </style>
</head>
<body>
  <main class="card">
    <h1>مرحباً بك في عربي سايكو</h1>
    <a class="btn" href="/dsm">📘 DSM</a>
    <a class="btn" href="/cbt">🧠 CBT</a>
    <a class="btn" href="/addiction">💊 Addiction</a>
    <a class="btn" href="/ipb">📑 Case Study</a>
  </main>
</body>
</html>
"""

def load_module_output(module_name):
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, "main"):
            return module.main()
        return f"تم استيراد {module_name} بنجاح."
    except Exception as e:
        return f"خطأ في تحميل {module_name}: {e}"

@app.get("/")
def home():
    return render_template_string(HTML)

@app.get("/dsm")
def dsm():
    return f"<h2>DSM.py</h2><pre>{load_module_output('DSM')}</pre>"

@app.get("/cbt")
def cbt():
    return f"<h2>CBT.py</h2><pre>{load_module_output('CBT')}</pre>"

@app.get("/addiction")
def addiction():
    return f"<h2>Addiction.py</h2><pre>{load_module_output('Addiction')}</pre>"

@app.get("/ipb")
def ipb():
    return f"<h2>ipb.py</h2><pre>{load_module_output('ipb')}</pre>"

@app.get("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
