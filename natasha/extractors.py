# coding: utf-8
from __future__ import unicode_literals

from collections import OrderedDict

from yargy import Parser

from .utils import Record
from .preprocess import normalize_text
from .markup import format_markup

from .grammars.name import NAME
from .grammars.date import DATE
from .grammars.money import MONEY
from .grammars.location import LOCATION
from .grammars.address import ADDRESS, ComplexGorodPipeline
from .grammars.organisation import ORGANISATION, OrganisationTypePipeline
from .grammars.person import PERSON, PositionsPipeline


def serialize(match):
    span = match.span
    fact = match.fact
    type = fact.__class__.__name__
    return OrderedDict([
        ('type', type),
        ('fact', fact.as_json),
        ('span', span),
    ])


class Matches(Record):
    __attributes__ = ['text', 'matches']

    def __init__(self, text, matches):
        self.text = text
        self.matches = sorted(matches, key=lambda _: _.span)

    def __iter__(self):
        return iter(self.matches)

    def __getitem__(self, index):
        return self.matches[index]

    def __len__(self):
        return len(self.matches)

    def __bool__(self):
        return bool(self.matches)

    @property
    def as_json(self):
        return [serialize(_) for _ in self.matches]

    def _repr_html_(self):
        spans = [_.span for _ in self.matches]
        return ''.join(format_markup(self.text, spans))


class Extractor(Record):
    __attributes__ = ['parser']

    def __init__(self, rule, pipelines=()):
        self.parser = Parser(rule, pipelines=pipelines)

    def __call__(self, text):
        text = normalize_text(text)
        matches = self.parser.findall(text)
        return Matches(text, matches)


class NamesExtractor(Extractor):
    def __init__(self):
        super(NamesExtractor, self).__init__(NAME)


class DatesExtractor(Extractor):
    def __init__(self):
        super(DatesExtractor, self).__init__(DATE)


class MoneyExtractor(Extractor):
    def __init__(self):
        super(MoneyExtractor, self).__init__(MONEY)


class LocationExtractor(Extractor):
    def __init__(self):
        super(LocationExtractor, self).__init__(LOCATION)


class AddressExtractor(Extractor):
    def __init__(self):
        super(AddressExtractor, self).__init__(
            ADDRESS,
            [ComplexGorodPipeline()]
        )


class OrganisationExtractor(Extractor):
    def __init__(self):
        super(OrganisationExtractor, self).__init__(
            ORGANISATION,
            [OrganisationTypePipeline()]
        )


class PersonExtractor(Extractor):
    def __init__(self):
        super(PersonExtractor, self).__init__(
            PERSON,
            [PositionsPipeline()]
        )
