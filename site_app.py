from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# صفحة الـ DSM
@app.route("/dsm")
def dsm():
    return render_template("dsm.html")

# صفحة الاختبارات
@app.route("/tests")
def tests():
    return render_template("tests.html")

# صفحة CBT
@app.route("/cbt")
def cbt():
    return render_template("cbt.html")

# صفحات الأخطاء
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    # للتشغيل المحلي
    app.run(host="0.0.0.0", port=5000, debug=True)
