# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import LocationExtractor
from natasha.grammars.location import Location


@pytest.fixture(scope='module')
def extractor():
    return LocationExtractor()

tests = [
    ['в Ярославской области', Location(name='ярославская область')],
    ['около красноярского края', Location(name='красноярский край')],
    ['события в северо-кавказском федеральном округе', Location(name='северо-кавказский федеральный округ')],
    ['Северо-западный ФО', Location(name='северо-западный фо')],
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    text = test[0]
    etalon = test[1:]
    guess = [_.fact for _ in extractor(text)]
    assert guess == etalon
