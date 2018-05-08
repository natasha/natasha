# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    and_, or_
)
from yargy.interpretation import fact, attribute
from yargy.predicates import (
    eq, gte, lte, length_eq,
    dictionary, normalized,
)


Date = fact(
    'Date',
    ['year', 'month', 'day', attribute('current_era', True)]
)


MONTHS = {
    'январь': 1,
    'февраль': 2,
    'март': 3,
    'апрель': 4,
    'май': 5,
    'июнь': 6,
    'июль': 7,
    'август': 8,
    'сентябрь': 9,
    'октябрь': 10,
    'ноябрь': 11,
    'декабрь': 12,
}


MONTH_NAME = dictionary(MONTHS).interpretation(
    Date.month.normalized().custom(MONTHS.__getitem__)
)

MONTH = and_(
    gte(1),
    lte(12)
).interpretation(
    Date.month.custom(int)
)

DAY = and_(
    gte(1),
    lte(31)
).interpretation(
    Date.day.custom(int)
)

YEAR_WORD = or_(
    rule('г', eq('.').optional()),
    rule(normalized('год'))
)

YEAR = and_(
    gte(1000),
    lte(2100)
).interpretation(
    Date.year.custom(int)
)

YEAR_SHORT = and_(
    length_eq(2),
    gte(0),
    lte(99)
).interpretation(
    Date.year.custom(lambda _: 1900 + int(_))
)

ERA_YEAR = and_(
    gte(1),
    lte(100000)
).interpretation(
    Date.year.custom(int)
)

ERA_WORD = rule(
    eq('до'),
    or_(
        rule('н', eq('.'), 'э', eq('.').optional()),
        rule(normalized('наша'), normalized('эра'))
    )
).interpretation(
    Date.current_era.const(False)
)

DATE = or_(
    rule(
        DAY,
        '.',
        MONTH,
        '.',
        or_(
            YEAR,
            YEAR_SHORT
        ),
        YEAR_WORD.optional()
    ),
    rule(
        YEAR,
        YEAR_WORD
    ),
    rule(
        DAY,
        MONTH_NAME
    ),
    rule(
        MONTH_NAME,
        YEAR,
        YEAR_WORD.optional()
    ),
    rule(
        DAY,
        MONTH_NAME,
        YEAR,
        YEAR_WORD.optional()
    ),
    rule(
        ERA_YEAR,
        YEAR_WORD,
        ERA_WORD,
    )
).interpretation(
    Date
)
