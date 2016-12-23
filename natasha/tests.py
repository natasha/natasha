# coding: utf-8
from __future__ import unicode_literals

try:
    range = xrange
except NameError:
    range = range

import sys
import unittest
import natasha


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.combinator = natasha.Combinator(natasha.DEFAULT_GRAMMARS)

class PersonGrammarsTestCase(BaseTestCase):

    def test_full(self):
        results = list(self.combinator.extract('Шерер Анна Павловна'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.Full, grammars)
        self.assertIn(['Шерер', 'Анна', 'Павловна'], values)

    def test_full_reversed(self):
        results = list(self.combinator.extract('Анна Павловна Шерер'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.FullReversed, grammars)
        self.assertIn(['Анна', 'Павловна', 'Шерер'], values)

    def test_firstname_and_lastname(self):
        results = list(self.combinator.extract('Анна Шерер'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.FisrtnameAndLastname, grammars)
        self.assertIn(['Анна', 'Шерер'], values)

    def test_lastname_and_firstname(self):
        results = list(self.combinator.extract('Шерер Анна'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.LastnameAndFirstname, grammars)
        self.assertIn(['Шерер', 'Анна'], values)

    def test_lastname(self):
        grammar, matches = next(self.combinator.extract('Шерер'))
        self.assertEqual(grammar, natasha.Person.Lastname)
        self.assertEqual(matches[0].value, 'Шерер')

    def test_firstname(self):
        grammar, matches = next(self.combinator.extract('Анна'))
        self.assertEqual(grammar, natasha.Person.Firstname)
        self.assertEqual(matches[0].value, 'Анна')

    def test_initials_and_lastname(self):
        results = list(self.combinator.extract('в имении Л. А. Раневской'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.InitialsAndLastname, grammars)
        self.assertIn(['Л', '.', 'А', '.', 'Раневской'], values)

    def test_gnc_matching(self):
        results = list(self.combinator.extract('есть даже марки машин'))
        self.assertEqual(results, [])

class DateTestCase(BaseTestCase):

    def test_full(self):
        results = list(self.combinator.extract('21 мая 1996 года'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.Full, grammars)
        self.assertIn([21, 'мая', 1996], values)

    def test_full_with_digits(self):
        results = list(self.combinator.extract('21/05/1996'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.FullWithDigits, grammars)
        self.assertIn([21, '/', 5, '/', 1996], values)
        results = list(self.combinator.extract('21 05 1996'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.FullWithDigits, grammars)
        self.assertIn([21, 5, 1996], values)

    def test_day_and_month(self):
        results = list(self.combinator.extract('21 мая'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.DayAndMonth, grammars)
        self.assertIn([21, 'мая'], values)

    def test_year(self):
        results = list(self.combinator.extract('21 год'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.Year, grammars)
        self.assertIn([21, 'год'], values)

    def test_year_float(self):
        grammar, tokens = next(self.combinator.extract('1.5 года'))
        self.assertEqual(grammar, natasha.Date.Year)
        self.assertEqual(type(tokens[0].value), float)
        self.assertEqual(tokens[0].value, 1.5)

    def test_partial_year(self):
        results = list(self.combinator.extract('в конце 2015 года'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.PartialYearObject, grammars)
        self.assertIn(['конце', 2015, 'года'], values)

    def test_partial_month(self):
        results = list(self.combinator.extract('в конце мая'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.PartialMonthObject, grammars)
        self.assertIn(['конце', 'мая'], values)

    def test_month(self):
        grammar, match = next(self.combinator.extract('мая'))
        self.assertEqual(grammar, natasha.Date.Month)
        self.assertEqual(match[0].value, 'мая')

    def test_day_of_week(self):
        grammar, match = next(self.combinator.extract('в пятницу'))
        self.assertEqual(grammar, natasha.Date.DayOfWeek)
        self.assertEqual(match[0].value, 'пятницу')

    @unittest.skipIf(sys.version_info.major < 3, 'python 2 and pypy creates different objects for same xrange calls')
    def test_day_range(self):
        results = list(self.combinator.extract('18-19 ноября'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.DayRange, grammars)
        self.assertIn([range(18, 19), 'ноября'], values)

    @unittest.skipIf(sys.version_info.major < 3, 'python 2 and pypy creates different objects for same xrange calls')
    def test_year_range(self):
        results = list(self.combinator.extract('18-20 лет'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.YearRange, grammars)
        self.assertIn([range(18, 20), 'лет'], values)

class GeoTestCase(BaseTestCase):

    def test_federal_district(self):
        grammar, match = next(self.combinator.extract('северо-западный федеральный округ'))
        self.assertEqual(grammar, natasha.Geo.FederalDistrict)
        self.assertEqual(['северо-западный', 'федеральный', 'округ'], [x.value for x in match])

    def test_federal_district_abbr(self):
        grammar, match = next(self.combinator.extract('северо-западный ФО'))
        self.assertEqual(grammar, natasha.Geo.FederalDistrictAbbr)
        self.assertEqual(['северо-западный', 'ФО'], [x.value for x in match])

    def test_region(self):
        grammar, match = next(self.combinator.extract('северо-западная область'))
        self.assertEqual(grammar, natasha.Geo.Region)
        self.assertEqual(['северо-западная', 'область'], [x.value for x in match])
        with self.assertRaises(StopIteration):
            next(self.combinator.extract('северо-западный область'))

    def test_complex_object(self):
        grammar, match = next(self.combinator.extract('северный кипр'))
        self.assertEqual(grammar, natasha.Geo.ComplexObject)
        with self.assertRaises(StopIteration):
            next(self.combinator.extract('северная кипр'))

    @unittest.skip('skip for now, because need to know something about gent(2?)+loct(2?) cases concordance')
    def test_partial_object(self):
        grammar, match = next(self.combinator.extract('на юго-западе кипра'))
        self.assertEqual(grammar, natasha.Geo.PartialObject)

    def test_object(self):
        grammar, match = next(self.combinator.extract('Москва́'))
        self.assertEqual(grammar, natasha.Geo.Object)
        self.assertEqual(['Москва'], [x.value for x in match])

class MoneyTestCase(BaseTestCase):

    def test_int_object_with_prefix(self):
        results = list(self.combinator.extract('1 миллион долларов'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Money.ObjectWithPrefix, grammars)
        self.assertIn([1, 'миллион', 'долларов'], values)

    def test_int_object_with_abbr_prefix(self):
        grammar, tokens = next(self.combinator.extract('1 млрд. долларов'))
        self.assertEqual(grammar, natasha.Money.ObjectWithPrefix)
        self.assertEqual(type(tokens[0].value), int)
        self.assertEqual([1, 'млрд', '.', 'долларов'], [x.value for x in tokens])

    def test_float_object_with_prefix(self):
        results = list(self.combinator.extract('1.2 миллиона долларов'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Money.ObjectWithPrefix, grammars)

    def test_float_object_with_abbr_prefix(self):
        results = list(self.combinator.extract('1.2 млрд. долларов'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Money.ObjectWithPrefix, grammars)

    def test_int_object(self):
        grammar, tokens = next(self.combinator.extract('10 долларов'))
        self.assertEqual(grammar, natasha.Money.Object)
        self.assertEqual(type(tokens[0].value), int)
        self.assertEqual([10, 'долларов'], [x.value for x in tokens])

    def test_float_object(self):
        grammar, tokens = next(self.combinator.extract('1.5 рубля'))
        self.assertEqual(grammar, natasha.Money.Object)
        self.assertEqual(type(tokens[0].value), float)
        self.assertEqual([1.5, 'рубля'], [x.value for x in tokens])

    def test_object_without_actual_number(self):
        grammar, match = next(self.combinator.extract('миллион долларов'))
        self.assertEqual(grammar, natasha.Money.ObjectWithoutActualNumber)
        self.assertEqual(['миллион', 'долларов'], [x.value for x in match])

    def test_hand_written_numbers(self):
        grammar, tokens = next(self.combinator.extract('сто рублей'))
        self.assertEqual(tokens[0].value, 'сто')
        self.assertEqual(grammar, natasha.Money.HandwrittenNumber)

    def test_hand_written_numbers_with_prefix(self):
        results = list(self.combinator.extract('два миллиона долларов'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Money.HandwrittenNumberWithPrefix, grammars)
        self.assertIn(['два', 'миллиона', 'долларов'], values)
        results = list(self.combinator.extract('семьдесят пять тысяч рублей'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Money.HandwrittenNumberWithPrefix, grammars)
        self.assertIn(['семьдесят', 'пять', 'тысяч', 'рублей'], values)

class OrganisationTestCase(BaseTestCase):

    def test_official_abbr_quoted(self):
        grammar, match = next(self.combinator.extract('ПАО «Газпром»'))
        self.assertEqual(grammar, natasha.Organisation.OfficialAbbrQuoted)
        self.assertEqual(['ПАО', '«', 'Газпром', '»'], [x.value for x in match])

    def test_abbr(self):
        grammar, match = next(self.combinator.extract('МВД'))
        self.assertEqual(grammar, natasha.Organisation.Abbr)
        self.assertEqual(['МВД'], [x.value for x in match])

    def test_individual_entrepreneur(self):
        results = list(self.combinator.extract('ИП Иванов Иван Иванович'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.IndividualEntrepreneur, grammars)
        self.assertIn(['ИП', 'Иванов', 'Иван', 'Иванович'], values)

    def test_simple_latin(self):
        results = list(self.combinator.extract('агентство Bloomberg'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.SimpleLatin, grammars)
        self.assertIn(['агентство', 'Bloomberg'], values)

    def test_education(self):
        results = list(self.combinator.extract('в стенах Санкт-Петербургского государственного университета'))
        grammars = (x[0] for x in results)
        values = ([y.forms[0]['normal_form'] for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.Educational, grammars)
        self.assertEqual(list(values), [['санкт-петербургский', 'государственный', 'университет']])

    def test_social(self):
        results = list(self.combinator.extract('в стенах общества андрологии и сексуальной медицины, возле министерства любви и цензуры РФ'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.Social, grammars)
        self.assertEqual(list(values), [
            ['общества', 'андрологии', 'и', 'сексуальной', 'медицины'],
            ['министерства', 'любви', 'и', 'цензуры', 'РФ'],
        ])


class EventsTestCase(BaseTestCase):

    def test_object(self):
        grammar, match = next(self.combinator.extract('шоу «Пятая империя»'))
        self.assertEqual(grammar, natasha.Event.Object)
        self.assertEqual(['шоу', '«', 'Пятая', 'империя', '»'], [x.value for x in match])
