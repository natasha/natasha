from enum import Enum
from natasha.grammars.base import TERM


class Person(Enum):

    # Иван Иванович Иванов
    Full = (
        ('word', {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
        ]}),
        ('word', {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
            ('gender-match', -1),
        ]}),
        ('word', {'labels': [
            ('gram', 'Patr'),
            ('gram-not', 'Abbr'),
            ('gender-match', -1),
        ]}),
        TERM
    )
    # Иванов Иван Иванович
    FullReversed = (
        ('word', {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
        ]}),
        ('word', {'labels': [
            ('gram', 'Patr'),
            ('gram-not', 'Abbr'),
            ('gender-match', -1),
        ]}),
        ('word', {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
            ('gender-match', -1),
        ]}),
        TERM
    )
    # Иван Иванов
    FisrtnameAndLastname = (
        ('word', {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
        ]}),
        ('word', {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
            ('gender-match', -1),
        ]}),
        TERM
    )
    # Иванов Иван
    LastnameAndFirstname = (
        ('word', {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
        ]}),
        ('word', {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
            ('gender-match', -1),
        ]}),
        TERM
    )
    # Иван Иванович
    FirstnameAndMiddlename = (
        ('word', {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
        ]}),
        ('word', {'labels': [
            ('gram', 'Patr'),
            ('gram-not', 'Abbr'),
            ('gender-match', -1),
        ]}),
        TERM
    )
    # Иванов
    Lastname = (
        ('word', {'labels': [
            ('gram', 'Surn'),
            ('gram-not', 'Abbr'),
        ]}),
        TERM
    )
    # Иван
    Firstname = (
        ('word', {'labels': [
            ('gram', 'Name'),
            ('gram-not', 'Abbr'),
        ]}),
        TERM
    )
