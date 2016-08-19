from enum import Enum
from natasha.grammars.base import TERM


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
        ('word', {
            'labels': [
                ('gram', 'ADJF'),
                ('dictionary', FEDERAL_DISTRICT_DICTIONARY),
            ],
        }),
        ('word', {
            'labels': [
                ('dictionary', {'федеральный', }),
            ],
        }),
        ('word', {
            'labels': [
                ('dictionary', {'округ', }),
            ],
        }),
        TERM,
    )

    FederalDistrictAbbr = (
        ('word', {
            'labels': [
                ('gram', 'ADJF'),
                ('dictionary', FEDERAL_DISTRICT_DICTIONARY),
            ],
        }),
        ('word', {
            'labels': [
                ('eq', 'ФО'),
            ],
        }),
        TERM,
    )

    Region = (
        ('word', {
            'labels': [
                ('gram', 'ADJF'),
            ],
        }),
        ('word', {
            'labels': [
                ('dictionary', REGION_TYPE_DICTIONARY),
                ('gender-match', -1),
            ],
        }),
        TERM,
    )

    ComplexObject = (
        ('word', {
            'labels': [
                ('gram', 'ADJF'),
                ('dictionary', COMPLEX_OBJECT_PREFIX_DICTIONARY),
            ],
        }),
        ('word', {
            'labels': [
                ('gram', 'NOUN'),
                ('gram', 'Geox'),
                ('gender-match', -1),
            ],
        }),
        TERM,
    )

    PartialObject = (
        ('word', {
            'labels': [
                ('gram', 'NOUN'),
                ('dictionary', PARTIAL_OBJECT_PREFIX_DICTIONARY),
            ],
        }),
        ('word', {
            'labels': [
                ('gram', 'NOUN'),
                ('gram', 'Geox'),
                ('gender-match', -1),
            ],
        }),
        TERM,
    )

    Object = (
        ('word', {
            'labels': [
                ('is-capitalized', True),
                ('gram', 'Geox'),
                ('gram-not', 'Abbr'),
            ],
        }),
        TERM,
    )

    AbbrObject = (
        ('word', {
            'labels': [
                ('gram', 'Geox'),
                ('is-upper', True),
            ],
        }),
        TERM,
    )
