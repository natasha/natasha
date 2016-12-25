# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    gram_not,
    gram_any,
    gram_not_in,
    gnc_match,
    in_,
    is_lower,
    dictionary,
    eq,
    is_capitalized,
)
from natasha.grammars import Person



class Organisation(Enum):

    OfficialAbbrQuoted = [
        {
            'labels': [
                gram('Orgn/Commercial'),
            ],
            'optional': True,
        },
        {
            'labels': [
                gram('Orgn/Abbr'),
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
                gram('Orgn/Commercial'),
            ],
        },
        {
            'labels': [
                gram('NOUN'),
                gram_not('Orgn/Abbr'),
                is_capitalized(True),
                gnc_match(-1, solve_disambiguation=True)
            ],
            'repeatable': True,
        },
    ]

    # "Коммерсантъ" сообщил ...
    NounQuoted = [
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
        {
            'labels': [
                gram('NOUN'),
                is_capitalized(True),
            ],
            'repeatable': True,
        },
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
    ]

    Abbr = [
        {
            'labels': [
                gram('Abbr'),
                gram('Orgn'),
                gram_not('Orgn/Abbr'),
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
                gram('Orgn/Commercial'),
            ],
        },
        {
            'labels': [
                gram_any({
                    'LATN',
                    'NUMBER',
                }),
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
                gram('Orgn/Educational'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        }
    ]

    # Общества андрологии и сексуальной медицины
    Social = [
        {
            'labels': [
                gram('Orgn/Social'),
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
                gnc_match(-1, solve_disambiguation=True),
            ],
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
            'optional': True,
            'repeatable': True,
        },
    ]

    AdjSocial = [
        {
            'labels': [
                gram('ADJF'),
            ],
        },
        {
            'labels': [
                gram('Orgn/Social'),
                is_lower(True),
                gnc_match(-1, solve_disambiguation=True),
            ]
        },
        Social[-1],
    ]
