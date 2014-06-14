# coding=UTF-8
import codecs
import sys

from plp import PLP

from stemmer import Stemmer


__author__ = 'mslawin'

from bs4 import BeautifulSoup
import re


class TestPreparer:
    def __init__(self):
        self.pattern = re.compile('[a-zA-Z]+')

    def start(self):
        city_map = []
        soup = BeautifulSoup(open('../urzedowy_wykaz/strona1.html'))
        for p in soup.find_all('p'):
            prev = p.span.text
            spans = p.find_all('span')
            last_item = self.get_span_with_hyphen(spans)
            if last_item is not None:
                if self.is_city(prev):
                    if not city_map.__contains__((prev, last_item.text)):
                        city_map.append((prev, last_item.text))
        return self.get_forms(city_map)

    def get_span_with_hyphen(self, spans):
        for i in reversed(range(spans.__len__())):
            s = spans.__getitem__(i)
            if s.text.startswith('-'):
                return s

    def is_city(self, city):
        return self.pattern.match(city)

    def get_forms(self, cities):
        city_map = dict()
        for city_tuple in cities:
            city_parts = city_tuple[0].split(' ')
            ending_parts = city_tuple[1].split(' ')
            form_parts = ''
            for i in range(city_parts.__len__()):
                form_parts = form_parts + self.get_form(city_parts[i], ending_parts[i]) + ' '
            city_map[city_tuple[0]] = form_parts.strip()
        return city_map

    def get_form(self, city, ending):
        ending = ending.replace('-', '')
        for i in reversed(range(city.__len__())):
            if city[i] == ending[0]:
                return city[:i] + ending


UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

test = TestPreparer()
cities = test.start()

plp = PLP()
plp._init()

s = Stemmer(plp)
s.load_from_file('trie_only_nouns.bak')
correct_number = 0
all_number = 0

for k, v in cities.iteritems():
    all_number += 1
    basic_form = ''
    for city_parts in v.split(' '):
        basic_form += s.find_basic_form(unicode(city_parts)) + ' '

    basic_form = basic_form.strip()
    if basic_form != k:
        print v, k, basic_form
    else:
        correct_number += 1

print "Score\n" + str(all_number) + "::" + str(correct_number)