# app.py — Flask web (Purple/Gold, DSM + CBT + Addiction + Case Study)
import os, importlib
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_HOME = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>عربي سايكو — DSM / CBT / Addiction / Case Study</title>
  <style>
    :root{ --purple:#4B0082; --gold:#FFD700; --white:#ffffff; }
    body{ margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
          background:var(--purple); font-family:"Tajawal","Segoe UI",system-ui,sans-serif; color:var(--white);}
    .card{ background:var(--gold); color:var(--purple); padding:40px 60px; border-radius:20px;
           box-shadow:0 8px 25px rgba(0,0,0,.3); text-align:center; }
    .card h1{margin:0 0 20px; font-size:2rem}
    .btn{ display:block; margin:10px auto; padding:12px 18px; border-radius:14px;
          background:var(--purple); color:var(--white); text-decoration:none; font-weight:700; width:220px; }
    .btn:hover{opacity:.9}
    .wrap{max-width:980px; margin:40px auto; padding:20px}
    .back{position:fixed; top:16px; right:16px}
    .back a{background:var(--gold); color:var(--purple); padding:8px 12px; border-radius:10px; text-decoration:none; font-weight:700}
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

def render_module(module_name: str, title_ar: str):
    """
    يحاول استدعاء module.main()، ولو رجّع HTML نعرضه كما هو.
    لو ما فيه main() أو صار خطأ، نعرض رسالة مفيدة.
    """
    try:
        m = importlib.import_module(module_name)
        if hasattr(m, "main"):
            content = m.main()
            # نعرض المحتوى كـ HTML فعلي
            page = f"""
            <html lang="ar" dir="rtl"><head>
            <meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
            <title>{title_ar}</title>
            <style>
              body{{font-family:"Tajawal","Segoe UI",system-ui,sans-serif; margin:0; background:#faf7e6}}
              .back{{position:fixed; top:16px; right:16px}}
              .back a{{background:#FFD700; color:#4B0082; padding:8px 12px; border-radius:10px; text-decoration:none; font-weight:700}}
              .wrap{{max-width:980px; margin:40px auto; padding:20px}}
            </style></head>
            <body>
              <div class="back"><a href="/">⬅ الرجوع</a></div>
              <div class="wrap">
                {content}
              </div>
            </body></html>
            """
            return render_template_string(page)
        else:
            msg = f"الملف <b>{module_name}.py</b> لا يحتوي دالة <code>main()</code> لعرض المحتوى."
            return render_template_string(f"<div class='wrap'>{msg}</div>")
    except Exception as e:
        return render_template_string(f"<div class='wrap'>خطأ أثناء تحميل <b>{module_name}</b>: {e}</div>")

@app.get("/")
def home():
    return render_template_string(HTML_HOME)

@app.get("/dsm")
def dsm():
    return render_module("DSM", "DSM")

@app.get("/cbt")
def cbt():
    return render_module("CBT", "CBT")

@app.get("/addiction")
def addiction():
    return render_module("Addiction", "Addiction")

@app.get("/ipb")
def ipb():
    return render_module("ipb", "Case Study")

@app.get("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
