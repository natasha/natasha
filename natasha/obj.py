
from itertools import zip_longest

from .record import Record


class Slot(Record):
    __attributes__ = ['key', 'value']


class Obj(Record):
    def __init__(self, *args, **kwargs):
        # by default init with none
        for key, value in zip_longest(self.__attributes__, args):
            self.__dict__[key] = value
        self.__dict__.update(kwargs)

    @property
    def slots(self):
        for key in self.__attributes__:
            value = getattr(self, key)
            if value:
                yield Slot(key, value)


class Name(Obj):
    __attributes__ = ['first', 'last', 'middle']


class Date(Obj):
    __attributes__ = ['year', 'month', 'day']


class Money(Obj):
    __attributes__ = ['amount', 'currency']


class AddrPart(Obj):
    __attributes__ = ['value', 'type']


class Addr(Obj):
    __attributes__ = ['parts']
