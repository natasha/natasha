# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    is_capitalized,
)


class Brand(Enum):

    Default = [
        {
            'labels': [
                gram('LATN'),
                is_capitalized(True),
            ],
            'repeatable': True,
        }
    ]
