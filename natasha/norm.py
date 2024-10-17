
from collections import defaultdict, deque

from .shape import recover_shape


PROPN = 'PROPN'
NOUN = 'NOUN'
ADJ = 'ADJ'
VERB = 'VERB'

GENDER = 'Gender'
NUMBER = 'Number'
CASE = 'Case'

NOM = 'Nom' #A constant representing the nominative case.

"""
two lists, words and tokens, and yields the result of applying the recover_shape function 
to each corresponding pair of elements in the two lists.
"""
def recover_shapes(words, tokens):
    for word, token in zip(words, tokens):
        yield recover_shape(word, token.text)

"""
takes two lists, words and tokens, and reconstructs a single string by inserting spaces 
according to the tokenization information in the tokens list.
"""
def recover_spaces(words, tokens):
    offset = None
    parts = []
    for index, (word, token) in enumerate(zip(words, tokens)):
        if index > 0:
            parts.append(' ' * (token.start - offset))
        parts.append(word)
        offset = token.stop
    return ''.join(parts)

#normalizes part-of-speech tags by converting "PROPN" to "NOUN."
def normal_pos(pos):
    if pos == PROPN:
        pos = NOUN
    return pos

"""
Compares two part-of-speech tags, a and b, after normalizing them using normal_pos. 
It checks if they match.
"""
def pos_match(a, b):
    return normal_pos(a) == normal_pos(b)

"""
Compares two feature dictionaries, a and b, to check if they match for gender, number, and case.
"""
def feats_match(a, b):
    return (
        a.get(GENDER) == b.get(GENDER)
        and a.get(NUMBER) == b.get(NUMBER)
        and a.get(CASE) == b.get(CASE)
    )

#Checks if a given form (presumably a word form), part of speech (pos), and feature dictionary (feats) match.
def form_match(form, pos, feats):
    return pos_match(form.pos, pos) and feats_match(form.feats, feats)

#Selects a suitable form from a list of forms based on part of speech and features.
def select_form(forms, pos, feats):
    for form in forms:
        if form_match(form, pos, feats):
            return form

#Normalizes a word by converting it to lowercase and replacing 'ё' with 'е'.
def normal_word(word):
    word = word.lower()
    return word.replace('ё', 'е')

#Inflects a word based on its part of speech and features.
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

"""
Inflects a list of tokens based on their part of speech and features. 
If ids are provided, it inflects only tokens with matching IDs.
"""
def inflect_words(vocab, tokens, ids=None):
    for token in tokens:
        if not ids or token.id in ids:
            yield inflect_word(vocab, token)
        else:
            yield token.text

"""
Selects tokens that can be inflected, 
typically those that are adjectives or verbs, by traversing the dependency tree.
"""
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

"""
It first selects inflectable tokens, inflects them, recovers their shapes, 
and reconstructs the spaces between words based on token information.
"""
def syntax_normalize(vocab, tokens):
    ids = set(select_inflectable(tokens))
    words = inflect_words(vocab, tokens, ids)
    words = recover_shapes(words, tokens)
    return recover_spaces(words, tokens)

"""
Applies a simpler form of normalization that doesn't consider inflection, 
only shape recovery, and space reconstruction.
"""
def normalize(vocab, tokens):
    words = inflect_words(vocab, tokens)
    words = recover_shapes(words, tokens)
    return recover_spaces(words, tokens)