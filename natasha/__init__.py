from copy import copy
from collections import deque

from yargy import FactParser, Combinator
from natasha.grammars import Person, Geo, Money, Date, Brand, Event, Organisation

__version__ = '0.2.0'

DEFAULT_GRAMMARS = [
    Money,
    Person,
    Geo,
    Date,
    Brand,
    Event,
    Organisation,
]
