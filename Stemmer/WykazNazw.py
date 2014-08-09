# coding=UTF-8
# -*- coding: utf-8 -*-
from __builtin__ import unicode
import codecs

from plp import PLP

from stemmer import Stemmer


__author__ = 'mslawin'


class TestPreparer:

    types = [u'wieś', u'miasto']

    def __init__(self):
        pass

    def start(self):
        city_map = []
        f = codecs.open('../miejscowosci.csv', 'r', 'utf-8')
        for line in f:
            line = unicode(line)
            line = line.replace('  ', ' ')
            if self.types.__contains__(line.strip().split(';')[2]):
                basic_form = line.split(';')[0]
                ending = line.split(';')[1].replace('-', ' -').replace('  ', ' ').strip()
                if not city_map.__contains__((basic_form, ending)):
                    city_map.append((basic_form, ending))
        return self.get_forms(city_map)

    def get_forms(self, cities):
        city_map = dict()
        for city_tuple in cities:
            has_hyphen = False
            city_parts = city_tuple[0].split(' ')
            if city_parts.__len__() == 1:
                city_parts = city_tuple[0].split('-')
                has_hyphen = True
            ending_parts = city_tuple[1].split(' ')
            form_parts = ''
            for i in range(city_parts.__len__()):
                form_parts = form_parts + self.get_form(city_parts[i], ending_parts[i])
                if has_hyphen:
                    form_parts += '-'
                else:
                    form_parts += ' '
            city_map[city_tuple[0]] = form_parts[0:form_parts.__len__()-1]
        return city_map

    def get_form(self, city, ending):
        ending = ending.replace('-', '')
        for i in reversed(range(city.__len__())):
            if ending == '':
                print ending
            if city[i] == ending[0]:
                return city[:i] + ending
        return city[:city.__len__()-1] + ending


test = TestPreparer()
cities = test.start()

plp = PLP()
plp._init()

print 'Loaded cities: ', cities.__len__()
print 'Starting analysis'

trie_files = ['trie.bak', 'trie_only_nouns.bak', 'trie_nouns_and_adjectives.bak', 'trie_nouns_and_numerals.bak', 'trie_nouns_adjectives_and_numerals.bak']

for trie_name in trie_files:
    print 'Starting', trie_name
    correct_number = 0
    all_number = 0
    s = Stemmer(plp, filename=trie_name, word_type=None)
    result_file = codecs.open('../wyniki/wies_miasto/' + trie_name.replace('bak', 'txt'), 'w', 'utf-8')
    result_file.write(u'Dopełniacz;Mianownik;Wynik Stemmera\n')
    for k, v in cities.iteritems():
        all_number += 1
        basic_form = ''
        has_hyphen = False
        if k.__contains__('-'):
            has_hyphen = True
            for city_parts in v.split('-'):
                basic_form += s.find_basic_form(city_parts) + '-'
            basic_form = basic_form[0:basic_form.__len__()-1]
        else:
            for city_parts in v.split(' '):
                basic_form += s.find_basic_form(city_parts) + ' '

        basic_form = basic_form.strip()
        if basic_form != k:
            result_file.write(v + ';' + k + ';' + basic_form + '\n')
        else:
            correct_number += 1
    result_file.write(u'Liczba miejscowości;Liczba niepoprawnie rozpoznanych;Liczba poprawnie rozpoznanych\n')
    result_file.write(str(cities.__len__()) + ';' + str(all_number-correct_number) + ';' + str(correct_number))
    print 'Done', trie_name