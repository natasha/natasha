# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import DatesExtractor


@pytest.fixture(scope='module')
def extractor():
    return DatesExtractor()


tests = [
    '24.01.2017',
    '27. 05.2008',
    '2015 год',
    '2014 г',
    '1 апреля',
    'май 2017 г.',
    '9 мая 2017 года',
]


@pytest.mark.parametrize('line', tests)
def test_extractor(extractor, line):
    matches = list(extractor(line))
    assert len(matches) == 1
    start, stop = matches[0].span
    assert line == line[start:stop]  # to see diff, not just spans
