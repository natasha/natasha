# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import MoneyRangeExtractor


@pytest.fixture(scope='module')
def extractor():
    return MoneyRangeExtractor()


tests = [
    [
        '20000-30000 рублей',
        '20000 RUB-30000 RUB'
    ],
    [
        'от 80 тысяч до 2 миллионов рублей',
        '80000 RUB-2000000 RUB'
    ],
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    line, etalon = test
    matches = list(extractor(line))
    assert len(matches) == 1
    fact = matches[0].fact
    guess = str(fact.normalized)
    assert guess == etalon
