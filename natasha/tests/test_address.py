# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha import AddressExtractor
from natasha.grammars.address import (
    Address, Index, Country,
    Region, Settlement,
    Street, Building, Room
)


@pytest.fixture(scope='module')
def extractor():
    return AddressExtractor()

tests = [
    [
        'Россия, Вологодская обл. г. Череповец, пр.Победы 93 б',
        Address(parts=[
            Country(name='Россия'),
            Region(name='Вологодская', type='область'),
            Settlement(name='Череповец', type='город'),
            Street(name='Победы', type='проспект'),
            Building(number='93 б')
        ])
    ],
    [
        '692909, РФ, Приморский край, г. Находка, ул. Добролюбова, 18',
        Address(parts=[
            Index(value=692909),
            Country(name='РФ'),
            Region(name='Приморский', type='край'),
            Settlement(name='Находка', type='город'),
            Street(name='Добролюбова', type='улица'),
            Building(number=18, type=None)
        ])
    ],
    [
        'д. Федоровка, ул. Дружбы, 13',
        Address(parts=[
            Settlement(name='Федоровка', type='деревня'),
            Street(name='Дружбы', type='улица'),
            Building(number=13, type=None)
        ])
    ],
    [
        'Россия, 129110, г.Москва, Олимпийский проспект, 22',
        Address(parts=[
            Index(value=129110),
            Settlement(name='Москва', type='город'),
            Street(name='Олимпийский', type='проспект'),
            Building(number=22, type=None)
        ])
    ],
    [
        '197342 г. Санкт-Петербург, Красногвардейский пер., д. 15',
        Address(parts=[
            Index(value=197342),
            Settlement(name='Санкт-Петербург', type='город'),
            Street(name='Красногвардейский', type='переулок'),
            Building(number=15, type='дом')
        ])
    ],
    [
        'Республика Карелия,г.Петрозаводск,ул.Маршала Мерецкова, д.8 Б,офис 4',
        Address(parts=[
            Region(name='Карелия', type='республика'),
            Settlement(name='Петрозаводск', type='город'),
            Street(name='Маршала Мерецкова', type='улица'),
            Building(number='8 Б', type='дом'),
            Room(number=4, type='офис')
        ])
    ]
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    text = test[0]
    etalon = test[1:]
    guess = [_.fact for _ in extractor(text)]
    assert guess == etalon


# TODO from pzz
# ул. Народного Ополчения д. 9к.3
# В п. 14
# Садовническая наб, вл.77стр1
# ул. Б. Пироговская, д.37/430 корп В
# ул.Б. Серпуховская ,вл.46, к.9
