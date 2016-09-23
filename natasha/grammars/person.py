from enum import Enum
from natasha.grammars.base import Token, TERM


class Person(Enum):

    # Иван Иванович Иванов
    Full = (
        (Token.Word, {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
        ]}),
        (Token.Word, {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]}),
        (Token.Word, {'labels': [
            ('gram', 'Patr'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]}),
        TERM
    )
    # Иванов Иван Иванович
    FullReversed = (
        (Token.Word, {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
        ]}),
        (Token.Word, {'labels': [
            ('gram', 'Patr'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]}),
        (Token.Word, {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]}),
        TERM
    )

    # Л. А. Раневская
    InitialsAndLastname = (
        (Token.Word, {'labels': [
            ('gram-in', ['Name', 'Abbr']),
        ]}),
        (Token.Punct, {}),
        (Token.Word, {'labels': [
            ('gram-in', ['Patr', 'Abbr']),
        ]}),
        (Token.Punct, {}),
        (Token.Word, {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
        ]}),
        TERM,
    )

    # Иван Иванов
    FisrtnameAndLastname = (
        (Token.Word, {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
        ]}),
        (Token.Word, {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]}),
        TERM
    )
    # Иванов Иван
    LastnameAndFirstname = (
        (Token.Word, {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
        ]}),
        (Token.Word, {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]}),
        TERM
    )
    # Иван Иванович
    FirstnameAndMiddlename = (
        (Token.Word, {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
        ]}),
        (Token.Word, {'labels': [
            ('gram', 'Patr'),
            ('gram-not', 'Abbr'),
            ('gnc-match', -1),
        ]}),
        TERM
    )
    # Иванов
    Lastname = (
        (Token.Word, {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
            ('is-capitalized', True),
        ]}),
        TERM
    )
    # Иван
    Firstname = (
        (Token.Word, {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
            ('is-capitalized', True),
        ]}),
        TERM
    )
