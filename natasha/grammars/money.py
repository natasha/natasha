# coding: utf-8
from __future__ import unicode_literals, division

import re

from yargy import (
    rule,
    and_, or_,
)
from yargy.interpretation import (
    fact,
    const
)
from yargy.predicates import (
    eq, length_eq,
    in_, in_caseless,
    gram, type,
    normalized, caseless, dictionary
)

from natasha.utils import Record

from natasha.dsl import (
    Normalizable,
    money as dsl
)


Money = fact(
    'Money',
    ['integer', 'fraction', 'multiplier', 'currency', 'coins']
)


class Money(Money, Normalizable):
    @property
    def normalized(self):
        amount = self.integer
        if self.fraction:
            amount += self.fraction / 100
        if self.multiplier:
            amount *= self.multiplier
        if self.coins:
            amount += self.coins / 100
        return dsl.Money(amount, self.currency)


Rate = fact(
    'Rate',
    ['money', 'period']
)


class Rate(Rate, Normalizable):
    @property
    def normalized(self):
        return dsl.Rate(
            self.money.normalized,
            self.period
        )


Range = fact(
    'Range',
    ['min', 'max']
)


class Range(Range, Normalizable):
    @property
    def normalized(self):
        min = self.min.normalized
        max = self.max.normalized
        if not min.currency:
            min.currency = max.currency
        return dsl.Range(min, max)


DOT = eq('.')
INT = type('INT')


########
#
#   CURRENCY
#
##########


EURO = or_(
    normalized('евро'),
    eq('€')
).interpretation(
    const(dsl.EURO)
)

DOLLARS = or_(
    normalized('доллар'),
    eq('$')
).interpretation(
    const(dsl.DOLLARS)
)

RUBLES = or_(
    rule(normalized('рубль')),
    rule(
        or_(
            caseless('руб'),
            caseless('р'),
            eq('₽')
        ),
        DOT.optional()
    )
).interpretation(
    const(dsl.RUBLES)
)

CURRENCY = or_(
    EURO,
    DOLLARS,
    RUBLES
).interpretation(
    Money.currency
)

KOPEIKA = or_(
    rule(normalized('копейка')),
    rule(
        or_(
            caseless('коп'),
            caseless('к')
        ),
        DOT.optional()
    )
)

CENT = or_(
    normalized('цент'),
    eq('¢')
)

EUROCENT = normalized('евроцент')

COINS_CURRENCY = or_(
    KOPEIKA,
    rule(CENT),
    rule(EUROCENT)
)


############
#
#  MULTIPLIER
#
##########


MILLIARD = or_(
    rule(caseless('млрд'), DOT.optional()),
    rule(normalized('миллиард'))
).interpretation(
    const(10**9)
)

MILLION = or_(
    rule(caseless('млн'), DOT.optional()),
    rule(normalized('миллион'))
).interpretation(
    const(10**6)
)

THOUSAND = or_(
    rule(caseless('т'), DOT),
    rule(caseless('тыс'), DOT.optional()),
    rule(normalized('тысяча'))
).interpretation(
    const(10**3)
)

MULTIPLIER = or_(
    MILLIARD,
    MILLION,
    THOUSAND
).interpretation(
    Money.multiplier
)


########
#
#  NUMERAL
#
#######


NUMR = or_(
    gram('NUMR'),
    # https://github.com/OpenCorpora/opencorpora/issues/818
    dictionary({
        'ноль',
        'один'
    }),
)

MODIFIER = in_caseless({
    'целых',
    'сотых',
    'десятых'
})

PART = or_(
    rule(
        or_(
            INT,
            NUMR,
            MODIFIER
        )
    ),
    MILLIARD,
    MILLION,
    THOUSAND,
    CURRENCY,
    COINS_CURRENCY
)

BOUND = in_('()//')

NUMERAL = rule(
    BOUND,
    PART.repeatable(),
    BOUND
)


#######
#
#   AMOUNT
#
########


def normalize_integer(value):
    integer = re.sub('[\s.,]+', '', value)
    return int(integer)


PART = and_(
    INT,
    length_eq(3)
)

SEP = in_(',.')

INTEGER = or_(
    rule(INT),
    rule(INT, PART),
    rule(INT, PART, PART),
    rule(INT, SEP, PART),
    rule(INT, SEP, PART, SEP, PART),
).interpretation(
    Money.integer.custom(normalize_integer)
)

FRACTION = and_(
    INT,
    or_(
        length_eq(1),
        length_eq(2)
    )
).interpretation(
    Money.fraction.custom(int)
)

AMOUNT = rule(
    INTEGER,
    rule(
        SEP,
        FRACTION
    ).optional(),
    MULTIPLIER.optional(),
    NUMERAL.optional()
)

COINS_INTEGER = and_(
    INT,
    or_(
        length_eq(1),
        length_eq(2)
    )
).interpretation(
    Money.coins.custom(int)
)

COINS_AMOUNT = rule(
    COINS_INTEGER,
    NUMERAL.optional()
)


#########
#
#   MONEY
#
###########


MONEY = rule(
    AMOUNT,
    CURRENCY,
    COINS_AMOUNT.optional(),
    COINS_CURRENCY.optional()
).interpretation(
    Money
)


###########
#
#   RATE
#
##########


RATE_MONEY = MONEY.interpretation(
    Rate.money
)

PERIODS = {
    'день': dsl.DAY,
    'сутки': dsl.DAY,
    'час': dsl.HOUR,
    'смена': dsl.SHIFT
}

PERIOD = dictionary(
    PERIODS
).interpretation(
    Rate.period.normalized().custom(PERIODS.__getitem__)
)

PER = or_(
    eq('/'),
    in_caseless({'в', 'за'})
)

RATE = rule(
    RATE_MONEY,
    PER,
    PERIOD
).interpretation(
    Rate
)


#######
#
#   RANGE
#
########


DASH = eq('-')

RANGE_MONEY = rule(
    AMOUNT,
    CURRENCY.optional()
).interpretation(
    Money
)

RANGE_MIN = rule(
    eq('от').optional(),
    RANGE_MONEY.interpretation(
        Range.min
    )
)

RANGE_MAX = rule(
    eq('до').optional(),
    RANGE_MONEY.interpretation(
        Range.max
    )
)

RANGE = rule(
    RANGE_MIN,
    DASH.optional(),
    RANGE_MAX
).interpretation(
    Range
)
