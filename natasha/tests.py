# coding: utf-8
from __future__ import unicode_literals

try:
    range = xrange
except NameError:
    range = range

import sys
import platform
import unittest
import natasha

from yargy.normalization import get_normalized_text


class BaseTestCase(unittest.TestCase):

    def setUp(self, grammars=natasha.DEFAULT_GRAMMARS):
        self.combinator = natasha.Combinator(grammars)

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

    @unittest.skipIf(sys.version_info.major < 3, 'python 2 creates different objects for same xrange calls')
    @unittest.skipIf(platform.python_implementation() == 'PyPy', 'pypy & pypy3 have same semantics for range objects')
    def test_day_range(self):
        results = list(self.combinator.extract('18-19 ноября'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.DayRange, grammars)
        self.assertIn([range(18, 19), 'ноября'], values)

    @unittest.skipIf(sys.version_info.major < 3, 'python 2 creates different objects for same xrange calls')
    @unittest.skipIf(platform.python_implementation() == 'PyPy', 'pypy & pypy3 have same semantics for range objects')
    def test_year_range(self):
        results = list(self.combinator.extract('18-20 лет'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.YearRange, grammars)
        self.assertIn([range(18, 20), 'лет'], values)

    def test_month_with_offset(self):
        results = list(self.combinator.extract('в прошлом январе'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.MonthWithOffset, grammars)
        self.assertIn(['прошлом', 'январе'], values)

        results = list(self.combinator.extract('в следующая январь'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertNotIn(natasha.Date.MonthWithOffset, grammars)
        self.assertNotIn(['следующая', 'январе'], values)

    def test_day_of_week_with_offset(self):
        results = list(self.combinator.extract('в прошлую пятницу'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.DayOfWeekWithOffset, grammars)
        self.assertIn(['прошлую', 'пятницу'], values)

        results = list(self.combinator.extract('в следующая понедельник'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertNotIn(natasha.Date.DayOfWeekWithOffset, grammars)
        self.assertNotIn(['следующая', 'понедельник'], values)

    def test_current_month_with_offset(self):
        results = list(self.combinator.extract('в следующем месяце'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Date.CurrentMonthWithOffset, grammars)
        self.assertIn(['следующем', 'месяце'], values)

        results = list(self.combinator.extract('в прошлых месяц'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertNotIn(natasha.Date.CurrentMonthWithOffset, grammars)
        self.assertNotIn(['прошлых', 'месяц'], values)

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
        self.assertEqual(
            [1, 'млрд', '.', 'долларов'], [x.value for x in tokens])

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
        results = list(
            self.combinator.extract('одиннадцать миллиардов долларов'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Money.HandwrittenNumberWithPrefix, grammars)
        self.assertIn(['одиннадцать', 'миллиардов', 'долларов'], values)
        results = list(self.combinator.extract('семьдесят пять тысяч рублей'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Money.HandwrittenNumberWithPrefix, grammars)
        self.assertIn(['семьдесят', 'пять', 'тысяч', 'рублей'], values)


class EventsTestCase(BaseTestCase):

    def test_object(self):
        grammar, match = next(self.combinator.extract('шоу «Вернувшиеся»'))
        self.assertEqual(grammar, natasha.Event.Object)
        self.assertEqual(
            ['шоу', '«', 'Вернувшиеся', '»'], [x.value for x in match])

    def test_adj_with_descriptor(self):
        grammar, match = next(
            self.combinator.extract('в рамках ближневосточного форума прошла встреча ...'))
        self.assertEqual(grammar, natasha.Event.AdjWithDescriptor)
        self.assertEqual(
            ['ближневосточного', 'форума'], [x.value for x in match])
