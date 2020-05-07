
from yargy import (
    rule,
    and_, or_
)
from yargy.interpretation import fact
from yargy.predicates import (
    eq, gte, lte, length_eq,
    dictionary, normalized,
)


Date = fact(
    'Date',
    ['year', 'month', 'day']
)


class Date(Date):
    @property
    def obj(self):
        from natasha import obj
        return obj.Date(self.year, self.month, self.day)


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
).interpretation(
    Date
)
