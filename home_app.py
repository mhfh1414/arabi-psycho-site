from flask import Flask, render_template_string
import dsm_suite
import cbt_suite
import addiction_suite

app = Flask(__name__)

# ---------------------------
# الواجهة الرئيسية (Home)
# ---------------------------
HOME_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>عربي سايكو | المنصة النفسية</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #00416A, #E4E5E6);
            font-family: 'Tajawal', sans-serif;
            color: #fff;
        }
        .navbar {
            background-color: #00324E;
        }
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5rem;
        }
        .hero {
            text-align: center;
            padding: 60px 20px;
        }
        .hero h1 {
            font-size: 2.8rem;
            margin-bottom: 15px;
        }
        .hero p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .btn-custom {
            margin: 15px;
            padding: 15px 30px;
            font-size: 1.1rem;
            border-radius: 12px;
            transition: 0.3s;
        }
        .btn-custom:hover {
            transform: scale(1.05);
        }
        footer {
            background-color: #00324E;
            text-align: center;
            padding: 15px;
            margin-top: 40px;
            font-size: 0.9rem;
            opacity: 0.8;
        }
    </style>
</head>
<body>

<!-- الشريط العلوي -->
<nav class="navbar navbar-dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">🧠 عربي سايكو</a>
    <span class="navbar-text">السرية والخصوصية أولويتنا</span>
  </div>
</nav>

<!-- البانر -->
<div class="hero">
    <h1>منصة عربي سايكو النفسية</h1>
    <p>تشخيص دقيق | خطط علاجية | تمارين معرفية سلوكية | خصوصية تامة</p>
    <div>
        <a href="/dsm" class="btn btn-warning btn-custom">📋 التشخيص (DSM)</a>
        <a href="/cbt" class="btn btn-success btn-custom">⚡ العلاج السلوكي المعرفي (CBT)</a>
        <a href="/addiction" class="btn btn-danger btn-custom">🚭 علاج الإدمان</a>
    </div>
</div>

<footer>
    <p>© 2025 عربي سايكو | منصة نفسية لخدمة الجميع</p>
</footer>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_PAGE)

# ---------------------------
# ربط DSM
# ---------------------------
@app.route("/dsm")
def dsm_page():
    return dsm_suite.render_page()

# ---------------------------
# ربط CBT
# ---------------------------
@app.route("/cbt")
def cbt_page():
    return cbt_suite.render_page()

# ---------------------------
# ربط الإدمان
# ---------------------------
@app.route("/addiction")
def addiction_page():
    return addiction_suite.render_page()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
