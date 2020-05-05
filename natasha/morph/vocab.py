
from functools import lru_cache

from pymorphy2.analyzer import (
    Parse as PymorphyParse,
    MorphAnalyzer as PymorphyAnalyzer
)


# https://github.com/kmike/russian-tagsets/blob/master/russian_tagsets/ud.py
OC_UD_POS = {
    'ADJF': 'ADJ',
    'ADJS': 'ADJ',

    'ADVB': 'ADV',
    'COMP': 'ADV',

    'VERB': 'VERB',
    'GRND': 'VERB',
    'INFN': 'VERB',
    'PRTF': 'VERB',
    'PRTS': 'VERB',

    'NOUN': 'NOUN',
    'NPRO': 'PRON',

    'NUMR': 'NUM',
    'NUMB': 'NUM',

    'Apro': 'DET',
    'CONJ': 'CCONJ',
    'INTJ': 'INTJ',
    'PART': 'PRCL',
    'PNCT': 'PUNCT',
    'PRCL': 'PART',
    'PREP': 'ADP',
}

# ordering is importance, dups in OC_UD_INDEX, UD_OC_FEATS
OC_UD_FEATS = [
    ['Animacy', 'anim', 'Anim'],
    ['Animacy', 'inan', 'Inan'],

    ['Aspect', 'impf', 'Imp'],
    ['Aspect', 'perf', 'Perf'],

    ['Case', 'ablt', 'Ins'],
    ['Case', 'accs', 'Acc'],
    ['Case', 'datv', 'Dat'],
    ['Case', 'gent', 'Gen'],
    ['Case', 'gen1', 'Gen'],
    ['Case', 'gen2', 'Gen'],
    ['Case', 'loct', 'Loc'],
    ['Case', 'loc2', 'Loc'],
    ['Case', 'nomn', 'Nom'],
    ['Case', 'voct', 'Nom'],

    ['Degree', 'COMP', 'Cmp'],
    ['Degree', 'Supr', 'Sup'],

    ['Gender', 'femn', 'Fem'],
    ['Gender', 'masc', 'Masc'],
    ['Gender', 'neut', 'Neut'],

    ['Mood', 'impr', 'Imp'],
    ['Mood', 'indc', 'Ind'],

    ['Number', 'plur', 'Plur'],
    ['Number', 'sing', 'Sing'],

    ['NumForm', 'NUMB', 'Digit'],

    ['Person', '1per', '1'],
    ['Person', '2per', '2'],
    ['Person', '3per', '3'],
    ['Person', 'excl', '2'],
    ['Person', 'incl', '1'],

    ['Tense', 'futr', 'Fut'],
    ['Tense', 'past', 'Past'],
    ['Tense', 'pres', 'Pres'],

    ['Variant', 'ADJS', 'Brev'],
    ['Variant', 'PRTS', 'Brev'],

    ['VerbForm', 'GRND', 'Conv'],
    ['VerbForm', 'INFN', 'Inf'],
    ['VerbForm', 'PRTF', 'Part'],
    ['VerbForm', 'PRTS', 'Part'],
    ['VerbForm', 'VERB', 'Fin'],

    ['Voice', 'actv', 'Act'],
    ['Voice', 'pssv', 'Pass'],

    ['Abbr', 'Abbr', 'Yes'],
]

OC_UD_INDEX = {}
UD_OC_FEATS = {}

for key, oc, ud in OC_UD_FEATS:
    # the only duplicate is PRTS in VerbForm, Variant
    # use Variant
    OC_UD_INDEX[oc] = (key, ud)

    # many duplicates, use first accurance: 1 -> 1per, ADJ -> ADJF
    if ud not in UD_OC_FEATS:
        UD_OC_FEATS[ud] = oc


def ud_pos(tag):
    # super rare pos are missing: PRED, ROMN
    return OC_UD_POS.get(tag._POS, 'X')


def ud_feats(tag):
    # a number of OC grams are missing:
    # ANim Adjx Af-p Anph Anum Apro Arch Cmp2 Coll Coun Dist Dmns Fimp
    # Fixd GNdr Geox Impe Impx Infr Inmx Litr Ms-f Name Orgn Patr Pltm
    # Poss Prdx Prnt Qual Ques Sgtm Slng Subx Surn V-be V-bi V-ej V-ey
    # V-oy V-sh Vpre intg intr real tran

    for gram in tag._grammemes_tuple:
        item = OC_UD_INDEX.get(gram)
        if item:
            yield item


def oc_grams(grams):
    for gram in grams:
        yield UD_OC_FEATS[gram]


class MorphForm(PymorphyParse):
    def __new__(cls, *args):  # PymorphyParse is namedtuple
        self = PymorphyParse.__new__(cls, *args)

        self.normal = self.normal_form
        self.pos = ud_pos(self.tag)
        self.feats = dict(ud_feats(self.tag))
        return self

    def inflect(self, grams):
        grams = set(oc_grams(grams))
        return PymorphyParse.inflect(self, grams)

    def __repr__(self):
        return (
            '{name}(normal={self.normal!r}, '
            'pos={self.pos!r}, feats={self.feats!r})'
        ).format(
            name=self.__class__.__name__,
            self=self
        )


CACHE_SIZE = 10000


class MorphVocab(PymorphyAnalyzer):
    def __init__(self):
        PymorphyAnalyzer.__init__(self, result_type=MorphForm)

    parse = lru_cache(CACHE_SIZE)(PymorphyAnalyzer.parse)
    __call__ = parse

    def __repr__(self):
        return '%s()' % self.__class__.__name__

    def lemmatize(self, word, pos, feats):
        from .lemma import lemmatize

        return lemmatize(self, word, pos, feats)
