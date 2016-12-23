# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    eq,
    gram,
    gram_not,
    gram_in,
    gnc_match,
    is_capitalized,
)


class Person(Enum):

    # Иван Иванович Иванов
    Full = [
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
            ],
        },
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]

    # Иванов Иван Иванович
    FullReversed = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
            ],
        },
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]

    # Л. А. Раневская
    InitialsAndLastname = [
        {
            'labels': [
                gram_in(['Name', 'Abbr']),
            ],
        },
        {
            'labels': [
                gram('PUNCT'),
                eq('.'),
            ],
        },
        {
            'labels': [
                gram_in(['Patr', 'Abbr']),
            ],
        },
        {
            'labels': [
                gram('PUNCT'),
                eq('.'),
            ],
        },
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
            ],
        },
    ]

    # Иван Иванов
    FisrtnameAndLastname = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
            ],
        },
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]

    # Иванов Иван
    LastnameAndFirstname = [
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
            ],
        },
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]

    # Иван Иванович
    FirstnameAndMiddlename = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
            ],
        },
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        },
    ]

    # Иванов
    Lastname = [
        {
            'labels': [
                gram('Surn'),
                gram_not('Abbr'),
                is_capitalized(True),
            ],
        },
    ]

    # Иванович
    Middlename = [
        {
            'labels': [
                gram('Patr'),
                gram_not('Abbr'),
                is_capitalized(True),
            ]
        }
    ]

    # Иван
    Firstname = [
        {
            'labels': [
                gram('Name'),
                gram_not('Abbr'),
                is_capitalized(True),
            ],
        },
    ]
