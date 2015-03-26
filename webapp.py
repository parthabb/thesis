from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

import lib
from lib import weblib
app = Flask(__name__)

@app.route('/')
def home():
#     weblib.initialize()
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


@app.route('/word/<word>')
def word_count(word):
    wl = weblib.WebLib()
    orig_word = word
    if not word.isdigit():
        word = wl.ht.encode(word)
    pwords, time_taken = wl.get_probable_words(word)
    result = {
        'word': orig_word,
        'hc': word,
        'pb': wl.get_word_probability(word),
        'probable_words': pwords,
        'time': time_taken
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
