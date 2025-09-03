from flask import Flask, render_template, request, jsonify

# ✅ استيراد من الملفات داخل المشروع
from tests.tests_psych import score_test, psych_info
from tests.tests_personality import personality_test  # تأكد أن الدالة موجودة
from data.dsm5.dsm import get_disorder                # تأكد أن الدالة موجودة
from services.recommend import get_recommendations    # تأكد أن الدالة موجودة

app = Flask(__name__)

# ======================
# صفحات أساسية
# ======================
@app.route('/')
def home():
    return render_template('main/index.html')

@app.route('/dsm')
def dsm_list():
    disorders = get_disorder()
    return render_template('dsm/dsm.html', disorders=disorders)

@app.route('/dsm/<string:disorder_id>')
def dsm_detail(disorder_id):
    disorder = get_disorder(disorder_id)
    return render_template('dsm/dsm_detail.html', disorder=disorder)

# ======================
# اختبارات
# ======================
@app.route('/tests/psych', methods=['POST'])
def run_psych_test():
    user_answers = request.json.get("answers", [])
    result = score_test(user_answers)
    return jsonify(result)

@app.route('/tests/personality', methods=['POST'])
def run_personality_test():
    user_answers = request.json.get("answers", [])
    result = personality_test(user_answers)
    return jsonify(result)

# ======================
# توصيات
# ======================
@app.route('/recommend', methods=['GET'])
def recommend():
    recs = get_recommendations()
    return jsonify(recs)

# ======================
# تشغيل
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
