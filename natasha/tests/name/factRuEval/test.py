
import os
import json

import pytest

from natasha import NamesExtractor
from natasha.utils import Record


class Token(Record):
    __attributes__ = ['value', 'start', 'stop']

    def __init__(self, value, start, stop):
        self.value = value
        self.start = start
        self.stop = stop


def load_json(path):
    with open(path) as file:
        return json.load(file)


def load_tests():
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'tests.json')
    data = load_json(path)
    for line, items in data:
        tokens = [
            Token(value, start, stop)
            for value, start, stop in items
        ]
        yield line, tokens


@pytest.fixture(scope='module')
def extractor():
    return NamesExtractor()


tests = list(load_tests())


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    line, etalon = test
    spans = [_.span for _ in extractor(line)]
    guess = [
        Token(line[start:stop], start, stop)
        for start, stop in spans
    ]
    assert guess == etalon
