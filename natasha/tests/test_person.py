# coding: utf-8
from __future__ import unicode_literals

import pytest

from natasha.grammars.person import Person
from natasha.grammars.name import Name
from natasha import PersonExtractor


@pytest.fixture(scope='module')
def extractor():
    return PersonExtractor()


tests = [
    [
        'президент Николя Саркози',
        Person(
            position='президент',
            name=Name(
                first='николя', last='саркози',
                middle=None, nick=None
            )
        )
    ],
    [
        'Вице-премьер правительства РФ Дмитрий Козак',
        Person(
            position='Вице-премьер правительства РФ',
            name=Name(
                first='дмитрий',
                last='козак',
                middle=None,
                nick=None
            )
        )
    ],
    # TODO Почему-то петров -> пётр
    # [
    #     'академик Н.Н. Петров',
    #     Person(
    #         position='академик',
    #         name=Name(
    #             first='Н',
    #             middle='Н',
    #             last='петров',
    #         )
    #     ),
    # ],
    [
        'Вице-президент Генадий Рушайло',
        Person(
            position='Вице-президент',
            name=Name(
                first='генадий',
                last='рушайло',
            )
        ),
    ],
]


@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    text = test[0]
    etalon = test[1:]
    guess = [_.fact for _ in extractor(text)]
    assert guess == etalon
