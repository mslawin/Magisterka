# coding=UTF-8
# -*- coding: utf-8 -*-
from __builtin__ import unicode
import codecs
import operator

from plp import PLP
from utils import Util

from stemmer import Stemmer


__author__ = 'mslawin'


class TestPreparer:
    """
    Class responsible for preparing test data
    """

    types = [u'wieś', u'miasto', u'kolonia', u'osada']

    def __init__(self):
        pass

    def start(self):
        city_map = dict()
        f = codecs.open('../miejscowosci.csv', 'r', 'utf-8')
        for line in f:
            line = unicode(line)
            line = line.replace('  ', ' ')
            basic_form = line.split(';')[0]
            ending = line.split(';')[1] #.replace('-', ' -').replace('  ', ' ').strip()
            if not basic_form.__contains__(' ') and not basic_form.__contains__('-'):
                # if self.types.__contains__(line.strip().split(';')[2]):
                if basic_form != '' and ending != '':
                    form = Util.get_form(basic_form, ending)
                    if not city_map.__contains__(basic_form) or city_map[basic_form] != form:
                        city_map[basic_form] = form
        return city_map

    def get_forms(self, cities):
        city_map = dict()
        for city_tuple in cities:
            # has_hyphen = False
            city_parts = city_tuple[0].split(' ')
            if city_parts.__len__() == 1:
                city_parts = city_tuple[0].split('-')
                has_hyphen = True
            ending_parts = city_tuple[1].split(' ')
            form_parts = ''
            for i in range(city_parts.__len__()):
                print city_parts[i], ending_parts[i]
                form_parts = form_parts + Util.get_form(city_parts[i], ending_parts[i])
                if has_hyphen:
                    form_parts += '-'
                else:
                    form_parts += ' '
            city_map[city_tuple[0]] = form_parts[0:form_parts.__len__() - 1]
        return city_map


class Test:
    """
    Class responsible for running test against cities retrieved by TestPreparer
    """

    trie_files = ['trie.bak', 'trie_only_nouns.bak', 'trie_nouns_and_adjectives.bak', 'trie_nouns_and_numerals.bak',
                  'trie_nouns_adjectives_and_numerals.bak']
    # trie_files = ['trie.bak']

    def __init__(self):
        self.plp = PLP()
        self.plp._init()
        print 'Initialized plp'
        self.cities = TestPreparer().start()

        # print 'Loaded cities: ', self.cities.__len__()

    def test(self):
        print 'Starting analysis'

        for trie_name in self.trie_files:
            print 'Starting', trie_name
            correct_number = 0
            all_number = 0
            s = Stemmer(self.plp, filename=trie_name, word_type=None)
            corrects_file = codecs.open('../wyniki/single_name/wies_miasto_kolonia_osada/success_' + trie_name.replace('bak', 'txt'), 'w', 'utf-8')
            result_file = codecs.open('../wyniki/single_name/wies_miasto_kolonia_osada/' + trie_name.replace('bak', 'txt'), 'w', 'utf-8')
            result_file.write(u'Dopełniacz;Mianownik;Wynik Stemmera\n')
            corrects_file.write(u'Dopełniacz;Mianownik;Wynik Stemmera\n')
            # for k, v in self.cities.iteritems():
            cities = codecs.open('../data/cities_wies_miasto_kolonia_osada.csv', 'r', 'utf-8')
            for city in cities:
                k = city.split(';')[1].strip()
                v = city.split(';')[0].strip()
                all_number += 1
                basic_form = ''
                # word_labels = []
                # if k.__contains__('-'):
                #     for city_parts in v.split('-'):
                #         b = s.find_basic_form(city_parts)
                #         basic_form += b.basic_form + '-'
                #         word_labels.append(b.word_labels)
                #     basic_form = basic_form[0:basic_form.__len__() - 1]
                # else:
                #     for city_parts in v.split(' '):
                #         b = s.find_basic_form(city_parts)
                #         basic_form += b.basic_form + ' '
                #         word_labels.append(b.word_labels)

                basic_form = s.find_basic_form(v).basic_form.strip()
                if basic_form != k:
                # if basic_form == k:
                    result_file.write(v + ';' + k + ';' + basic_form + ';')
                    # for w_label in word_labels:
                    #     result_file.write(self.find_most_label(w_label) + ' ')
                    result_file.write('\n')
                else:
                #     corrects_file.write(v + ';' + k + ';' + basic_form + ';')
                    # for label in s.find_labels(word_labels):
                    #     corrects_file.write(label + ' ')
                    # corrects_file.write('\n')
                    correct_number += 1
            result_file.write(u'Liczba miejscowości;Liczba niepoprawnie rozpoznanych;Liczba poprawnie rozpoznanych\n')
            result_file.write(
                str(all_number) + ';' + str(all_number - correct_number) + ';' + str(correct_number))
            print 'Done', trie_name

    def find_most_label(self, w_label):
        max_labels = dict()
        for word in w_label:
            for id in self.plp.rec(word):
                label = self.plp.label(id)
                if label in max_labels:
                    max_labels[label] += 1
                else:
                    max_labels[label] = 1
        return max(max_labels.iteritems(), key=operator.itemgetter(1))[0]


    def prepare_cities(self):
        print 'Preparing cities'
        res_file = codecs.open('../data/cities.csv', 'w', 'utf-8')
        res_file.write(u'Dopełniacz;Mianownik\n')
        for k, v in self.cities.iteritems():
            res_file.write(v + ';' + k + '\n')

Test().prepare_cities()