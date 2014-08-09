# coding=UTF-8
from utils import Util

__author__ = 'mslawin'

import marisa_trie


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
        self.atergo_trie.save(filename)

    def prepare(self, word_type):
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
        similar_words = self.find_similar_words(strange_form)
        how_many_forms = dict()
        for word in similar_words:
            form = self.atergo_trie[word]
            if form[0] in how_many_forms:
                how_many_forms[form[0]] += 1
            else:
                how_many_forms[form[0]] = 1
        max_forms = 0
        max_form = ('', '')
        for key in how_many_forms.keys():
            if how_many_forms[key] > max_forms:
                max_forms = how_many_forms[key]
                max_form = key

        max_form0 = max_form[0].split('\x00')[0].decode('utf-8')
        max_form1 = max_form[1].split('\x00')[0].decode('utf-8')
        return strange_form[:len(strange_form) - len(max_form0)] + max_form1

    def find_similar_words(self, strange_form):
        reversed_strange_form = Util.reverse(strange_form)
        index = 0
        while index < len(strange_form) and self.atergo_trie.has_keys_with_prefix(unicode(reversed_strange_form[:index])):
            index += 1
        return self.atergo_trie.keys(unicode(reversed_strange_form[:index - 1]))