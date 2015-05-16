__author__ = 'maciej'

import codecs
import collections


class Rules:
    rules = []

    def __init__(self):
        rules_file = codecs.open('../data/rules.csv', 'r', 'utf-8')
        for rule in rules_file:
            new_rule = collections.namedtuple('rules', ['d', 'm'])
            new_rule.m = rule.split(';')[0]
            new_rule.d = rule.split(';')[1].strip()
            self.rules.append(new_rule)

    def process_rules(self, save_changes):
        for rule in self.rules:
            cities_file = codecs.open('../data/wrong_cities.csv', 'r', 'utf-8')
            wrong_cities = []
            rule_count_total = 0
            rule_count_correct = 0
            for city in cities_file:
                if not city.__contains__(' ') and not city.__contains__('-'):
                    if city.split(';')[1].strip().endswith(rule.m):
                        city_d = city.split(';')[1].strip().replace(rule.m, rule.d)
                        rule_count_total += 1
                        if city_d == city.split(';')[0]:
                            rule_count_correct += 1
                        else:
                            wrong_cities.append(city)
                            print (city_d + ' ' + city.split(';')[0] + ' ' + city.split(';')[1].strip())
                    else:
                        wrong_cities.append(city)
            print ('Liczba miast z regula ' + rule.m + ' -> ' + rule.d + ': ' + str(rule_count_total) + ', poprawnych: ' +
                   str(rule_count_correct) + '\n')
            if save_changes:
                wrong_cities_file = codecs.open('../data/wrong_cities.csv', 'w', 'utf-8')
                for wrong_city in wrong_cities:
                    wrong_cities_file.write(wrong_city.split(';')[0] + ';' + wrong_city.split(';')[1])

Rules().process_rules(False)