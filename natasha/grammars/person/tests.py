# coding: utf-8
from __future__ import unicode_literals


import natasha

from natasha.tests import BaseTestCase
from natasha.grammars.person import PersonObject

from yargy.normalization import get_normalized_text
from yargy.interpretation import InterpretationEngine


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
        self.assertIn(natasha.Person.FirstnameAndLastname, grammars)
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

    def test_lastname_and_initials(self):
        results = list(self.combinator.extract('в имении Раневской Л. А.'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.LastnameAndInitials, grammars)
        self.assertIn(['Раневской', 'Л', '.', 'А', '.'], values)

        results = list(self.combinator.extract('Миронова Т.И."'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.LastnameAndInitials, grammars)
        self.assertIn(['Миронова', 'Т', '.', 'И', '.'], list(values))

    def test_gnc_matching(self):
        results = list(self.combinator.extract('есть даже марки машин'))
        self.assertEqual(results, [])

    def test_firstname_and_lastname_with_particle(self):
        results = list(
            self.combinator.extract('Немецкий канцлер Отто фон Бисмарк'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(
            natasha.Person.FirstnameAndLastnameWithNobilityParticle, grammars)
        self.assertIn(['Отто', 'фон', 'Бисмарк'], values)

    def test_person_name_with_position(self):
        results = list(self.combinator.extract('князь Иоанн Грозный'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.WithPosition, grammars)
        self.assertIn(['князь', 'Иоанн', 'Грозный'], values)

        results = list(
            self.combinator.extract('президента РФ Владимира Путина'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.WithPosition, grammars)
        self.assertIn(['президента', 'РФ', 'Владимира', 'Путина'], values)

        results = list(
            self.combinator.extract('исполнителя главной роли сергея шувалова'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.WithPosition, grammars)
        self.assertIn(
            ['исполнителя', 'главной', 'роли', 'сергея', 'шувалова'], values)

        results = list(
            self.combinator.extract('губернатор Камчатки Владимир Илюхин'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.WithPosition, grammars)
        self.assertIn(['губернатор', 'Камчатки', 'Владимир', 'Илюхин'], values)

        results = list(self.combinator.extract(
            'основатель и генеральный директор хостинг-провайдера Timeweb Александр Бойков'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Person.WithPosition, grammars)
        self.assertIn(
            ['директор', 'хостинг-провайдера', 'Timeweb', 'Александр', 'Бойков'], values)

    def test_person_name_with_position_normalization(self):
        results = self.combinator.extract(
            'исполнителя главной роли сергея шувалова')
        for grammar, tokens in results:
            if grammar == natasha.Person.WithPosition:
                normalized = get_normalized_text(tokens)
                self.assertEqual(
                    normalized, 'исполнитель главной роли сергей шувалов')

class PersonInterpretationTestCase(BaseTestCase):

    def setUp(self):
        self.engine = InterpretationEngine(PersonObject)
        super(PersonInterpretationTestCase, self).setUp()

    def test_get_person_object(self):
        matches = self.combinator.resolve_matches(
            self.combinator.extract('иванов иван иванович')
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].firstname.value, 'иван')
        self.assertEqual(objects[0].middlename.value, 'иванович')
        self.assertEqual(objects[0].lastname.value, 'иванов')
        self.assertEqual(objects[0].descriptor, None)

    def test_get_person_gender(self):
        matches = self.combinator.resolve_matches(
            self.combinator.extract('канцлер ФРГ ангела меркель')
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].firstname.value, 'ангела')
        self.assertEqual(objects[0].lastname.value, 'меркель')
        self.assertEqual(objects[0].descriptor.value, 'канцлер')
        genders = sorted(objects[0].gender.most_common(2))
        self.assertEqual(genders, [
            ('femn', 1),
            ('masc', 1),
        ])

        matches = self.combinator.resolve_matches(
            self.combinator.extract('президент РФ владимир путин')
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].firstname.value, 'владимир')
        self.assertEqual(objects[0].lastname.value, 'путин')
        self.assertEqual(objects[0].descriptor.value, 'президент')
        genders = sorted(objects[0].gender.most_common(2))
        self.assertEqual(genders, [
            ('masc', 4),
        ])

        matches = self.combinator.resolve_matches(
            self.combinator.extract('пётр порошенко')
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].firstname.value, 'пётр')
        self.assertEqual(objects[0].lastname.value, 'порошенко')
        self.assertEqual(objects[0].descriptor, None)
        genders = sorted(objects[0].gender.most_common(2))
        self.assertEqual(genders, [
            ('masc', 1),
        ])
