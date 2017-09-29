from tqdm import tqdm_notebook as log_progress

import re
import os
from collections import namedtuple
from subprocess import check_call
import xml.etree.ElementTree as ET

from random import sample
from random import seed as random_seed

from natasha import NamesExtractor
from natasha.markup import show_markup


BIN_DIR = 'tomita'
TOMITA_BIN = os.path.join(BIN_DIR, 'tomita-mac')
ALGFIO_DIR = os.path.join(BIN_DIR, 'algfio')
ALGFIO_TEXTS = os.path.join(ALGFIO_DIR, 'texts')
ALGFIO_FACTS = os.path.join(ALGFIO_DIR, 'facts.xml')
ALGFIO_CONFIG = os.path.join(ALGFIO_DIR, 'config.proto')

REVIEWS = 'reviews.txt'
NEWS = 'news.txt'


AlgfioFact = namedtuple(
    'AlgfioFact',
    ['last', 'first', 'middle', 'known_surname']
)
TomitaMatch = namedtuple(
    'TomitaMatch',
    ['span', 'fact']
)


def load_xml(path):
    text = load_text(path)
    return ET.fromstring(text.encode('utf8'))


def parse_algfio_tomita_facts_(xml):
    facts = xml.find('facts')
    for item in facts.findall('Person'):
        start = int(item.get('pos'))
        size = int(item.get('len'))
        last = item.find('Name_Surname')
        if last is not None:
            last = last.get('val') or None
        first = item.find('Name_FirstName')
        if first is not None:
            first = first.get('val')
        middle = item.find('Name_Patronymic')
        if middle is not None:
            middle = middle.get('val')
        known_surname = item.find('Name_SurnameIsDictionary')
        if known_surname is not None:
            known_surname = int(known_surname.get('val'))
        known_surname = bool(known_surname)
        span = (start, start + size)
        fact = AlgfioFact(last, first, middle, known_surname)
        yield TomitaMatch(span, fact)


def parse_algfio_tomita_facts(xml):
    for document in xml.findall('document'):
        url = document.get('url')
        index, = re.match(r'^\\(\d+).txt$', url).groups()
        index = int(index)
        matches = list(parse_algfio_tomita_facts_(document))
        yield index, matches


def load_lines(path):
    with open(path) as file:
        for line in file:
            yield line.rstrip()


def load_text(path):
    with open(path) as file:
        return file.read()
        
        
def dump_text(text, path):
    with open(path, 'w') as file:
        file.write(text)

        
def get_algfio_text_path(index):
    return os.path.join(
        ALGFIO_TEXTS,
        '{index}.txt'.format(index=index)
    )


def clean_algfio_texts():
    for filename in os.listdir(ALGFIO_TEXTS):
        path = os.path.join(ALGFIO_TEXTS, filename)
        os.remove(path)


def run_algfio_tomita(texts):
    clean_algfio_texts()
    for index, text in enumerate(texts):
        path = get_algfio_text_path(index)
        dump_text(text, path)
    bin = os.path.relpath(TOMITA_BIN, ALGFIO_DIR)
    config = os.path.relpath(ALGFIO_CONFIG, ALGFIO_DIR)
    check_call([bin, config], cwd=ALGFIO_DIR)
    xml = load_xml(ALGFIO_FACTS)
    mapping = dict(parse_algfio_tomita_facts(xml))
    for index in range(len(texts)):
        yield mapping.get(index, [])
    clean_algfio_texts()
    os.remove(ALGFIO_FACTS)
