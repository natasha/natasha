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
from natasha.grammars.location.interpretation import LocationObject, AddressObject


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
    'тракт',
    'дорога',
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
                    'б-р', # бульвар
                    'бул', # бульвар
                    'наб', # набережная
                    'ш', # шоссе
                    'тупой', # тупик, #88
                    'дора', # дорога, #88
                }),
                in_({
                    'пер', # переулок, #88,
                    'н', # набережная
                }),
            )),
        },
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.StreetDescriptor,
        },
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
        'interpretation': {
            'attribute': AddressObject.Attributes.StreetName,
        },
    },
    {
        'labels': [
            eq('-'),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.StreetName,
        },
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
        'interpretation': {
            'attribute': AddressObject.Attributes.StreetName,
        },
    }
]

NUMERIC_STREET_PART_WITHOUT_SUFFIX_RULE = NUMERIC_STREET_PART_RULE[:1]

HOUSE_NUMBER_FULL_GRAMMAR = [ # дом 1, дом 2 и т.д.
    {
        'labels': [
            dictionary({
                'дом',
            }),
        ],
        'normalization': NormalizationType.Inflected,
        'interpretation': {
            'attribute': AddressObject.Attributes.HouseNumberDescriptor,
        },
    },
    {
        'labels': [
            gram('INT'),
            gte(1),
        ],
        'interpretation': {
            'attribute': AddressObject.Attributes.HouseNumber,
        },
    }
]

HOUSE_NUMBER_SHORT_GRAMMAR = [
    {
        'labels': [
            dictionary({
                'далее', # д. #88
            })
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.HouseNumberDescriptor,
        },
    },
    {
        'labels': [
            eq('.'),
        ],
        'optional': True,
        'normalization': NormalizationType.Original,
    },
    HOUSE_NUMBER_FULL_GRAMMAR[-1],
]

OPTIONAL_COMMA_GRAMMAR = [
    {
        'labels': [
            eq(','),
        ],
        'optional': True,
        'normalization': NormalizationType.Original,
    }
]

