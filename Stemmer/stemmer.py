#coding=UTF-8
__author__ = 'maciej'

from plp import *
import marisa_trie
import string

class Stemmer:
    def __init__(self, plp):
        self.plp = plp

    def prepare(self):
        old = ""
        index = 0
        keys = []
        values = []
        print 'Form ToAdd ToRemove Changed'
        for i in range(16777231,18663982):
            if index == 10:
                break
            if self.isBadValue(i):
                continue
            form = self.plp.bform(i)

            if old != form:
                toRemove = ""
                toAdd = ""
                for s in plp.forms(i):
                    if len(s) > 0:
                        if i == 16777312:
                            print 'found abdominalnej'
                        a = self.substr(s, form)
                        toRemove = s[len(a) : len(s)]
                        toAdd = form[len(a) : len(form)]
                        keys.append(self.reverse(s))
                        print s + " " + toRemove + " " + toAdd
                        a = unicode(toRemove).encode('utf-8')
                        b = unicode(toAdd).encode('utf-8')
                        values.append((a, b))
                index += 1                        #najbardziej pasujace slowo, a jak wiecej niz jedno to po count z formEntry

            old = plp.bform(i)
        fmt = '<15s15s15'
        self.atergoTrie = marisa_trie.RecordTrie(fmt, zip(keys, values))

    def findBasicForm(self, strangeForm):
        similarWords = self.findSimilarWords(strangeForm)
        howManyForms = dict()
        for word in similarWords:
            form = self.atergoTrie[word]
            if howManyForms.has_key(form[0]):
                howManyForms[form[0]] += 1
            else:
                howManyForms[form[0]] = 1
        max = 0
        maxForm = ('', '')
        for key in howManyForms.keys():
            if howManyForms[key] > max:
                max = howManyForms[key]
                maxForm = key

        print maxForm[0] + ' ' + maxForm[1]
        unicode(maxForm[1]).strip()
        return strangeForm[:len(strangeForm) - len(maxForm[0])] + maxForm[1]

    def substr(self, s1, s2):
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return s1[0 : i]

    def isBadValue(self, i):
        return (i <= 16824383 and i >= 16824368) or (i >= 16786128 and i <= 16786143) or \
               (i <= 16873663 and i >= 16873632) or (i >= 16926016 and i <= 16926031) or \
               (i <= 17035263 and i >= 17035232) or (i >= 17060080 and i <= 17060095) or \
               (i <= 17087487 and i >= 17087456) or (i >= 17998800 and i <= 17998815) or \
               (i <= 18128432 and i >= 18128416) or (i >= 18260592 and i <= 18260607) or \
               (i <= 18347183 and i >= 18347168)

    def reverse(self, s):
        result = ''
        i = len(s) -1
        while (i >= 0):
            result += s[i]
            i -= 1
        return result

    def findSimilarWords(self, strangeForm):
        reversedStrangeForm = self.reverse(strangeForm)
        index = 0
        while(index < len(strangeForm) and self.atergoTrie.has_keys_with_prefix( \
                reversedStrangeForm[:index])):
            index += 1
        return self.atergoTrie.keys(reversedStrangeForm[:index-1])


plp = PLP()
plp._init()


s = Stemmer(plp)
s.prepare()
print '\n###################\n'
print s.findBasicForm(u'turków')