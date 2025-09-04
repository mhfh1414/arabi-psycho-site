site_app.py
```python
from flask import Flask, render_template, request
from .tests.tests_psych import score_test, psych_info
from .tests.tests_personality import personality_test
from .services.recommend import get_recommendation

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main/index.html')

@app.route('/tests/psych', methods=['GET', 'POST'])
def psych_test():
    if request.method == 'POST':
        answers = request.form.getlist('answers')
        result = score_test(answers)
        return render_template('tests/result.html', result=result)
    return render_template('tests/psych.html')

@app.route('/tests/personality', methods=['GET', 'POST'])
def personality():
    if request.method == 'POST':
        answers = request.form.getlist('answers')
        result = personality_test(answers)
        return render_template('tests/result.html', result=result)
    return render_template('tests/personality.html')

@app.route('/recommend')
def recommend():
    rec = get_recommendation()
    return render_template('recommend.html', rec=rec)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
