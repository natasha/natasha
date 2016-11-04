from enum import Enum


class Person(Enum):

    # Иван Иванович Иванов
    Full = [
        {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
        ]},
        {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]},
        {'labels': [
            ('gram', 'Patr'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]},
    ]

    # Иванов Иван Иванович
    FullReversed = [
        {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
        ]},
        {'labels': [
            ('gram', 'Patr'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]},
        {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]},
    ]

    # Л. А. Раневская
    InitialsAndLastname = [
        {'labels': [
            ('gram-in', ['Name', 'Abbr']),
        ]},
        {
            'labels': [
                ('gram', 'PUNCT'),
            ],
        },
        {'labels': [
            ('gram-in', ['Patr', 'Abbr']),
        ]},
        {
            'labels': [
                ('gram', 'PUNCT'),
            ],
        },
        {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
        ]},
    ]

    # Иван Иванов
    FisrtnameAndLastname = [
        {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
        ]},
        {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]},
    ]

    # Иванов Иван
    LastnameAndFirstname = [
        {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
        ]},
        {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]},
    ]

    # Иван Иванович
    FirstnameAndMiddlename = [
        {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
        ]},
        {'labels': [
            ('gram', 'Patr'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]},
    ]

    # Иванов
    Lastname = [
        {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
            ('is-capitalized', True),
        ]},
    ]

    # Иван
    Firstname = [
        {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
            ('is-capitalized', True),
        ]},
    ]
