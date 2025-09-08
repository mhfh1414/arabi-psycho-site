# -*- coding: utf-8 -*-
from flask import Flask
from home import home_bp
from dsm_suite import dsm_bp
from cbt_suite import cbt_bp
from addiction_suite import addiction_bp

def create_app():
    app = Flask(__name__)

    # سجّل البلوبربنتس
    app.register_blueprint(home_bp)       # /
    app.register_blueprint(dsm_bp)        # /dsm , /dsm/
    app.register_blueprint(cbt_bp)        # /cbt
    app.register_blueprint(addiction_bp)  # /addiction

    # اطبع خريطة المسارات في اللوجز لتشخيص أي مشاكل
    print("== URL MAP ==")
    print(app.url_map)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
