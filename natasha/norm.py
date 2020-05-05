
from collections import defaultdict, deque

from .shape import recover_shape


PROPN = 'PROPN'
NOUN = 'NOUN'
ADJ = 'ADJ'
VERB = 'VERB'

GENDER = 'Gender'
NUMBER = 'Number'
CASE = 'Case'

NOM = 'Nom'


def recover_shapes(words, tokens):
    for word, token in zip(words, tokens):
        yield recover_shape(word, token.text)


def recover_spaces(words, tokens):
    offset = None
    parts = []
    for index, (word, token) in enumerate(zip(words, tokens)):
        if index > 0:
            parts.append(' ' * (token.start - offset))
        parts.append(word)
        offset = token.stop
    return ''.join(parts)


def normal_pos(pos):
    if pos == PROPN:
        pos = NOUN
    return pos


def pos_match(a, b):
    return normal_pos(a) == normal_pos(b)


def feats_match(a, b):
    return (
        a.get(GENDER) == b.get(GENDER)
        and a.get(NUMBER) == b.get(NUMBER)
        and a.get(CASE) == b.get(CASE)
    )


def form_match(form, pos, feats):
    return pos_match(form.pos, pos) and feats_match(form.feats, feats)


def select_form(forms, pos, feats):
    for form in forms:
        if form_match(form, pos, feats):
            return form


def normal_word(word):
    word = word.lower()
    return word.replace('ё', 'е')


def inflect_word(vocab, token):
    word, pos, feats = token.text, token.pos, token.feats
    word = normal_word(word)

    if pos not in (PROPN, NOUN, ADJ, VERB):
        return word

    if feats.get(CASE) == NOM:
        return word

    forms = vocab(word)
    form = select_form(forms, pos, feats)
    if form:
        form = form.inflect({NOM})
        if form:
            return normal_word(form.word)

    return word


def inflect_words(vocab, tokens, ids=None):
    for token in tokens:
        if not ids or token.id in ids:
            yield inflect_word(vocab, token)
        else:
            yield token.text


def select_inflectable(tokens):
    index = {}
    for token in tokens:
        index[token.id] = token

    roots = set()
    children = defaultdict(list)
    for token in tokens:
        if token.head_id not in index:
            roots.add(token.id)
        else:
            children[token.head_id].append(token.id)

    stack = deque(roots)
    while stack:
        id = stack.popleft()
        yield id
        for child in children[id]:
            token = index[child]
            if token.pos in (ADJ, VERB):
                stack.append(child)


def syntax_normalize(vocab, tokens):
    ids = set(select_inflectable(tokens))
    words = inflect_words(vocab, tokens, ids)
    words = recover_shapes(words, tokens)
    return recover_spaces(words, tokens)


def normalize(vocab, tokens):
    words = inflect_words(vocab, tokens)
    words = recover_shapes(words, tokens)
    return recover_spaces(words, tokens)
