import unittest
import natasha

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.combinator = natasha.Combinator(natasha.DEFAULT_GRAMMARS)

class PersonGrammarsTestCase(BaseTestCase):

    def test_full(self):
        grammar, rule, _ = next(self.combinator.extract("Шерер Анна Павловна"))
        self.assertEqual(grammar, natasha.Person)
        self.assertEqual(rule, "Full")

    def test_full_reversed(self):
        grammar, rule, _ = next(self.combinator.extract("Анна Павловна Шерер"))
        self.assertEqual(grammar, natasha.Person)
        self.assertEqual(rule, "FullReversed")

    def test_firstname_and_lastname(self):
        grammar, rule, _ = next(self.combinator.extract("Анна Шерер"))
        self.assertEqual(grammar, natasha.Person)
        self.assertEqual(rule, "FisrtnameAndLastname")

    def test_lastname_and_firstname(self):
        grammar, rule, _ = next(self.combinator.extract("Шерер Анна"))
        self.assertEqual(grammar, natasha.Person)
        self.assertEqual(rule, "LastnameAndFirstname")

    def test_lastname(self):
        grammar, rule, _ = next(self.combinator.extract("Шерер"))
        self.assertEqual(grammar, natasha.Person)
        self.assertEqual(rule, "Lastname")

    def test_firstname(self):
        grammar, rule, _ = next(self.combinator.extract("Анна"))
        self.assertEqual(grammar, natasha.Person)
        self.assertEqual(rule, "Firstname")

class DateTestCase(BaseTestCase):

    def test_full(self):
        grammar, rule, _ = next(self.combinator.extract("21 мая 1996 года"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "Full")

    def test_full_with_digits(self):
        grammar, rule, _ = next(self.combinator.extract("21/05/1996"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "FullWithDigits")
        grammar, rule, _ = next(self.combinator.extract("21 05 1996"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "FullWithDigits")

    def test_day_and_month(self):
        grammar, rule, _ = next(self.combinator.extract("21 мая"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "DayAndMonth")

    def test_year(self):
        grammar, rule, _ = next(self.combinator.extract("21 год"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "Year")

    def test_year_float(self):
        grammar, rule, _ = next(self.combinator.extract("1.5 года"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "YearFloat")

    def test_partial_year(self):
        grammar, rule, _ = list(self.combinator.extract("в конце 2015 года"))[-1]
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "PartialYearObject")

    def test_partial_month(self):
        grammar, rule, _ = next(self.combinator.extract("в конце мая"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "PartialMonthObject")

    def test_month(self):
        grammar, rule, _ = next(self.combinator.extract("мая"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "Month")

    def test_day_of_week(self):
        grammar, rule, _ = next(self.combinator.extract("в пятницу"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "DayOfWeek")
