# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    gram_not,
    gram_not_in,
    dictionary,
    is_capitalized,
    gnc_match,
    eq,
    gte,
    or_,
    in_,
)
from yargy.normalization import NormalizationType
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

    AutonomousDistrict = [
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
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'автономный', }),
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

    AutonomousDistrictAbbr = [
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
                eq('АО'),
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
    AdjfFederation = [
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

    # Соединенные Штаты / Соединенные Штаты Америки
    AdjxFederation = [
        {
            'labels': [
                gram('Adjx'),
                is_capitalized(True),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('Adjx'),
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
                    'штат',
                }),
            ],
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('gent'),
            ],
            'optional': True,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        }
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

STREET_DESCRIPTOR_DICTIONARY = {
    'улица',
    'площадь',
    'проспект',
    'проезд',
    'бульвар',
    'набережная',
    'шоссе',
    'вал',
    'аллея',
    'переулок',
    'тупик',
}

SHORT_STREET_DESCRIPTOR_RULE = [
    {
        'labels': {
            or_((
                dictionary({
                    'ул', # улица
                    'пр', # проспект / проезд?
                    'проспа', # проспект
                    'пр-том', # see kmike/github issue #88
                    'площадь', # площадь,
                    'пр-кт', # проспект
                    'пр-далее', # проезд
                    'б-литр', # бульвар, #88
                    'наб', # набережная
                    'ш', # шоссе
                    'тупой', # тупик, #88
                }),
                in_({
                    'пер' # переулок, #88
                }),
            )),
        },
        'normalization': NormalizationType.Original,
    },
    {
        'labels': [
            eq('.'),
        ],
        'optional': True,
        'normalization': NormalizationType.Original,
    }
]

NUMERIC_STREET_PART_RULE = [ # 1-я, 10-й, 100500-ой и т.д.
    {
        'labels': [
            gram('INT'),
            gte(1),
        ],
        'normalization': NormalizationType.Original,
    },
    {
        'labels': [
            eq('-'),
        ],
        'normalization': NormalizationType.Original,
    },
    {
        'labels': [
            gram_not_in({
                'PUNCT',
                'QUOTE',
                'LATN',
                'NUMBER',
                'PHONE',
                'EMAIL',
                'RANGE',
                'END-OF-LINE',
            }),
        ],
        'normalization': NormalizationType.Original,
    }
]

NUMERIC_STREET_PART_WITHOUT_SUFFIX_RULE = NUMERIC_STREET_PART_RULE[:1]

class Address(Enum):

    # Садовая улица
    AdjFull = [
        {
            'labels': [
                gram('ADJF'),
                gram_not('Abbr'),
            ],
            'normalization': NormalizationType.Inflected,
        },
        {
            'labels': [
                gram('ADJF'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'repeatable': True,
            'optional': True,
            'normalization': NormalizationType.Inflected,
        },
        {
            'labels': [
                dictionary(STREET_DESCRIPTOR_DICTIONARY),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
        },
    ]

    # улица Садовая
    AdjFullReversed = [
        {
            'labels': [
                dictionary(STREET_DESCRIPTOR_DICTIONARY),
            ],
            'normalization': NormalizationType.Inflected,
        },
        {
            'labels': [
                gram('ADJF'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'repeatable': True,
            'normalization': NormalizationType.Inflected,
        },
    ]

    # ул. Садовая
    AdjShort = SHORT_STREET_DESCRIPTOR_RULE + AdjFull[:2]

    # Садовая ул.
    AdjShortReversed = AdjFull[:2] + SHORT_STREET_DESCRIPTOR_RULE

    # улица Красных Десантников
    AdjNounFull = [AdjFullReversed[0]] + AdjFull[:2] + [
        {
            'labels': [
                gram('gent'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'repeatable': True,
            'normalization': NormalizationType.Inflected,
        }
    ]

    # ул. Красных Десантников
    AdjNounShort = AdjShort + [
        AdjNounFull[-1]
    ]

    # улица Карла Маркса
    GentFullReversed = [
        AdjFullReversed[0],
        {
            'labels': [
                gram('gent'),
                gram_not('Abbr'),
            ],
            'normalization': NormalizationType.Original,
        },
        {
            'labels': [
                gram('gent'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True)
            ],
            'optional': True,
            'repeatable': True,
            'normalization': NormalizationType.Original,
        },
    ]

    # улица К. Маркса
    GentFullReversedWithShortcut = [
        GentFullReversed[0],
        {
            'labels': [
                gram('Abbr'),
            ],
            'normalization': NormalizationType.Original,
        },
        {
            'labels': [
                eq('.'),
            ],
            'normalization': NormalizationType.Original,
        },
    ] + GentFullReversed[1:]

    # улица В. В. Ленина
    GentFullReversedWithExtendedShortcut = GentFullReversedWithShortcut[:3] + GentFullReversedWithShortcut[1:3] + GentFullReversedWithShortcut[3:]

    # пр. Маршала жукова
    GentShortReversed = SHORT_STREET_DESCRIPTOR_RULE + GentFullReversed[1:]

    # пр. К. Маркса
    GentShortReversedWithShortcut = SHORT_STREET_DESCRIPTOR_RULE + GentFullReversedWithShortcut[1:]

    # пл. В. В. Ленина
    GentShortReversedWithExtendedShortcut = SHORT_STREET_DESCRIPTOR_RULE + GentFullReversedWithExtendedShortcut[1:]

    # Николая Ершова улица
    GentFull = GentFullReversed[1:] + GentFullReversed[:1]

    # Обуховской Обороны пр-кт
    GentShort = GentShortReversed[2:] + SHORT_STREET_DESCRIPTOR_RULE

    # 1-я новорублевская улица
    AdjFullWithNumericPart = NUMERIC_STREET_PART_RULE + AdjFull

    # улица 1-я новорублевская
    AdjFullReversedWithNumericPart = AdjFullReversed[:1] + AdjFullWithNumericPart[:-1]

    # 1-я новорублевская ул.
    AdjShortWithNumericPart = AdjFullWithNumericPart[:-1] + SHORT_STREET_DESCRIPTOR_RULE

    # ул. 1-я промышленная
    AdjShortReversedWithNumericPart = SHORT_STREET_DESCRIPTOR_RULE + AdjFullWithNumericPart[:-1]

    # проспект 50 лет октября
    GentFullReversedWithNumericPrefix = GentFullReversed[:1] + NUMERIC_STREET_PART_WITHOUT_SUFFIX_RULE + GentFullReversed[1:2] + GentFullReversed[1:]

    # пр-т. 50 лет советской власти
    GentShortReversedWithNumericPrefix = GentShortReversed[:2] + NUMERIC_STREET_PART_WITHOUT_SUFFIX_RULE + GentFullReversed[1:2] + GentFullReversed[1:]

    # 2-ой проезд Перова Поля
    GentNumericSplittedByFullDescriptor = NUMERIC_STREET_PART_RULE + GentFullReversed

    # 7-я ул. текстильщиков
    GentNumericSplittedByShortDescriptor = NUMERIC_STREET_PART_RULE + GentShortReversed
