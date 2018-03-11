# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import MoneyRateExtractor


@pytest.fixture(scope='module')
def extractor():
    return MoneyRateExtractor()


tests = [
    ['2000 руб. / сутки', '2000 RUB/DAY'],
    ['2000 руб./смена', '2000 RUB/SHIFT'],
    ['2000 руб. в час', '2000 RUB/HOUR'],
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    line, etalon = test
    matches = list(extractor(line))
    assert len(matches) == 1
    fact = matches[0].fact
    guess = str(fact.normalized)
    assert guess == etalon
