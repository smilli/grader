from flask import Flask, jsonify, make_response
import json
from spellcheck import SpellChecker


app = Flask(__name__)
assignments = [
    'This is a student\'s alsignment',
    'This is another student\'s assignment'
]
spellchecker = SpellChecker(assignments)


def create_word(word_text):
    word = {}
    word['text'] = word_text
    correction = spellchecker.correct(word_text)
    if correction != word_text:
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
    data = []
    for assignment in assignments:
        words = assignment.split()
        data_assignment = []
        for word in words:
            data_assignment.append(create_word(word))
        data.append(data_assignment)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True)
