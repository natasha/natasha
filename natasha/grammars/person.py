# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    eq,
    gram,
    gram_not,
    gram_not_in,
    gram_any,
    gram_in,
    gnc_match,
    is_capitalized,
    dictionary,
    is_upper,
    and_,
    or_,
)

NAME_NOBILITY_PARTICLE_DICTIONARY = {
    'да',
    'де',
    'ди',
    'ван',
    'фон',
    'дель',
    'бен',
    'дю',
}

class Person(Enum):

    # Иван Иванович Иванов
    Full = [
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
            ],
        },
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]

    # Иванов Иван Иванович
    FullReversed = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
            ],
        },
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]

    # Л. А. Раневская
    InitialsAndLastname = [
        {
            'labels': [
                gram_in(['Name', 'Abbr']),
            ],
        },
        {
            'labels': [
                gram('PUNCT'),
                eq('.'),
            ],
        },
        {
            'labels': [
                gram_in(['Patr', 'Abbr']),
            ],
        },
        {
            'labels': [
                gram('PUNCT'),
                eq('.'),
            ],
        },
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
            ],
        },
    ]

    # Раневская Л. А.
    LastnameAndInitials = [
        InitialsAndLastname[-1],
    ] + InitialsAndLastname[:4]

    # Раневская Л.
    LastnameAndFirstnameAsInitials = [
        InitialsAndLastname[-1],
    ] + InitialsAndLastname[:2]

    # Л. Раневская
    FistnameAsInitialsAndLastname = InitialsAndLastname[:2] + [
        InitialsAndLastname[-1],
    ]

    # Иван Иванов
    FisrtnameAndLastname = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
            ],
        },
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]

    # Иванов Иван
    LastnameAndFirstname = [
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
            ],
        },
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]

    # Иван Иванович
    FirstnameAndMiddlename = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
            ],
        },
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]

    # Иванов
    Lastname = [
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
                is_capitalized(True),
            ],
        },
    ]

    # Иванович
    Middlename = [
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                is_capitalized(True),
            ]
        }
    ]

    # Иван
    Firstname = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
                is_capitalized(True),
            ],
        },
    ]

    # Отто фон Бисмарк
    FirstnameAndLastnameWithNobilityParticle = [
        FullReversed[0],
        {
            'labels': [
                dictionary(NAME_NOBILITY_PARTICLE_DICTIONARY),
            ],
        },
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
                gnc_match(0, solve_disambiguation=True)
            ],
        },
    ]

    # Премьер-министр РФ Дмитрий Медведев
    WithPosition = [
        {
            'labels': [
                gram('Person/Position'),
            ],
        },
        {
            'labels': [
                or_((
                    and_((
                        or_((
                            gram_any({
                                'ablt',
                                'loct',
                                'gent',
                            }),
                            gram('Fixd'),
                        )),
                        gram_not_in({
                            'Name',
                            'Patr',
                            'Surn',
                        }),
                    )),
                    gram({
                        'Abbr',
                    }),
                )),
            ],
            'optional': True,
            'repeatable': True,
        },
        {
            'labels': [
                gram_any({
                    'Name',
                    'Patr',
                    'Surn',
                }),
                gnc_match(0, solve_disambiguation=True),
            ],
            'repeatable': True,
        }
    ]


POSSIBLE_PART_OF_NAME_GRAMMAR = {
    'labels': [
        gram('NOUN'),
        gram_any({'masc', 'femn'}),
        gram_not('inan'),
        gram_not('Abbr'),
        is_upper(False),
        is_capitalized(True),
    ]
}

POSSIBLE_PART_OF_NAME_WITH_GNC_MATCH_GRAMMAR = {
    'labels': [
        gram('NOUN'),
        gram_any({'masc', 'femn'}),
        gram_not('Abbr'),
        is_capitalized(True),
        gnc_match(-1, solve_disambiguation=True),
    ]
}


class ProbabilisticPerson(Enum):

    '''
    This grammars matches words that looks like (but may not to be) person names
    Not included in natasha DEFAULT_GRAMMARS, but shows good result on factRuEval-16 testset
    '''

    Full = [
        POSSIBLE_PART_OF_NAME_GRAMMAR,
        POSSIBLE_PART_OF_NAME_WITH_GNC_MATCH_GRAMMAR,
        POSSIBLE_PART_OF_NAME_WITH_GNC_MATCH_GRAMMAR,
    ]

    FirstnameAndLastname = [
        POSSIBLE_PART_OF_NAME_GRAMMAR,
        POSSIBLE_PART_OF_NAME_WITH_GNC_MATCH_GRAMMAR,
    ]

    InitialsAndLastname = Person.InitialsAndLastname.value[:4] + [
        POSSIBLE_PART_OF_NAME_GRAMMAR,
    ]

    LastnameAndInitials = [
        POSSIBLE_PART_OF_NAME_GRAMMAR
    ] + Person.InitialsAndLastname.value[:4]

    FirstnameAsInitialsAndLastname = Person.InitialsAndLastname.value[:2] + [
        POSSIBLE_PART_OF_NAME_GRAMMAR,
    ]

    LastnameAndfirstnameAsInitials = [
        POSSIBLE_PART_OF_NAME_GRAMMAR,
    ] + Person.InitialsAndLastname.value[:2]

    FirstnameAndLastnameWithNobilityParticle = [
        POSSIBLE_PART_OF_NAME_GRAMMAR,
        {
            'labels': [
                dictionary(NAME_NOBILITY_PARTICLE_DICTIONARY),
            ],
        },
        POSSIBLE_PART_OF_NAME_GRAMMAR,
    ]

    FullWithPosition = Person.WithPosition.value[:-1] + Full
    FisrtnameAndLastnameWithPosition = Person.WithPosition.value[:-1] + FirstnameAndLastname
