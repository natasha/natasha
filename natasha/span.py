
from intervaltree import IntervalTree

from .record import Record


class Span(Record):
    __attributes__ = ['start', 'stop', 'type']


def adapt_spans(spans):
    for span in spans:
        yield Span(span.start, span.stop, span.type)


def offset_spans(spans, offset):
    for span in spans:
        yield Span(
            offset + span.start,
            offset + span.stop,
            span.type
        )


def index_spans(spans):
    index = IntervalTree()
    for span in spans:
        index.addi(span.start, span.stop, span)
    return index


def query_spans_index(index, span):
    return [
        _.data
        for _ in sorted(index.envelop(span.start, span.stop))
    ]
