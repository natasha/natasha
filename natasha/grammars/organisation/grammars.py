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
    not_eq,
    is_capitalized,
    and_,
    or_,
    label,
    string_required,
)
from yargy.normalization import NormalizationType


from natasha.grammars import Person
from natasha.grammars.organisation.interpretation import OrganisationObject


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
        }
    ]

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

    AdjSocial = [
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
