# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    and_, or_,
    fact
)
from yargy.predicates import (
    eq, in_,
    gram, normalized, caseless
)


Money = fact(
    'Money',
    ['amount', 'currency']
)


EURO = normalized('евро')

DOLLARS = or_(
    normalized('доллар'),
    eq('$')
)

RUBLES = or_(
    rule(normalized('рубль')),
    rule(
        or_(
            caseless('руб'),
            caseless('р')
        ),
        eq('.').optional()
    )
)

CURRENCY = or_(
    rule(EURO),
    rule(DOLLARS),
    RUBLES
).interpretation(
    Money.currency
)

INT = gram('INT')

AMOUNT_ = or_(
    rule(INT),
    rule(INT, INT),
    rule(INT, INT, INT),
    rule(INT, '.', INT),
    rule(INT, '.', INT, '.', INT),
)

FRACTION_AMOUN = rule(
    AMOUNT_,
    in_({',', '.'}),
    INT
)

AMOUNT = or_(
    AMOUNT_,
    FRACTION_AMOUN
).interpretation(
    Money.amount
)

MONEY = rule(
    AMOUNT, CURRENCY
).interpretation(
    Money
)
