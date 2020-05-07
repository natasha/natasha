
from yargy import Parser as YargyParser
from yargy.morph import MorphAnalyzer
from yargy.tokenizer import MorphTokenizer

from .record import Record
from . import obj


#######
#
#   EXTRACTOR
#
######


class Parser(YargyParser):
    def __init__(self, rule, morph):
        # wraps pymorphy subclass
        # add methods check_gram, normalized
        # uses parse method that is cached
        morph = MorphAnalyzer(morph)

        tokenizer = MorphTokenizer(morph=morph)
        YargyParser.__init__(self, rule, tokenizer=tokenizer)


class Match(Record):
    __attributes__ = ['start', 'stop', 'fact']


def adapt_match(match):
    start, stop = match.span
    fact = match.fact.obj
    return Match(start, stop, fact)


class Extractor:
    def __init__(self, rule, morph):
        self.parser = Parser(rule, morph)

    def __call__(self, text):
        for match in self.parser.findall(text):
            yield adapt_match(match)

    def find(self, text):
        match = self.parser.find(text)
        if match:
            return adapt_match(match)


class NamesExtractor(Extractor):
    def __init__(self, morph):
        from .grammars.name import NAME
        Extractor.__init__(self, NAME, morph)


class DatesExtractor(Extractor):
    def __init__(self, morph):
        from .grammars.date import DATE
        Extractor.__init__(self, DATE, morph)


class MoneyExtractor(Extractor):
    def __init__(self, morph):
        from .grammars.money import MONEY
        Extractor.__init__(self, MONEY, morph)


class AddrExtractor(Extractor):
    def __init__(self, morph):
        from .grammars.addr import ADDR_PART
        Extractor.__init__(self, ADDR_PART, morph)

    def find(self, text):
        matches = list(self(text))
        if not matches:
            return

        matches = sorted(matches, key=lambda _: _.start)
        start = matches[0].start
        stop = matches[-1].stop
        parts = [_.fact for _ in matches]
        return Match(start, stop, obj.Addr(parts))
