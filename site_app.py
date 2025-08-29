from flask import Flask, render_template
app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dsm")
def dsm():
    return render_template("dsm.html")

@app.route("/cbt", methods=["GET", "POST"])
def cbt():
    # لا نحفظ بيانات على السيرفر – كل الحفظ محلي بالمتصفح (localStorage)
    return render_template("cbt.html")

@app.route("/tests")
def tests():
    return render_template("tests.html")

# لِتشغيل محلياً
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
