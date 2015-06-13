import codecs

from plp import PLP
from stemmer import Stemmer

__author__ = 'maciej'

plp = PLP()
plp._init()

ile_poprawnych = 0
ile_wszystkich = 0

s = Stemmer(plp, filename='trie.bak', word_type=None)
f = codecs.open('test.txt', 'r', 'utf-8')

for line in f:
    ile_wszystkich += 1
    parts = line.split(',')
    b_form = s.find_basic_form(parts[0])
    if b_form.basic_form.strip() == parts[1].strip():
        ile_poprawnych += 1
    else:
        print b_form.basic_form, ';', parts[1], ';', parts[0]

print 'Liczba poprawnie rozpoznanych: ', ile_poprawnych, '\nLiczba niepoprawnie rozpoznanych:', ile_wszystkich - ile_poprawnych
