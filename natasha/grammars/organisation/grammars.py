# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    gram_not,
    gram_any,
    gram_in,
    gram_not_in,
    gnc_match,
    case_match,
    in_,
    is_lower,
    dictionary,
    dictionary_not,
    eq,
    not_eq,
    is_capitalized,
    and_,
    or_,
    label,
    is_upper,
    string_required,
)
from yargy.parser import OR
from yargy.normalization import NormalizationType


from natasha.grammars import Person
from natasha.grammars.organisation.interpretation import OrganisationObject


NAMED_ORG_INITIALS_PREFIX_RULE = [
    OR(
        [
            {
                'labels': [
                    eq('им'), # имени
                ],
                'normalization': NormalizationType.Original,
                'interpretation': {
                    'attribute': OrganisationObject.Attributes.Name,
                },
            },
            {
                'labels': [
                    eq('.'),
                ],
                'normalization': NormalizationType.Original,
            }
        ],
        [
            {
                'labels': [
                    eq('имени'),
                ],
                'normalization': NormalizationType.Original,
                'interpretation': {
                    'attribute': OrganisationObject.Attributes.Name,
                },
            }
        ]
    )
]

NAMED_ORG_INITIALS_AND_LASTNAME = [
    {
        'labels': [
            gram_in(['Name', 'Abbr']),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': OrganisationObject.Attributes.Name,
        },
    },
    {
        'labels': [
            gram('PUNCT'),
            eq('.'),
        ],
        'normalization': NormalizationType.Original,
    },
    {
        'labels': [
            gram_in(['Patr', 'Abbr']),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': OrganisationObject.Attributes.Name,
        },
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
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': OrganisationObject.Attributes.Name,
        },
    },
]

NAMED_ORG_FIRSTNAME_AS_INITIALS_AND_LASTNAME = NAMED_ORG_INITIALS_AND_LASTNAME[:2] + [
    NAMED_ORG_INITIALS_AND_LASTNAME[-1],
]

NAMED_ORG_INITIALS_RULE = [
    OR(
        NAMED_ORG_INITIALS_AND_LASTNAME,
        NAMED_ORG_FIRSTNAME_AS_INITIALS_AND_LASTNAME,
    )
]

LASTNAME_GRAMMAR = [
    {
        'labels': [
            gram('Surn'),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': OrganisationObject.Attributes.Name,
        },
    },
]

POSSIBLE_LASTNAME_GRAMMAR = [
    {
        'labels': [
            is_capitalized(True),
            is_upper(False),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': OrganisationObject.Attributes.Name,
        },
    },
]

PROBABILISTIC_NAMED_ORG_INITIALS_AND_LASTNAME = NAMED_ORG_INITIALS_AND_LASTNAME[:4] + POSSIBLE_LASTNAME_GRAMMAR

PROBABILISTIC_NAMED_ORG_FIRSTNAME_AS_INITIALS_AND_LASTNAME = NAMED_ORG_INITIALS_AND_LASTNAME[:2] + POSSIBLE_LASTNAME_GRAMMAR

PROBABILISTIC_NAMED_ORG_INITIALS_RULE = [
    OR(
        PROBABILISTIC_NAMED_ORG_INITIALS_AND_LASTNAME,
        PROBABILISTIC_NAMED_ORG_FIRSTNAME_AS_INITIALS_AND_LASTNAME,
    )
]

@label
@string_required
def is_abbr(case, token, value):
    '''
    Returns true if token contains only uppercased letters
    '''
    return token.value.isupper() == case


