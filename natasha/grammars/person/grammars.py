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
    case_match,
    number_match,
)
from yargy.normalization import NormalizationType
from natasha.grammars.person.interpretation import PersonObject


NAME_NOBILITY_PARTICLE_DICTIONARY = {
    'ле',
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
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Lastname,
            },
        },
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Firstname,
            },
        },
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Middlename,
            },
        },
    ]

    # Иванов Иван Иванович
    FullReversed = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Firstname,
            },
        },
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Middlename,
            },
        },
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Lastname,
            },
        },
    ]

    # Л. А. Раневская
    InitialsAndLastname = [
        {
            'labels': [
                gram_in(['Name', 'Abbr']),
            ],
            'interpretation': {
                'attribute': PersonObject.Attributes.Firstname,
            },
            'normalization': NormalizationType.Original,
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
                gnc_match(0, solve_disambiguation=True),
            ],
            'interpretation': {
                'attribute': PersonObject.Attributes.Middlename,
            },
            'normalization': NormalizationType.Original,
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
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Lastname,
            },
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
    FirstnameAsInitialsAndLastname = InitialsAndLastname[:2] + [
        InitialsAndLastname[-1],
    ]

    # Иван Иванов
    FirstnameAndLastname = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
            ],
            'interpretation': {
                'attribute': PersonObject.Attributes.Firstname,
            },
        },
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Lastname,
            },
        },
    ]

    # Иванов Иван
    LastnameAndFirstname = [
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Lastname,
            },
        },
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Firstname,
            },
        },
    ]

    # Иван Иванович
    FirstnameAndMiddlename = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Firstname,
            },
        },
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Middlename,
            },
        },
    ]

    # Иванов
    Lastname = [
        {
            'labels': [
                gram('Surn'),
                gram_any({
                    'sing',
                    'Stgm',
                }),
                gram_not('Abbr'),
                is_capitalized(True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Lastname,
            },
        },
    ]

    # Иванович
    Middlename = [
        {
            'labels': [
                gram('Patr'),
                gram_any({
                    'sing',
                    'Stgm',
                }),
                gram_not('Abbr'),
                is_capitalized(True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Middlename,
            },
        }
    ]

    # Иван
    Firstname = [
        {
            'labels': [
                gram('Name'),
                gram_any({
                    'sing',
                    'Stgm',
                }),
                gram_not('Abbr'),
                is_capitalized(True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Firstname,
            },
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
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Lastname,
            },
        },
    ]

    # Премьер-министр РФ Дмитрий Медведев
    WithPosition = [
        {
            'labels': [
                gram('Person/Position'),
            ],
            'interpretation': {
                'attribute': PersonObject.Attributes.Descriptor,
            },
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
                    gram('Abbr'),
                    gram('LATN'),
                )),
            ],
            'optional': True,
            'repeatable': True,
            'normalization': NormalizationType.Original,
        },
        {
            'labels': [
                gram('Name'),
                case_match(0, solve_disambiguation=True),
                number_match(0, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Firstname,
            },
        },
        {
            'labels': [
                gram('Patr'),
                case_match(0, solve_disambiguation=True),
                number_match(0, solve_disambiguation=True),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'optional': True,
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Middlename,
            },
        },
        {
            'labels': [
                gram('Surn'),
                case_match(0, solve_disambiguation=True),
                number_match(0, solve_disambiguation=True),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': PersonObject.Attributes.Lastname,
            },
        },
    ]

    # Пресс-секретарь «Роснефти» Михаил Леонтьев
    WithPositionAndQuotedOrganisationName = (
        WithPosition[:2] + [
            {
                'labels': [
                    gram('QUOTE'),
                ],
                'normalization': NormalizationType.Original,
            },
            {
                'labels': [
                    gram_not('QUOTE'),
                    gram_not_in('END-OF-LINE'),
                ],
                'repeatable': True,
                'normalization': NormalizationType.Original,
            },
            {
                'labels': [
                    gram('QUOTE'),
                ],
                'normalization': NormalizationType.Original,
            },
        ] + WithPosition[2:]
    )

    # граф де Кристо
    PositionAndNobilitySurname = [
        {
            'labels': [
                gram('Person/Position'),
            ],
        },
        {
            'labels': [
                dictionary(NAME_NOBILITY_PARTICLE_DICTIONARY),
            ],
        },
        {
            'labels': [
                gram('Surn'),
                gnc_match(0, solve_disambiguation=True),
            ],
            'interpretation': {
                'attribute': PersonObject.Attributes.Lastname,
            },
        }
    ]

    # Генрих Восьмой / Карл XII
    NameWithNumericPart = [
        {
            'labels': [
                gram_in({
                    'Name',
                    'sing',
                }),
                gram_not('Abbr'),
            ],
            'interpretation': {
                'attribute': PersonObject.Attributes.Firstname,
            },
        },
        {
            'labels': [
                or_((
                    and_((
                        gram_in({
                            'ADJF',
                            'Anum',
                        }),
                        gnc_match(-1, solve_disambiguation=True)
                    )),
                    gram('ROMN'),
                ))
            ]
        }
    ]


POSSIBLE_PART_OF_NAME_GRAMMAR = {
    'labels': [
        is_upper(False),
        is_capitalized(True),
        gram_not_in({
            'Geox',
            'Orgn',
        }),
    ]
}

class ProbabilisticPerson(Enum):

    '''
    This grammars matches words that looks like (but may not to be) person names
    Not included in natasha DEFAULT_GRAMMARS, but shows good result on factRuEval-16 testset
    '''

    FirstnameAndLastname = [
        Person.Firstname.value[0],
        POSSIBLE_PART_OF_NAME_GRAMMAR,
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

    FirstnameAndLastnameWithPosition = Person.WithPosition.value[:-1] + [
        FirstnameAndLastname[-1]
    ]

    Latin = [
        {
            'labels': [
                gram('LATN'),
                is_capitalized(True),
            ],
        },
        {
            'labels': [
                gram('LATN'),
                is_capitalized(True),
            ],
        },
        {
            'labels': [
                gram('PUNCT'),
                eq('.')
            ],
        },
        {
            'labels': [
                gram('LATN'),
                is_capitalized(True),
            ],
        },
    ]
