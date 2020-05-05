
from slovnet import Syntax as SlovnetSyntax

from ipymarkup import show_dep_ascii_markup

from .data import NEWS_SYNTAX
from .record import Record


########
#
#   MARKUP
#
######


class SyntaxToken(Record):
    __attributes__ = ['id', 'text', 'head_id', 'rel']


class SyntaxMarkup(Record):
    __attributes__ = ['tokens']

    def print(self):
        print_markup(self)


def adapt_tokens(tokens):
    for token in tokens:
        yield SyntaxToken(
            token.id, token.text,
            token.head_id, token.rel
        )


def adapt_markup(markup):
    return SyntaxMarkup(
        list(adapt_tokens(markup.tokens))
    )


def token_deps(tokens):
    ids = {}
    for index, token in enumerate(tokens):
        ids[token.id] = index

    for token in tokens:
        source = ids.get(token.head_id)
        target = ids[token.id]
        if source and source != target:  # skip root, loop
            yield source, target, token.rel


def markup_words(markup):
    return [_.text for _ in markup.tokens]


def print_markup(markup):
    words = markup_words(markup)
    deps = token_deps(markup.tokens)
    show_dep_ascii_markup(words, deps)


######
#
#   PARSER
#
#######


class SyntaxParser(SlovnetSyntax):
    def __init__(self, emb, path):
        infer, *args = SlovnetSyntax.load(path)
        SlovnetSyntax.__init__(self, infer, *args)
        self.navec(emb)

    def map(self, items):
        markups = SlovnetSyntax.map(self, items)
        for markup in markups:
            yield adapt_markup(markup)


class NewsSyntaxParser(SyntaxParser):
    def __init__(self, emb, path=NEWS_SYNTAX):
        SyntaxParser.__init__(self, emb, path)
