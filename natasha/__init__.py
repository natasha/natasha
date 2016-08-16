from copy import copy
from collections import deque

from yargy import FactParser

from natasha.grammars import Person, Geo, Money, Date


class Combinator(object):

    DEFAULT_GRAMMARS = [
        Money,
        Person,
        Geo,
        Date,
    ]

    def __init__(self, grammars=None, cache_size=50000):
        self.grammars = grammars or self.DEFAULT_GRAMMARS
        self.parser = FactParser(cache_size=cache_size)

    def extract(self, text):
        tokens = deque(self.parser.tokenizer.transform(text))
        for grammar in self.grammars:
            for grammar_type, rule in grammar.__members__.items():
                for match in self.parser.extract(copy(tokens), rule.value):
                    yield (grammar, grammar_type, match)
