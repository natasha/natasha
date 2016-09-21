from enum import Enum
from natasha.grammars import Person
from natasha.grammars.base import TERM


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

    OfficialAbbrQuoted = (
        ('word', {
            'labels': [
                ('in', ABBR_PREFIX_DICTIONARY),
            ],
        }),
        ('quote', {}),
        ('word', {
            'repeat': True,
        }),
        ('quote', {}),
        TERM,
    )

    Abbr = (
        ('word', {
            'labels': [
                ('gram', 'Abbr'),
                ('gram', 'Orgn'),
            ]
        }),
        TERM,
    )

    IndividualEntrepreneur = (
        ('word', {
            'labels': [
                ('eq', 'ИП'),
            ],
        }),
        *Person.Full.value[:-1],
        TERM,
    )

    SimpleLatin = (
        ('word', {
            'labels': [
                ('dictionary', ORG_TYPE_DICTIONARY),
            ],
        }),
        ('word', {
            'labels': [
                ('gram', 'LATN'),
            ],
            'repeat': True,
        }),
        TERM,
    )
