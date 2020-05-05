
import pytest

from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,
)


@pytest.fixture(scope='session')
def segmenter():
    return Segmenter()


@pytest.fixture(scope='session')
def morph_vocab():
    return MorphVocab()


@pytest.fixture(scope='session')
def embedding():
    return NewsEmbedding()


@pytest.fixture(scope='session')
def morph_tagger(embedding):
    return NewsMorphTagger(embedding)


@pytest.fixture(scope='session')
def syntax_parser(embedding):
    return NewsSyntaxParser(embedding)


@pytest.fixture(scope='session')
def ner_tagger(embedding):
    return NewsNERTagger(embedding)


@pytest.fixture(scope='session')
def names_extractor(morph_vocab):
    return NamesExtractor(morph_vocab)


@pytest.fixture(scope='session')
def dates_extractor(morph_vocab):
    return DatesExtractor(morph_vocab)


@pytest.fixture(scope='session')
def money_extractor(morph_vocab):
    return MoneyExtractor(morph_vocab)


@pytest.fixture(scope='session')
def addr_extractor(morph_vocab):
    return AddrExtractor(morph_vocab)
