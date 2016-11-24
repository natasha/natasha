# coding: utf-8
from __future__ import unicode_literals

import unittest
import natasha


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.combinator = natasha.Combinator(natasha.DEFAULT_GRAMMARS)

class PersonGrammarsTestCase(BaseTestCase):

    def test_full(self):
        grammars = (x[0] for x in self.combinator.extract('Шерер Анна Павловна'))
        self.assertIn(natasha.Person.Full, grammars)

    def test_full_reversed(self):
        grammars = (x[0] for x in self.combinator.extract('Анна Павловна Шерер'))
        self.assertIn(natasha.Person.FullReversed, grammars)

    def test_firstname_and_lastname(self):
        grammars = (x[0] for x in self.combinator.extract('Анна Шерер'))
        self.assertIn(natasha.Person.FisrtnameAndLastname, grammars)

    def test_lastname_and_firstname(self):
        grammars = (x[0] for x in self.combinator.extract('Шерер Анна'))
        self.assertIn(natasha.Person.LastnameAndFirstname, grammars)

    def test_lastname(self):
        grammar, match = next(self.combinator.extract('Шерер'))
        self.assertEqual(grammar, natasha.Person.Lastname)

    def test_firstname(self):
        grammar, match = next(self.combinator.extract('Анна'))
        self.assertEqual(grammar, natasha.Person.Firstname)

    def test_initials_and_lastname(self):
        grammars = (x[0] for x in self.combinator.extract('в имении Л. А. Раневской'))
        self.assertIn(natasha.Person.InitialsAndLastname, grammars)

class DateTestCase(BaseTestCase):

    def test_full(self):
        grammars = (x[0] for x in self.combinator.extract('21 мая 1996 года'))
        self.assertIn(natasha.Date.Full, grammars)

    def test_full_with_digits(self):
        grammars = (x[0] for x in self.combinator.extract('21/05/1996'))
        self.assertIn(natasha.Date.FullWithDigits, grammars)
        grammars = (x[0] for x in self.combinator.extract('21 05 1996'))
        self.assertIn(natasha.Date.FullWithDigits, grammars)

    def test_day_and_month(self):
        grammars = (x[0] for x in self.combinator.extract('21 мая'))
        self.assertIn(natasha.Date.DayAndMonth, grammars)

    def test_year(self):
        grammars = (x[0] for x in self.combinator.extract('21 год'))
        self.assertIn(natasha.Date.Year, grammars)

    def test_year_float(self):
        grammar, tokens = next(self.combinator.extract('1.5 года'))
        self.assertEqual(grammar, natasha.Date.Year)
        self.assertEqual(type(tokens[0].value), float)

    def test_partial_year(self):
        grammars = (x[0] for x in self.combinator.extract('в конце 2015 года'))
        self.assertIn(natasha.Date.PartialYearObject, grammars)

    def test_partial_month(self):
        grammar, match = next(self.combinator.extract('в конце мая'))
        self.assertEqual(grammar, natasha.Date.PartialMonthObject)

    def test_month(self):
        grammar, match = next(self.combinator.extract('мая'))
        self.assertEqual(grammar, natasha.Date.Month)

    def test_day_of_week(self):
        grammar, match = next(self.combinator.extract('в пятницу'))
        self.assertEqual(grammar, natasha.Date.DayOfWeek)

    def test_day_range(self):
        grammars = (x[0] for x in self.combinator.extract('18-19 ноября'))
        self.assertIn(natasha.Date.DayRange, grammars)

    def test_year_range(self):
        grammars = (x[0] for x in self.combinator.extract('18-20 лет'))
        self.assertIn(natasha.Date.YearRange, grammars)

