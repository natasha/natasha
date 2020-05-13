
from .const import ORG
from .record import Record
from .obj import Slot
from .span import envelop_spans
from .norm import normalize, syntax_normalize


class Record(Record):
    def __repr__(self):
        return compact_repr(self)

    def _repr_pretty_(self, printer, cycle):
        printer.text(repr(self))


class DocToken(Record):
    __attributes__ = ['start', 'stop', 'text',
                      'id', 'head_id', 'rel',
                      'pos', 'feats', 'lemma']

    def __init__(self, start, stop, text,
                 id=None, head_id=None, rel=None,
                 pos=None, feats=None, lemma=None):
        self.start = start
        self.stop = stop
        self.text = text

        self.id = id
        self.head_id = head_id
        self.rel = rel

        self.pos = pos
        self.feats = feats
        self.lemma = lemma

    def lemmatize(self, vocab):
        self.lemma = vocab.lemmatize(self.text, self.pos, self.feats)


class DocFact(Record):
    __attributes__ = ['slots']
    __annotations__ = {
        'slots': [Slot]
    }

    @property
    def as_dict(self):
        return {
            key: value
            for key, value in self.slots
        }


class DocSpan(Record):
    __attributes__ = ['start', 'stop', 'type', 'text',
                      'tokens', 'normal', 'fact']
    __annotations__ = {
        'tokens': [DocToken],
        'fact': DocFact
    }

    def __init__(self, start, stop, type, text,
                 tokens=None, normal=None, fact=None):
        self.start = start
        self.stop = stop
        self.type = type
        self.text = text

        self.tokens = tokens
        self.normal = normal
        self.fact = fact

    def normalize(self, vocab):
        method = (
            syntax_normalize
            if self.type == ORG
            else normalize
        )
        self.normal = method(vocab, self.tokens)

    def extract_fact(self, extractor):
        match = extractor.find(self.normal)
        if match:
            slots = list(match.fact.slots)
            self.fact = DocFact(slots)


class DocSent(Record):
    __attributes__ = ['start', 'stop', 'text', 'tokens', 'spans']
    __annotations__ = {
        'tokens': [DocToken],
        'spans': [DocSpan]
    }

    def __init__(self, start, stop, text,
                 tokens=None, spans=None):
        self.start = start
        self.stop = stop
        self.text = text

        self.tokens = tokens
        self.spans = spans

    @property
    def morph(self):
        return morph_markup(self.tokens)

    @property
    def syntax(self):
        return syntax_markup(self.tokens)

    @property
    def ner(self):
        return ner_markup(self.text, self.spans, -self.start)


class Doc(Record):
    __attributes__ = ['text', 'tokens', 'spans', 'sents']
    __annotations__ = {
        'tokens': [DocToken],
        'spans': [DocSpan],
        'sents': [DocSent]
    }

    def __init__(self, text, tokens=None, spans=None, sents=None):
        self.text = text
        self.tokens = tokens
        self.spans = spans
        self.sents = sents

    def segment(self, segmenter):
        segment_doc(self, segmenter)

    def tag_morph(self, tagger):
        tag_morph_doc(self, tagger)

    def parse_syntax(self, parser):
        parse_syntax_doc(self, parser)

    def tag_ner(self, tagger):
        tag_ner_doc(self, tagger)

    @property
    def morph(self):
        return morph_markup(self.tokens)

    @property
    def syntax(self):
        return syntax_markup(self.tokens)

    @property
    def ner(self):
        return ner_markup(self.text, self.spans)

    def envelop_span_tokens(self):
        envelop_span_tokens(self.tokens, self.spans)

    def envelop_sent_spans(self):
        envelop_sent_spans(self.spans, self.sents)

    def envelop_sent_tokens(self):
        envelop_sent_tokens(self.tokens, self.sents)

    def clear_envelopes(self):
        clear_envelopes(self)


#######
#
#  SEGMENT
#
#######


def adapt_token(token):
    start, stop, text = token
    return DocToken(start, stop, text)


def adapt_sent(sent):
    start, stop, text = sent
    return DocSent(start, stop, text)


