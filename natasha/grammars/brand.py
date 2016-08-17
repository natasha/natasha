from enum import Enum
from natasha.grammars.base import TERM


class Brand(Enum):

    Default = (
        ('word', {
            'labels': [
                ('gram', 'LATN'),
            ],
            'repeat': True,
        }),
        TERM,
    )
