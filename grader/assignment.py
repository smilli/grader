class Assignment():

    def __init__(self, prompt, answers=None):
        self.prompt = prompt
        if not answers:
            self.answers = []
        else:
            self.answers = answers
        self.graded = {}

    def add_graded(self, answer_id, graded):
        self.graded[answer_id] = graded

    def is_graded(self, answer_id):
        return answer_id in self.graded

    def get_answer(self, answer_id):
        return self.answers[answer_id]

    def get_graded(self, answer_id):
        return self.graded[answer_id]

    def num_answers(self):
        return len(self.answers)
