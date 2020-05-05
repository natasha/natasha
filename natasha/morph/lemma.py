

def normal_word(word):
    word = word.lower()
    return word.replace('ё', 'е')


NORMAL_POSES = {
    'PROPN': 'NOUN',
    'AUX': 'VERB',  # был
    'SCONJ': 'CCONJ'
}


def normal_pos(pos):
    return NORMAL_POSES.get(pos, pos)


def pos_sim(a, b):
    return normal_pos(a) == normal_pos(b)


# ignore Animacy, Voice, ...
FEATS = {
    'Case', 'Gender', 'Number',
    'Aspect', 'NumForm', 'Person', 'Tense', 'Variant'
}


def feats_sim(a, b):
    return sum(
        a[_] == b[_]
        for _ in a.keys() & b.keys()
        if _ in FEATS
    )


def grams_sim(a_pos, a_feats, b_pos, b_feats):
    return pos_sim(a_pos, b_pos) + feats_sim(a_feats, b_feats)


def best_form(forms, pos, feats):
    max, best = 0, None
    for form in forms:
        if form.pos == pos and form.feats == feats:
            return form

        sim = grams_sim(form.pos, form.feats, pos, feats)
        if sim > max:
            best = form
            max = sim
    return best


def lemmatize(vocab, word, pos, feats):
    word = normal_word(word)
    forms = vocab(word)
    form = best_form(forms, pos, feats)
    if form:
        return normal_word(form.normal)
    return word
