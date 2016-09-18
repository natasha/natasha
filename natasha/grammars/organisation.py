from enum import Enum
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
                ('dictionary', ABBR_PREFIX_DICTIONARY),
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
        ('word', {
            'labels': [
                ('gram', 'Surn'),
            ],
        }),
        ('word', {
            'labels': [
                ('gram', 'Name'),
                ('gram-not', 'Abbr'),
                ('gender-match', -1),
            ],
        }),
        ('word', {
            'labels': [
                ('gram', 'Patr'),
                ('gram-not', 'Abbr'),
                ('gender-match', -1),
            ],
        }),
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
