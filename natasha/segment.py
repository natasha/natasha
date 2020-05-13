
from razdel import sentenize, tokenize

from .record import Record


class Sent(Record):
    __attributes__ = ['start', 'stop', 'text']


class Token(Record):
    __attributes__ = ['start', 'stop', 'text']


def adapt_token(token):
    start, stop, text = token
    return Token(start, stop, text)


def adapt_sent(sent):
    start, stop, text = sent
    return Sent(start, stop, text)


class Segmenter(Record):
    def tokenize(self, text):
        for token in tokenize(text):
            yield adapt_token(token)

    def sentenize(self, text):
        if not text:
            return  # razdel return empty sent

        for sent in sentenize(text):
            yield adapt_sent(sent)
