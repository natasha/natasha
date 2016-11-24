# coding: utf-8
from __future__ import unicode_literals

from enum import Enum


FEDERAL_DISTRICT_DICTIONARY = {
    'центральный',
    'северо-западный',
    'южный',
    'северо-кавказский',
    'приволжский',
    'уральский',
    'сибирский',
    'дальневосточный',
}

REGION_TYPE_DICTIONARY = {
    'край',
    'район',
    'область',
    'губерния',
    'уезд',
}

COMPLEX_OBJECT_PREFIX_DICTIONARY = {
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
    'дальний',
}

PARTIAL_OBJECT_PREFIX_DICTIONARY = {
    'север',
    'северо-восток',
    'северо-запад',
    'юг',
    'юго-восток',
    'юго-запад',
    'запад',
    'восток',
}

class Geo(Enum):

    FederalDistrict = [
        {
            'labels': [
                ('gram', 'ADJF'),
                ('dictionary', FEDERAL_DISTRICT_DICTIONARY),
            ],
        },
        {
            'labels': [
                ('dictionary', {'федеральный', }),
            ],
        },
        {
            'labels': [
                ('dictionary', {'округ', }),
            ],
        },
    ]

    FederalDistrictAbbr = [
        {
            'labels': [
                ('gram', 'ADJF'),
                ('dictionary', FEDERAL_DISTRICT_DICTIONARY),
            ],
        },
        {
            'labels': [
                ('eq', 'ФО'),
            ],
        },
    ]

    Region = [
        {
            'labels': [
                ('gram', 'ADJF'),
            ],
        },
        {
            'labels': [
                ('dictionary', REGION_TYPE_DICTIONARY),
                ('gnc-match', -1),
            ],
        },
    ]

    ComplexObject = [
        {
            'labels': [
                ('gram', 'ADJF'),
                ('dictionary', COMPLEX_OBJECT_PREFIX_DICTIONARY),
            ],
        },
        {
            'labels': [
                ('gram', 'NOUN'),
                ('gram', 'Geox'),
                ('gnc-match', -1),
            ],
        },
    ]

    PartialObject = [
        {
            'labels': [
                ('gram', 'NOUN'),
                ('dictionary', PARTIAL_OBJECT_PREFIX_DICTIONARY),
            ],
        },
        {
            'labels': [
                ('gram', 'NOUN'),
                ('gram', 'Geox'),
                ('gnc-match', -1),
            ],
        },
    ]

    Object = [
        {
            'labels': [
                ('is-capitalized', True),
                ('gram', 'Geox'),
                ('gram-not', 'Abbr'),
            ],
        },
    ]
