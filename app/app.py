from flask import Flask, jsonify, make_response
import json
from spellcheck import SpellChecker


app = Flask(__name__)
assignments = [
    'This is a student\'s alsignment',
    'This is another student\'s assignment',
    'I like to eat chese.',
    'My favrie type of food is pata.'
]
problem = 'What is your favorite type of food?'
spellchecker = SpellChecker(assignments, problem)


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


@app.route('/assignments/<int:id>', methods=['GET', 'POST'])
def get_assignments(id):
    if id < len(assignments) and id >= 0:
        assignment = assignments[id]
        words = assignment.split()
        return json.dumps([create_word(word) for word in words])
    return 'false'


@app.route('/grade/<int:id>', methods=['GET', 'POST'])
def grade_assignment(id):
    if id < len(assignments) and id >= 0:
        return None
    return None


if __name__ == '__main__':
    app.run(debug=True)
