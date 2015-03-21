__author__ = 'mslawin'


class Util:
    def __init__(self):
        pass

    @staticmethod
    def is_word_unneeded(word):
        """
        Exclude all words from clp that cannot be decoded to unicode.
        :param word: string word to exclude or not
        :return: true when word should be excluded, false otherwise
        """
        return (16824383 >= word >= 16824368) or (16786128 <= word <= 16786143) or \
               (16873663 >= word >= 16873632) or (16926016 <= word <= 16926031) or \
               (17035263 >= word >= 17035232) or (17060080 <= word <= 17060095) or \
               (17087487 >= word >= 17087456) or (17998800 <= word <= 17998815) or \
               (18128432 >= word >= 18128416) or (18260592 <= word <= 18260607) or \
               (18347183 >= word >= 18347168)

    @staticmethod
    def substring(s1, s2):
        """
        Util method for determining common part of given strings
        :param s1: first string
        :param s2: second string
        :return: common part of first and second strings
        """
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return s1[0: i]

    @staticmethod
    def reverse(s):
        """
        Util method used to generate a reversed version of string s
        :param s: string that will be reversed
        :return: reversed string s
        """
        result = ''
        i = len(s) - 1
        while i >= 0:
            result += s[i]
            i -= 1
        return result

    @staticmethod
    def is_word_appropriate_type(label, word_type):
        """
        Util method for working with clp. Checks if given word has given type, by analysing its label
        :param label: clp label
        :param word_type: wanted part of speech
        :return: true if given clp label matches wanted part of speech, false otherwise
        """
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

    @staticmethod
    def get_form(city, ending):
        """
        Util method that concatenates basic form of a word with ending specific for a inflectional form
        :param city: basic form of a city
        :param ending: ending of a inflectional form
        :return: infelctional form of a given word
        """
        ending = ending.replace('-', '')
        for i in reversed(range(city.__len__())):
            if city[i] == ending[0]:
                return city[:i] + ending
        return city[:city.__len__()-1] + ending


class WordsType:
    """
    Enum class for storing parts of speech
    """
    def __init__(self):
        pass

    nouns = 1
    nouns_and_numerals = 2
    nouns_and_adjectives = 3
    nouns_adjectives_and_numerals = 4
    all = 5