class GeoTestCase(BaseTestCase):

    def test_federal_district(self):
        grammar, match = next(self.combinator.extract('северо-западный федеральный округ'))
        self.assertEqual(grammar, natasha.Geo.FederalDistrict)

    def test_federal_district_abbr(self):
        grammar, match = next(self.combinator.extract('северо-западный ФО'))
        self.assertEqual(grammar, natasha.Geo.FederalDistrictAbbr)

    def test_region(self):
        grammar, match = next(self.combinator.extract('северо-западная область'))
        self.assertEqual(grammar, natasha.Geo.Region)
        with self.assertRaises(StopIteration):
            next(self.combinator.extract('северо-западный область'))

    def test_complex_object(self):
        grammar, match = next(self.combinator.extract('северный кипр'))
        self.assertEqual(grammar, natasha.Geo.ComplexObject)
        with self.assertRaises(StopIteration):
            next(self.combinator.extract('северная кипр'))

    def test_partial_object(self):
        grammar, match = next(self.combinator.extract('на юго-западе кипра'))
        self.assertEqual(grammar, natasha.Geo.PartialObject)

    def test_object(self):
        grammar, match = next(self.combinator.extract('Москва́'))
        self.assertEqual(grammar, natasha.Geo.Object)

class MoneyTestCase(BaseTestCase):

    def test_int_object_with_prefix(self):
        grammars = (x[0] for x in self.combinator.extract('1 миллион долларов'))
        self.assertIn(natasha.Money.ObjectWithPrefix, grammars)

    def test_int_object_with_abbr_prefix(self):
        grammar, tokens = next(self.combinator.extract('1 млрд. долларов'))
        self.assertEqual(grammar, natasha.Money.ObjectWithPrefix)
        self.assertEqual(type(tokens[0].value), int)

    def test_float_object_with_prefix(self):
        grammars = (x[0] for x in self.combinator.extract('1.2 миллиона долларов'))
        self.assertIn(natasha.Money.ObjectWithPrefix, grammars)

    def test_float_object_with_abbr_prefix(self):
        grammars = (x[0] for x in self.combinator.extract('1.2 млрд. долларов'))
        self.assertIn(natasha.Money.ObjectWithPrefix, grammars)

    def test_int_object(self):
        grammar, tokens = next(self.combinator.extract('10 долларов'))
        self.assertEqual(grammar, natasha.Money.Object)
        self.assertEqual(type(tokens[0].value), int)

    def test_float_object(self):
        grammar, tokens = next(self.combinator.extract('1.5 рубля'))
        self.assertEqual(grammar, natasha.Money.Object)
        self.assertEqual(type(tokens[0].value), float)

    def test_object_without_actual_number(self):
        grammar, match = next(self.combinator.extract('миллион долларов'))
        self.assertEqual(grammar, natasha.Money.ObjectWithoutActualNumber)

    def test_hand_written_numbers(self):
        grammar, tokens = next(self.combinator.extract('сто рублей'))
        self.assertEqual(tokens[0].value, 'сто')
        self.assertEqual(grammar, natasha.Money.HandwrittenNumber)

    def test_hand_written_numbers_with_prefix(self):
        grammars = (x[0] for x in self.combinator.extract('два миллиона долларов'))
        self.assertIn(natasha.Money.HandwrittenNumberWithPrefix, grammars)
        grammars = (x[0] for x in self.combinator.extract('семьдесят пять тысяч рублей'))
        self.assertIn(natasha.Money.HandwrittenNumberWithPrefix, grammars)

class OrganisationTestCase(BaseTestCase):

    def test_official_abbr_quoted(self):
        grammar, match = next(self.combinator.extract('ПАО «Газпром»'))
        self.assertEqual(grammar, natasha.Organisation.OfficialAbbrQuoted)

    def test_abbr(self):
        grammar, match = next(self.combinator.extract('МВД'))
        self.assertEqual(grammar, natasha.Organisation.Abbr)

    def test_individual_entrepreneur(self):
        grammars = (x[0] for x in self.combinator.extract('ИП Иванов Иван Иванович'))
        self.assertIn(natasha.Organisation.IndividualEntrepreneur, grammars)

    def test_simple_latin(self):
        grammars = (x[0] for x in self.combinator.extract('агентство Bloomberg'))
        self.assertIn(natasha.Organisation.SimpleLatin, grammars)
