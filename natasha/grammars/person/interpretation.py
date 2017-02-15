# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from collections import Counter
from yargy.normalization import get_normalized_text
from yargy.interpretation import InterpretationObject


class PersonObject(InterpretationObject):

    class Attributes(Enum):

        Firstname = 0 # владимир
        Middlename = 1 # владимирович
        Lastname = 2 # путин
        Descriptor = 3 # президент
        DescriptorDestination = 4 # российской федерации

    @property
    def gender(self):
        '''
        Very simple gender prediction algorithm
        '''
        counter = Counter()
        for field, token in self.__dict__.items():
            if not token:
                continue
            for form in token.forms:
                grammemes = set()
                if ('Ms-f' in form['grammemes']) or ('Fixd' in form['grammemes']):
                    continue
                elif 'femn' in form['grammemes']:
                    grammemes |= {'femn'}
                elif 'masc' in form['grammemes']:
                    grammemes |= {'masc'}
                counter.update(grammemes)
        return counter
