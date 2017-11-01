# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    fact,
    not_,
    and_,
    or_,
    attribute,
)

from yargy.predicates import (
    eq,
    in_,
    true,
    gram,
    caseless,
    normalized,
    is_capitalized,
)

from yargy.relations import (
    gnc_relation,
    case_relation,
)
from yargy.pipelines import MorphPipeline


from natasha.grammars.name import NAME_
from natasha.grammars.person import PERSON_


Organisation = fact('Organisation', ['name'])


class OrganisationTypePipeline(MorphPipeline):
    grammemes = {'OrganisationType'}
    keys = [
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
        'оффшор - компания',
        'радиокомпания',
        'телекомпания',
        'телерадиокомпания',
        'траст - компания',
        'фактор - компания',
        'холдинг - компания',
        'энергокомпания',
        'компания - производитель',
        'компания - изготовитель',
        'компания - заказчик',
        'компания - исполнитель',
        'компания - посредник',
        'группа управляющих компаний',
        'агрофирма',
        'турфирма',
        'юрфирма',
        'фирма - производитель',
        'фирма - изготовитель',
        'фирма - заказчик',
        'фирма - исполнитель',
        'фирма - посредник',
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

case = case_relation()
GENT_GROUP = rule(
    gram('gent').match(case)
).repeatable().optional()

QUOTED = rule(
    gram('OrganisationType'),
    gram('QUOTE'),
    not_(
        or_(
            gram('QUOTE'),
            gram('END-OF-LINE'),
        )).repeatable(),
    gram('QUOTE'),
).interpretation(Organisation.name)

QUOTED_WITH_ADJF_PREFIX = rule(
    ADJF_PREFIX,
    QUOTED,
).interpretation(Organisation.name)


BASIC = rule(
    ADJF_PREFIX,
    gram('OrganisationType'),
).interpretation(Organisation.name)

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
        NAME_,
        PERSON_,
    ),
).interpretation(Organisation.name)

LATIN = rule(
    gram('OrganisationType'),
    or_(
        rule(
            and_(
                gram('LATN'),
                is_capitalized(),
            )
        ),
        rule(
            gram('LATN'),
            in_({'&', '/', '.'}),
            gram('LATN'),
        )
    ).repeatable()
).interpretation(Organisation.name)

KNOWN = rule(
    gram('Orgn'),
    GENT_GROUP,
).interpretation(Organisation.name)

ORGANISATION_ = or_(
    QUOTED,
    QUOTED_WITH_ADJF_PREFIX,
    BASIC,
    NAMED,
    LATIN,
    KNOWN,
)

ORGANISATION = ORGANISATION_.interpretation(Organisation)
