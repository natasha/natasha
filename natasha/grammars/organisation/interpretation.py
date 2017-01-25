# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.interpretation import InterpretationObject


class OrganisationObject(InterpretationObject):

    class Attributes(Enum):

        Descriptor = 0 # завод
        Name = 1 # кировский