def segment_doc(doc, segmenter):
    doc.tokens = [adapt_token(_) for _ in segmenter.tokenize(doc.text)]
    doc.sents = [adapt_sent(_) for _ in segmenter.sentenize(doc.text)]
    doc.envelop_sent_tokens()


#######
#
#  MORPH
#
####


def sent_words(sent):
    return [_.text for _ in sent.tokens]


def inject_morph(targets, sources):
    for target, source in zip(targets, sources):
        target.pos = source.pos
        target.feats = source.feats


def tag_morph_doc(doc, tagger):
    chunk = [sent_words(_) for _ in doc.sents]
    markups = tagger.map(chunk)
    for sent, markup in zip(doc.sents, markups):
        inject_morph(sent.tokens, markup.tokens)


#######
#
#  SYNTAX
#
######


def offset_syntax(sent_id, tokens):
    for token in tokens:
        token.id = '%s_%s' % (sent_id, token.id)
        token.head_id = '%s_%s' % (sent_id, token.head_id)


def inject_syntax(targets, sources):
    for target, source in zip(targets, sources):
        target.id = source.id
        target.head_id = source.head_id
        target.rel = source.rel


def parse_syntax_doc(doc, parser):
    chunk = [sent_words(_) for _ in doc.sents]
    markups = parser.map(chunk)
    for sent_id, (sent, markup) in enumerate(zip(doc.sents, markups), 1):
        inject_syntax(sent.tokens, markup.tokens)
        offset_syntax(sent_id, sent.tokens)


#########
#
#   NER
#
######


def adapt_spans(doc, spans):
    for start, stop, type in spans:
        text = doc.text[start:stop]
        yield DocSpan(start, stop, type, text)


def tag_ner_doc(doc, tagger):
    if not doc.text.strip():
        doc.spans = []
        return

    markup = tagger(doc.text)
    doc.spans = list(adapt_spans(doc, markup.spans))

    doc.envelop_span_tokens()
    doc.envelop_sent_spans()


######
#
#   ENVELOP
#
#####


def envelop_span_tokens(tokens, spans):
    groups = envelop_spans(tokens, spans)
    for group, span in zip(groups, spans):
        span.tokens = group


def envelop_sent_tokens(tokens, sents):
    groups = envelop_spans(tokens, sents)
    for group, sent in zip(groups, sents):
        sent.tokens = group


def envelop_sent_spans(spans, sents):
    groups = envelop_spans(spans, sents)
    for group, sent in zip(groups, sents):
        sent.spans = group


def clear_envelopes(doc):
    if doc.sents:
        for sent in doc.sents:
            sent.tokens = None
            sent.spans = None

    if doc.spans:
        for span in doc.spans:
            span.tokens = None


#####
#
#   MARKUP
#
######


def morph_markup(tokens):
    from .morph.tagger import adapt_tokens, MorphMarkup

    tokens = list(adapt_tokens(tokens))
    return MorphMarkup(tokens)


def syntax_markup(tokens):
    from .syntax import adapt_tokens, SyntaxMarkup

    tokens = list(adapt_tokens(tokens))
    return SyntaxMarkup(tokens)


def ner_markup(text, spans, offset=0):
    from .span import adapt_spans, offset_spans
    from .ner import NERMarkup

    spans = adapt_spans(spans)
    spans = list(offset_spans(spans, offset))
    return NERMarkup(text, spans)


#######
#
#   REPR
#
######


FEATS = 'feats'


def format_feats(feats):
    values = (feats[_] for _ in sorted(feats))
    return '<%s>' % ','.join(values)


def capped_str(value, cap=50):
    if len(value) <= cap:
        return value
    return value[:cap] + '...'


HIDE_LIST = '[...]'


def compact_repr(record):
    parts = []
    for key in record.__attributes__:
        value = getattr(record, key)
        if not value:
            continue

        if isinstance(value, list):
            value = HIDE_LIST
        elif key == FEATS:
            value = format_feats(value)
        else:
            value = repr(value)

        value = capped_str(value)
        parts.append('%s=%s' % (key, value))

    return '%s(%s)' % (record.__class__.__name__, ', '.join(parts))
