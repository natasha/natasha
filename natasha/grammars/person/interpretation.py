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

    def __eq__(self, other):
        score = 0.0
        if self.firstname and other.firstname:
            if get_normalized_text([self.firstname]).lower() == get_normalized_text([other.firstname]).lower():
                score += 1.0
            elif other.firstname.value.lower().startswith(self.firstname.value[0].lower()) or self.firstname.value.lower().startswith(other.firstname.value[0].lower()):
                score += 0.5
            else:
                score -= 0.5
        if self.middlename and other.middlename:
            if get_normalized_text([self.middlename]).lower() == get_normalized_text([other.middlename]).lower():
                score += 1.0
            elif other.middlename.value.lower().startswith(self.middlename.value[0].lower()) or self.middlename.value.lower().startswith(other.firstname.value[0].lower()):
                score += 0.5
            else:
                score -= 0.5
        if self.lastname and other.lastname:
            if get_normalized_text([self.lastname]).lower() == get_normalized_text([other.lastname]).lower():
                score += 1.0
            else:
                score -= 1.0
        if self.gender and other.gender:
            if self.gender.most_common(1)[0] == other.gender.most_common(1)[0]:
                score += 0.5
            else:
                score -= 0.5
        if score >= 1.0:
            if (not other.firstname) and self.firstname:
                other.firstname = self.firstname
            elif (other.firstname and self.firstname) and (len(other.firstname.value) == 1 and len(self.firstname.value) > 1):
                other.firstname = self.firstname
            if not other.middlename and self.middlename:
                other.middlename = self.middlename
            if not other.lastname and self.lastname:
                other.lastname = self.lastname
            return True
        else:
            return False
