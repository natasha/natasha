# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    and_, or_, not_,
    fact
)
from yargy.predicates import (
    eq, length_eq,
    gram, dictionary,
    is_single, is_capitalized
)
from yargy.relations import gnc_relation

from natasha.data import load_lines


Name = fact(
    'Name',
    ['first', 'last', 'middle', 'nick']
)


FIRST_DICT = set(load_lines('first.txt'))
MAYBE_FIRST_DICT = set(load_lines('maybe_first.txt'))
LAST_DICT = set(load_lines('last.txt'))
MAYBE_LAST_DICT = set(load_lines('maybe_last.txt'))


##########
#
#  COMPONENTS
#
###########


IS_FIRST = dictionary(FIRST_DICT)

MAYBE_FIRST = or_(
    and_(
        gram('Name'),
        not_(gram('Abbr'))  # А. Леонидов
    ),
    dictionary(MAYBE_FIRST_DICT)
)

TITLE_FIRST = and_(
    or_(
        IS_FIRST,
        MAYBE_FIRST
    ),
    is_capitalized()
)

TITLE_FIRST_ABBR = and_(
    length_eq(1),
    is_capitalized()
)

TITLE_MIDDLE = and_(
    gram('Patr'),
    not_(gram('Abbr')),  # Фил О’Рейли -> "О" is Patr
    is_capitalized()
)

TITLE_MIDDLE_ABBR = and_(
    length_eq(1),
    is_capitalized()
)

IS_LAST = dictionary(LAST_DICT)

MAYBE_LAST = or_(
    gram('Surn'),
    dictionary(MAYBE_LAST_DICT)
)

TITLE_LAST = and_(
    or_(
        IS_LAST,
        MAYBE_LAST
    ),
    is_capitalized()
)


#########
#
#  FI IF
#
#########


gnc = gnc_relation()

FIRST_LAST = rule(
    IS_FIRST.match(gnc).interpretation(
        Name.first.inflected()
    ),
    IS_LAST.match(gnc).interpretation(
        Name.last.inflected()
    )
)

gnc = gnc_relation()

LAST_FIRST = rule(
    IS_LAST.match(gnc).interpretation(
        Name.last.inflected()
    ),
    IS_FIRST.match(gnc).interpretation(
        Name.first.inflected()
    )
)

gnc = gnc_relation()

TITLE_FIRST_LAST = rule(
    TITLE_FIRST.match(gnc).interpretation(
        Name.first.inflected()
    ),
    TITLE_LAST.match(gnc).interpretation(
        Name.last.inflected()
    )
)

gnc = gnc_relation()

TITLE_LAST_FIRST = rule(
    TITLE_LAST.match(gnc).interpretation(
        Name.last.inflected()
    ),
    TITLE_FIRST.match(gnc).interpretation(
        Name.first.inflected()
    )
)


###########
#
#  ABBR
#
###########


ABBR_FIRST_LAST = rule(
    TITLE_FIRST_ABBR.interpretation(
        Name.first
    ),
    '.',
    TITLE_LAST.interpretation(
        Name.last.inflected()
    )
)

LAST_ABBR_FIRST = rule(
    TITLE_LAST.interpretation(
        Name.last.inflected()
    ),
    TITLE_FIRST_ABBR.interpretation(
        Name.first
    ),
    '.',
)

ABBR_FIRST_MIDDLE_LAST = rule(
    TITLE_FIRST_ABBR.interpretation(
        Name.first
    ),
    '.',
    TITLE_MIDDLE_ABBR.interpretation(
        Name.middle
    ),
    '.',
    TITLE_LAST.interpretation(
        Name.last.inflected()
    )
)

LAST_ABBR_FIRST_MIDDLE = rule(
    TITLE_LAST.interpretation(
        Name.last.inflected()
    ),
    TITLE_FIRST_ABBR.interpretation(
        Name.first
    ),
    '.',
    TITLE_MIDDLE_ABBR.interpretation(
        Name.middle
    ),
    '.'
)


##############
#
#  MIDDLE
#
#############


gnc = gnc_relation()

TITLE_FIRST_MIDDLE = rule(
    TITLE_FIRST.match(gnc).interpretation(
        Name.first.inflected()
    ),
    TITLE_MIDDLE.match(gnc).interpretation(
        Name.middle.inflected()
    )
)

gnc1 = gnc_relation()
gnc2 = gnc_relation()

TITLE_FIRST_MIDDLE_LAST = rule(
    TITLE_FIRST.match(gnc1).interpretation(
        Name.first.inflected()
    ),
    TITLE_MIDDLE.match(gnc2).interpretation(
        Name.middle.inflected()
    ),
    TITLE_LAST.match(gnc1, gnc2).interpretation(
        Name.last.inflected()
    )
)

gnc1 = gnc_relation()
gnc2 = gnc_relation()

TITLE_LAST_FIRST_MIDDLE = rule(
    TITLE_LAST.match(gnc1, gnc2).interpretation(
        Name.last.inflected()
    ),
    TITLE_FIRST.match(gnc1).interpretation(
        Name.first.inflected()
    ),
    TITLE_MIDDLE.match(gnc2).interpretation(
        Name.middle.inflected()
    )
)


##############
#
#  SINGLE
#
#############


JUST_FIRST = rule(
    and_(
        IS_FIRST,
        is_single(),
    ).interpretation(
        Name.first.inflected()
    )
)

JUST_LAST = rule(
    and_(
        IS_LAST,
        is_single(),
    ).interpretation(
        Name.last.inflected()
    )
)

NAME_ = or_(
    FIRST_LAST,
    LAST_FIRST,
    TITLE_FIRST_LAST,
    TITLE_LAST_FIRST,

    ABBR_FIRST_LAST,
    LAST_ABBR_FIRST,
    ABBR_FIRST_MIDDLE_LAST,
    LAST_ABBR_FIRST_MIDDLE,

    TITLE_FIRST_MIDDLE,
    TITLE_FIRST_MIDDLE_LAST,
    TITLE_LAST_FIRST_MIDDLE,

    JUST_FIRST,
    JUST_LAST,
)

NAME = NAME_.interpretation(
    Name
)
