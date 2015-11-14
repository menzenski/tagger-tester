#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.tag.stanford import StanfordPOSTagger

from .config import DATA_DIR_NAME, PATH_TO_DATA_DIR
from .files import TrainingFile, write_to_directory
from .files import to_unicode_or_bust as tuob
from .tag import FilePair

class TaggerTester(object):
    """Collection of files for training/testing part-of-speech taggers. """

    def __init__(self):
        """Initialize the test suite."""
        pass

class SentencePair(object):
    """Pair of sentences: one tagged by hand, one by a POS tagger."""

    def __init__(self, idx=1, hand_tagged_sentence, separator='_'):
        """Initialize the object.

           Parameters
           ----------
             hand_tagged_sentence (list) OR (unicode / str) : a sentence
               which has been tagged by hand (i.e., it belongs to part of
               the original training file which was set aside to serve as a
               test set)
             separator (str) : the character which serves to separate
               words from their part-of-speech tags (likely '_' or '/')
        """
        self.idx = idx # index in the original (complete) training file
        if isinstance(hand_tagged_sentence, basestring):
            self.hand_tagged = tuob(hand_tagged_sentence).split()
        if isinstance(hand_tagged_sentence, list):
            self.hand_tagged = [tuob(w) for w in hand_tagged_sentence]
        self.sep = tuob(separator)
        # to be populated when the sentence is tagged by the tagger
        self.auto_tagged = []

    def strip_training_tags(self, sentence=None, sep=None):
        """Remove the part-of-speech tags from a test sentence."""
        if sentence == None:
            sentence = self.hand_tagged
        if sep == None:
            sep = self.sep
        return [w.split(sep, 1)[0] for w in sentence]

    def compare_sentences(self, auto_tagged, hand_tagged=None):
        """Compare the hand-tagged original to the auto-tagged sentence.

           Parameters
           ----------
             auto_tagged (list) : list of 2-tuples comprised of word + tag
               for the words in the original hand_tagged sentence
        """
        if hand_tagged == None:
            hand_tagged = self.hand_tagged
        if len(auto_tagged) == len(hand_tagged):
            print u'HAND TAGGED:'
            for idx, w in enumerate(hand_tagged):
                print u'\t{}\t{}'.format(idx, w)
            print u'AUTO TAGGED:'
            for idx, w in enumerate(auto_tagged):
                print u'\t{}\t{}_{}'.format(idx, w[0], w[1])

    def comparison(self, idx=1, hand_tagged=None, auto_tagged=None):
        """Return a tuple containing index and tagging result accuracy.

           Returns
           -------
             (tuple) : 2-tuple structured like the following:
                 (134, [1, 1, 1, 0, 1, 1])
              in which the first item is the index of this sentence in the
              original (complete) hand-tagged training file and the second
              item is a list of length len(hand_tagged). In each position in
              the list a 1 indicates that the tagger output matches the
              hand-tagged input perfectly, and a 0 indicates that it doesn't.
        """
        if hand_tagged == None:
            hand_tagged = self.hand_tagged
        if auto_tagged == None:
            auto_tagged = self.auto_tagged
        if len(hand_tagged) == len(auto_tagged):
            rl = [1 if hand_tagged[i] == auto_tagged[i] else 0
                    for i in xrange(0, len(hand_tagged))]
            return (idx, rl)
        else:
            return (idx, "Sentence lengths don't match!")
