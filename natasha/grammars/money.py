# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    dictionary,
)


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

PREFIX_GRAMMAR = {'labels': [
        dictionary(PREFIX_DICTIONARY),
    ]
}

CURRENCY_GRAMMAR = {'labels': [
        dictionary(CURRENCY_DICTIONARY),
    ]
}

OPTIONAL_PUNCT_GRAMMAR = {
    'labels': [
        gram('PUNCT'),
    ],
    'optional': True,
}

NUMBER_GRAMMAR = {
    'labels': [
        gram('NUMBER'),
    ],
}

HAND_WRITTEN_NUMBER_GRAMMAR = {
    'labels': [
        gram('NUMR')
    ],
    'repeatable': True,
}

class Money(Enum):

    HandwrittenNumberWithPrefix = [
        HAND_WRITTEN_NUMBER_GRAMMAR,
        PREFIX_GRAMMAR,
        OPTIONAL_PUNCT_GRAMMAR,
        CURRENCY_GRAMMAR,
    ]

    HandwrittenNumber = [
        HAND_WRITTEN_NUMBER_GRAMMAR,
        CURRENCY_GRAMMAR,
    ]

    ObjectWithPrefix = [
        NUMBER_GRAMMAR,
        PREFIX_GRAMMAR,
        OPTIONAL_PUNCT_GRAMMAR,
        CURRENCY_GRAMMAR,
    ]

    Object = [
        NUMBER_GRAMMAR,
        CURRENCY_GRAMMAR,
    ]

    ObjectWithoutActualNumber = [
        PREFIX_GRAMMAR,
        CURRENCY_GRAMMAR,
    ]
