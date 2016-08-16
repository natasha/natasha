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

YEAR_GRAMMAR = ('int', {
    'labels': [
        ('gte', 1),
    ],
})

class Date(Enum):

    Full = (
        DAY_GRAMMAR,
        MONTH_GRAMMAR,
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
        ('word', {
            'labels': [
                ('dictionary', {'год', })
            ]
        }),
        TERM,

    )
