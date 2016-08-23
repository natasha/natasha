from enum import Enum
from natasha.grammars.base import TERM


ABBR_PREFIX_DICTIONARY = {
    'ООО',
    'ОАО',
    'ПАО',
    'ЗАО',
    'АО',
}


class Organisation(Enum):

    AbbrPrefixQuoted = (
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
    )
