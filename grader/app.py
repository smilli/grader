from flask import Flask, jsonify, make_response, request
import json
from spellcheck import SpellChecker
from nltk.tokenize import word_tokenize
from assignment import Assignment

app = Flask(__name__)
assignment = Assignment(
    'What is your favorite food?',
    ['My farite food is past.  I like the tast and the txture.',
    'I lik all food, but my favorite is bread.',
    'I lic to eat cheese.',
    'My favrie type of food is pata.']
)
spellchecker = SpellChecker(assignment)


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


@app.route('/assignments/<int:ans_id>', methods=['POST'])
def get_assignments(ans_id):
    if 0 <= ans_id < assignment.num_answers():
        if assignment.is_graded(ans_id):
            return json.dumps({'graded': True, 'assignment':
                assignment.get_graded(ans_id)})
        else:
            answer = assignment.get_answer(ans_id)
            return json.dumps({'graded': False, 'assignment': 
                    [create_word(word) for word in word_tokenize(answer)]})
    return 'false'


@app.route('/grade/<int:ans_id>', methods=['POST'])
def grade_assignment(ans_id):
    if 0 <= ans_id < assignment.num_answers():
        answer = request.json['answer']
        words = []
        corrections = []
        teacher_corrected_list = []
        for w in answer:
            words.append(w['text'])
            is_teach_corrected = w['teacherCorrection'] != False
            teacher_corrected_list.append(is_teach_corrected)
            if not w['correct']:
                if is_teach_corrected:
                    corrections.append(w['teacherCorrection'])
                else:
                    corrections.append(w['correction'])
            else:
                corrections.append(w['text'])
        spellchecker.grade(words, corrections, teacher_corrected_list)
        assignment.add_graded(ans_id, answer)
        return 'true'
    return 'false'


@app.route('/reset/', methods=['POST'])
def reset():
    assignment.graded = {}
    spellchecker.reset()
    return 'true'

@app.route('/assignment-info/', methods=['POST'])
def assignment_info():
    return json.dumps({'numAnswers': str(assignment.num_answers()),
            'prompt': assignment.prompt})


if __name__ == '__main__':
    app.run(debug=True)
