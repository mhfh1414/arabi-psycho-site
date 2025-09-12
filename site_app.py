from flask import Flask, render_template_string, url_for, redirect

app = Flask(__name__)

# —————— الصفحة الرئيسية (واجهة أنيقة) ——————
HOME_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>عربي سايكو</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body {
        background: radial-gradient(1000px 600px at 80% -10%, #1f38ff22, transparent),
                    radial-gradient(900px 500px at -10% 100%, #00ffc822, transparent),
                    #0f1420;
        color: #eaf2ff;
        min-height: 100vh;
      }
      .brand {
        font-weight: 800; letter-spacing: 0.5px;
        background: linear-gradient(90deg,#8ad5ff,#7bffcc);
        -webkit-background-clip: text; background-clip: text; color: transparent;
      }
      .card-glass {
        background: #121a2a88;
        border: 1px solid #2a3b5a;
        backdrop-filter: blur(10px);
        border-radius: 18px;
        box-shadow: 0 10px 30px #00000055, inset 0 1px 0 #ffffff11;
      }
      .btn-pill {
        border-radius: 9999px;
        font-weight: 700;
        letter-spacing: .3px;
      }
      .chip {
        display:inline-block; padding:.4rem .75rem; border-radius:9999px;
        background:#1b2740; border:1px solid #2a3b5a; color:#9ec5ff; font-size:.9rem;
        margin:.2rem .2rem 0 0;
      }
      a, a:hover { text-decoration: none; }
    </style>
  </head>
  <body>
    <div class="container py-5">
      <header class="d-flex flex-wrap align-items-center justify-content-between mb-4">
        <h1 class="brand m-0">عربي سايكو</h1>
        <div>
          <a href="{{ url_for('cbt_home') }}" class="btn btn-pill btn-primary me-2">منظومة CBT</a>
          <a href="{{ url_for('dsm_home') }}" class="btn btn-pill btn-success">نظام DSM</a>
        </div>
      </header>

      <section class="row g-4">
        <div class="col-12 col-lg-7">
          <div class="p-4 card-glass">
            <h3 class="mb-2">مركز الأدوات السلوكية المعرفية</h3>
            <p class="text-light mb-4">
              حزمة أدوات إكلينيكية لمتابعة الحالات، دفاتر عمل، وسلالم تقييم
              مدعومة بأفضل الممارسات. واجهة خفيفة وسريعة للعمل اليومي.
            </p>
            <div class="mb-3">
              <span class="chip">جداول متابعة</span>
              <span class="chip">دفتر الأفكار</span>
              <span class="chip">ERP</span>
              <span class="chip">BA</span>
              <span class="chip">REBT</span>
            </div>
            <a class="btn btn-pill btn-primary px-4" href="{{ url_for('cbt_home') }}">الدخول إلى CBT</a>
          </div>
        </div>

        <div class="col-12 col-lg-5">
          <div class="p-4 card-glass h-100">
            <h3 class="mb-2">التشخيص الإكلينيكي (DSM)</h3>
            <p class="text-light">معلومات منظمة عن الاضطرابات، مع أعراض ومعايير مرتبة للرجوع السريع.</p>
            <a class="btn btn-pill btn-success px-4" href="{{ url_for('dsm_home') }}">عرض أقسام DSM</a>
          </div>
        </div>
      </section>

      <footer class="pt-5 text-center text-secondary">
        <small>© {{ year }} عربي سايكو – منصة إكلينيكية باللغة العربية</small>
      </footer>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
"""

@app.route("/")
def index():
    from datetime import datetime
    return render_template_string(HOME_HTML, year=datetime.now().year)

# —————— CBT ——————
@app.route("/cbt")
def cbt_home():
    # ضع هنا استيراد أو ربط وحدات cbt الفعلية إن وجدت
    return "CBT Suite — شغّال ✅. (اربط أدواتك هنا)"

# —————— DSM ——————
@app.route("/dsm")
def dsm_home():
    # ضع هنا عرض قائمة الاضطرابات/الأعراض أو صفحاتك
    return "DSM Suite — شغّال ✅. (أضف صفحات التشخيص هنا)"

# نقطة تشغيل محليّة (غير مستخدمة على Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
