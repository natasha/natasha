# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import NamesExtractor
from natasha.grammars.name import Name


@pytest.fixture(scope='module')
def extractor():
    return NamesExtractor()


tests = [
    ['Мустафа Джемилев', Name(first='мустафа', last='джемилев')],
    ['Егору Свиридову', Name(first='егор', last='свиридов')],
    ['Ахмат-Хаджи Кадырова', Name(first='ахмат-хаджи', last='кадыров')],
    ['Стрыжак Алеся', Name(first='алеся', last='стрыжак')],
    ['владимир путин', Name(first='владимир', last='путин')],
    ['плаксюк саша', Name(first='саша', last='плаксюк')],

    ['М.С. Горбачевым', Name(first='М', last='горбачёв', middle='С')],
    ['О. Дерипаска', Name(first='О', last='дерипаск')],
    ['Ищенко Е.П.', Name(first='Е', last='ищенко', middle='П')],

    ['Фёдора Ивановича Шаляпина',
     Name(first='фёдор', last='шаляпин', middle='иванович')],
    ['Ипполит Матвеевич', Name(first='ипполит', middle='матвеевич')],

    ['Януковичем', Name(last='янукович')],
    ['Авраама', Name(first='авраам')],

    # TODO
    # ['Лев', Name(first='левый')]
    # ['ВОВ', None]
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    text = test[0]
    etalon = test[1:]
    guess = [_.fact for _ in extractor(text)]
    assert guess == etalon
