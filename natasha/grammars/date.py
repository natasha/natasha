from enum import Enum
from natasha.grammars.base import TERM


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

DAY_GRAMMAR = ('int', {
    'labels': [
        ('gte', 1),
        ('lte', 31),
    ],
})

MONTH_GRAMMAR = ('word', {
    'labels': [
        ('dictionary', MONTH_DICTIONARY),
    ],
})

DAY_OF_WEEK_GRAMMAR = ('word', {
    'labels': [
        ('dictionary', DAY_OF_WEEK_DICTIONARY),
    ],
})

YEAR_GRAMMAR = ('int', {
    'labels': [
        ('gte', 1),
    ],
})

YEAR_FLOAT_GRAMMAR = ('float', {
    'labels': [
        ('gte', 0.0),
    ],
})

YEAR_SUFFIX_GRAMMAR = ('word', {
    'labels': [
        ('dictionary', {'год', })
    ],
})

PARTIAL_DATE_GRAMMAR = ('word', {
    'labels': [
        ('dictionary', PARTIAL_DATE_DICTIONARY),
    ],
})

class Date(Enum):

    Full = (
        DAY_GRAMMAR,
        MONTH_GRAMMAR,
        YEAR_GRAMMAR,
        TERM,
    )

    FullWithDigits = (
        DAY_GRAMMAR,
        ('punct', {'optional': True}),
        ('int', {
            'labels': [
                ('gte', 1),
                ('lte', 12),
            ],
        }),
        ('punct', {'optional': True}),
        YEAR_GRAMMAR,
        TERM,
    )

    DayAndMonth = (
        DAY_GRAMMAR,
        MONTH_GRAMMAR,
        TERM,
    )

    Year = (
        YEAR_GRAMMAR,
        YEAR_SUFFIX_GRAMMAR,
        TERM,
    )

    YearFloat = (
        YEAR_FLOAT_GRAMMAR,
        YEAR_SUFFIX_GRAMMAR,
        TERM,
    )

    PartialYearObject = (
        PARTIAL_DATE_GRAMMAR,
        YEAR_GRAMMAR,
        YEAR_SUFFIX_GRAMMAR,
        TERM,
    )

    PartialMonthObject = (
        PARTIAL_DATE_GRAMMAR,
        MONTH_GRAMMAR,
        TERM,
    )

    Month = (
        MONTH_GRAMMAR,
        TERM,
    )

    DayOfWeek = (
        DAY_OF_WEEK_GRAMMAR,
        TERM,
    )
