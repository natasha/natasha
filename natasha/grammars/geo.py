from enum import Enum
from natasha.grammars.base import Token, TERM


FEDERAL_DISTRICT_DICTIONARY = {
    'центральный',
    'северо-западный',
    'южный',
    'северо-кавказский',
    'приволжский',
    'уральский',
    'сибирский',
    'дальневосточный',
}

REGION_TYPE_DICTIONARY = {
    'край',
    'район',
    'область',
    'губерния',
    'уезд',
}

COMPLEX_OBJECT_PREFIX_DICTIONARY = {
    'северный',
    'северо-западный',
    'северо-восточный',
    'южный',
    'юго-западный',
    'юго-восточный',
    'западный',
    'восточный',
    'верхний',
    'вышний',
    'нижний',
    'великий',
    'дальний',
}

PARTIAL_OBJECT_PREFIX_DICTIONARY = {
    'север',
    'северо-восток',
    'северо-запад',
    'юг',
    'юго-восток',
    'юго-запад',
    'запад',
    'восток',
}

class Geo(Enum):

    FederalDistrict = (
        (Token.Word, {
            'labels': [
                ('gram', 'ADJF'),
                ('dictionary', FEDERAL_DISTRICT_DICTIONARY),
            ],
        }),
        (Token.Word, {
            'labels': [
                ('dictionary', {'федеральный', }),
            ],
        }),
        (Token.Word, {
            'labels': [
                ('dictionary', {'округ', }),
            ],
        }),
        TERM,
    )

    FederalDistrictAbbr = (
        (Token.Word, {
            'labels': [
                ('gram', 'ADJF'),
                ('dictionary', FEDERAL_DISTRICT_DICTIONARY),
            ],
        }),
        (Token.Word, {
            'labels': [
                ('eq', 'ФО'),
            ],
        }),
        TERM,
    )

    Region = (
        (Token.Word, {
            'labels': [
                ('gram', 'ADJF'),
            ],
        }),
        (Token.Word, {
            'labels': [
                ('dictionary', REGION_TYPE_DICTIONARY),
                ('gnc-match', -1),
            ],
        }),
        TERM,
    )

    ComplexObject = (
        (Token.Word, {
            'labels': [
                ('gram', 'ADJF'),
                ('dictionary', COMPLEX_OBJECT_PREFIX_DICTIONARY),
            ],
        }),
        (Token.Word, {
            'labels': [
                ('gram', 'NOUN'),
                ('gram', 'Geox'),
                ('gnc-match', -1),
            ],
        }),
        TERM,
    )

    PartialObject = (
        (Token.Word, {
            'labels': [
                ('gram', 'NOUN'),
                ('dictionary', PARTIAL_OBJECT_PREFIX_DICTIONARY),
            ],
        }),
        (Token.Word, {
            'labels': [
                ('gram', 'NOUN'),
                ('gram', 'Geox'),
                ('gnc-match', -1),
            ],
        }),
        TERM,
    )

    Object = (
        (Token.Word, {
            'labels': [
                ('is-capitalized', True),
                ('gram', 'Geox'),
                ('gram-not', 'Abbr'),
            ],
        }),
        TERM,
    )
