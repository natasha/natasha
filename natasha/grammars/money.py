# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    and_, or_,
    fact
)
from yargy.predicates import (
    eq, in_,
    gram, normalized, caseless,
    dictionary)


Money = fact(
    'Money',
    ['amount', 'range', 'currency']
)


EURO = or_(
    normalized('евро'),
    eq('€')
)

DOLLARS = or_(
    normalized('доллар'),
    eq('$')
)

RUBLES = or_(
    rule(normalized('рубль')),
    rule(
        or_(
            caseless('руб'),
            caseless('р'),
            eq('₽')
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

AMWORD = rule(
    or_(
        dictionary({
            'тысяча',
            'миллион'
        }),
        eq('т')
    ),
    eq('.').optional()
)

SEP = in_({',', '.'})

AMOUNT_ = or_(
    rule(INT),
    rule(INT, INT),
    rule(INT, INT, INT),
    rule(INT, SEP, INT),
    rule(INT, SEP, INT, SEP, INT),
)

FRACTION_AMOUN = rule(
    AMOUNT_,
    SEP,
    INT
)

AMOUNT = or_(
    AMOUNT_,
    rule(AMOUNT_, AMWORD),
    FRACTION_AMOUN,
    rule(FRACTION_AMOUN, AMWORD)
).interpretation(
    Money.amount
)

RANGE_OT = rule(
    eq('от'),
    AMOUNT
)

RANGE_DO = rule(
    eq('до'),
    AMOUNT
)

RANGE = or_(
    RANGE_OT,
    RANGE_DO,
    rule(
        RANGE_OT,
        RANGE_DO
    ),
    rule(
        AMOUNT_,
        eq('-'),
        AMOUNT_
    )
).interpretation(
    Money.range
)

TIME = rule(
    or_(
        eq('/'),
        eq('в')
    ).optional(),
    dictionary({
        'сутки',
        'час',
        'смена'
    })
)

MONEY = rule(
    or_(
        AMOUNT,
        RANGE,
        rule(RANGE, CURRENCY),
        rule(RANGE, CURRENCY, TIME),
        rule(RANGE, AMWORD, CURRENCY),
        rule(RANGE, AMWORD, CURRENCY, TIME),
        rule(AMOUNT, CURRENCY),
        rule(AMOUNT, CURRENCY, TIME),
    )
).interpretation(
    Money
)
