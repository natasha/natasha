import unittest
import natasha


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.combinator = natasha.Combinator(natasha.DEFAULT_GRAMMARS)

class PersonGrammarsTestCase(BaseTestCase):

    def test_full(self):
        grammar, match = list(self.combinator.extract('Шерер Анна Павловна'))[3]
        self.assertEqual(grammar, natasha.Person.Full)

    def test_full_reversed(self):
        grammar, match = list(self.combinator.extract('Анна Павловна Шерер'))[2]
        self.assertEqual(grammar, natasha.Person.FullReversed)

    def test_firstname_and_lastname(self):
        grammar, match = list(self.combinator.extract('Анна Шерер'))[1]
        self.assertEqual(grammar, natasha.Person.FisrtnameAndLastname)

    def test_lastname_and_firstname(self):
        grammar, match = list(self.combinator.extract('Шерер Анна'))[1]
        self.assertEqual(grammar, natasha.Person.LastnameAndFirstname)

    def test_lastname(self):
        grammar, match = next(self.combinator.extract('Шерер'))
        self.assertEqual(grammar, natasha.Person.Lastname)

    def test_firstname(self):
        grammar, match = next(self.combinator.extract('Анна'))
        self.assertEqual(grammar, natasha.Person.Firstname)

    def test_initials_and_lastname(self):
        grammar, match = next(self.combinator.extract('в имении Л. А. Раневской'))
        self.assertEqual(grammar, natasha.Person.InitialsAndLastname)

class DateTestCase(BaseTestCase):

    def test_full(self):
        grammar, match = list(self.combinator.extract('21 мая 1996 года'))[2]
        self.assertEqual(grammar, natasha.Date.Full)

    def test_full_with_digits(self):
        grammar, match = next(self.combinator.extract('21/05/1996'))
        self.assertEqual(grammar, natasha.Date.FullWithDigits)
        grammar, match = next(self.combinator.extract('21 05 1996'))
        print(grammar, match)
        self.assertEqual(grammar, natasha.Date.FullWithDigits)

    def test_day_and_month(self):
        grammar, match = next(self.combinator.extract('21 мая'))
        self.assertEqual(grammar, natasha.Date.DayAndMonth)

    def test_year(self):
        grammar, ((match, *_), *_) = next(self.combinator.extract('21 год'))
        self.assertEqual(grammar, natasha.Date.Year)
        self.assertEqual(type(match), int)

    def test_year_float(self):
        grammar, ((match, *_), *_) = next(self.combinator.extract('1.5 года'))
        self.assertEqual(grammar, natasha.Date.Year)
        self.assertEqual(type(match), float)

    def test_partial_year(self):
        grammar, rule = list(self.combinator.extract('в конце 2015 года'))[-1]
        self.assertEqual(grammar, natasha.Date.PartialYearObject)

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
        grammar, match = next(self.combinator.extract('18-19 ноября'))
        self.assertEqual(grammar, natasha.Date.DayRange)

    def test_year_range(self):
        grammar, match = next(self.combinator.extract('18-20 лет'))
        self.assertEqual(grammar, natasha.Date.YearRange)

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
        grammar, ((match, *_), *_) = next(self.combinator.extract('1 миллион долларов'))
        self.assertEqual(grammar, natasha.Money.ObjectWithPrefix)
        self.assertEqual(type(match), int)

    def test_int_object_with_abbr_prefix(self):
        grammar, ((match, *_), *_) = next(self.combinator.extract('1 млрд. долларов'))
        self.assertEqual(grammar, natasha.Money.ObjectWithPrefix)
        self.assertEqual(type(match), int)

    def test_float_object_with_prefix(self):
        grammar, ((match, *_), *_) = next(self.combinator.extract('1.2 миллиона долларов'))
        self.assertEqual(grammar, natasha.Money.ObjectWithPrefix)
        self.assertEqual(type(match), float)

    def test_float_object_with_abbr_prefix(self):
        grammar, ((match, *_), *_) = next(self.combinator.extract('1.2 млрд. долларов'))
        self.assertEqual(grammar, natasha.Money.ObjectWithPrefix)
        self.assertEqual(type(match), float)

    def test_int_object(self):
        grammar, ((match, *_), *_) = next(self.combinator.extract('10 долларов'))
        self.assertEqual(grammar, natasha.Money.Object)
        self.assertEqual(type(match), int)

    def test_float_object(self):
        grammar, ((match, *_), *_) = next(self.combinator.extract('1.5 рубля'))
        self.assertEqual(grammar, natasha.Money.Object)
        self.assertEqual(type(match), float)

    def test_object_without_actual_number(self):
        grammar, match = next(self.combinator.extract('миллион долларов'))
        self.assertEqual(grammar, natasha.Money.ObjectWithoutActualNumber)

    def test_hand_written_numbers(self):
        grammar, ((match, *_), *_) = next(self.combinator.extract('сто рублей'))
        self.assertEqual(match, 'сто')
        self.assertEqual(grammar, natasha.Money.HandwrittenNumber)

    def test_hand_written_numbers_with_prefix(self):
        grammar, ((match, *_), *_) = next(self.combinator.extract('два миллиона долларов'))
        self.assertEqual(match, 'два')
        self.assertEqual(grammar, natasha.Money.HandwrittenNumberWithPrefix)
        grammar, ((head, *_), (tail, *_), *_) = next(self.combinator.extract('семьдесят пять тысяч рублей'))
        self.assertEqual(head, 'семьдесят')
        self.assertEqual(tail, 'пять')
        self.assertEqual(grammar, natasha.Money.HandwrittenNumberWithPrefix)

class OrganisationTestCase(BaseTestCase):

    def test_official_abbr_quoted(self):
        grammar, match = next(self.combinator.extract('ПАО «Газпром»'))
        self.assertEqual(grammar, natasha.Organisation.OfficialAbbrQuoted)

    def test_abbr(self):
        grammar, match = next(self.combinator.extract('МВД'))
        self.assertEqual(grammar, natasha.Organisation.Abbr)

    def test_individual_entrepreneur(self):
        grammar, match = list(self.combinator.extract('ИП Иванов Иван Иванович'))[-1]
        self.assertEqual(grammar, natasha.Organisation.IndividualEntrepreneur)

    def test_simple_latin(self):
        grammar, rule = list(self.combinator.extract('агентство Bloomberg'))[-1]
        self.assertEqual(grammar, natasha.Organisation.SimpleLatin)
