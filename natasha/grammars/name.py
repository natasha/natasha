
from yargy import (
    rule,
    and_, or_, not_,
)
from yargy.interpretation import fact
from yargy.predicates import (
    gram,
    is_capitalized
)
from yargy.predicates.bank import DictionaryPredicate as dictionary

from natasha.data import (
    FIRST, MAYBE_FIRST, LAST,
    load_dict
)


Name = fact(
    'Name',
    ['first', 'last', 'middle']
)


class Name(Name):
    @property
    def obj(self):
        from natasha import obj
        return obj.Name(self.first, self.last, self.middle)


FIRST_DICT = {
    item
    for path in (FIRST, MAYBE_FIRST)
    for item in load_dict(path)
}
LAST_DICT = set(load_dict(LAST))

IN_FIRST = dictionary(FIRST_DICT)
IN_LAST = dictionary(LAST_DICT)

TITLE = is_capitalized()


########
#
#   FIRST
#
########


ABBR = gram('Abbr')
NAME = and_(
    gram('Name'),
    not_(ABBR)
)
PATR = and_(
    gram('Patr'),
    not_(ABBR)
)

FIRST = or_(
    NAME,
    IN_FIRST
).interpretation(
    Name.first
)

FIRST_ABBR = and_(
    ABBR,
    TITLE
).interpretation(
    Name.first
)


##########
#
#   LAST
#
#########


SURN = gram('Surn')

LAST = or_(
    SURN,
    IN_LAST
).interpretation(
    Name.last
)

MAYBE_LAST = and_(
    TITLE,
    not_(ABBR)
).interpretation(Name.last)


########
#
#   MIDDLE
#
#########


MIDDLE = PATR.interpretation(
    Name.middle
)

MIDDLE_ABBR = and_(
    ABBR,
    TITLE
).interpretation(
    Name.middle
)


#########
#
#  FI IF
#
#########


FIRST_LAST = rule(
    FIRST,
    MAYBE_LAST
)

LAST_FIRST = rule(
    MAYBE_LAST,
    FIRST
)


###########
#
#  ABBR
#
###########


ABBR_FIRST_LAST = rule(
    FIRST_ABBR,
    '.',
    MAYBE_LAST
)

LAST_ABBR_FIRST = rule(
    MAYBE_LAST,
    FIRST_ABBR,
    '.',
)

ABBR_FIRST_MIDDLE_LAST = rule(
    FIRST_ABBR,
    '.',
    MIDDLE_ABBR,
    '.',
    MAYBE_LAST
)

LAST_ABBR_FIRST_MIDDLE = rule(
    MAYBE_LAST,
    FIRST_ABBR,
    '.',
    MIDDLE_ABBR,
    '.'
)


##############
#
#  MIDDLE
#
#############


FIRST_MIDDLE = rule(
    FIRST,
    MIDDLE
)

FIRST_MIDDLE_LAST = rule(
    FIRST,
    MIDDLE,
    MAYBE_LAST
)

LAST_FIRST_MIDDLE = rule(
    MAYBE_LAST,
    FIRST,
    MIDDLE
)


##############
#
#  SINGLE
#
#############


JUST_FIRST = FIRST

JUST_LAST = LAST


########
#
#    FULL
#
########


NAME = or_(
    FIRST_LAST,
    LAST_FIRST,

    ABBR_FIRST_LAST,
    LAST_ABBR_FIRST,
    ABBR_FIRST_MIDDLE_LAST,
    LAST_ABBR_FIRST_MIDDLE,

    FIRST_MIDDLE,
    FIRST_MIDDLE_LAST,
    LAST_FIRST_MIDDLE,

    JUST_FIRST,
    JUST_LAST,
).interpretation(
    Name
)
