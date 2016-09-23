from enum import Enum
from natasha.grammars.base import Token, TERM


class Brand(Enum):

    Default = (
        (Token.Word, {
            'labels': [
                ('gram', 'LATN'),
                ('is-capitalized', True),
            ],
            'repeat': True,
        }),
        TERM,
    )
