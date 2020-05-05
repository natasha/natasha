

from slovnet import NER as SlovnetNER

from ipymarkup import show_span_ascii_markup

from .data import NEWS_NER
from .record import Record
from .span import Span


#####
#
#   MARKUP
#
######


class NERMarkup(Record):
    __attributes__ = ['text', 'spans']

    def print(self):
        show_span_ascii_markup(self.text, self.spans)


def adapt_spans(spans):
    for span in spans:
        yield Span(span.start, span.stop, span.type)


def adapt_markup(markup):
    return NERMarkup(
        markup.text,
        list(adapt_spans(markup.spans))
    )


######
#
#   TAGGER
#
#########


class NERTagger(SlovnetNER):
    def __init__(self, emb, path):
        infer, *args = SlovnetNER.load(path)
        SlovnetNER.__init__(self, infer, *args)
        self.navec(emb)

    def map(self, items):
        markups = SlovnetNER.map(self, items)
        for markup in markups:
            yield adapt_markup(markup)


class NewsNERTagger(NERTagger):
    def __init__(self, emb, path=NEWS_NER):
        NERTagger.__init__(self, emb, path)
