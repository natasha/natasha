
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


def append_sentinel(items, sentinel=None):
    for item in items:
        yield item
    yield sentinel


def envelop_spans(spans, envelopes):
    if not spans or not envelopes:
        return

    spans = append_sentinel(spans)
    span = next(spans)

    envelopes = append_sentinel(envelopes)
    envelope = next(envelopes)

    buffer = []
    while span and envelope:
        if span.start < envelope.start:
            span = next(spans)

        elif span.stop <= envelope.stop:
            buffer.append(span)
            span = next(spans)

        else:
            if buffer:
                yield buffer
                buffer = []
            envelope = next(envelopes)

    if buffer:
        yield buffer
