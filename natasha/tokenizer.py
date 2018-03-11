# coding: utf-8
from __future__ import unicode_literals

from yargy.tokenizer import (
    MorphTokenizer,
    TagMorphTokenizer
)

from .crf import (
    CrfTagger,
    get_street_features,
    get_name_features
)
from .data import get_model_path


TOKENIZER = MorphTokenizer().remove_types('EOL')

NAME_TAGGER = CrfTagger(
    get_model_path('name.crf.json'),
    get_name_features
)
NAME_TOKENIZER = TagMorphTokenizer(
    NAME_TAGGER,
    TOKENIZER.rules,
    TOKENIZER.morph
)

STREET_TAGGER = CrfTagger(
    get_model_path('street.crf.json'),
    get_street_features
)
STREET_TOKENIZER = TagMorphTokenizer(
    STREET_TAGGER,
    TOKENIZER.rules,
    TOKENIZER.morph
)
