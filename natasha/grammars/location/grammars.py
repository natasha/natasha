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
    length_eq,
    eq,
    gte,
    or_,
    in_,
)
from yargy.parser import OR
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
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'федеральный', }),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
        {
            'labels': [
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'округ', }),
            ],
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'автономный', }),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Descriptor,
            },
        },
        {
            'labels': [
                gnc_match(-1, solve_disambiguation=True),
                dictionary({'округ', }),
            ],
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                dictionary(REGION_TYPE_DICTIONARY),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
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
                    'империя',
                }),
            ],
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gnc_match(0, solve_disambiguation=True),
                dictionary({
                    'штат',
                    'эмират',
                }),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': LocationObject.Attributes.Name,
            },
        },
        {
            'labels': [
                gram('gent'),
            ],
            'optional': True,
            'normalization': NormalizationType.Inflected,
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
            'normalization': NormalizationType.Inflected,
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
            'attribute': AddressObject.Attributes.Street_Descriptor,
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
            'attribute': AddressObject.Attributes.Street_Name,
        },
    },
    {
        'labels': [
            eq('-'),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.Street_Name,
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
            'attribute': AddressObject.Attributes.Street_Name,
        },
    }
]

NUMERIC_STREET_PART_WITHOUT_SUFFIX_RULE = NUMERIC_STREET_PART_RULE[:1]


