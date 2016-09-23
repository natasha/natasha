from enum import Enum
from natasha.grammars.base import Token, TERM

PREFIX_DICTIONARY = {
    'тысяча',
    'миллион',
    'миллиард',
    'триллион',
}

CURRENCY_DICTIONARY = {
    'рубль',
    'доллар',
    'евро',
}

PREFIX_GRAMMAR = (Token.Word, {'labels': [
        ('dictionary', PREFIX_DICTIONARY),
    ]
})

CURRENCY_GRAMMAR = (Token.Word, {'labels': [
        ('dictionary', CURRENCY_DICTIONARY),
    ]
})

class Money(Enum):

    ObjectWithPrefix = (
        (Token.Number, {}),
        PREFIX_GRAMMAR,
        (Token.Punct, {'optional': True}),
        CURRENCY_GRAMMAR,
        TERM,
    )

    Object = (
        (Token.Number, {}),
        CURRENCY_GRAMMAR,
        TERM,
    )

    ObjectWithoutActualNumber = (
        PREFIX_GRAMMAR,
        CURRENCY_GRAMMAR,
        TERM,
    )
