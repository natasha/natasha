
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

#extends the functionality of YargyParser
#used for text parsing
class Parser(YargyParser):
    def __init__(self, rule, morph):
        # wraps pymorphy subclass
        # add methods check_gram, normalized
        # uses parse method that is cached
        morph = MorphAnalyzer(morph)

        tokenizer = MorphTokenizer(morph=morph)
        YargyParser.__init__(self, rule, tokenizer=tokenizer)

#inherits from local class Record
#represents a matching result from parsing text
class Match(Record):
    #start token, stop token, information to process
    __attributes__ = ['start', 'stop', 'fact']


def adapt_match(match):
    start, stop = match.span #start position, end position of text
    fact = match.fact.obj #parsed object or fact
    return Match(start, stop, fact)

#extracts information from match input and returns 'Match' object
class Extractor:
    #nitialized with a parsing rule and a morph parameter
    def __init__(self, rule, morph):
        self.parser = Parser(rule, morph)

    #iterates over matches found in input and yields them as Match objects
    def __call__(self, text):
        for match in self.parser.findall(text):
            yield adapt_match(match)

    #finds first match in input text and returns it as Match object
    def find(self, text):
        match = self.parser.find(text)
        if match:
            return adapt_match(match)

"""
SUBCLASSES OF EXTRACTOR THAT EXTRACT SPECIFIC TYPES OF INFORMATION
"""

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

"""
overrides the find method to extract address information
collects multiple matches, sorts them, and combines them into a single Match object representing an address
"""
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
