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
    dictionary({
        'центральный',
        'северо-западный',
        'южный',
        'северо-кавказский',
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

LOCATION = or_(
    REGION,
    FEDERAL_DISTRICT,
).interpretation(Location)
