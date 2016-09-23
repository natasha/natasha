from enum import Enum
from natasha.grammars.base import Token, TERM

EVENT_TYPE_DICTIONARY = {
    'фестиваль',
    'шоу',
}

class Event(Enum):

    Object = (
        (Token.Word, {
            'labels': [
                ('gram', 'NOUN'),
                ('dictionary', EVENT_TYPE_DICTIONARY),
            ],
        }),
        (Token.Quote, {}),
        (Token.Word, {
            "repeat": True,
        }),
        (Token.Quote, {}),
        TERM,
    )