class Street(Enum):

    # Садовая улица
    AdjFull = [
        {
            'labels': [
                gram('ADJF'),
                gram_not('Abbr'),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Name,
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
                'attribute': AddressObject.Attributes.Street_Name,
            },
        },
        {
            'labels': [
                dictionary(STREET_DESCRIPTOR_DICTIONARY),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Inflected,
            'interpretation': {
                'attribute': AddressObject.Attributes.Street_Descriptor,
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
                'attribute': AddressObject.Attributes.Street_Descriptor,
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
                'attribute': AddressObject.Attributes.Street_Name,
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
                'attribute': AddressObject.Attributes.Street_Name,
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
                'attribute': AddressObject.Attributes.Street_Name,
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
                'attribute': AddressObject.Attributes.Street_Name,
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
                'attribute': AddressObject.Attributes.Street_Name,
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


STREET_GRAMMAR = [
    OR(*[_.value for _ in Street])
]


HOUSE_NUMBER_SINGLE_DIGIT_GRAMMAR = [
    {
        'labels': [
            gram('INT'),
            gte(1),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Number,
        },
    },
]

HOUSE_NUMBER_DIGIT_WITH_SLASH_GRAMMAR = [
    {
        'labels': [
            gram('INT'),
            gte(1),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Number,
        },
    },
    {
        'labels': [
            eq('/')
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Number,
        },
    },
    {
        'labels': [
            gram('INT'),
            gte(1),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Number,
        },
    },
]

HOUSE_NUMBER_DIGIT_GRAMMAR = [
    OR(
        HOUSE_NUMBER_SINGLE_DIGIT_GRAMMAR,
        HOUSE_NUMBER_DIGIT_WITH_SLASH_GRAMMAR
    )
]


HOUSE_NUMBER_FULL_GRAMMAR = [
    {
        'labels': [
            dictionary({
                'дом',
            }),
        ],
    },
] + HOUSE_NUMBER_DIGIT_GRAMMAR

HOUSE_NUMBER_SHORT_GRAMMAR = [
    {
        'labels': [
            eq('д')
        ],
    },
    {
        'labels': [
            eq('.'),
        ],
        'optional': True,
    },
] + HOUSE_NUMBER_DIGIT_GRAMMAR

HOUSE_NUMBER_GRAMMAR = [
    OR(
        HOUSE_NUMBER_SHORT_GRAMMAR,
        HOUSE_NUMBER_FULL_GRAMMAR,
        HOUSE_NUMBER_DIGIT_GRAMMAR
    )
]


SYMBOLS = set('абвгдежзиклмнопрстАБВГДЕЖЗИКЛМНОПРСТabcdeABCDE')

HOUSE_LETTER_SINGLE_SYMBOL_GRAMMAR = [
    {
        'labels': [
            in_(SYMBOLS)
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Letter
        },

    },
]

HOUSE_LETTER_QUOTED_SYMBOL_GRAMMAR = [
    {
        'labels': [
            gram('QUOTE'),
        ],
    },
    HOUSE_LETTER_SINGLE_SYMBOL_GRAMMAR[0],
    {
        'labels': [
            gram('QUOTE'),
        ],
    },
]

HOUSE_LETTER_SYMBOL_GRAMMAR = [
    OR(
        HOUSE_LETTER_SINGLE_SYMBOL_GRAMMAR,
        HOUSE_LETTER_QUOTED_SYMBOL_GRAMMAR
    )
]

HOUSE_LETTER_FULL_GRAMMAR = [
    {
        'labels': [
            dictionary({
                'литер',
            }),
        ],
    },
] + HOUSE_LETTER_SYMBOL_GRAMMAR

HOUSE_LETTER_SHORT_GRAMMAR = [
    {
        'labels': [
            or_((
                eq('лит'), # литер
                eq('л'),
            )),
        ],
    },
    {
        'labels': [
            eq('.'),
        ],
        'optional': True,
    },
] + HOUSE_LETTER_SYMBOL_GRAMMAR

HOUSE_LETTER_GRAMMAR = [
    OR(
        HOUSE_LETTER_FULL_GRAMMAR,
        HOUSE_LETTER_SHORT_GRAMMAR,
        HOUSE_LETTER_SYMBOL_GRAMMAR
    )
]


HOUSE_CORPUS_FULL_GRAMMAR = [
    {
        'labels': [
            dictionary({
                'корпус',
            }),
        ],
    },
    {
        'labels': [
            gram('INT'),
            gte(1),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Corpus
        },
    }
]

HOUSE_CORPUS_SHORT_GRAMMAR = [
    {
        'labels': [
            in_({
                'корп',
                'кор',
                'к'
            })
        ],
    },
    {
        'labels': [
            eq('.'),
        ],
        'optional': True,
    },
    HOUSE_CORPUS_FULL_GRAMMAR[-1],
]

HOUSE_CORPUS_GRAMMAR = [
    OR(
        HOUSE_CORPUS_FULL_GRAMMAR,
        HOUSE_CORPUS_SHORT_GRAMMAR
    )
]

HOUSE_BUILDING_FULL_GRAMMAR = [
    {
        'labels': [
            dictionary({
                'строение',
            }),
        ],
    },
    {
        'labels': [
            gram('INT'),
            gte(1),
        ],
        'normalization': NormalizationType.Original,
        'interpretation': {
            'attribute': AddressObject.Attributes.House_Building
        },
    }
]

HOUSE_BUILDING_SHORT_GRAMMAR = [
    {
        'labels': [
            in_({
                'стр',
                'ст',
                'с',
            })
        ],
    },
    {
        'labels': [
            eq('.'),
        ],
        'optional': True,
    },
    HOUSE_BUILDING_FULL_GRAMMAR[-1],
]

HOUSE_BUILDING_GRAMMAR = [
    OR(
        HOUSE_BUILDING_FULL_GRAMMAR,
        HOUSE_BUILDING_SHORT_GRAMMAR
    )
]

OPTIONAL_COMMA_GRAMMAR = [
    {
        'labels': [
            eq(','),
        ],
        'optional': True,
    }
]


OPTIONAL_DASH_GRAMMAR = [
    {
        'labels': [
            eq('-'),
        ],
        'optional': True,
    }
]


class Address(Enum):
    StreetHouseNumber = STREET_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR

    StreetHouseNumberCorpus = STREET_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_CORPUS_GRAMMAR

    StreetHouseNumberLetter = STREET_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + OPTIONAL_DASH_GRAMMAR + HOUSE_LETTER_GRAMMAR

    StreetHouseNumberLetterCorpus = STREET_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + OPTIONAL_DASH_GRAMMAR + HOUSE_LETTER_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_CORPUS_GRAMMAR
    
    StreetHouseNumberBuilding = STREET_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_BUILDING_GRAMMAR

    StreetHouseNumberCorpusBuilding = STREET_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_CORPUS_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_BUILDING_GRAMMAR

    StreetHouseNumberLetterBuilding = STREET_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + OPTIONAL_DASH_GRAMMAR + HOUSE_LETTER_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_BUILDING_GRAMMAR

    StreetHouseNumberLetterCorpusBuilding = STREET_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_NUMBER_GRAMMAR + OPTIONAL_DASH_GRAMMAR + HOUSE_LETTER_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_CORPUS_GRAMMAR + OPTIONAL_COMMA_GRAMMAR + HOUSE_BUILDING_GRAMMAR
    
