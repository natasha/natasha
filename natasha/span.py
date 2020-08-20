
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


def envelop_spans(spans, envelopes):
    index = 0
    for envelope in envelopes:
        chunk = []
        while index < len(spans):
            span = spans[index]
            index += 1
            if span.start < envelope.start:
                continue
            elif span.stop <= envelope.stop:
                chunk.append(span)
            else:
                index -= 1
                break
        yield chunk
