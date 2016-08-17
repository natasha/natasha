from enum import Enum
from natasha.grammars.base import TERM

EVENT_TYPE_DICTIONARY = {
    'фестиваль',
    'шоу',
}

class Event(Enum):

    Object = (
        ('word', {
            'labels': [
                ('gram', 'NOUN'),
                ('dictionary', EVENT_TYPE_DICTIONARY),
            ],
        }),
        ('quote', {}),
        ('word', {
            "repeat": True,
        }),
        ('quote', {}),
        TERM,
    )
