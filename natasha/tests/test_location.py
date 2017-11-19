# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import LocationExtractor
from natasha.grammars.location import Location


@pytest.fixture(scope='module')
def extractor():
    return LocationExtractor()

tests = [
    [
        'в Ярославской области',
        Location(name='ярославская область')
    ],
    [
        'около красноярского края',
        Location(name='красноярский край')
    ],
    [
        'события в северо-кавказском федеральном округе',
        Location(name='северо-кавказский федеральный округ')
    ],
    [
        'Северо-западный ФО',
        Location(name='северо-западный фо')
    ],
    # TODO: решить проблемы с дефисами
    # [
    #     'Ямало-Ненецкий автономный округ',
    #     Location(name='ямало-ненецкий автономный округ'),
    # ],
    [
        'В Чеченской республике на день рождения ...',
        Location(name='чеченская республика'),
    ],
    [
        'Донецкая народная республика провозгласила ...',
        Location(name='донецкая народная республика'),
    ],
    [
        'Российская Федерация',
        Location(name='российская федерация'),
    ],
    [
        'в Соединенных Штатах Америки',
        Location(name='соединённый штат америка'),
    ],
    [
        'речь шла о Обьединенных Арабских Эмиратах',
        Location(name='обьединённый арабский эмират'),
    ],
    [
        'Соединённые Штаты',
        Location(name='соединённый штат'),
    ],
    [
        'в штате Вашингтон',
        Location(name='штат вашингтон'),
    ],
    [
        'возле штата Южная Каролина',
        Location(name='штат южная каролина'),
    ],
    [
        'графство Корнуолл',
        Location(name='графство корнуолл'),
    ],
    [
        'город Москва',
        Location(name='город москва'),
    ],
    [
        'Москва',
        Location(name='москва'),
    ],
    [
        'город Ленинград',
        Location(name='город ленинград'),
    ],
    [
        'деревня Верхние Петушки',
        Location(name='деревня верхний петушок'),
    ],
    [
        'село Новое Кукуево',
        Location(name='севшее новое кукуево'),
    ],
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    text = test[0]
    etalon = test[1:]
    guess = [_.fact for _ in extractor(text)]
    assert guess == etalon
