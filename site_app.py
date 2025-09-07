# -*- coding: utf-8 -*-
# site_app.py — الملف الرئيسي لتشغيل موقع عربي سايكو

from flask import Flask, render_template, redirect

app = Flask(__name__)

# ================= صفحات رئيسية =================
@app.route("/")
def home():
    return render_template("home.html")

# ربط DSM
@app.route("/dsm")
def dsm():
    # يحوّل إلى ملف DSM المستقل
    return redirect("/run_dsm", code=302)

# ربط CBT
@app.route("/cbt")
def cbt():
    return redirect("/run_cbt", code=302)

# ربط علاج الإدمان
@app.route("/addiction")
def addiction():
    return redirect("/run_addiction", code=302)

# ================= روابط التواصل =================
@app.route("/contact/whatsapp")
def contact_whatsapp():
    return redirect("https://wa.me/9665XXXXXXXX", code=302)

@app.route("/contact/telegram")
def contact_telegram():
    return redirect("https://t.me/USERNAME", code=302)

@app.route("/contact/email")
def contact_email():
    return redirect("mailto:info@arabipsycho.com", code=302)

# ================= تشغيل =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
