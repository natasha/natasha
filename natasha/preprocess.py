# coding: utf-8
from __future__ import unicode_literals


def make_translation_table(source, target):
    assert len(source) == len(target)
    return {
        ord(a): ord(b)
        for a, b in zip(source, target)
    }


DASHES = make_translation_table(
    '‑–—−',
    '----'
)


def normalize_text(text):
    return text.translate(DASHES)
