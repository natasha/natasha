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
            Index(value='692909'),
            Country(name='РФ'),
            Region(name='Приморский', type='край'),
            Settlement(name='Находка', type='город'),
            Street(name='Добролюбова', type='улица'),
            Building(number='18', type=None)
        ])
    ],
    [
        'д. Федоровка, ул. Дружбы, 13',
        Address(parts=[
            Settlement(name='Федоровка', type='деревня'),
            Street(name='Дружбы', type='улица'),
            Building(number='13', type=None)
        ])
    ],
    [
        'Россия, 129110, г.Москва, Олимпийский проспект, 22',
        Address(parts=[
            Country(name='Россия'),
            Index(value='129110'),
            Settlement(name='Москва', type='город'),
            Street(name='Олимпийский', type='проспект'),
            Building(number='22', type=None)
        ])
    ],
    [
        'г. Санкт-Петербург, Красногвардейский пер., д. 15',
        Address(parts=[
            Settlement(name='Санкт-Петербург', type='город'),
            Street(name='Красногвардейский', type='переулок'),
            Building(number='15', type='дом')
        ])
    ],
    [
        'Республика Карелия,г.Петрозаводск,ул.Маршала Мерецкова, д.8 Б,офис 4',
        Address(parts=[
            Region(name='Карелия', type='республика'),
            Settlement(name='Петрозаводск', type='город'),
            Street(name='Маршала Мерецкова', type='улица'),
            Building(number='8 Б', type='дом'),
            Room(number='4', type='офис')
        ])
    ],
    [
        '628000, ХМАО-Югра, г.Ханты-Мансийск, ул. Ледовая , д.19',
        Address(parts=[
            Index(value='628000'),
            Region(name='ХМАО-Югра', type=None),
            Settlement(name='Ханты-Мансийск', type='город'),
            Street(name='Ледовая', type='улица'),
            Building(number='19', type='дом')
        ])
    ],
    [
        'ХМАО г.Нижневартовск пер.Ягельный 17',
        Address(parts=[
            Region(name='ХМАО', type=None),
            Settlement(name='Нижневартовск', type='город'),
            Street(name='Ягельный', type='переулок'),
            Building(number='17', type=None)
        ])
    ],
    [
        'Белгородская обл, пгт Борисовка,ул. Рудого д.160',
        Address(parts=[
            Region(name='Белгородская', type='область'),
            Settlement(name='Борисовка', type='посёлок'),
            Street(name='Рудого', type='улица'),
            Building(number='160', type='дом')
        ])
    ],
    [
        'Самарская область, п.г.т. Алексеевка, ул. Ульяновская д. 21',
        Address(parts=[
            Region(name='Самарская', type='область'),
            Settlement(name='Алексеевка', type='посёлок'),
            Street(name='Ульяновская', type='улица'),
            Building(number='21', type='дом')
        ])

    ],
    [
        'Мурманская обл поселок городского типа Молочный, ул.Гальченко д.11',
        Address(parts=[
            Region(name='Мурманская', type='область'),
            Settlement(name='Молочный', type='посёлок'),
            Street(name='Гальченко', type='улица'),
            Building(number='11', type='дом')
        ])
    ],
    [
        'ул. Народного Ополчения д. 9к.3',
        Address(parts=[
            Street(name='Народного Ополчения', type='улица'),
            Building(number='9к', type='дом')
        ])
    ],
    [
        'ул. Б. Пироговская, д.37/430',
        Address(parts=[
            Street(name='Б. Пироговская', type='улица'),
            Building(number='37/430', type='дом')
        ])
    ],
    [
        'г. Таганрог, ул. Шило, 247/1',
        Address(parts=[
            Settlement(name='Таганрог', type='город'),
            Street(name='Шило', type='улица'),
            Building(number='247/1', type=None)
        ])
    ]
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    text = test[0]
    etalon = test[1:]
    guess = [_.fact for _ in extractor(text)]
    assert guess == etalon
