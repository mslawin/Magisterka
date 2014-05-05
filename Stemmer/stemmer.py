#coding=UTF-8
__author__ = 'maciej'

from plp import *
import marisa_trie
import sys
import codecs

class Stemmer:
    def __init__(self, plp):
        self.plp = plp

    def writeTrieToFile(self, filename):
        self.atergoTrie.save(filename)

    def loadFromFile(self, filename):
        fmt = '<15s15s15'
        self.atergoTrie = marisa_trie.RecordTrie(fmt)
        self.atergoTrie.load(filename)

    def prepare(self, onlyNouns):
        old = ""
        index = 0
        keys = []
        values = []
        for i in range(16777231,18663982):
            if onlyNouns == True:
                if self.plp.label(i)[0] != u'A':
                    continue
#            if index == 10:
#                break
            if self.isBadValue(i):
                continue
            form = self.plp.bform(i)

            if old != form:
                toRemove = ""
                toAdd = ""
                for s in self.plp.forms(i):
                    if len(s) > 0:
                        a = self.substr(s, form)
                        toRemove = s[len(a) : len(s)]
                        toAdd = form[len(a) : len(form)]
                        keys.append(self.reverse(s))
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

        maxForm0 = maxForm[0].split('\x00')[0].decode('utf-8')
        maxForm1 = maxForm[1].split('\x00')[0].decode('utf-8')
        return strangeForm[:len(strangeForm) - len(maxForm0)] + maxForm1

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
#s.prepare(True)
#s.writeTrieToFile('trie_only_nouns.bak')
s.loadFromFile('trie.bak')
print '\n###################\n'
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

f = codecs.open('test.txt', 'r', 'utf-8')
ilePoprawnych = 0
ileWszystkich = 0
for line in f:
    ileWszystkich += 1
    a = line.split(',')
    basci_form = s.findBasicForm(unicode(a[0]))
    x = unicode(a[1])
    if basci_form != a[1].strip():
        print (a[0] + "::" + basci_form + "::" + a[1])
    else:
        ilePoprawnych += 1

print "Score\n" + str(ileWszystkich) + "::" + str(ilePoprawnych)

while True:
    print s.findBasicForm(unicode(raw_input(), 'utf-8'))
