# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    in_,
    is_capitalized,
)


class Brand(Enum):

    Latin = [
        {
            'labels': [
                gram('LATN'),
                is_capitalized(True),
            ],
            'repeatable': True,
        },
        {
            'labels': [
                gram('INT'),
            ],
            'optional': True,
        }
    ]

    WithConj = [
        Latin[0],
        {
            'labels': [
                in_({
                    '&',
                    '/',
                }),
            ],
        },
        Latin[0],
    ]

    Trademark = [
        {
            'labels': [
                gram('Trad'),
            ],
        }
    ]
