from enum import Enum
from natasha.grammars import Person
from natasha.grammars.base import Token, TERM


ABBR_PREFIX_DICTIONARY = {
    'ООО',
    'ОАО',
    'ПАО',
    'ЗАО',
    'АО',
}

ORG_TYPE_DICTIONARY = {
    'агентство',
    'компания',
}

class Organisation(Enum):

    OfficialAbbrQuoted = (
        (Token.Word, {
            'labels': [
                ('in', ABBR_PREFIX_DICTIONARY),
            ],
        }),
        (Token.Quote, {}),
        (Token.Word, {
            'repeat': True,
        }),
        (Token.Quote, {}),
        TERM,
    )

    Abbr = (
        (Token.Word, {
            'labels': [
                ('gram', 'Abbr'),
                ('gram', 'Orgn'),
            ]
        }),
        TERM,
    )

    IndividualEntrepreneur = (
        (Token.Word, {
            'labels': [
                ('eq', 'ИП'),
            ],
        }),
        *Person.Full.value[:-1],
        TERM,
    )

    SimpleLatin = (
        (Token.Word, {
            'labels': [
                ('dictionary', ORG_TYPE_DICTIONARY),
            ],
        }),
        (Token.Word, {
            'labels': [
                ('gram', 'LATN'),
            ],
            'repeat': True,
        }),
        TERM,
    )
