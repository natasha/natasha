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

OPTIONAL_PUNCT_GRAMMAR = (Token.Punct, {'optional': True})

HAND_WRITTEN_NUMBER_GRAMMAR = (Token.Word, {
    'labels': [
        ('gram', 'NUMR')
    ],
    'repeat': True,
})

class Money(Enum):

    HandwrittenNumberWithPrefix = (
        HAND_WRITTEN_NUMBER_GRAMMAR,
        PREFIX_GRAMMAR,
        OPTIONAL_PUNCT_GRAMMAR,
        CURRENCY_GRAMMAR,
        TERM,
    )

    HandwrittenNumber = (
        HAND_WRITTEN_NUMBER_GRAMMAR,
        CURRENCY_GRAMMAR,
        TERM,
    )

    ObjectWithPrefix = (
        (Token.Number, {}),
        PREFIX_GRAMMAR,
        OPTIONAL_PUNCT_GRAMMAR,
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
