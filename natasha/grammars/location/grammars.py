# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    gram_not,
    dictionary,
    is_capitalized,
    gnc_match,
    eq,
)
from natasha.grammars.location.interpretation import LocationObject


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

class Location(Enum):

    FederalDistrict = [
        {
            'labels': [
                gram('ADJF'),
                dictionary(FEDERAL_DISTRICT_DICTIONARY),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'федеральный', }),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
        {
            'labels': [
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'округ', }),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
    ]

    FederalDistrictAbbr = [
        {
            'labels': [
                gram('ADJF'),
                dictionary(FEDERAL_DISTRICT_DICTIONARY),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                eq('ФО'),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
    ]

    Region = [
        {
            'labels': [
                gram('ADJF'),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                dictionary(REGION_TYPE_DICTIONARY),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
    ]

    ComplexObject = [
        {
            'labels': [
                gram('ADJF'),
                dictionary(COMPLEX_OBJECT_PREFIX_DICTIONARY),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('NOUN'),
                gram('Geox'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
    ]

    PartialObject = [
        {
            'labels': [
                gram('NOUN'),
                dictionary(PARTIAL_OBJECT_PREFIX_DICTIONARY),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('NOUN'),
                gram('Geox'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
    ]

    # Донецкая народная республика / Российская Федерация
    AdjFederation = [
        {
            'labels': [
                gram('ADJF'),
                is_capitalized(True),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('ADJF'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'optional': True,
            'repeatable': True,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gnc_match(0, solve_disambiguation=True),
                dictionary({
                    'федерация',
                    'республика',
                }),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
    ]

    Object = [
        {
            'labels': [
                is_capitalized(True),
                gram('Geox'),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
    ]
