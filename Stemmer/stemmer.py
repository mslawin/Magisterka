# coding=UTF-8
__author__ = 'mslawin'

import marisa_trie


class Stemmer:
    def __init__(self, plp):
        self.plp = plp

    def write_trie_to_file(self, filename):
        self.atergo_trie.save(filename)

    def load_from_file(self, filename):
        fmt = '<15s15s15'
        self.atergo_trie = marisa_trie.RecordTrie(fmt)
        self.atergo_trie.load(filename)

    def prepare(self, only_nouns):
        old = ""
        index = 0
        keys = []
        values = []
        for i in range(16777231, 18663982):
            if only_nouns:
                if self.plp.label(i)[0] != u'A':
                    continue
            if self.is_bad_value(i):
                continue
            form = self.plp.bform(i)

            if old != form:
                for s in self.plp.forms(i):
                    if len(s) > 0:
                        a = self.substr(s, form)
                        to_remove = s[len(a): len(s)]
                        to_add = form[len(a): len(form)]
                        keys.append(self.reverse(s))
                        a = unicode(to_remove).encode('utf-8')
                        b = unicode(to_add).encode('utf-8')
                        values.append((a, b))
                index += 1

            old = self.plp.bform(i)
        fmt = '<15s15s15'
        self.atergo_trie = marisa_trie.RecordTrie(fmt, zip(keys, values))

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

    def substr(self, s1, s2):
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return s1[0: i]

    def is_bad_value(self, i):
        return (16824383 >= i >= 16824368) or (16786128 <= i <= 16786143) or \
               (16873663 >= i >= 16873632) or (16926016 <= i <= 16926031) or \
               (17035263 >= i >= 17035232) or (17060080 <= i <= 17060095) or \
               (17087487 >= i >= 17087456) or (17998800 <= i <= 17998815) or \
               (18128432 >= i >= 18128416) or (18260592 <= i <= 18260607) or \
               (18347183 >= i >= 18347168)

    def reverse(self, s):
        result = ''
        i = len(s) - 1
        while i >= 0:
            result += s[i]
            i -= 1
        return result

    def find_similar_words(self, strange_form):
        reversed_strange_form = self.reverse(strange_form)
        index = 0
        while index < len(strange_form) and self.atergo_trie.has_keys_with_prefix(reversed_strange_form[:index]):
            index += 1
        return self.atergo_trie.keys(reversed_strange_form[:index - 1])

        # f = codecs.open('test.txt', 'r', 'utf-8')