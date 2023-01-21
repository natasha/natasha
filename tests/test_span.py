
import pytest

from natasha.span import (
    Span,
    envelop_spans
)


tests = [
    [
        [(0, 1)],
        [],
        []
    ],
    [
        [],
        [(0, 1)],
        [[]]
    ],
    [
        [(0, 1), (1, 2)],
        [(1, 2)],
        [[(1, 2)]]
    ],
    [
        [(0, 1), (1, 2)],
        [(0, 1)],
        [[(0, 1)]]
    ],
    [
        [(0, 1), (1, 2)],
        [(0, 1), (1, 2)],
        [[(0, 1)], [(1, 2)]]
    ],
]


def adapt_spans(spans):
    for start, stop in spans:
        yield Span(start, stop, type=None)


@pytest.mark.parametrize('test', tests)
def test_envelope_spans(test):
    spans, envelopes, target = test
    spans = list(adapt_spans(spans))
    envelopes = list(adapt_spans(envelopes))
    target = [
        list(adapt_spans(group))
        for group in target
    ]
    pred = list(envelop_spans(spans, envelopes))
    assert pred == target
