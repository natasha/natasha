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
        'публичное акционерное общество "Газпром"',
        Organisation(name='публичное акционерное общество "Газпром"'),
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
        Organisation(name='Кировский Механический Завод имени Ленина'),
    ],
    [
        'Московский государственный университет имени М.В.Ломоносова',
        Organisation(
            name='Московский государственный университет имени М.В.Ломоносова'
        ),
    ],
    [
        # TODO: группа с gent (кого/чего? петра великого)
        'Санкт-Петербургский политехнический университет Петра Великого',
        Organisation(name='Санкт-Петербургский политехнический университет'),
    ],
    [
        'Научно-исследовательский институт онкологии им. Н.Н. Петрова',
        Organisation(
            name='Научно-исследовательский институт онкологии им. Н.Н. Петрова'
        ),
    ],
    # # TODO:
    # [
    #     'НАЦИОНАЛЬНЫЙ МЕДИЦИНСКИЙ ИССЛЕДОВАТЕЛЬСКИЙ ЦЕНТР '
    #     'имени академика Н.Н. Петрова',
    #     Organisation(),
    # ],
    # [
    #     'Ленинградский институт методов и техники управления',
    #     Organisation(
    #         name='Ленинградский институт методов и техники управления'
    #     ),
    # ],
    [
        'агентство Reuters',
        Organisation(name='агентство Reuters'),
    ],
    [
        'компания Rambler&Co',
        Organisation(name='компания Rambler&Co')
    ],
    [
        'компания Standard Oil Co. Inc.',
        Organisation(name='компания Standard Oil Co. Inc')
    ],
    [
        'ООН',
        Organisation(name='ООН'),
    ],
    [
        'МИД России',
        Organisation(name='МИД России'),
    ],
    [
        'МВД Приморского района Петербурга',
        Organisation(name='МВД Приморского района Петербурга'),
    ],
    [
        'Авиакомпания "Аэрофлот"',
        Organisation(name='Авиакомпания "Аэрофлот"'),
    ],
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    text = test[0]
    etalon = test[1:]
    guess = [_.fact for _ in extractor(text)]
    assert guess == etalon
