# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    and_, or_, not_,
    fact
)

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
    }),
).interpretation(Location.name.inflected())

gnc1 = gnc_relation()
gnc2 = gnc_relation()

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
    }).match(gnc1),
    or_(
        rule(
            dictionary({'федеральный'}).match(gnc1, gnc2),
            dictionary({'округ'}).match(gnc2),
        ),
        rule('ФО'),
    ),
).interpretation(Location.name.inflected())

gnc1 = gnc_relation()
gnc2 = gnc_relation()

AUTONOMOUS_DISTRICT = rule(
    gram('ADJF').match(gnc).repeatable(),
    or_(
        rule(
            dictionary({'автономный'}).match(gnc1, gnc2),
            dictionary({'округ'}).match(gnc2),
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

gnc1 = gnc_relation()
gnc2 = gnc_relation()

ADJX_FEDERATION = rule(
    or_(
        gram('Adjx'),
        gram('ADJF'),
    ).match(gnc1).repeatable(),
    dictionary({
        'штат',
        'эмират',
    }).match(gnc1),
    (
        gram('gent')
        .match(gnc2)
        .optional()
        .repeatable()
    ),
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
    or_(
        rule(
            dictionary({
                'город',
                'деревня',
                'село',
            }),
        ),
        rule(normalized('город'), '-', normalized('герой')),
        rule(
            or_(
                caseless('г'),
                caseless('д'),
                caseless('с'),
            ),
            eq('.'),
        ),
    ),
    gram('ADJF').match(gnc).optional(),
    or_(
        gram('NOUN'),
        gram('Geox'),
    ).match(gnc),
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
