# coding=UTF-8
from utils import Util

__author__ = 'mslawin'

import marisa_trie
import collections
import operator


class Stemmer:
    fmt = '<15s15s15'

    def __init__(self, plp, filename, word_type):
        self.plp = plp
        if filename:
            self.atergo_trie = marisa_trie.RecordTrie(self.fmt)
            self.atergo_trie.load(filename)

        elif word_type:
            self.atergo_trie = marisa_trie.RecordTrie(self.fmt, self.prepare(word_type))

    def write_trie_to_file(self, filename):
        """
        Saves backup of trie structure to a file
        :param filename: filename where trie will be stored
        :return: None
        """
        self.atergo_trie.save(filename)

    def prepare(self, word_type):
        """
        Generates trie structure containing all words from clp
        :param word_type: part of speech of which kind read words from clp data
        :return: None
        """
        old = ""
        index = 0
        keys = []
        values = []
        for i in range(16777231, 18663982):
            if Util.is_word_unneeded(i):
                continue
            if Util.is_word_appropriate_type(self.plp.label(i)[0], word_type):
                continue
            form = self.plp.bform(i)

            if old != form:
                for s in self.plp.forms(i):
                    if len(s) > 0:
                        a = Util.substring(s, form)
                        to_remove = s[len(a): len(s)]
                        to_add = form[len(a): len(form)]
                        keys.append(Util.reverse(s))
                        a = unicode(to_remove).encode('utf-8')
                        b = unicode(to_add).encode('utf-8')
                        values.append((a, b))
                index += 1

            old = self.plp.bform(i)
        return zip(keys, values)

    def find_basic_form(self, strange_form):
        """
        Method finds basic form for given inflectional form
        :param strange_form: inflectional form of word
        :return: basic form of given word
        """
        similar_words = self.find_similar_words(strange_form)
        how_many_forms = dict()
        word_labels = dict()
        for word in similar_words:
            form = self.atergo_trie[word]
            if form[0] in how_many_forms:
                how_many_forms[form[0]] += 1
            else:
                how_many_forms[form[0]] = 1
            if not form[0] in word_labels:
                word_labels[form[0]] = []
            word_labels[form[0]].append(Util.reverse(word))
        max_form = max(how_many_forms.iteritems(), key=operator.itemgetter(1))[0]

        max_form0 = max_form[0].split('\x00')[0].decode('utf-8')
        max_form1 = max_form[1].split('\x00')[0].decode('utf-8')
        result = collections.namedtuple('result', ['basic_form', 'word_labels'])
        result.basic_form = strange_form[:len(strange_form) - len(max_form0)] + max_form1
        result.word_labels = word_labels[max_form]
        return result

    def find_similar_words(self, strange_form):
        """
        Method finds words in trie structure which has longest coomon part with given word
        :param strange_form: inflectional form of given word
        :return: list of words which has longest common part of given word
        """
        reversed_strange_form = Util.reverse(strange_form)
        index = 0
        while index < len(strange_form) and \
                self.atergo_trie.has_keys_with_prefix(unicode(reversed_strange_form[:index])):
            index += 1
        return self.atergo_trie.keys(unicode(reversed_strange_form[:index - 1]))

    def find_labels(self, word_labels):
        labels = []
        idss = dict()
        for word_label in word_labels:
            max_label = dict()
            for word in word_label:
                ids = self.plp.rec(unicode(word))
                for id in ids:
                    l = self.plp.label(id)
                    if l in max_label:
                        max_label[l] += 1
                    else:
                        max_label[l] = 1
                    idss[l] = id
            labels.append(max(max_label.iteritems(), key=operator.itemgetter(1))[0])
        r = collections.namedtuple('r', ['x', 'y'])
        r.x = labels
        return labels