class Organisation(Enum):

    OfficialQuoted = [
        {
            'labels': [
                or_((
                    gram('Orgn/Commercial'),
                    gram('Orgn/Social'),
                    gram('Orgn/Abbr'),
                )),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Descriptor,
            },
        },
        {
            'labels': [
                is_abbr(True),
            ],
            'optional': True,
            'repeatable': True,
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Descriptor,
            },
        },
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
        {
            'labels': [
                gram_not('QUOTE'),
                gram_not_in('END-OF-LINE'),
                not_eq('.'),
            ],
            'repeatable': True,
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
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
            ],
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
        },
    ]

    IndividualEntrepreneur = [
        {
            'labels': [
                eq('ИП'),
            ],
            'normalization': NormalizationType.Original,
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
            'normalization': NormalizationType.Normalized,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Descriptor,
            },
        },
        {
            'labels': [
                gram_any({
                    'LATN',
                    'NUMBER',
                }),
            ],
            'repeatable': True,
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
        },
    ]

    # Санкт-Петербургский Государственный университет
    Educational = [
        {
            'labels': [
                gram('ADJF'),
                is_capitalized(True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('ADJF'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'optional': True,
            'repeatable': True,
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('Orgn/Educational'),
                gnc_match(0, solve_disambiguation=True),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Normalized,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Descriptor,
            },
        },
        {
            'labels': [
                gram_any({
                    'ablt',
                    'gent',
                }),
                gram_not_in({
                    'PREP',
                }),
                dictionary_not({
                    'имя',
                }),
            ],
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
            'optional': True,
            'repeatable': True,
        }
    ]

    # Публичная библиотека имени М. Е. Салтыкова-Щедрина
    EducationalWithInitials = Educational + NAMED_ORG_INITIALS_PREFIX_RULE + NAMED_ORG_INITIALS_RULE
    # Публичная библиотека имени Салтыкова-Щедрина
    EducationalWithLastname = Educational + NAMED_ORG_INITIALS_PREFIX_RULE + LASTNAME_GRAMMAR

    # Кировский завод
    AdjCommercial = Educational[:2] + [
        {
            'labels': [
                gram('Orgn/Commercial'),
                gnc_match(0, solve_disambiguation=True),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Normalized,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Descriptor,
            },
        },
        Educational[-1],
    ]

    AdjCommercialWithInitials = AdjCommercial + NAMED_ORG_INITIALS_PREFIX_RULE + NAMED_ORG_INITIALS_RULE
    AdjCommercialWithLastname = AdjCommercial + NAMED_ORG_INITIALS_PREFIX_RULE + LASTNAME_GRAMMAR

    # Общества андрологии и сексуальной медицины
    Social = [
        {
            'labels': [
                gram('Orgn/Social'),
                gram('sing'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Descriptor,
            },
        },
        {
            'labels': [
                gram_not_in({
                    'PREP',
                    'CONJ',
                }),
                gram_any({
                    'accs',
                    'datv',
                    'gent',
                }),
            ],
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram_any({
                    'gent',
                    'accs',
                    'ablt',
                }),
                gram_not_in({
                    'PREP',
                    'Name',
                    'Patr',
                    'Surn',
                }),
            ],
            'optional': True,
            'repeatable': True,
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
        },
    ]

    SocialWithInitials = Social + NAMED_ORG_INITIALS_PREFIX_RULE + NAMED_ORG_INITIALS_RULE
    SocialWithLastname = Social + NAMED_ORG_INITIALS_PREFIX_RULE + LASTNAME_GRAMMAR

    AdjSocial = [
        {
            'labels': [
                gram('ADJF'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('ADJF'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'optional': True,
            'repeatable': True,
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('Orgn/Social'),
                gnc_match(0, solve_disambiguation=True),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Descriptor,
            },
        },
        Social[-1],
    ]

    AdjSocialWithInitials = AdjSocial + NAMED_ORG_INITIALS_PREFIX_RULE + NAMED_ORG_INITIALS_RULE
    AdjSocialWithLastname = AdjSocial + NAMED_ORG_INITIALS_PREFIX_RULE + LASTNAME_GRAMMAR

class ProbabilisticOrganisation(Enum):

    # "Коммерсантъ" сообщил ...
    NounQuoted = [
        {
            'labels': [
                gram('QUOTE'),
            ],
            'skip': True,
        },
        {
            'labels': [
                is_capitalized(True),
                gram_any({
                    'NOUN',
                    'ADJF',
                    'LATN',
                }),
            ],
            'repeatable': True,
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('QUOTE'),
            ],
            'skip': True,
        },
    ]

    EducationalWithInitials = Organisation.Educational.value + NAMED_ORG_INITIALS_PREFIX_RULE + PROBABILISTIC_NAMED_ORG_INITIALS_RULE
    SocialWithInitials = Organisation.Social.value + NAMED_ORG_INITIALS_PREFIX_RULE + PROBABILISTIC_NAMED_ORG_INITIALS_RULE
    AdjSocialWithInitials = Organisation.AdjSocial.value + NAMED_ORG_INITIALS_PREFIX_RULE + PROBABILISTIC_NAMED_ORG_INITIALS_RULE
    AdjCommercialWithInitials = Organisation.AdjCommercial.value + NAMED_ORG_INITIALS_PREFIX_RULE + PROBABILISTIC_NAMED_ORG_INITIALS_RULE

    EducationalWithLastname = Organisation.Educational.value + NAMED_ORG_INITIALS_PREFIX_RULE + POSSIBLE_LASTNAME_GRAMMAR
    SocialWithLastname = Organisation.Social.value + NAMED_ORG_INITIALS_PREFIX_RULE + POSSIBLE_LASTNAME_GRAMMAR
    AdjSocialWithLastname = Organisation.AdjSocial.value + NAMED_ORG_INITIALS_PREFIX_RULE + POSSIBLE_LASTNAME_GRAMMAR
    AdjCommercialWithLastname = Organisation.AdjCommercial.value + NAMED_ORG_INITIALS_PREFIX_RULE + POSSIBLE_LASTNAME_GRAMMAR

