import nltk
import string
from nltk.util import ngrams
from nltk.corpus import gutenberg
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from collections import Counter, defaultdict
from perceptron import MulticlassPerceptron

class SpellChecker():

    def __init__(self, assignment=None):
        """
        Constructor for SpellChecker.

        Params:
        assignment (Assignment) - Assignment obj for this assignment
        """
        self.eng_dict = set(words.words())
        self.corpus_freqs = nltk.FreqDist([word.lower() for word in gutenberg.words()])
        self.corpus_size = len(gutenberg.words())
        self.imp_words = self.get_imp_words(assignment.answers)
        self.teacher_corrections = defaultdict(int)
        if assignment:
            self.problem = word_tokenize(assignment.prompt)
        else:
            self.problem = []
        self.features = ['InDict', 'CorpFreq', 'KnownWord',
                'ImpWord', 'IsEdit1', 'IsEdit2',
                'IsTeacherCorrection', 'InProblem']
        self.weights = [20, 2, 200, 5, 5, 2, 40, 10]
        self.clf = MulticlassPerceptron(self.features, self.weights)

    def add_correction(self, word, corrected):
        """
        Modify the spell checker to take into account a teacher corrected word.
        """
        self.teacher_corrections[(word, corrected)] += 1

    def get_imp_words(self, documents):
        """
        Extracts important words out of the given documents.  The important
        words are words that occur in high frequency in the documents, but in
        low frequency in the corpus.

        Params:
        documents (String[]) - a list of documents that will later be spell
            checked
        """
        # TODO(smilli): make this useful
        #d_words = []
        #for d in documents:
        #    d_words += word_tokenize(d)
        #d_words_freq = nltk.FreqDist(d_words)
        #imp_words = set()
        #for w in set([w for w in d_words if w in self.eng_dict]):
        #    if (d_words_freq[w] / len(d_words)) / ((self.corpus_freqs[w] + 1) /
        #            self.corpus_size) > 5:
        #        imp_words.add(w)
        return []

    def _calc_edits1(self, word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in
                string.ascii_lowercase if b]
        inserts    = [a + c + b     for a, b in splits for c in
                string.ascii_lowercase]
        return set(deletes + transposes + replaces + inserts)

    def _calc_edits2(self, word):
        return set(e2 for e1 in self._calc_edits1(word)
                for e2 in self._calc_edits1(e1))

    def _known(self, words):
        return set(w for w in words if w and
                (w in self.corpus_freqs or w in self.eng_dict))

    def correct(self, word):
        """Returns a corrected version of misspelled word"""
        if self._should_check_word(word):
            features_list, corrections = self._get_pos_correction_feats(word)
            return self.clf.predict([features_list], [corrections])[0]
            #return max(candidates, key=lambda x: self.corpus_freqs.get(x) if
            #        self.corpus_freqs.get(x) else -1)
        return word

    def _get_teacher_corrections(self, word):
        return [(c, self.teacher_corrections[(w, c)]) for (w, c) in
            self.teacher_corrections.keys() if w == word]

    def _get_pos_correction_feats(self, word):
        edit1_cands = self._known(self._calc_edits1(word))
        edit2_cands = self._known(self._calc_edits2(word))
        features_list = []
        corrections = []
        features_list.append({})
        corrections.append(word)
        for edit1 in edit1_cands:
            features_list.append({'IsEdit1': 1})
            corrections.append(edit1)
            for (correction, num) in self._get_teacher_corrections(edit1):
                features_list.append({'IsTeacherCorrection': num, 'IsEdit1': 1})
                corrections.append(correction)
        for edit2 in edit2_cands:
            features_list.append({'IsEdit2': 1})
            corrections.append(edit2)
            for (correction, num) in self._get_teacher_corrections(edit2):
                features_list.append({'IsTeacherCorrection': num, 'IsEdit2': 1})
                corrections.append(correction)
        for (correction, num) in self._get_teacher_corrections(word):
            features_list.append({'IsTeacherCorrection': num})
            corrections.append(correction)
        self._add_feats(word, features_list, corrections)
        for (c, f) in zip(corrections, features_list):
            print(c, f)
        return [features_list, corrections]

    def _add_feats(self, word, features_list, corrections):
        """
        Adds remaining features to the list of possible corrections

        Params:
        word (string) - Word to be corrected.
        features_list (dict{}[]) - List of possible corrections.
            Each possible correction is a dict that may already have IsEdit1,
            IsEdit2, and IsTeacherCorrection set.
        corrections (string[]) - List of corrections corresponding to each
            feature.
        """
        for (features, correction) in zip(features_list, corrections):
            if 'IsEdit1' not in features:
                features['IsEdit1'] = -1
            if 'IsEdit2' not in features:
                features['IsEdit2'] = -1
            features['CorpFreq'] = (
                1 if self.corpus_freqs[correction] > 100 else -1)
            features['ImpWord'] = 1 if correction in self.imp_words else -1
            if 'IsTeacherCorrection' not in features:
                features['IsTeacherCorrection'] = (
                        self.teacher_corrections[(word, correction)] if
                        (word, correction) in self.teacher_corrections else -1)
            features['InProblem'] = 1 if correction in self.problem else -1
            features['InDict'] = 1 if correction.lower() in self.eng_dict else -1
            features['KnownWord'] = 1 if (word == correction and
                features['InDict'] > 0 and (self.corpus_freqs[correction] > 20 or
                    features['ImpWord'] > 0)) else -1

    def _is_valid_word(self, word):
        return word[0].isalpha() and all(letter in string.ascii_lowercase
                or letter == '-' for letter in word[1:])

    def _should_check_word(self, word):
        return self._is_valid_word(word) and not (self.corpus_freqs[word] > 1000 or
            self.corpus_freqs[word.lower()] > 1000)

    def grade(self, words, corrections, teacher_corrected_list):
        training_feats = []
        pos_target_names_list = []
        for word, correct, teacher_corrected in zip(words, corrections,
                teacher_corrected_list):
            if teacher_corrected:
                self.add_correction(word, correct)
            # TODO(smilli): should check to see if word was corrected in first place
            features_list, pos_target_names = self._get_pos_correction_feats(word)
            try:
                correctInd = pos_target_names.index(correct)
                features_list[correctInd]['IsTeacherCorrection'] = teacher_corrected
            except ValueError:
                self._add_feats(word, [features], [correct])
                features_list.append(features)
                pos_target_names.append(correct)
            training_feats.append(features_list)
            pos_target_names_list.append(pos_target_names)
        self.clf.train(training_feats, pos_target_names_list, corrections)

    def reset(self):
        self.clf.reset()
