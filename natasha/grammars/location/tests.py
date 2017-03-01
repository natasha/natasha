# coding: utf-8
from __future__ import unicode_literals


import natasha
import unittest

from natasha.tests import BaseTestCase
from natasha.grammars.location import LocationObject

from yargy.normalization import get_normalized_text
from yargy.interpretation import InterpretationEngine


class LocationTestCase(BaseTestCase):

    def test_federal_district(self):
        grammar, match = list(
            self.combinator.extract('северо-западный федеральный округ'))[0]
        self.assertEqual(grammar, natasha.Location.FederalDistrict)
        self.assertEqual(
            ['северо-западный', 'федеральный', 'округ'], [x.value for x in match])

    def test_autonomous_district(self):
        grammar, match = list(
            self.combinator.extract('Ямало-Ненецкого автономного округа'))[0]
        self.assertEqual(grammar, natasha.Location.AutonomousDistrict)
        self.assertEqual(
            ['Ямало-Ненецкого', 'автономного', 'округа'], [x.value for x in match])

    def test_federal_district_abbr(self):
        grammar, match = list(self.combinator.extract('северо-западный ФО'))[0]
        self.assertEqual(grammar, natasha.Location.FederalDistrictAbbr)
        self.assertEqual(['северо-западный', 'ФО'], [x.value for x in match])

    def test_region(self):
        grammar, match = list(
            self.combinator.extract('северо-западная область'))[0]
        self.assertEqual(grammar, natasha.Location.Region)
        self.assertEqual(
            ['северо-западная', 'область'], [x.value for x in match])
        with self.assertRaises(IndexError):
            list(self.combinator.extract('северо-западный область'))[0]

    def test_complex_object(self):
        grammar, match = list(self.combinator.extract('северный кипр'))[0]
        self.assertEqual(grammar, natasha.Location.ComplexObject)
        with self.assertRaises(IndexError):
            list(self.combinator.extract('северная кипр'))[0]

    @unittest.skip('skip for now, because need to know something about gent(2?)+loct(2?) cases concordance')
    def test_partial_object(self):
        grammar, match = list(self.combinator.extract('на юго-западе кипра'))[0]
        self.assertEqual(grammar, natasha.Location.PartialObject)

    def test_object(self):
        grammar, match = list(self.combinator.extract('Москва́'))[0]
        self.assertEqual(grammar, natasha.Location.Object)
        self.assertEqual(['Москва'], [x.value for x in match])

    def test_adj_federation(self):
        grammar, match = list(self.combinator.extract('В Донецкой народной республике'))[0]
        self.assertEqual(grammar, natasha.Location.AdjfFederation)
        self.assertEqual(['Донецкой', 'народной', 'республике'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Соединенными Штатами Америки')
            )
        )[0]
        self.assertEqual(grammar, natasha.Location.AdjxFederation)
        self.assertEqual(['Соединенными', 'Штатами', 'Америки'], [x.value for x in match])

