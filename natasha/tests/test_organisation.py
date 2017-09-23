# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import OrganisationExtractor
from natasha.grammars.organisation import Organisation


@pytest.fixture(scope='module')
def extractor():
    return OrganisationExtractor()

tests = [
    [
        'ПАО «Газпром»',
        Organisation(name='ПАО «Газпром»'),
    ],
    [
        'историческое общество "Мемориал"',
        Organisation(name='историческое общество "Мемориал"'),
    ],
    [
        'коммерческое производственное объединение "Вектор"',
        Organisation(name='коммерческое производственное объединение "Вектор"')
    ],
    [
        'Международное историко-просветительское, правозащитное'
        ' и благотворительное общество «Мемориал»',
        Organisation(
            name='Международное историко-просветительское, '
                 'правозащитное и благотворительное общество «Мемориал»'
        ),
    ],
    [
        'правозащитный центр «Мемориал»',
        Organisation(name='правозащитный центр «Мемориал»'),
    ],
    [
        'Кировский завод',
        Organisation(name='Кировский завод'),
    ],
    [
        # TODO: нормализация
        'Кировский Механический Завод имени Ленина',
        Organisation(name='Кировский Механический Завод имени ленин'),
    ],
    [
        # TODO: группа с gent (кого/чего? петра великого)
        'Санкт-Петербургский политехнический университет Петра Великого',
        Organisation(name='Санкт-Петербургский политехнический университет'),
    ],
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    text = test[0]
    etalon = test[1:]
    guess = [_.fact for _ in extractor(text)]
    assert guess == etalon
