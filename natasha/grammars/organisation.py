# coding: utf-8
from __future__ import unicode_literals
import re

from enum import Enum
from yargy.labels import (
    gram,
    gram_not,
    gram_any,
    gram_not_in,
    gnc_match,
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
    'издательство',
    'газета',
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
    'фонд',
}

EDUCATION_TYPE_DICTIONARY = {
    'обсерватория',
    'университет',
    'институт',
    'политех',
    'колледж',
}

SOCIAL_TYPE_DICTIONARY = {
    'ассамблея',
    'оргкомитет',
    'пресс-служба',
    'подразделение',
    'комитет',
    'редакция',
    'храм',
    'центр',
    'союз',
    'совет',
    'общество',
    'объединение',
    'министерство',
    'правительство',
    'руководство',
    'администрация',
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
                is_capitalized(True),
                not_in(ABBR_INTERFIX_DICTIONARY),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'repeatable': True,
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

    # Санкт-Петербургский Государственный университет
    Educational = [
        {
            'labels': [
                gram('ADJF'),
                is_capitalized(True),
            ],
        },
        {
            'labels': [
                gram('ADJF'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'optional': True,
            'repeatable': True,
        },
        {
            'labels': [
                dictionary(EDUCATION_TYPE_DICTIONARY),
                gnc_match(-1, solve_disambiguation=True),
            ],
        }
    ]

    # Общества андрологии и сексуальной медицины
    Social = [
        {
            'labels': [
                dictionary(SOCIAL_TYPE_DICTIONARY),
            ],
        },
        {
            'labels': [
                gram_not_in({
                    'CONJ',
                    'PREP',
                }),
                gram_any({
                    'datv',
                    'gent',
                    'Orgn',
                }),
                gram_not_in({
                    'Name',
                    'Patr',
                    'Surn',
                }),
            ]
        },
        {
            'labels': [
                gram_any({
                    'datv',
                    'gent',
                    'ablt',
                    'Orgn',
                }),
                gram_not_in({
                    'Name',
                    'Patr',
                    'Surn',
                }),
            ],
            'repeatable': True,
        },
    ]
