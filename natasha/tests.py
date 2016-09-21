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

    def test_day_range(self):
        grammar, rule, _ = next(self.combinator.extract("18-19 ноября"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "DayRange")

    def test_year_range(self):
        grammar, rule, _ = next(self.combinator.extract("18-20 лет"))
        self.assertEqual(grammar, natasha.Date)
        self.assertEqual(rule, "YearRange")

class GeoTestCase(BaseTestCase):

    def test_federal_district(self):
        grammar, rule, _ = next(self.combinator.extract("северо-западный федеральный округ"))
        self.assertEqual(grammar, natasha.Geo)
        self.assertEqual(rule, "FederalDistrict")

    def test_federal_district_abbr(self):
        grammar, rule, _ = next(self.combinator.extract("северо-западный ФО"))
        self.assertEqual(grammar, natasha.Geo)
        self.assertEqual(rule, "FederalDistrictAbbr")

    def test_region(self):
        grammar, rule, _ = next(self.combinator.extract("северо-западная область"))
        self.assertEqual(grammar, natasha.Geo)
        self.assertEqual(rule, "Region")
        with self.assertRaises(StopIteration):
            next(self.combinator.extract("северо-западный область"))

    def test_complex_object(self):
        grammar, rule, _ = next(self.combinator.extract("северный кипр"))
        self.assertEqual(grammar, natasha.Geo)
        self.assertEqual(rule, "ComplexObject")
        with self.assertRaises(StopIteration):
            next(self.combinator.extract("северная кипр"))

    def test_partial_object(self):
        grammar, rule, _ = next(self.combinator.extract("на юго-западе кипра"))
        self.assertEqual(grammar, natasha.Geo)
        self.assertEqual(rule, "PartialObject")

    def test_object(self):
        grammar, rule, _ = next(self.combinator.extract("Москва́"))
        self.assertEqual(grammar, natasha.Geo)
        self.assertEqual(rule, "Object")

class MoneyTestCase(BaseTestCase):

    def test_int_object_with_prefix(self):
        grammar, rule, _ = next(self.combinator.extract("1 миллион долларов"))
        self.assertEqual(grammar, natasha.Money)
        self.assertEqual(rule, "IntObjectWithPrefix")

    def test_int_object_with_abbr_prefix(self):
        grammar, rule, _ = next(self.combinator.extract("1 млрд. долларов"))
        self.assertEqual(grammar, natasha.Money)
        self.assertEqual(rule, "IntObjectWithPrefix")

    def test_float_object_with_prefix(self):
        grammar, rule, _ = next(self.combinator.extract("1.2 миллиона долларов"))
        self.assertEqual(grammar, natasha.Money)
        self.assertEqual(rule, "FloatObjectWithPrefix")

    def test_float_object_with_abbr_prefix(self):
        grammar, rule, _ = next(self.combinator.extract("1.2 млрд. долларов"))
        self.assertEqual(grammar, natasha.Money)
        self.assertEqual(rule, "FloatObjectWithPrefix")

    def test_int_object(self):
        grammar, rule, _ = next(self.combinator.extract("10 долларов"))
        self.assertEqual(grammar, natasha.Money)
        self.assertEqual(rule, "IntObject")

    def test_float_object(self):
        grammar, rule, _ = next(self.combinator.extract("1.5 рубля"))
        self.assertEqual(grammar, natasha.Money)
        self.assertEqual(rule, "FloatObject")

    def test_object_without_actual_number(self):
        grammar, rule, _ = next(self.combinator.extract("миллион долларов"))
        self.assertEqual(grammar, natasha.Money)
        self.assertEqual(rule, "ObjectWithoutActualNumber")

class OrganisationTestCase(BaseTestCase):

    def test_official_abbr_quoted(self):
        grammar, rule, _ = next(self.combinator.extract("ПАО «Газпром»"))
        self.assertEqual(grammar, natasha.Organisation)
        self.assertEqual(rule, "OfficialAbbrQuoted")

    def test_abbr(self):
        grammar, rule, _ = next(self.combinator.extract("МВД"))
        self.assertEqual(grammar, natasha.Organisation)
        self.assertEqual(rule, "Abbr")

    def test_individual_entrepreneur(self):
        grammar, rule, _ = list(self.combinator.extract("ИП Иванов Иван Иванович"))[-1]
        self.assertEqual(grammar, natasha.Organisation)
        self.assertEqual(rule, "IndividualEntrepreneur")

    def test_simple_latin(self):
        grammar, rule, _ = list(self.combinator.extract("агентство Bloomberg"))[-1]
        self.assertEqual(grammar, natasha.Organisation)
        self.assertEqual(rule, "SimpleLatin")
