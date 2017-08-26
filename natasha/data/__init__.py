# coding: utf-8
from __future__ import unicode_literals
from yargy.compat import RUNNING_ON_PYTHON_2_VERSION

import os


def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def maybe_strip_comment(line):
    if '#' in line:
        line = line[:line.index('#')]
        line = line.rstrip()
    return line


def load_lines(filename):
    path = get_path(filename)
    with open(path) as file:
        for line in file:
            if RUNNING_ON_PYTHON_2_VERSION:
                line = line.decode('utf-8')
            line = line.rstrip('\n')
            line = maybe_strip_comment(line)
            yield line
