# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    and_, or_, not_
)
from yargy.interpretation import fact
from yargy.predicates import (
    caseless, normalized,
    eq, length_eq,
    gram, dictionary,
    is_single, is_title
)
from yargy.relations import gnc_relation


Location = fact(
    'Location',
    ['name'],
)


gnc = gnc_relation()

REGION = rule(
    gram('ADJF').match(gnc),
    dictionary({
        'край',
        'район',
        'область',
        'губерния',
        'уезд',
    }).match(gnc),
).interpretation(Location.name.inflected())

gnc = gnc_relation()

FEDERAL_DISTRICT = rule(
    rule(caseless('северо'), '-').optional(),
    dictionary({
        'центральный',
        'западный',
        'южный',
        'кавказский',
        'приволжский',
        'уральский',
        'сибирский',
        'дальневосточный',
    }).match(gnc),
    or_(
        rule(
            dictionary({'федеральный'}).match(gnc),
            dictionary({'округ'}).match(gnc),
        ),
        rule('ФО'),
    ),
).interpretation(Location.name.inflected())

gnc = gnc_relation()

AUTONOMOUS_DISTRICT = rule(
    gram('ADJF').match(gnc).repeatable(),
    or_(
        rule(
            dictionary({'автономный'}).match(gnc),
            dictionary({'округ'}).match(gnc),
        ),
        rule('АО'),
    ),
).interpretation(Location.name.inflected())

gnc = gnc_relation()

FEDERATION = rule(
    gram('ADJF').match(gnc).repeatable(),
    dictionary({
        'республика',
        'федерация',
    }).match(gnc)
).interpretation(Location.name.inflected())

gnc = gnc_relation()

ADJX_FEDERATION = rule(
    or_(
        gram('Adjx'),
        gram('ADJF'),
    ).match(gnc).repeatable(),
    dictionary({
        'штат',
        'эмират',
    }).match(gnc),
    gram('gent').optional().repeatable()
).interpretation(Location.name.inflected())

gnc = gnc_relation()

STATE = rule(
    dictionary({
        'графство',
        'штат',
    }),
    gram('ADJF').match(gnc).optional(),
    gram('NOUN').match(gnc),
).interpretation(Location.name.inflected())

gnc = gnc_relation()

LOCALITY = rule(
    and_(
        dictionary({
            'город',
            'деревня',
            'село',
        }),
        not_(
            or_(
                gram('Abbr'),
                gram('PREP'),
                gram('CONJ'),
                gram('PRCL'),
            ),
        ),
    ).optional(),
    and_(
        gram('ADJF'),
    ).match(gnc).optional(),
    and_(
        gram('Geox'),
        not_(
            or_(
                gram('Abbr'),
                gram('PREP'),
                gram('CONJ'),
                gram('PRCL'),
            ),
        ),
    ).match(gnc)
).interpretation(Location.name.inflected())

LOCATION = or_(
    REGION,
    FEDERAL_DISTRICT,
    AUTONOMOUS_DISTRICT,
    FEDERATION,
    ADJX_FEDERATION,
    STATE,
    LOCALITY,
).interpretation(Location)
