from flask import Flask

# إنشاء التطبيق
app = Flask(__name__)

# مسار رئيسي للتجربة
@app.route("/")
def home():
    return "<h1>مبروك يا أبو فارس 🚀</h1><p>الموقع شغال على Render</p>"
