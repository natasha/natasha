from enum import Enum
from natasha.grammars.base import TERM


class Geo(Enum):

    Region = (
        ('word', {
            'labels': [
                ('gram', 'ADJF'),
            ],
        }),
        ('word', {
            'labels': [
                ('dictionary', [
                    'край',
                    'область',
                    'губерния',
                    'уезд'
                ]),
                ('gender-match', -1),
            ],
        }),
        TERM,
    )

    ComplexObject = (
        ('word', {
            'labels': [
                ('gram', 'ADJF'),
                ('dictionary', {
                    'северный',
                    'северо-западный',
                    'северо-восточный',
                    'южный',
                    'юго-западный',
                    'юго-восточный',
                    'западный',
                    'восточный',
                    'верхний',
                    'вышний',
                    'нижний',
                    'великий',
                })
            ],
        }),
        ('word', {
            'labels': [
                ('gram', 'NOUN'),
                ('gram', 'Geox'),
                ('gender-match', -1),
            ],
        }),
        TERM,
    )

    PartialObject = (
        ('word', {
            'labels': [
                ('gram', 'NOUN'),
                ('dictionary', {
                    'север',
                    'северо-восток',
                    'северо-запад',
                    'юг',
                    'юго-восток',
                    'юго-запад',
                    'запад',
                    'восток',
                })
            ],
        }),
        ('word', {
            'labels': [
                ('gram', 'NOUN'),
                ('gram', 'Geox'),
                ('gender-match', -1),
            ],
        }),
        TERM,
    )

    Object = (
        ('word', {
            'labels': [
                ('is-capitalized', None),
                ('gram', 'Geox'),
                ('gram-not', 'Abbr'),
            ],
        }),
        TERM,
    )
