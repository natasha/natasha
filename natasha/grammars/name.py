# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    and_, or_, not_,
)
from yargy.interpretation import fact
from yargy.predicates import (
    eq, length_eq,
    gram, tag,
    is_single, is_capitalized
)
from yargy.predicates.bank import DictionaryPredicate as dictionary
from yargy.relations import gnc_relation

from natasha.data import load_dict

from yargy.rule.transformators import RuleTransformator
from yargy.rule.constructors import Rule
from yargy.predicates.constructors import AndPredicate


Name = fact(
    'Name',
    ['first', 'middle', 'last', 'nick']
)


FIRST_DICT = set(load_dict('first.txt'))
MAYBE_FIRST_DICT = set(load_dict('maybe_first.txt'))
LAST_DICT = set(load_dict('last.txt'))


##########
#
#  COMPONENTS
#
###########


IN_FIRST = dictionary(FIRST_DICT)
IN_MAYBE_FIRST = dictionary(MAYBE_FIRST_DICT)
IN_LAST = dictionary(LAST_DICT)

gnc = gnc_relation()


########
#
#   FIRST
#
########


TITLE = is_capitalized()

NOUN = gram('NOUN')
NAME_CRF = tag('I')

ABBR = gram('Abbr')
SURN = gram('Surn')
NAME = and_(
    gram('Name'),
    not_(ABBR)
)
PATR = and_(
    gram('Patr'),
    not_(ABBR)
)

FIRST = and_(
    NAME_CRF,
    or_(
        NAME,
        IN_MAYBE_FIRST,
        IN_FIRST
    )
).interpretation(
    Name.first.inflected()
).match(gnc)

FIRST_ABBR = and_(
    ABBR,
    TITLE
).interpretation(
    Name.first
).match(gnc)


##########
#
#   LAST
#
#########


LAST = and_(
    NAME_CRF,
    or_(
        SURN,
        IN_LAST
    )
).interpretation(
    Name.last.inflected()
).match(gnc)


########
#
#   MIDDLE
#
#########


MIDDLE = PATR.interpretation(
    Name.middle.inflected()
).match(gnc)

MIDDLE_ABBR = and_(
    ABBR,
    TITLE
).interpretation(
    Name.middle
).match(gnc)


#########
#
#  FI IF
#
#########


FIRST_LAST = rule(
    FIRST,
    LAST
)

LAST_FIRST = rule(
    LAST,
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
    LAST
)

LAST_ABBR_FIRST = rule(
    LAST,
    FIRST_ABBR,
    '.',
)

ABBR_FIRST_MIDDLE_LAST = rule(
    FIRST_ABBR,
    '.',
    MIDDLE_ABBR,
    '.',
    LAST
)

LAST_ABBR_FIRST_MIDDLE = rule(
    LAST,
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
    LAST
)

LAST_FIRST_MIDDLE = rule(
    LAST,
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


class StripCrfTransformator(RuleTransformator):
    def visit_term(self, item):
        if isinstance(item, Rule):
            return self.visit(item)
        elif isinstance(item, AndPredicate):
            predicates = [_ for _ in item.predicates if _ != NAME_CRF]
            return AndPredicate(predicates)
        else:
            return item


SIMPLE_NAME = NAME.transform(
    StripCrfTransformator
)
