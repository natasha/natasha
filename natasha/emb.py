
from navec import Navec

from .data import NEWS_EMBEDDING


class Embedding(Navec):
    def __init__(self, path):
        meta, vocab, pq = Navec.load(path)
        Navec.__init__(self, meta, vocab, pq)


class NewsEmbedding(Embedding):
    def __init__(self, path=NEWS_EMBEDDING):
        Embedding.__init__(self, path)