class AddressTestCase(BaseTestCase):

    def test_adj_full(self):
        grammar, match = list(self.combinator.extract('на зеленой улице'))[0]
        self.assertEqual(grammar, natasha.Address.AdjFull)
        self.assertEqual(['зеленой', 'улице'], [x.value for x in match])

        grammar, match = list(self.combinator.extract('около красной площади'))[0]
        self.assertEqual(grammar, natasha.Address.AdjFull)
        self.assertEqual(['красной', 'площади'], [x.value for x in match])

        # TODO: this grammar fails on pypy
        # grammar, match = list(
        #     self.combinator.resolve_matches(
        #         self.combinator.extract('улица Красная Набережная')
        #     )
        # )[0]
        # self.assertEqual(grammar, natasha.Address.AdjFull)
        # self.assertEqual(['Красная', 'Набережная'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('вторая московская улица')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjFull)
        self.assertEqual(['вторая', 'московская', 'улица'], [x.value for x in match])

    def test_adj_full_with_house_number(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('на зеленой улице, дом 7')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjFullWithHn)
        self.assertEqual(['зеленой', 'улице', ',', 'дом', 7], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('на зеленой улице, д. 7')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjFullWithHn)
        self.assertEqual(['зеленой', 'улице', ',', 'д', '.', 7], [x.value for x in match])

    def test_adj_short(self):
        grammar, match = list(self.combinator.extract('ул. Нижняя Красносельская'))[0]
        self.assertEqual(grammar, natasha.Address.AdjShort)
        self.assertEqual(['ул', '.', 'Нижняя', 'Красносельская'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пл. Ленина')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShort)
        self.assertEqual(['пл', '.', 'Ленина'], [x.value for x in match])

    def test_adj_short_with_house_number(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. Нижняя Красносельская, дом 7')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortWithHn)
        self.assertEqual(['ул', '.', 'Нижняя', 'Красносельская', ',', 'дом', 7], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. Нижняя Красносельская д 7')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortWithHn)
        self.assertEqual(['ул', '.', 'Нижняя', 'Красносельская', 'д', 7], [x.value for x in match])

    def test_adj_short_reversed(self):

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('московская ул.')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortReversed)
        self.assertEqual(['московская', 'ул', '.'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Настасьинский пер.')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortReversed)
        self.assertEqual(['Настасьинский', 'пер', '.'], [x.value for x in match])

    def test_adj_short_reversed_with_house_number(self):

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('московская ул. дом 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortReversedWithHn)
        self.assertEqual(['московская', 'ул', '.', 'дом', 1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Настасьинский пер., дом 2')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortReversedWithHn)
        self.assertEqual(['Настасьинский', 'пер', '.', ',', 'дом', 2], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('московская ул. д 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortReversedWithHn)
        self.assertEqual(['московская', 'ул', '.', 'д', 1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Настасьинский пер., д. 2')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortReversedWithHn)
        self.assertEqual(['Настасьинский', 'пер', '.', ',', 'д', '.', 2], [x.value for x in match])

    def test_adj_full_reversed(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Зеленая')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjFullReversed)
        self.assertEqual(['улица', 'Зеленая'], [x.value for x in match])

    def test_adj_full_reversed_with_house_number(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Зеленая дом 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjFullReversedWithHn)
        self.assertEqual(['улица', 'Зеленая', 'дом', 1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Зеленая д 2')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjFullReversedWithHn)
        self.assertEqual(['улица', 'Зеленая', 'д', 2], [x.value for x in match])

    def test_adj_noun_full(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Красной Гвардии')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjNounFull)
        self.assertEqual(['улица', 'Красной', 'Гвардии'], [x.value for x in match])

    def test_adj_noun_full_with_house_number(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Красной Гвардии, дом 2')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjNounFullWithHn)
        self.assertEqual(['улица', 'Красной', 'Гвардии', ',', 'дом', 2], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Красной Гвардии д1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjNounFullWithHn)
        self.assertEqual(['улица', 'Красной', 'Гвардии', 'д', 1], [x.value for x in match])

    def test_adj_noun_short(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. Брянской пролетарской дивизии')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjNounShort)
        self.assertEqual(['ул', '.', 'Брянской', 'пролетарской', 'дивизии'], [x.value for x in match])

    def test_adj_noun_short_with_house_number(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. Брянской пролетарской дивизии дом 2')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjNounShortWithHn)
        self.assertEqual(['ул', '.', 'Брянской', 'пролетарской', 'дивизии', 'дом', 2], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. Брянской пролетарской дивизии, д. 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjNounShortWithHn)
        self.assertEqual(['ул', '.', 'Брянской', 'пролетарской', 'дивизии', ',', 'д', '.', 1], [x.value for x in match])

    def test_gent_full(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Николая Ершова улица')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFull)
        self.assertEqual(['Николая', 'Ершова', 'улица'], [x.value for x in match])

    def test_gent_full_with_house_number(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Николая Ершова улица дом1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullWithHn)
        self.assertEqual(['Николая', 'Ершова', 'улица', 'дом', 1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Николая Ершова улица, д.1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullWithHn)
        self.assertEqual(['Николая', 'Ершова', 'улица', ',', 'д', '.', 1], [x.value for x in match])

    def test_gent_short(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Обуховской Обороны пр-кт')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShort)
        self.assertEqual(['Обуховской', 'Обороны', 'пр-кт'], [x.value for x in match])

    def test_gent_short_with_house_number(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Обуховской Обороны пр-кт, дом 5')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortWithHn)
        self.assertEqual(['Обуховской', 'Обороны', 'пр-кт', ',','дом', 5], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Обуховской Обороны пр-кт д 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortWithHn)
        self.assertEqual(['Обуховской', 'Обороны', 'пр-кт', 'д', 1], [x.value for x in match])

    def test_gent_full_reversed(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('проспект Юрия Гагарина')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversed)
        self.assertEqual(['проспект', 'Юрия', 'Гагарина'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Богомягкова')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversed)
        self.assertEqual(['улица', 'Богомягкова'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Федосеенко')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversed)
        self.assertEqual(['улица', 'Федосеенко'], [x.value for x in match])

    def test_gent_full_reversed_with_house_number(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('проспект Юрия Гагарина, дом 10')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithHn)
        self.assertEqual(['проспект', 'Юрия', 'Гагарина', ',', 'дом', 10], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Богомягкова дом 10')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithHn)
        self.assertEqual(['улица', 'Богомягкова', 'дом', 10], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Федосеенко дом5')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithHn)
        self.assertEqual(['улица', 'Федосеенко', 'дом', 5], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('проспект Юрия Гагарина д1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithHn)
        self.assertEqual(['проспект', 'Юрия', 'Гагарина', 'д', 1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Богомягкова, д. 10')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithHn)
        self.assertEqual(['улица', 'Богомягкова', ',', 'д', '.', 10], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Федосеенко д 10')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithHn)
        self.assertEqual(['улица', 'Федосеенко', 'д', 10], [x.value for x in match])

    def test_gent_full_reversed_with_shortcut(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица К. Маркса')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithShortcut)
        self.assertEqual(['улица', 'К', '.', 'Маркса'], [x.value for x in match])

    def test_gent_full_reversed_with_extended_shortcut(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица В. В. Ленина')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithExtendedShortcut)
        self.assertEqual(['улица', 'В', '.', 'В', '.', 'Ленина'], [x.value for x in match])

    def test_gent_full_reversed_with_shortcut_with_h_n(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица К. Маркса дом 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithShortcutWithHn)
        self.assertEqual(['улица', 'К', '.', 'Маркса', 'дом',  1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица К. Маркса, д. 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithShortcutWithHn)
        self.assertEqual(['улица', 'К', '.', 'Маркса', ',', 'д', '.', 1], [x.value for x in match])

    def test_gent_full_reversed_with_extended_shortcut_with_h_n(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица В. В. Ленина дом 2')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithExtendedShortcutWithHn)
        self.assertEqual(['улица', 'В', '.', 'В', '.', 'Ленина', 'дом', 2], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица В. В. Ленина д 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithExtendedShortcutWithHn)
        self.assertEqual(['улица', 'В', '.', 'В', '.', 'Ленина', 'д', 1], [x.value for x in match])

    def test_gent_short_reversed(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр. Маршала Жукова')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversed)
        self.assertEqual(['пр', '.', 'Маршала', 'Жукова'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пл. Металлургов')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversed)
        self.assertEqual(['пл', '.', 'Металлургов'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр-т Культуры')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversed)
        self.assertEqual(['пр-т', 'Культуры'], [x.value for x in match])

        # TODO:
        # grammar, match = list(
        #     self.combinator.resolve_matches(
        #         self.combinator.extract('ул. Розы Люксембург')
        #     )
        # )[0]
        # self.assertEqual(grammar, natasha.Address.GentShortReversed)
        # self.assertEqual(['ул', '.', 'Розы', 'Люксембург'], [x.value for x in match])

    def test_gent_short_reversed_with_f_house_number(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр. Маршала Жукова дом 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithHn)
        self.assertEqual(['пр', '.', 'Маршала', 'Жукова', 'дом', 1], [x.value for x in match])

    def test_gent_short_reversed_with_s_house_number(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр. Маршала Жукова д. 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithHn)
        self.assertEqual(['пр', '.', 'Маршала', 'Жукова', 'д', '.', 1], [x.value for x in match])

    def test_gent_short_reversed_with_shortcut(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр. М. Жукова')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithShortcut)
        self.assertEqual(['пр', '.', 'М', '.', 'Жукова'], [x.value for x in match])

    def test_gent_short_reversed_with_extended_shortcut(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр. В. В. Ленина')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithExtendedShortcut)
        self.assertEqual(['пр', '.', 'В', '.', 'В', '.', 'Ленина'], [x.value for x in match])

    def test_gent_short_reversed_with_shortcut_with_h_n(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. К. Маркса дом 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithShortcutWithHn)
        self.assertEqual(['ул', '.', 'К', '.', 'Маркса', 'дом',  1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. К. Маркса, д. 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithShortcutWithHn)
        self.assertEqual(['ул', '.', 'К', '.', 'Маркса', ',', 'д', '.', 1], [x.value for x in match])

    def test_gent_short_reversed_with_extended_shortcut_with_h_n(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. В. В. Ленина дом 2')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithExtendedShortcutWithHn)
        self.assertEqual(['ул', '.', 'В', '.', 'В', '.', 'Ленина', 'дом', 2], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. В. В. Ленина д 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithExtendedShortcutWithHn)
        self.assertEqual(['ул', '.', 'В', '.', 'В', '.', 'Ленина', 'д', 1], [x.value for x in match])

    def test_numeric_adj_full(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('2-я новорублевская улица')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjFullWithNumericPart)
        self.assertEqual([2, '-', 'я', 'новорублевская', 'улица'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('1-й бадаевский проезд')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjFullWithNumericPart)
        self.assertEqual([1, '-', 'й', 'бадаевский', 'проезд'], [x.value for x in match])


    def test_numeric_adj_full_reversed(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица 1-я промышленная')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjFullReversedWithNumericPart)
        self.assertEqual(['улица', 1, '-', 'я', 'промышленная'], [x.value for x in match])

    def test_numeric_adj_short(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('1-я промышленная ул.')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortWithNumericPart)
        self.assertEqual([1, '-', 'я', 'промышленная', 'ул', '.'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('1-й басманный пер.')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortWithNumericPart)
        self.assertEqual([1, '-', 'й', 'басманный', 'пер', '.'], [x.value for x in match])

    def test_numeric_adj_short_reversed(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. 1-я промышленная')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjShortReversedWithNumericPart)
        self.assertEqual(['ул', '.', 1, '-', 'я', 'промышленная'], [x.value for x in match])

    def test_numeric_gent_full_reversed_with_numeric_prefix(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('проспект 50 лет октября')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithNumericPrefix)
        self.assertEqual(['проспект', 50, 'лет', 'октября'], [x.value for x in match])

        # TODO:
        # grammar, match = list(
        #     self.combinator.resolve_matches(
        #         self.combinator.extract('площадь 1905 года')
        #     )
        # )[0]
        # self.assertEqual(grammar, natasha.Address.GentFullReversedWithNumericPrefix)
        # self.assertEqual(['площадь', 1905, 'года'], [x.value for x in match])

    def test_numeric_gent_full_reversed_with_numeric_prefix_with_h_n(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('проспект 50 лет октября д 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithNumericPrefixWithHn)
        self.assertEqual(['проспект', 50, 'лет', 'октября', 'д', 1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('проспект 50 лет октября дом 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentFullReversedWithNumericPrefixWithHn)
        self.assertEqual(['проспект', 50, 'лет', 'октября', 'дом', 1], [x.value for x in match])

    def test_numeric_gent_short_reversed_with_numeric_prefix(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр-т. 50 лет советской власти')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithNumericPrefix)
        self.assertEqual(['пр-т', '.', 50, 'лет', 'советской', 'власти'], [x.value for x in match])

        # TODO:        
        # grammar, match = list(
        #     self.combinator.resolve_matches(
        #         self.combinator.extract('ул. 9 мая')
        #     )
        # )[0]
        # self.assertEqual(grammar, natasha.Address.GentShortReversedWithNumericPrefix)
        # self.assertEqual(['ул', '.', 9, 'мая'], [x.value for x in match])

    def test_numeric_gent_short_reversed_with_numeric_prefix_with_h_n(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр-т. 50 лет советской власти д 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithNumericPrefixWithHn)
        self.assertEqual(['пр-т', '.', 50, 'лет', 'советской', 'власти', 'д', 1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр-т. 50 лет советской власти дом 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentShortReversedWithNumericPrefixWithHn)
        self.assertEqual(['пр-т', '.', 50, 'лет', 'советской', 'власти', 'дом', 1], [x.value for x in match])

    def test_numeric_gent_splitted_by_full_descriptor(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('7-я улица текстильщиков')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentNumericSplittedByFullDescriptor)
        self.assertEqual([7, '-', 'я', 'улица', 'текстильщиков'], [x.value for x in match])

    def test_numeric_gent_splitted_by_full_descriptor_with_h_n(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('7-я улица текстильщиков д 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentNumericSplittedByFullDescriptorWithHn)
        self.assertEqual([7, '-', 'я', 'улица', 'текстильщиков', 'д', 1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('7-я улица текстильщиков дом 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentNumericSplittedByFullDescriptorWithHn)
        self.assertEqual([7, '-', 'я', 'улица', 'текстильщиков', 'дом', 1], [x.value for x in match])


    def test_numeric_gent_splitted_by_short_descriptor(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('7-я ул. текстильщиков')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentNumericSplittedByShortDescriptor)
        self.assertEqual([7, '-', 'я', 'ул', '.', 'текстильщиков'], [x.value for x in match])

    def test_numeric_gent_splitted_by_short_descriptor_with_h_n(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('7-я ул. текстильщиков д 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentNumericSplittedByShortDescriptorWithHn)
        self.assertEqual([7, '-', 'я', 'ул', '.', 'текстильщиков', 'д', 1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('7-я ул. текстильщиков д 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentNumericSplittedByShortDescriptorWithHn)
        self.assertEqual([7, '-', 'я', 'ул', '.', 'текстильщиков', 'д', 1], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('7-я ул. текстильщиков дом 1')
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.GentNumericSplittedByShortDescriptorWithHn)
        self.assertEqual([7, '-', 'я', 'ул', '.', 'текстильщиков', 'дом', 1], [x.value for x in match])

    def test_street_name_with_house_letter(self):
        text = 'Литовский бульвар 9/7).15 этаж блочного дома.В'
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract(text)
            )
        )[0]
        self.assertEqual(grammar, natasha.Address.AdjFullWithHn)
        self.assertEqual(['Литовский', 'бульвар', 9], [x.value for x in match])

class LocationInterpretationTestCase(BaseTestCase):

    def setUp(self):
        self.engine = InterpretationEngine(LocationObject)
        super(LocationInterpretationTestCase, self).setUp()

    def test_get_location_object(self):
        matches = self.combinator.resolve_matches(
            self.combinator.extract('Российская Федерация')
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].name.value, 'Российская')
        self.assertEqual(objects[0].descriptor.value, 'Федерация')

        matches = self.combinator.resolve_matches(
            self.combinator.extract('Москва')
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].name.value, 'Москва')
        self.assertEqual(objects[0].descriptor, None)

        matches = self.combinator.resolve_matches(
            self.combinator.extract('Нижний Новгород')
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 1)
        self.assertEqual([t.value for t in objects[0].name], ['Нижний', 'Новгород'])
        self.assertEqual(objects[0].descriptor, None)
