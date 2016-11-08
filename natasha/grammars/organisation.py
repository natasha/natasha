from enum import Enum
from natasha.grammars import Person


ABBR_PREFIX_DICTIONARY = {
    'ООО',
    'ОАО',
    'ПАО',
    'ЗАО',
    'АО',
}

ORG_TYPE_DICTIONARY = {
    'агентство',
    'компания',
}

class Organisation(Enum):

    OfficialAbbrQuoted = [
        {
            'labels': [
                ('in', ABBR_PREFIX_DICTIONARY),
            ],
        },
        {
            'labels': [
                ('gram', 'QUOTE'),
            ],
        },
        {
            'labels': [
                ('gram-not', 'QUOTE'),
            ],
            'repeatable': True,
        },
        {
            'labels': [
                ('gram', 'QUOTE'),
            ],
        },
    ]

    Abbr = [
        {
            'labels': [
                ('gram', 'Abbr'),
                ('gram', 'Orgn'),
            ]
        },
    ]

    IndividualEntrepreneur = [
        {
            'labels': [
                ('eq', 'ИП'),
            ],
        },
        Person.Full.value[0],
        Person.Full.value[1],
        Person.Full.value[2],
    ]

    SimpleLatin = [
        {
            'labels': [
                ('dictionary', ORG_TYPE_DICTIONARY),
            ],
        },
        {
            'labels': [
                ('gram', 'LATN'),
            ],
            'repeatable': True,
        },
    ]
