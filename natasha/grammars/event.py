# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    gram_any,
    gram_not,
    gnc_match,
    dictionary,
)

EVENT_TYPE_DICTIONARY = {
    'фестиваль',
    'форум',
    'выставка',
    'ярмарка',
    'конференция',
    'шоу',
}

class Event(Enum):

    Object = [
        {
            'labels': [
                gram('NOUN'),
                dictionary(EVENT_TYPE_DICTIONARY),
            ],
        },
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
        {
            'labels': [
                gram_not('QUOTE'),
            ],
            'repeatable': True,
        },
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
    ]

    # Московский международный форум
    AdjWithDescriptor = [
        {
            'labels': [
                gram('ADJF'),
            ],
        },
        {
            'labels': [
                gram('ADJF'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'optional': True,
            'repeatable': True,
        },
        {
            'labels': [
                dictionary(EVENT_TYPE_DICTIONARY),
                gnc_match(0, solve_disambiguation=True),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]
