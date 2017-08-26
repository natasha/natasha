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
]


@pytest.mark.parametrize('line', tests)
def test_extractor(extractor, line):
    matches = list(extractor(line))
    assert len(matches) == 1
    start, stop = matches[0].span
    assert line == line[start:stop]  # to see diff, not just spans
