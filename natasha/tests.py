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
