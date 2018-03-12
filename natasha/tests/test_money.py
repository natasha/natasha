# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import MoneyExtractor


@pytest.fixture(scope='module')
def extractor():
    return MoneyExtractor()


tests = [
    [
        '1 599 059, 38 Евро',
        '1599059.38 EUR'
    ],
    [
        '2 134 472,44 рубля',
        '2134472.44 RUB'
    ],
    [
        '420 долларов',
        '420 USD'
    ],
    [
        '20 млн руб',
        '20000000 RUB'],
    [
        '20 000 долларов',
        '20000 USD'
    ],
    [
        '2,2 млн.руб.',
        '2020000.0 RUB'
    ],
    [
        '20 тыс руб',
        '20000 RUB'
    ],
    [
        '20 т. р.',
        '20000 RUB'
    ],
    [
        '2 200 000 руб.',
        '2200000 RUB'
    ],
    [
        '20.000 руб.',
        '20000 RUB'
    ],
    [
        '20,000 руб',
        '20000 RUB'
    ],
    [
        '20,00 руб',
        '20 RUB'
    ],
    [
        '124 451 рубль 50 копеек',
        '124451.5 RUB',
    ],
    [
        ('881 913 (Восемьсот восемьдесят одна '
         'тысяча девятьсот тринадцать) руб. 98 коп.'),
        '881913.98 RUB'
    ]
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    line, etalon = test
    matches = list(extractor(line))
    assert len(matches) == 1
    fact = matches[0].fact
    guess = str(fact.normalized)
    assert guess == etalon
