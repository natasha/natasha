# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.interpretation import InterpretationObject


class LocationObject(InterpretationObject):

    class Attributes(Enum):

        Name = 0 # российская
        Descriptor = 1 # федерация

class AddressObject(InterpretationObject):

    class Attributes(Enum):

        StreetDescriptor = 0
        StreetName = 1

        HouseNumberDescriptor = 2
        HouseNumber = 3
