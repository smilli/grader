from flask import Flask, jsonify, make_response, request
import json
from spellcheck import SpellChecker

app = Flask(__name__)
assignments = [
    'This is a stud\'s alsignment',
    'This is another student\'s alsignment',
    'I like to eat chese.',
    'My favrie type of food is pata.'
]
problem = 'What is your favorite type of food?'
spellchecker = SpellChecker(assignments, problem)


def create_word(word_text):
    correction = spellchecker.correct(word_text)
    return {
        'text': word_text,
        'selected': False,
        'teacherCorrection': False,
        'correction': correction if correction != word_text else '',
        'correct': correction == word_text
    }


@app.route('/')
def main():
    return make_response(open('templates/index.html').read())


@app.route('/assignments/<int:id>', methods=['POST'])
def get_assignments(id):
    if 0 <= id < len(assignments):
        return json.dumps([create_word(word) for word in assignments[id].split()])
    return 'false'


@app.route('/grade/<int:id>', methods=['POST'])
def grade_assignment(id):
    if 0 <= id < len(assignments):
        assignment = request.json['assignment']
        words = []
        corrections = []
        teacher_corrected_list = []
        for w in assignment:
            if not w['correct']:
                words.append(w['text'])
                is_teach_corrected = w['teacherCorrection'] != False
                teacher_corrected_list.append(is_teach_corrected)
                if is_teach_corrected:
                    corrections.append(w['teacherCorrection'])
                else:
                    corrections.append(w['correction'])
        spellchecker.grade(words, corrections, teacher_corrected_list)
        return 'true'
    return 'false'


@app.route('/reset/', methods=['POST'])
def reset():
    spellchecker.reset()
    return 'true'


if __name__ == '__main__':
    app.run(debug=True)
