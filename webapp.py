from flask import Flask
from flask import render_template
from flask import request

from lib import weblib
app = Flask(__name__)

@app.route('/')
def home():
    weblib.initialize()
    return render_template('home.html')

@app.route('/correct', methods=['POST'])
def correct():
    data = weblib.add_error_and_correct(request.form['test_data'],
                                        float(request.form['ber']) / 100.0)
    results = {'error_text': data[0],
               'corrected_text': data[1],
               'time': data[2],
               'cpc': data[3],
               'epc': data[4]}
    return render_template('home.html',
                           results=results,
                           ber=request.form['ber'],
                           test_data=request.form['test_data'])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
