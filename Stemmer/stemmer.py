
__author__ = 'maciej'

from plp import *

class FormEntry:
    def __init__(self, toAdd, toRemove, form):
        self.toAdd = toAdd
        self.toRemove = toRemove
        self.form = form

class Stemmer:
    def __init__(self, plp):
        self.plp = plp
    def prepare(self):
        old = ""
        index = 0
        print 'Form ToAdd ToRemove Changed'
        for i in range(16777231,18663982):
            if index == 10:
                break
            if old != self.plp.bform(i):
                toRemove = ""
                toAdd = ""
                form = self.plp.bform(i)
                for s in plp.forms(i):
                    if len(s) > 0:
                        a = self.getForm(s, form)
                        toRemove = s[len(a) : len(s)]
                        toAdd = form[len(self.getForm(s, form)) : len(form)]
                        f = FormEntry()
                        f.toAdd = toAdd
                        f.toRemove = toRemove
                        f.form = s
                        print form + " " + toAdd + " " + toRemove + " " + s
                index += 1
            old = plp.bform(i)

    def getForm(self, s1, s2):
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return s1[0 : i]

plp = PLP()
plp._init()


s = Stemmer(plp)
s.prepare()