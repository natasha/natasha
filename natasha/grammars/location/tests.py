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
        self.assertEqual(grammar, natasha.Location.AdjFederation)
        self.assertEqual(['Донецкой', 'народной', 'республике'], [x.value for x in match])

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
