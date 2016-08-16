from enum import Enum
from natasha.grammars.base import TERM

PREFIX_DICTIONARY = {
    'тысяча',
    'миллион',
    'миллиард',
}

CURRENCY_DICTIONARY = {
    'рубль',
    'доллар',
}

PREFIX_GRAMMAR = ('word', {'labels': [
        ('dictionary', PREFIX_DICTIONARY),
    ]
})

CURRENCY_GRAMMAR = ('word', {'labels': [
        ('dictionary', CURRENCY_DICTIONARY),
    ]
})

class Money(Enum):

    IntObjectWithPrefix = (
        ('int', {}),
        PREFIX_GRAMMAR,
        CURRENCY_GRAMMAR,
        TERM,
    )

    FloatObjectWithPrefix = (
        ('float', {}),
        PREFIX_GRAMMAR,
        CURRENCY_GRAMMAR,
        TERM,
    )

    IntObject = (
        ('int', {}),
        CURRENCY_GRAMMAR,
        TERM,
    )

    FloatObject = (
        ('float', {}),
        CURRENCY_GRAMMAR,
        TERM,
    )
