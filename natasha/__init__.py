from yargy import Parser, Combinator
from natasha.grammars import Person, Geo, Money, Date, Brand, Event, Organisation

__version__ = '0.3.0'

DEFAULT_GRAMMARS = [
    Money,
    Person,
    Geo,
    Date,
    Brand,
    Event,
    Organisation,
]
