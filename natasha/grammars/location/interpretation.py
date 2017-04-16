# coding: utf-8
from __future__ import unicode_literals

from enum import Enum

from yargy.normalization import get_normalized_text
from yargy.interpretation import (
    InterpretationObject,
    damerau_levenshtein_distance,
)


class LocationObject(InterpretationObject):

    class Attributes(Enum):

        Name = 0 # российская
        Descriptor = 1 # федерация

class AddressObject(InterpretationObject):

    class Attributes(Enum):

        Street_Descriptor = 0
        Street_Name = 1

        House_Number = 3
        House_Letter = 4
        House_Corpus = 5
        House_Building = 6

    @property
    def normalized_street(self):
        return get_normalized_text(self.street_name)

    @property
    def normalized_house(self):
        house = get_normalized_text(self.house_number, delimiter='')
        if self.house_letter:
            letter = get_normalized_text(self.house_letter).upper()
            house += letter
        if self.house_corpus:
            corpus = 'к' + get_normalized_text(self.house_corpus)
            house += corpus
        if self.house_building:
            build = 'с' + get_normalized_text(self.house_building)
            house += build
        return house
        
