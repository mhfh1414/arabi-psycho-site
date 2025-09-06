# -*- coding: utf-8 -*-
from flask import Flask, request
from home import render_home, WA_LINK, TG_LINK, EMAIL_LINK
from dsm_suite import render_dsm_get, render_dsm_post
from cbt_suite import render_cbt_home, render_test
from addiction_suite import render_addiction_get, render_addiction_post

app = Flask(__name__)

# ===================== الرئيسية والاتصال =====================
@app.route("/")
def home():
    return render_home()

@app.route("/contact/whatsapp")
def contact_whatsapp():
    return f'<meta http-equiv="refresh" content="0; url={WA_LINK}">'

@app.route("/contact/telegram")
def contact_telegram():
    return f'<meta http-equiv="refresh" content="0; url={TG_LINK}">'

@app.route("/contact/email")
def contact_email():
    return f'<meta http-equiv="refresh" content="0; url={EMAIL_LINK}">'

# ===================== DSM (نموذج + نتيجة) =====================
@app.route("/dsm", methods=["GET", "POST"])
def dsm():
    if request.method == "POST":
        return render_dsm_post(request.form)
    return render_dsm_get()

# ===================== CBT والاختبارات =====================
@app.route("/cbt", methods=["GET"])
def cbt():
    return render_cbt_home()

@app.route("/cbt/tests/<slug>", methods=["GET", "POST"])
def cbt_test(slug):
    return render_test(slug, request)

# ===================== الإدمان =====================
@app.route("/addiction", methods=["GET", "POST"])
def addiction():
    if request.method == "POST":
        return render_addiction_post(request.form)
    return render_addiction_get()

# ===================== التشغيل =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
