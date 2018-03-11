# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    not_,
    and_,
    or_,
)
from yargy.interpretation import attribute, fact
from yargy.predicates import (
    eq,
    in_,
    true,
    gram,
    type,
    caseless,
    normalized,
    is_capitalized,
)
from yargy.relations import (
    gnc_relation,
    case_relation,
)
from yargy.pipelines import morph_pipeline
from yargy.tokenizer import QUOTES

from .name import SIMPLE_NAME
from .person import POSITION_NAME

from yargy.rule.transformators import RuleTransformator


class StripInterpretationTransformator(RuleTransformator):
    def visit_InterpretationRule(self, item):
        return self.visit(item.rule)


NAME = SIMPLE_NAME.transform(StripInterpretationTransformator)
PERSON = POSITION_NAME.transform(StripInterpretationTransformator)


Organisation = fact('Organisation', ['name'])


TYPE = morph_pipeline([
    'АО',
    'ОАО',
    'ООО',
    'ЗАО',
    'ПАО',

    # TODO Check abbrs
    # 'ик',
    # 'нк',
    # 'хк',
    # 'ип',
    # 'чп',
    # 'ичп',
    # 'гпф',
    # 'нпф',
    # 'бф',
    # 'спао',
    # 'сро',

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

    'авиакомпания',
    'госкомпания',
    'инвесткомпания',
    'медиакомпания',
    'оффшор-компания',
    'радиокомпания',
    'телекомпания',
    'телерадиокомпания',
    'траст-компания',
    'фактор-компания',
    'холдинг-компания',
    'энергокомпания',
    'компания-производитель',
    'компания-изготовитель',
    'компания-заказчик',
    'компания-исполнитель',
    'компания-посредник',
    'группа управляющих компаний',
    'агрофирма',
    'турфирма',
    'юрфирма',
    'фирма-производитель',
    'фирма-изготовитель',
    'фирма-заказчик',
    'фирма-исполнитель',
    'фирма-посредник',
    'авиапредприятие',
    'агропредприятие',
    'госпредприятие',
    'нацпредприятие',
    'промпредприятие',
    'энергопредприятие',
    'авиакорпорация',
    'госкорпорация',
    'профорганизация',
    'стартап',
    'нотариальная контора',
    'букмекерская контора',
    'авиазавод',
    'автозавод',
    'винзавод',
    'подстанция',
    'гидроэлектростанция',
])

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

case = case_relation()
GENT_GROUP = rule(
    gram('gent').match(case)
).repeatable().optional()

QUOTED = rule(
    TYPE,
    in_(QUOTES),
    not_(in_(QUOTES)).repeatable(),
    in_(QUOTES),
)

QUOTED_WITH_ADJF_PREFIX = rule(
    ADJF_PREFIX,
    QUOTED,
)

BASIC = rule(
    ADJF_PREFIX,
    TYPE,
)

NAMED = rule(
    or_(
        QUOTED,
        QUOTED_WITH_ADJF_PREFIX,
        BASIC,
    ),
    GENT_GROUP,
    or_(
        rule(normalized('имя')),
        rule(caseless('им'), eq('.').optional()),
    ),
    or_(
        NAME,
        PERSON,
    ),
)

LATIN = rule(
    TYPE,
    or_(
        rule(
            and_(
                type('LATIN'),
                is_capitalized(),
            )
        ),
        rule(
            type('LATIN'),
            in_({'&', '/', '.'}),
            type('LATIN'),
        )
    ).repeatable()
)

KNOWN = rule(
    gram('Orgn'),
    GENT_GROUP,
)

ORGANISATION_ = or_(
    QUOTED,
    QUOTED_WITH_ADJF_PREFIX,
    BASIC,
    NAMED,
    LATIN,
    KNOWN,
)

ORGANISATION = ORGANISATION_.interpretation(
    Organisation.name
).interpretation(
    Organisation
)
