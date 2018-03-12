# coding: utf-8
from __future__ import unicode_literals

from collections import Counter

from .data import load_json


##########
#
#   MODEL
#
###########


OUTSIDE = 'O'
INSIDE = 'I'
LABELS = [OUTSIDE, INSIDE]


class Model(object):
    def __init__(self, transitions, state_features):
        self.transitions = transitions
        self.state_features = state_features


def parse_model(data):
    transitions = {}
    for a, b, weight in data[0]:
        transitions[LABELS.index(b), LABELS.index(a)] = weight
    state_features = Counter()
    for feature, label, weight in data[1]:
        state_features[feature, LABELS.index(label)] = weight
    return Model(transitions, state_features)


def load_model(path):
    data = load_json(path)
    return parse_model(data)


def argmax(items):
    position = None
    value = None
    for index, item in enumerate(items):
        if value is None or item > value:
            value = item
            position = index
    return position, value


def viterbi(features, model):
    if not features:
        return []

    assert len(LABELS) == 2
    labels = range(len(LABELS))
    state = []
    weights = model.state_features
    for attributes in features:
        scores = [
            sum(weights[__, _] for __ in attributes)
            for _ in labels
        ]
        state.append(scores)

    previous = state[0]
    path = []
    weights = model.transitions
    for scores in state[1:]:
        step = []
        current = []
        for target in labels:
            options = [
                previous[_] + weights[_, target]
                for _ in labels
            ]
            index, value = argmax(options)
            current.append(scores[target] + value)
            step.append(index)
        previous = current
        path.append(step)

    index, _ = argmax(previous)
    labels = [index]
    for step in reversed(path):
        index = step[index]
        labels.append(index)
    return [LABELS[_] for _ in reversed(labels)]


class CrfTagger(object):
    def __init__(self, path, get_features):
        self.model = load_model(path)
        self.get_features = get_features

    def check_tag(self, tag):
        return tag in LABELS

    def __call__(self, tokens):
        tokens = list(tokens)
        features = list(self.get_features(tokens))
        labels = viterbi(features, self.model)
        assert len(tokens) == len(labels)
        for token, label in zip(tokens, labels):
            yield token.tagged(label)


############
#
#   STREET
#
###########


def get_shape(token):
    item = token.value
    if item.isdigit():
        return 'DIGIT'
    elif item.isalpha():
        if item.islower():
            return 'oo'
        elif item.isupper():
            return 'OO'
        elif item.istitle():
            return 'Oo'
        else:
            return 'OTHER'
    else:
        return 'PUNCT'


def get_normalized(token):
    if token.type == 'RU':
        return token.normalized
    elif token.type == 'PUNCT':
        return token.value
    else:
        return 'OTHER'


def get_street_token_features(tokens, index):
    token = tokens[index]
    yield 'bias'
    yield 'shape=' + get_shape(token)
    yield 'norm=' + get_normalized(token)

    if index > 1:
        token = tokens[index - 2]
        yield '-2:shape=' + get_shape(token)
        yield '-2:norm=' + get_normalized(token)
    else:
        yield 'BOS'

    if index > 0:
        token = tokens[index - 1]
        yield '-1:shape=' + get_shape(token)
        yield '-1:norm=' + get_normalized(token)
    else:
        yield 'BOS'

    if index < len(tokens) - 1:
        token = tokens[index + 1]
        yield '+1:shape=' + get_shape(token)
        yield '+1:norm=' + get_normalized(token)
    else:
        yield 'EOS'


def get_street_features(tokens):
    for index, _ in enumerate(tokens):
        yield list(get_street_token_features(tokens, index))


########
#
#   NAME
#
###########


def get_pos(token):
    if token.type == 'RU':
        form = token.forms[0].raw
        return form.tag.POS or 'UNKNOWN'
    else:
        return 'UNKNOWN'


def get_name(token):
    if token.type == 'RU':
        form = token.forms[0]
        grams = form.grams
        if 'Name' in grams:
            return 'Name'
        elif 'Surn' in grams:
            return 'Surn'
    return 'UNKNOWN'


def get_name_token_features(base, size, **features):
    yield 'bias'

    for offset in (-3, -2, -1, 0, 1, 2, 3):
        index = base + offset
        if index < 0:
            yield 'BOS'
        elif index >= size:
            yield 'EOS'
        else:
            for key, values in features.items():
                value = values[index]
                yield '{offset}:{key}={value}'.format(
                    offset=offset,
                    key=key,
                    value=value
                )


def get_name_features(tokens):
    shapes = [get_shape(_) for _ in tokens]
    poses = [get_pos(_) for _ in tokens]
    names = [get_name(_) for _ in tokens]
    size = len(tokens)
    for index in range(len(tokens)):
        yield list(get_name_token_features(
            index, size,
            shape=shapes, pos=poses, name=names
        ))
