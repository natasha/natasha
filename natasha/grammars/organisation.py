# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    gram_not,
    in_,
    dictionary,
    eq,
    is_capitalized,
)
from natasha.grammars import Person


ABBR_PREFIX_DICTIONARY = {
    'ООО',
    'ОАО',
    'ПАО',
    'ЗАО',
    'АО',
    'ГК',
}

ORG_TYPE_DICTIONARY = {
    'агентство',
    'компания',
    'организация',
    'концерн',
}

class Organisation(Enum):

    OfficialAbbrQuoted = [
        {
            'labels': [
                in_(ABBR_PREFIX_DICTIONARY),
            ],
        },
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
        {
            'labels': [
                gram_not('QUOTE'),
            ],
            'repeatable': True,
        },
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
    ]

    PrefixAndNoun = [
        {
            'labels': [
                dictionary(ORG_TYPE_DICTIONARY),
            ],
        },
        {
            'labels': [
                gram('NOUN'),
                gram('gent'),
                is_capitalized(True),
            ]
        },
    ]

    Abbr = [
        {
            'labels': [
                gram('Abbr'),
                gram('Orgn'),
            ]
        },
    ]

    IndividualEntrepreneur = [
        {
            'labels': [
                eq('ИП'),
            ],
        },
        Person.Full.value[0],
        Person.Full.value[1],
        Person.Full.value[2],
    ]

    SimpleLatin = [
        {
            'labels': [
                dictionary(ORG_TYPE_DICTIONARY),
            ],
        },
        {
            'labels': [
                gram('LATN'),
            ],
            'repeatable': True,
        },
    ]
