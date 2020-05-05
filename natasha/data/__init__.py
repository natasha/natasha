
from os.path import join, dirname


DATA_DIR = dirname(__file__)
DICT_DIR = join(DATA_DIR, 'dict')
MODEL_DIR = join(DATA_DIR, 'model')
EMB_DIR = join(DATA_DIR, 'emb')

FIRST = join(DICT_DIR, 'first.txt')
LAST = join(DICT_DIR, 'last.txt')
MAYBE_FIRST = join(DICT_DIR, 'maybe_first.txt')

NEWS_EMBEDDING = join(EMB_DIR, 'navec_news_v1_1B_250K_300d_100q.tar')

NEWS_MORPH = join(MODEL_DIR, 'slovnet_morph_news_v1.tar')
NEWS_NER = join(MODEL_DIR, 'slovnet_ner_news_v1.tar')
NEWS_SYNTAX = join(MODEL_DIR, 'slovnet_syntax_news_v1.tar')


def load_dict(path):
    with open(path, encoding='utf8') as file:
        for line in file:
            index = line.find('#')
            if index > 0:
                line = line[:index]
            yield line.rstrip()
