from flask import Flask, render_template

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def index():
    return render_template("main/index.html")

# DSM
@app.route("/dsm")
def dsm_page():
    return render_template("dsm/dsm.html")

# CBT
@app.route("/cbt")
def cbt_page():
    return render_template("cbt/cbt.html")

# Case Study
@app.route("/case")
def case_page():
    return render_template("case/case_study.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
