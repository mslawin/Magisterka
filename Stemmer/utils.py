__author__ = 'mslawin'


class Util:
    def __init__(self):
        pass

    @staticmethod
    def is_word_unneeded(word):
        return (16824383 >= word >= 16824368) or (16786128 <= word <= 16786143) or \
               (16873663 >= word >= 16873632) or (16926016 <= word <= 16926031) or \
               (17035263 >= word >= 17035232) or (17060080 <= word <= 17060095) or \
               (17087487 >= word >= 17087456) or (17998800 <= word <= 17998815) or \
               (18128432 >= word >= 18128416) or (18260592 <= word <= 18260607) or \
               (18347183 >= word >= 18347168)

    @staticmethod
    def substring(s1, s2):
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return s1[0: i]

    @staticmethod
    def reverse(s):
        result = ''
        i = len(s) - 1
        while i >= 0:
            result += s[i]
            i -= 1
        return result

    @staticmethod
    def is_word_appropriate_type(label, word_type):
        if word_type == WordsType.nouns:
            if label != u'A':
                return False
        elif word_type == WordsType.nouns_and_adjectives:
            if label != u'A' and label != u'C':
                return False
        elif word_type == WordsType.nouns_and_numerals:
            if label != u'A' and label != u'D':
                return False
        elif word_type == WordsType.nouns_adjectives_and_numerals:
            if label != u'A' and label != u'C' and label != u'D':
                return False
        return True


class WordsType:
    def __init__(self):
        pass

    nouns = 1
    nouns_and_numerals = 2
    nouns_and_adjectives = 3
    nouns_adjectives_and_numerals = 4
    all = 5