import os
import re
import json
from collections import Counter, OrderedDict

from tqdm import tqdm_notebook as log_progress

from natasha.utils import Record
from natasha import NamesExtractor
from natasha.markup import show_markup


FACTRU_DIR = 'factRuEval-2016'
DEVSET_DIR = os.path.join(FACTRU_DIR, 'devset')
TESTSET_DIR = os.path.join(FACTRU_DIR, 'testset')


class Span(Record):
    __attributes__ = ['id', 'type', 'start', 'stop']

    def __init__(self, id, type, start, stop):
        self.id = id
        self.type = type
        self.start = start
        self.stop = stop


class Entity(Record):
    __attributes__ = ['id', 'type', 'spans']

    def __init__(self, id, type, spans):
        self.id = id
        self.type = type
        self.spans = spans


class Coref(Record):
    __attributes__ = ['id', 'entities', 'normalized']

    def __init__(self, id, entities, normalized):
        self.id = id
        self.entities = entities
        self.normalized = normalized


class Token(Record):
    __attributes__ = ['value', 'start', 'stop']

    def __init__(self, value, start, stop):
        self.value = value
        self.start = start
        self.stop = stop

    @property
    def as_json(self):
        return [self.value, self.start, self.stop]

    @property
    def span(self):
        return self.start, self.stop

    def shifted(self, shift):
        return Token(
            self.value,
            self.start + shift,
            self.stop + shift
        )


class Name(Record):
    __attributes__ = ['first', 'middle', 'last', 'nick']

    def __init__(self, first, middle, last, nick):
        self.first = first
        self.middle = middle
        self.last = last
        self.nick = nick

    @property
    def as_json(self):
        data = OrderedDict()
        for key in self.__attributes__:
            value = getattr(self, key)
            if value is not None:
                data[key] = value.as_json
        return data

    @property
    def span(self):
        starts = []
        stops = []
        for token in self:
            if token:
                starts.append(token.start)
                stops.append(token.stop)
        return min(starts), max(stops)

    def shifted(self, shift):
        tokens = [
            (_.shifted(shift) if _ else _)
            for _ in self
        ]
        return Name(*tokens)


class NamePart(Record):
    __attributes__ = ['type', 'token']

    def __init__(self, type, token):
        self.type = type
        self.token = token


class ComplexName(Record):
    __attributes__ = ['parts']

    def __init__(self, parts):
        self.parts = parts


class CoreferenceGroup(Record):
    __attributes__ = ['normalized', 'items']

    def __init__(self, normalized, items):
        self.normalized = normalized
        self.items = items


class Test(Record):
    __attributes__ = ['text', 'names']

    def __init__(self, text, names):
        self.text = text
        self.names = names


def load_text(path):
    with open(path) as file:
        return file.read()


def load_factru_doc(id, extension):
    for dir in [DEVSET_DIR, TESTSET_DIR]:
        filename = 'book_{id}.{extension}'.format(
            id=id,
            extension=extension
        )
        path = os.path.join(dir, filename)
        if os.path.exists(path):
            return load_text(path)


def load_factru_text(id):
    return load_factru_doc(id, 'txt')


def list_factru_ids(dir=None):
    if dir is None:
        dirs = [DEVSET_DIR, TESTSET_DIR]
    else:
        dirs = [dir]
    for dir in dirs:
        for filename in os.listdir(dir):
            match = re.match('book_(\d+)\.txt', filename)
            if match:
                id = int(match.group(1))
                yield id


# [('loc_name', 2434),
#  ('org_name', 2265),
#  ('surname', 1959),
#  ('org_descr', 1684),
#  ('job', 1386),
#  ('name', 1341),
#  ('loc_descr', 321),
#  ('geo_adj', 220),
#  ('nickname', 68),
#  ('patronymic', 42),
#  ('prj_name', 22),
#  ('prj_descr', 10),
#  ('facility_descr', 2)]


def parse_factru_spans(text):
    for line in text.splitlines():
        match = re.match('^(\d+) ([^ ]+) (\d+) (\d+)[^$]+$', line)
        id, type, start, size = match.groups()
        id = int(id)
        start = int(start)
        size = int(size)
        yield Span(id, type, start, start + size)


