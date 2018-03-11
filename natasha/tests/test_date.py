# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import DatesExtractor
from natasha.grammars.date import Date


@pytest.fixture(scope='module')
def extractor():
    return DatesExtractor()


tests = [
    [
        '24.01.2017',
        Date(
            year=2017,
            month=1,
            day=24
        )
    ],
    [
        '27. 05.99',
        Date(
            year=1999,
            month=5,
            day=27
        )
    ],
    [
        '2015 год',
        Date(year=2015)
    ],
    [
        '2014 г',
        Date(year=2014)
    ],
    [
        '1 апреля',
        Date(
            month=4,
            day=1
        )
    ],
    [
        'май 2017 г.',
        Date(
            year=2017,
            month=5
        )
    ],
    [
        '9 мая 2017 года',
        Date(
            year=2017,
            month=5,
            day=9
        )
    ]
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    line, etalon = test
    matches = list(extractor(line))
    assert len(matches) == 1
    guess = matches[0].fact
    assert guess == etalon
