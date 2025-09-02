from flask import Flask, render_template

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")

# صفحة DSM
@app.route("/dsm")
def dsm_list():
    return render_template("dsm_list.html")

# صفحة CBT
@app.route("/cbt")
def cbt_list():
    return render_template("cbt_list.html")

# صفحة الاختبارات
@app.route("/tests")
def tests_list():
    return render_template("tests_list.html")

# صفحة الإدمان
@app.route("/addiction")
def addiction_list():
    return render_template("addiction_list.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