class Address(Enum):

    # Садовая улица
    AdjFull = [
        {
            'labels': [
                gram('ADJF'),
                gram_not('Abbr'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.StreetName,
            },
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
            'interpretation': {
                'attribute': AddressObject.Attributes.StreetName,
            },
        },
        {
            'labels': [
                dictionary(STREET_DESCRIPTOR_DICTIONARY),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.StreetDescriptor,
            },
        },
    ]

    # улица Садовая
    AdjFullReversed = [
        {
            'labels': [
                dictionary(STREET_DESCRIPTOR_DICTIONARY),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.StreetDescriptor,
            },
        },
        {
            'labels': [
                gram('ADJF'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'repeatable': True,
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.StreetName,
            },
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
            'interpretation': {
                'attribute': AddressObject.Attributes.StreetName,
            },
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
            'interpretation': {
                'attribute': AddressObject.Attributes.StreetName,
            },
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
            'interpretation': {
                'attribute': AddressObject.Attributes.StreetName,
            },
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
            'interpretation': {
                'attribute': AddressObject.Attributes.StreetName,
            },
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

    '''
    Street names with prefixed house numbers
    '''

    # Зеленая улица, дом 7
    AdjFullWithFHn = AdjFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    AdjFullWithSHn = AdjFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # улица Зеленая, дом 7
    AdjFullReversedWithFHn = AdjFullReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    AdjFullReversedWithSHn = AdjFullReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # ул. Нижняя Красносельская дом 7
    AdjShortWithFHn = AdjShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    AdjShortWithSHn = AdjShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # Настасьинский пер., дом 2
    AdjShortReversedWithFHn = AdjShortReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    AdjShortReversedWithSHn = AdjShortReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # улица Красной Гвардии, дом 2
    AdjNounFullWithFHn = AdjNounFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    AdjNounFullWithSHn = AdjNounFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # ул. Брянской пролетарской дивизии дом 2
    AdjNounShortWithFHn = AdjNounShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    AdjNounShortWithSHn = AdjNounShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # Николая Ершова улица дом 1
    GentFullWithFHn = GentFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentFullWithSHn = GentFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # улица Карла Маркса дом 1
    GentFullReversedWithFHn = GentFullReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentFullReversedWithSHn = GentFullReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # улица К. Маркса, дом 1
    GentFullReversedWithShortcutAndFHn = GentFullReversedWithShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentFullReversedWithShortcutAndSHn = GentFullReversedWithShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # улица В. И. Ленина, дом 1
    GentFullReversedWithExtendedShortcutAndFHn = GentFullReversedWithExtendedShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentFullReversedWithExtendedShortcutAndSHn = GentFullReversedWithExtendedShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # Обуховской Обороны пр-кт дом 1
    GentShortWithFHn = GentShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentShortWithSHn = GentShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # пр-кт Обуховской Обороны дом 1
    GentShortReversedWithFHn = GentShortReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentShortReversedWithSHn = GentShortReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # ул. К. Маркса, дом 1
    GentShortReversedWithShortcutAndFHn = GentShortReversedWithShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentShortReversedWithShortcutAndSHn = GentShortReversedWithShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # ул. В. И. Ленина, дом 1
    GentShortReversedWithExtendedShortcutAndFHn = GentShortReversedWithExtendedShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentShortReversedWithExtendedShortcutAndSHn = GentShortReversedWithExtendedShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # 1-я новорублевская улица дом 1
    AdjFullWithNumericPartWithFHn = AdjFullWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    AdjFullWithNumericPartWithSHn = AdjFullWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # улица 1-я новорублевская, дом 1
    AdjFullReversedWithNumericPartWithFHn = AdjFullReversedWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    AdjFullReversedWithNumericPartWithSHn = AdjFullReversedWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # 1-я новорублевская ул. дом 1
    AdjShortWithNumericPartWithFHn = AdjShortWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    AdjShortWithNumericPartWithSHn = AdjShortWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # ул. 1-я промышленная, дом 1
    AdjShortReversedWithNumericPartWithFHn = AdjShortReversedWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    AdjShortReversedWithNumericPartWithSHn = AdjShortReversedWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # проспект 50 лет октября, дом 1
    GentFullReversedWithNumericPrefixWithFHn = GentFullReversedWithNumericPrefix + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentFullReversedWithNumericPrefixWithSHn = GentFullReversedWithNumericPrefix + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # пр-т. 50 лет советской власти, дом 1
    GentShortReversedWithNumericPrefixWithFHn = GentShortReversedWithNumericPrefix + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentShortReversedWithNumericPrefixWithSHn = GentShortReversedWithNumericPrefix + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # 2-ой проезд Перова Поля, дом 1
    GentNumericSplittedByFullDescriptorWithFHn = GentNumericSplittedByFullDescriptor + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentNumericSplittedByFullDescriptorWithSHn = GentNumericSplittedByFullDescriptor + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR

    # 7-я ул. текстильщиков, дом 1
    GentNumericSplittedByShortDescriptorWithFHn = GentNumericSplittedByShortDescriptor + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR
    GentNumericSplittedByShortDescriptorWithSHn = GentNumericSplittedByShortDescriptor + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_SHORT_GRAMMAR


    '''
    Street names with not prefixed house numbers
    '''

    # Зеленая улица, 7
    AdjFullWithRHn = AdjFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # улица Зеленая, 7
    AdjFullReversedWithRHn = AdjFullReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # ул. Нижняя Красносельская, 7
    AdjShortWithRHn = AdjShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # Настасьинский пер., 2
    AdjShortReversedWithRHn = AdjShortReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # улица Красной Гвардии, 2
    AdjNounFullWithRHn = AdjNounFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # ул. Брянской пролетарской дивизии, 2
    AdjNounShortWithRHn = AdjNounShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # Николая Ершова улица, 1
    GentFullWithRHn = GentFull + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # улица Карла Маркса, 1
    GentFullReversedWithRHn = GentFullReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # улица К. Маркса, 1
    GentFullReversedWithShortcutAndRHn = GentFullReversedWithShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # улица В. И. Ленина, 1
    GentFullReversedWithExtendedShortcutAndRHn = GentFullReversedWithExtendedShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # Обуховской Обороны пр-кт, 1
    GentShortWithRHn = GentShort + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # пр-кт Обуховской Обороны, 1
    GentShortReversedWithRHn = GentShortReversed + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # ул. К. Маркса, 1
    GentShortReversedWithShortcutAndRHn = GentShortReversedWithShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]
 
    # ул. В. И. Ленина, 1
    GentShortReversedWithExtendedShortcutAndRHn = GentShortReversedWithExtendedShortcut + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # 1-я новорублевская улица, 1
    AdjFullWithNumericPartWithRHn = AdjFullWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # улица 1-я новорублевская, 1
    AdjFullReversedWithNumericPartWithRHn = AdjFullReversedWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # 1-я новорублевская ул., 1
    AdjShortWithNumericPartWithRHn = AdjShortWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # ул. 1-я промышленная, 1
    AdjShortReversedWithNumericPartWithRHn = AdjShortReversedWithNumericPart + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # проспект 50 лет октября, 1
    GentFullReversedWithNumericPrefixWithRHn = GentFullReversedWithNumericPrefix + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # пр-т. 50 лет советской власти, 1
    GentShortReversedWithNumericPrefixWithRHn = GentShortReversedWithNumericPrefix + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # 2-ой проезд Перова Поля, 1
    GentNumericSplittedByFullDescriptorWithRHn = GentNumericSplittedByFullDescriptor + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]

    # 7-я ул. текстильщиков, 1
    GentNumericSplittedByShortDescriptorWithRHn = GentNumericSplittedByShortDescriptor + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_FULL_GRAMMAR[1:]
