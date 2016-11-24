# coding: utf-8
from __future__ import unicode_literals

from enum import Enum

EVENT_TYPE_DICTIONARY = {
    'фестиваль',
    'шоу',
}

class Event(Enum):

    Object = [
        {
            'labels': [
                ('gram', 'NOUN'),
                ('dictionary', EVENT_TYPE_DICTIONARY),
            ],
        },
        {
            'labels': [
                ('gram', 'QUOTE'),
            ],
        },
        {
            'repeatable': True,
        },
        {
            'labels': [
                ('gram', 'QUOTE'),
            ],
        },
    ]
