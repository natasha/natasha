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
                ('dictionary', {
                    'северный',
                    'южный',
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
