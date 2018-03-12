# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import SimpleNamesExtractor
from natasha.grammars.name import Name


@pytest.fixture(scope='module')
def extractor():
    return SimpleNamesExtractor()


tests = [
    ['Мустафа Джемилев', Name(first='мустафа', last='джемилев')],
    ['Егору Свиридову', Name(first='егор', last='свиридов')],
    ['Стрыжак Алеся', Name(first='алеся', last='стрыжак')],
    ['владимир путин', Name(first='владимир', last='путин')],
    ['плаксюк саша', Name(first='саша', last='плаксюк')],

    ['О. Дерипаска', Name(first='О', last='дерипаск')],
    ['Ищенко Е.П.', Name(first='Е', last='ищенко', middle='П')],

    ['Фёдора Ивановича Шаляпина',
     Name(first='фёдор', last='шаляпин', middle='иванович')],
    ['Ипполит Матвеевич', Name(first='ипполит', middle='матвеевич')],

    ['Януковичем', Name(last='янукович')],
    ['Авраама', Name(first='авраам')],
    ['Гоша Куценко', Name(first='гоша', last='куценко')],
    [
        'Юрий Георгиевич Куценко',
        Name(first='юрий', last='куценко', middle='георгиевич'),
    ],
    ['Наталья Ищенко', Name(first='наталья', last='ищенко')],
    [
        'Наталья Сергеевна Ищенко',
        Name(first='наталья', last='ищенко', middle='сергеевна'),
    ],
    [
        'МОНИНОЙ Нине Гафуровне',
        Name(first='нина', last='монина', middle='гафуровна')
    ],
    [
        'АЗЫЕВОЙ ГАЛИНЕ АЛЕКСАНДРОВНЕ',
        Name(first='галина', last='азыева', middle='александровна')
    ],
    [
        'В. И. Ленин',
        Name(first='В', last='ленин', middle='И', nick=None),
    ],

    # TODO
    # С одной версией словарей получается горбачёв, с другой горбачев
    # ['М.С. Горбачевым', Name(first='М', last='горбачёв', middle='С')],

    # ['Ахмат-Хаджи Кадырова', Name(first='ахмат-хаджи', last='кадыров')],
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    text = test[0]
    etalon = test[1:]
    guess = [_.fact for _ in extractor(text)]
    assert guess == etalon
