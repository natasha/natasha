# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import MoneyExtractor


@pytest.fixture(scope='module')
def extractor():
    return MoneyExtractor()


tests = [
    '1 599 059, 38 Евро',
    '2 134 472,44 рубля',
    '420 долларов',
    '20 млн',
    '20 000',
    '2,2 млн.руб.',
    '20000',
    '20000-30000',
    '20000-30000 рублей',
    '30-40 тысяч рублей',
    'от 20 до 30 тысяч рублей',
    'от 20.1233 до 30,12312 тысяч рублей',
    'от 80 тысяч до 2 миллионов рублей',
    '2 200 000 руб.',
    '20 тыс',
    '20 т',
    '20.000 руб.',
    '20,000 руб',
    '2000 руб./сутки',
    '2000 руб./смена',
    '2000 руб./час',
    '20-30 руб./сутки',
    'от 2 млн руб в смену'
]


@pytest.mark.parametrize('line', tests)
def test_extractor(extractor, line):
    matches = list(extractor(line))
    assert len(matches) == 1
    start, stop = matches[0].span
    assert line == line[start:stop]  # to see diff, not just spans
