from flask import Flask, jsonify, make_response
import json
app = Flask(__name__)


def create_word(word_text, correction=None):
    word = {}
    word['text'] = word_text
    if correction:
        word['correction'] = correction
        word['correct'] = False
    else:
        word['correction'] = ''
        word['correct'] = True
    word['selected'] = False
    return word


@app.route('/')
def main():
    return make_response(open('templates/index.html').read())


@app.route('/assignments', methods=['GET', 'POST'])
def get_assignments():
    assignments = [
        'This is a student\'s assignment',
        'This is another student\'s assignment'
    ]
    data = []
    for assignment in assignments:
        words = assignment.split()
        for word in words:
            data.append(create_word(word))
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True)
