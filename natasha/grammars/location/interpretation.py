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

        House_Number_Descriptor = 2
        House_Number_Letter = 3
        House_Number = 4