def load_factru_spans(id):
    text = load_factru_doc(id, 'spans')
    return parse_factru_spans(text)


# [('Org', 2821),
#  ('Person', 2129),
#  ('LocOrg', 1399),
#  ('Location', 1257),
#  ('Project', 22),
#  ('Facility', 2)]


def parse_factru_entities(text):
    for line in text.splitlines():
        match = re.match('^(\d+) ([^ ]+) ([\d ]+)[^$]+$', line)
        id, type, spans = match.groups()
        id = int(id)
        spans = [int(_) for _ in spans.split()]
        yield Entity(id, type, spans)


def load_factru_entities(id):
    text = load_factru_doc(id, 'objects')
    return parse_factru_entities(text)


def parse_factru_corefs(text):
    id = None
    entities = None
    normalized = {}
    for line in text.splitlines():
        if not line:
            yield Coref(id, entities, normalized)
            id = None
            entities = None
            normalized = {}
        else:
            match = re.match('^(\d+) ([\d ]+)$', line)
            if match:
                id, entities = match.groups()
                id = int(id)
                entities = [int(_) for _ in entities.split()]
            else:
                key, value = line.split(' ', 1)
                normalized[key] = value


def load_factru_corefs(id):
    text = load_factru_doc(id, 'coref')
    return parse_factru_corefs(text)


def span_token(text, span):
    start = span.start
    stop = span.stop
    value = text[start:stop]
    return Token(value, start, stop)


def prepare_name_part(text, span):
    type = span.type
    token = span_token(text, span)
    return NamePart(type, token)


def prepare_name(text, spans):
    counts = Counter(_.type for _ in spans)
    assert set(counts.keys()) <= {'name', 'patronymic', 'surname', 'nickname'}
    if all(_ == 1 for _ in counts.values()):
        mapping = {
            _.type: span_token(text, _)
            for _ in spans
        }
        return Name(
            mapping.get('name'),
            mapping.get('patronymic'),
            mapping.get('surname'),
            mapping.get('nickname')
        )
    else:
        parts = [prepare_name_part(text, _) for _ in spans]
        return ComplexName(parts)


def prepare_entity(id, text, id_entities, id_spans):
    entity = id_entities[id]
    spans = [id_spans[_] for _ in entity.spans]
    if entity.type == 'Person':
        return prepare_name(text, spans)


def prepare_normalized_name(data):
    if set(data) <= {
        'firstname',
        'lastname',
        'wikidata',
        'patronymic',
        'nickname'
    }:
        return Name(
            data.get('firstname'),
            data.get('patronymic'),
            data.get('lastname'),
            data.get('nickname')
        )
    else:
        parts = [
            NamePart(_, data[_])
            for _ in data
        ]
        return ComplexName(parts)


def load_factru(id):
    text = load_factru_text(id)
    spans = list(load_factru_spans(id))
    corefs = list(load_factru_corefs(id))
    entities = list(load_factru_entities(id))
    id_spans = {_.id: _ for _ in spans}
    id_entities = {_.id: _ for _ in entities}
    for coref in corefs:
        normalized = prepare_normalized_name(coref.normalized)
        items = [
            prepare_entity(_, text, id_entities, id_spans)
            for _ in coref.entities
        ]
        if all(items):
            yield CoreferenceGroup(normalized, items)


def dump_json(data, path):
    with open(path, 'w') as file:
        dump = json.dumps(data, ensure_ascii=False, indent=4)
        file.write(dump)


def get_line_tokens(text):
    for match in re.finditer('([^\n]+)', text):
        value = match.group(1)
        start = match.start()
        stop = match.end()
        yield Token(value, start, stop)


def is_inside(a, b):
    a_start, a_stop = a
    b_start, b_stop = b
    return a_start >= b_start and a_stop <= b_stop


def split_test(test):
    text, names = test
    for line in get_line_tokens(text):
        items = []
        for name in names:
            if is_inside(name.span, line.span):
                items.append(name.shifted(-line.start))
        yield Test(line.value, items)
