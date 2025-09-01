from flask import Flask, render_template, request, redirect, url_for
from modules import PSYCH_TESTS, score_psych, PERS_TESTS, score_personality, recommend_tests_from_case

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dsm')
def dsm():
    return render_template('dsm.html')

@app.route('/dsm/<string:diagnosis>')
def dsm_detail(diagnosis):
    return render_template('dsm_detail.html', diagnosis=diagnosis)

@app.route('/tests')
def tests():
    return render_template('tests.html', 
                           psych_tests=PSYCH_TESTS, 
                           pers_tests=PERS_TESTS)

@app.route('/tests/run/<string:test_type>/<string:test_name>', methods=['GET', 'POST'])
def test_run(test_type, test_name):
    if request.method == 'POST':
        answers = request.form.to_dict()
        if test_type == 'psych':
            score = score_psych(test_name, answers)
        else:
            score = score_personality(test_name, answers)
        return render_template('test_result.html', score=score, test_name=test_name)

    return render_template('test_run.html', test_type=test_type, test_name=test_name)

@app.route('/case-study', methods=['GET', 'POST'])
def case_study():
    if request.method == 'POST':
        case_data = request.form.to_dict()
        recommendations = recommend_tests_from_case(case_data)
        return render_template('case_study.html', recommendations=recommendations)
    return render_template('case_study.html')

# تشغيل التطبيق
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
