__author__ = 'maciej'

import codecs
import collections


class Rules:
    rules = []

    def __init__(self):
        pass

    def prepare_rules(self):
        rules_file = codecs.open('../data/rules.csv', 'r', 'utf-8')
        for rule in rules_file:
            new_rule = collections.namedtuple('rules', ['d', 'm'])
            new_rule.m = rule.split(';')[0]
            new_rule.d = rule.split(';')[1].strip()
            self.rules.append(new_rule)

    def process_rules(self):
        for rule in self.rules:
            cities_file = codecs.open('../data/cities.csv', 'r', 'utf-8')
            wrong_cities = []
            rule_count_total = 0
            rule_count_correct = 0
            for city in cities_file:
                if not city.__contains__(' ') and not city.__contains__('-'):
                    if city.strip().endswith(rule.m):
                        li = city.split(';')[1].strip().rsplit(rule.m, 1)
                        city_d = rule.d.join(li)
                        rule_count_total += 1
                        if city_d == city.split(';')[0]:
                            rule_count_correct += 1
                        else:
                            print(city_d, city.split(';')[0], city.split(';')[1])
                    else:
                        wrong_cities.append(city)
            print('Liczba miast z regula ' + rule.m + ' -> ' + rule.d + ': ' + str(rule_count_total) + ', poprawnych: ' +
                  str(rule_count_correct) + '\n')
            cities_file.close()
            # wrong_cities_file = codecs.open('../data/wrong_cities.csv', 'w', 'utf-8')
            # for wrong_city in wrong_cities:
            #     wrong_cities_file.write(wrong_city.split(';')[0] + ';' + wrong_city.split(';')[1])
            # wrong_cities_file.close()

    def process_rules_multi_parts(self):
        cities_file = codecs.open('../data/cities_multiword.csv', 'r', 'utf-8')
        rule_count_total = dict()
        for rule in self.rules:
            print(rule.m + ' -> ' + rule.d)
        for city in cities_file:
            city_parts_m = city.split(';')[1].strip().split(' ')
            city_parts_d = city.split(';')[0].strip().split(' ')
            for c in city_parts_m:
                if len(city_parts_d) <= city_parts_m.index(c):
                    continue
                for rule in self.rules:
                    if c.endswith(rule.m):
                        li = c.rsplit(rule.m, 1)
                        c_d = rule.d.join(li)
                        correct = 0
                        if c_d == city_parts_d[city_parts_m.index(c)]:
                            correct = 1
                        if rule not in rule_count_total:
                            rule_count = collections.namedtuple('rules_count', ['total', 'correct'])
                            rule_count.correct = correct
                            rule_count.total = 1
                            rule_count_total[rule] = rule_count
                        else:
                            rule_count = rule_count_total[rule]
                            rule_count.correct += correct
                            rule_count.total += 1
                        break
        for rule, count in rule_count_total.items():
            # print ('Liczba miast z regula ' + r.m + ' -> ' + r.d + ': ' + str(count.total) + ', poprawnych: ' + str(count.correct) + '\n')
            print('-' + rule.m + ';-' + rule.d + ';' + str(count.total) + ';' + str(count.correct))
        cities_file.close()


r = Rules()
r.prepare_rules()
r.process_rules()
