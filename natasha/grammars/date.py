# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    dictionary,
    gte,
    lte,
)


MONTH_DICTIONARY = {
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
}

DAY_OF_WEEK_DICTIONARY = {
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресенье',
}

PARTIAL_DATE_DICTIONARY = {
    'начало',
    'середина',
    'конец',
}

TIME_WORD_DICTIONARY = {
    'утро',
    'полдень',
    'вечер',
    'ночь',
}

DAY_GRAMMAR = {
    'labels': [
        gram('INT'),
        gte(1),
        lte(31),
    ],
}

MONTH_GRAMMAR = {
    'labels': [
        dictionary(MONTH_DICTIONARY),
    ],
}

DAY_OF_WEEK_GRAMMAR = {
    'labels': [
        dictionary(DAY_OF_WEEK_DICTIONARY),
    ],
}

YEAR_GRAMMAR = {
    'labels': [
        gram('NUMBER'),
        gte(1),
    ],
}

YEAR_SUFFIX_GRAMMAR = {
    'labels': [
        dictionary({'год', })
    ],
}

PARTIAL_DATE_GRAMMAR = {
    'labels': [
        dictionary(PARTIAL_DATE_DICTIONARY),
    ],
}

class Date(Enum):

    Full = [
        DAY_GRAMMAR,
        MONTH_GRAMMAR,
        YEAR_GRAMMAR,
    ]

    FullWithDigits = [
        DAY_GRAMMAR,
        {
            'labels': [
                gram('PUNCT'),
            ],
            'optional': True
        },
        {
            'labels': [
                gram('INT'),
                gte(1),
                lte(12),
            ],
        },
        {
            'labels': [
                gram('PUNCT'),
            ],
            'optional': True
        },
        YEAR_GRAMMAR,
    ]

    DayAndMonth = [
        DAY_GRAMMAR,
        MONTH_GRAMMAR,
    ]

    Year = [
        YEAR_GRAMMAR,
        YEAR_SUFFIX_GRAMMAR,
    ]

    PartialYearObject = [
        PARTIAL_DATE_GRAMMAR,
        YEAR_GRAMMAR,
        YEAR_SUFFIX_GRAMMAR,
    ]

    PartialMonthObject = [
        PARTIAL_DATE_GRAMMAR,
        MONTH_GRAMMAR,
    ]

    DayRange = [
        {
            'labels': [
                gram('INT-RANGE')
            ]
        },
        MONTH_GRAMMAR,
    ]

    YearRange = [
        {
            'labels': [
                gram('INT-RANGE')
            ]
        },
        {
            'labels': [
                dictionary({'год', }),
            ],
        },
    ]

    Month = [
        MONTH_GRAMMAR,
    ]

    DayOfWeek = [
        DAY_OF_WEEK_GRAMMAR,
    ]
