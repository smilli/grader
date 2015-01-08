import nltk
import string
from nltk.util import ngrams
from nltk.corpus import gutenberg
from collections import Counter, defaultdict
import enchant
from perceptron import MulticlassPerceptron

class SpellChecker():

    def __init__(self, documents=None, problem=None):
        """
        Constructor for SpellChecker.

        Params:
        documents (String[]) - a list of documents that will later be spell
            checked
        """
        self.eng_dict = enchant.Dict("en_GB")
        self.corpus_freqs = nltk.FreqDist([word.lower() for word in gutenberg.words()])
        self.imp_words = self.get_imp_words(documents)
        self.teacher_corrections = defaultdict(int)
        # TODO(smilli): tokenize using nltk
        if problem:
            self.problem = problem.split()
        else:
            self.problem = []
        self.features = ['CorpFreq', 'ImpWord', 'IsEdit1', 'IsEdit2',
                'IsTeacherCorrection', 'InProblem']
        self.clf = MulticlassPerceptron(self.features)

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
        #TODO(smilli)
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
                (w in self.corpus_freqs or self.eng_dict.check(w)))

    def correct(self, word):
        """Returns a corrected version of misspelled word"""
        if self._should_check_word(word):
            features_list, corrections = self._get_pos_correction_feats(word)
            return self.clf.predict([features_list], [corrections])[0]
            #return max(candidates, key=lambda x: self.corpus_freqs.get(x) if
            #        self.corpus_freqs.get(x) else 0)
        return word

    def _get_pos_correction_feats(self, word):
        edit1_cands = self._known(self._calc_edits1(word))
        edit2_cands = self._known(self._calc_edits2(word))
        features_list = []
        corrections = []
        for edit1 in edit1_cands:
            features_list.append({'IsEdit1': 1, 'IsEdit2': 0})
            corrections.append(edit1)
        for edit2 in edit2_cands:
            features_list.append({'IsEdit1': 0, 'IsEdit2': 1})
            corrections.append(edit2)
        self._add_feats(word, features_list, corrections)
        return [features_list, corrections]

    def _add_feats(self, word, features_list, corrections):
        """
        Adds the non-edit features to the list of possible corrections

        Params:
        word (string) - Word to be corrected.
        features_list (dict{}[]) - List of possible corrections.
            Each possible correction is a dict that already has IsEdit1 and
            IsEdit2 set.
        corrections (string[]) - List of corrections corresponding to each
            feature.
        """
        for (features, correction) in zip(features_list, corrections):
            features['CorpFreq'] = self.corpus_freqs[correction]
            features['ImpWord'] = 1 if correction in self.imp_words else 0
            features['IsTeacherCorrection'] = (1 if (word, correction) in
                self.teacher_corrections else 0)
            features['InProblem'] = 1 if correction in self.problem else 0

    def _is_valid_word(self, word):
        return word[0].isalpha() and all(letter in string.ascii_lowercase
                or letter == '-' for letter in word[1:])

    def _should_check_word(self, word):
        """Returns true if word should be checked for spelling"""
        # don't correct anything that has digits or capital letters beyond 1st
        # letter (prob acronyms or some weird words)
        return (self._is_valid_word(word) and not (self.eng_dict.check(word)
                or self.eng_dict.check(word.lower())))

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
                features = {'IsEdit1': 0, 'IsEdit2': 0}
                self._add_feats(word, [features], [correct])
                features_list.append(features)
                pos_target_names.append(correct)
            training_feats.append(features_list)
            pos_target_names_list.append(pos_target_names)
        print(training_feats, pos_target_names_list, corrections)
        self.clf.train(training_feats, pos_target_names_list, corrections)
