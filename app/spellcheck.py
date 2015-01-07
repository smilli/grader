import nltk
import string
from nltk.util import ngrams
from nltk.corpus import gutenberg
from collections import Counter, defaultdict
import enchant


class SpellChecker():

    def __init__(self, documents):
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
        pass

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

    def correct(self, word, prev_word=None, next_word=None):
        """Returns a corrected version of misspelled word"""
        if self._should_check_word(word):
            candidates = (self._known([word])
                    or self._known(self._calc_edits1(word))
                    or self._known(self._calc_edits2(word)) or [word])
            print(candidates)
            return max(candidates, key=lambda x: self.corpus_freqs.get(x) if
                    self.corpus_freqs.get(x) else 0)
        return word

    def _is_valid_word(self, word):
        return word[0].isalpha() and all(letter in string.ascii_lowercase
                or letter == '-' for letter in word[1:])

    def _should_check_word(self, word):
        """Returns true if word should be checked for spelling"""
        # don't correct anything that has digits or capital letters beyond 1st
        # letter (prob acronyms or some weird words)
        return (self._is_valid_word(word) and not (self.eng_dict.check(word)
                or self.eng_dict.check(word.lower())))
