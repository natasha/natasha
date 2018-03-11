# coding: utf-8
from __future__ import unicode_literals

import os
import json

from io import open


def get_path(dir, filename):
    return os.path.join(
        os.path.dirname(__file__),
        dir, filename
    )


def get_dict_path(filename):
    return get_path('dicts', filename)


def get_model_path(filename):
    return get_path('models', filename)


def maybe_strip_comment(line):
    if '#' in line:
        line = line[:line.index('#')]
        line = line.rstrip()
    return line


def load_dict(filename):
    path = get_dict_path(filename)
    with open(path, encoding='utf-8') as file:
        for line in file:
            line = line.rstrip('\n')
            line = maybe_strip_comment(line)
            yield line


def load_json(path):
    with open(path, encoding='utf-8') as file:
        return json.load(file)
