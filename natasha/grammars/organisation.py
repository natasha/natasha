# coding: utf-8
from __future__ import unicode_literals
import re

from enum import Enum
from yargy.labels import (
    gram,
    gram_not,
    in_,
    not_in,
    dictionary,
    eq,
    is_capitalized,
    custom
)
from natasha.grammars import Person

ORG_TYPE_DICTIONARY = {
    'агентство',
    'компания',
    'организация',
    'концерн',
    'фирма',
    'завод',
    'торговый дом',
    'предприятие',
    'корпорация',
    'группа',
    'группа компаний',
    'санаторий',
    'производственное объединение',
    'бюро',
    'подразделение',
    'филиал',
    'представительство',
    'ф-л',
}

ABBR_INTERFIX_DICTIONARY = {
    'ООО',
    'ЗАО',
    'ОАО',
    'АО',
    'ТОО',
    'ФГУП',
    'ПАО',
    'УФПС'
}

ABBR_REGEXP = re.compile('[А-ЯA-Z]{2,4}')


def is_abbr(token, stack):
    return bool(ABBR_REGEXP.fullmatch(str(token.value)))


class Organisation(Enum):
    OfficialAbbrQuoted = [
        {
            'labels': [
                dictionary(ORG_TYPE_DICTIONARY),
            ],
            'optional': True
        },
        {
            'labels': [
                in_(ABBR_INTERFIX_DICTIONARY),
            ],
        },
        {
            'labels': [
                custom(is_abbr),
            ],
            'optional': True
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
                not_in(ABBR_INTERFIX_DICTIONARY)
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
