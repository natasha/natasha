# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    fact,
    not_,
    or_,
    attribute,
)

from yargy.predicates import (
    eq,
    true,
    gram,
    caseless,
    normalized,
)

from yargy.relations import gnc_relation
from yargy.pipelines import MorphPipeline


from natasha.grammars.name import NAME_


Organisation = fact('Organisation', ['name'])


class OrganisationTypePipeline(MorphPipeline):
    grammemes = {'OrganisationType'}
    keys = [
        'АО',
        'ОАО',
        'ООО',
        'ЗАО',
        'ПАО',

        'общество',
        'акционерное общество',
        'открытое акционерное общество',
        'общество с ограниченной ответственностью',
        'закрытое акционерное общество',
        'публичное акционерное общество',

        'агентство',
        'компания',
        'организация',
        'издательство',
        'газета',
        'концерн'
        'фирма',
        'завод',
        'предприятие',
        'корпорация',
        'группа',
        'группа компаний',
        'санаторий',
        'объединение',
        'бюро',
        'подразделение',
        'филиал',
        'представительство',
        'фонд',
        'центр',

        'нии',
        'академия',
        'академия наук',
        'обсерватория',
        'университет',
        'институт',
        'политех',
        'колледж',
        'техникум',
        'училище',
        'школа',
        'музей',
        'библиотека',
    ]

gnc = gnc_relation()
ADJF_PREFIX = rule(
    or_(
        rule(gram('ADJF').match(gnc)),  # международное
        rule(  # историко-просветительское
            true(),
            eq('-'),
            gram('ADJF').match(gnc),
        ),
    ),
    or_(caseless('и'), eq(',')).optional(),
).repeatable()

QUOTED = rule(
    gram('OrganisationType'),
    gram('QUOTE'),
    not_(gram('QUOTE')).repeatable(),
    gram('QUOTE'),
)

QUOTED_WITH_ADJF_PREFIX = rule(
    ADJF_PREFIX,
    QUOTED,
)


BASIC = rule(
    ADJF_PREFIX,
    gram('OrganisationType'),
)

NAMED = rule(
    or_(
        QUOTED,
        QUOTED_WITH_ADJF_PREFIX,
        BASIC,
    ),
    or_(
        rule(normalized('имя')),
        rule(caseless('им'), eq('.').optional()),
    ),
    NAME_,
)

ORGANISATION = or_(
    QUOTED.interpretation(Organisation.name),
    QUOTED_WITH_ADJF_PREFIX.interpretation(Organisation.name),
    BASIC.interpretation(Organisation.name),
    NAMED.interpretation(Organisation.name),
).interpretation(Organisation)
