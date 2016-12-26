# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    dictionary,
    gte,
    lte,
    gnc_match,
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

DATE_OFFSET_PREFIX_DICTIONARY = {
    'следующий',
    'прошлый',
}

DATE_OFFSET_PREFIX_GRAMMAR = {
    'labels': [
        dictionary(DATE_OFFSET_PREFIX_DICTIONARY),
    ],
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

MONTH_WITH_GNC_MATCHING_GRAMMAR = {
    'labels': [
        dictionary(MONTH_DICTIONARY),
        gnc_match(-1, solve_disambiguation=True),
    ]
}

DAY_OF_WEEK_GRAMMAR = {
    'labels': [
        dictionary(DAY_OF_WEEK_DICTIONARY),
    ],
}

DAY_OF_WEEK_WITH_GNC_MATCHING_GRAMMAR = {
    'labels': [
        dictionary(DAY_OF_WEEK_DICTIONARY),
        gnc_match(-1, solve_disambiguation=True),
    ]
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

    MonthWithOffset = [
        DATE_OFFSET_PREFIX_GRAMMAR,
        MONTH_WITH_GNC_MATCHING_GRAMMAR,
    ]

    DayOfWeekWithOffset = [
        DATE_OFFSET_PREFIX_GRAMMAR,
        DAY_OF_WEEK_WITH_GNC_MATCHING_GRAMMAR,
    ]

    CurrentMonthWithOffset = [
        DATE_OFFSET_PREFIX_GRAMMAR,
        {
            'labels': [
                dictionary({
                    'месяц',
                }),
                gnc_match(-1, solve_disambiguation=True),
            ],
        }
    ]
