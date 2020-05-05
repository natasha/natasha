
from slovnet import Morph as SlovnetMorph

from natasha.data import NEWS_MORPH
from natasha.record import Record


###########
#
#   MARKUP
#
#######


class MorphToken(Record):
    __attributes__ = ['text', 'pos', 'feats']


class MorphMarkup(Record):
    __attributes__ = ['tokens']

    def print(self):
        print_markup(self)


def adapt_tokens(tokens):
    for token in tokens:
        yield MorphToken(token.text, token.pos, token.feats)


def adapt_markup(markup):
    return MorphMarkup(
        list(adapt_tokens(markup.tokens))
    )


def format_tag(pos, feats):
    if not feats:
        return pos

    feats = '|'.join(
        '%s=%s' % (_, feats[_])
        for _ in sorted(feats)
    )
    return '%s|%s' % (pos, feats)


def format_markup(markup, size=20):
    for token in markup.tokens:
        word = token.text.rjust(size)
        tag = format_tag(token.pos, token.feats)
        yield '%s %s' % (word, tag)


def print_markup(markup):
    for line in format_markup(markup):
        print(line)


##########
#
#   TAGGER
#
#######


class MorphTagger(SlovnetMorph):
    def __init__(self, emb, path):
        infer, *args = SlovnetMorph.load(path)
        SlovnetMorph.__init__(self, infer, *args)
        self.navec(emb)

    def map(self, items):
        markups = SlovnetMorph.map(self, items)
        for markup in markups:
            yield adapt_markup(markup)


class NewsMorphTagger(MorphTagger):
    def __init__(self, emb, path=NEWS_MORPH):
        MorphTagger.__init__(self, emb, path)
