# coding: utf-8
from __future__ import unicode_literals


import natasha

from natasha.tests import BaseTestCase
from natasha.grammars.organisation import OrganisationObject

from yargy.normalization import get_normalized_text
from yargy.interpretation import InterpretationEngine


class OrganisationTestCase(BaseTestCase):

    def test_official_abbr_quoted(self):
        results = list(self.combinator.extract('ПАО «Газпром»'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.OfficialQuoted, grammars)
        self.assertIn(['ПАО', '«', 'Газпром', '»'], values)

        # TODO Wrong first matching from Geo grammar, maybe it needs separated
        # combinator for each Test Case?
        results = list(self.combinator.extract('филиал ОАО «МРСК Юга»'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.OfficialQuoted, grammars)
        self.assertIn(['филиал', 'ОАО', '«', 'МРСК', 'Юга', '»'], values)

        results = list(self.combinator.extract('АО ХК "Якутуголь"'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.OfficialQuoted, grammars)
        self.assertIn(['АО', 'ХК', '"', 'Якутуголь', '"'], values)

        # invalid quotes test case
        results = list(self.combinator.extract(
            'компании».\nОб этом документе слухи в американской пресс"'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertNotIn(natasha.Organisation.OfficialQuoted, grammars)
        self.assertEqual(list(values), [])

        # TODO: match quotes
        # results = list(self.combinator.extract(
        #     'ПАО «НК «Роснефть»'
        # )) 
        # grammars = (x[0] for x in results)
        # values = ([y.value for y in x[1]] for x in results)
        # self.assertIn(natasha.Organisation.OfficialQuoted, grammars)
        # self.assertEqual(list(values), [])

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

    def test_multiword_commercial(self):
        results = list(
            self.combinator.extract('производственное объединение «Алмаз-Антей»'))
        grammars = (x[0] for x in results)
        values = ([y.forms[0]['normal_form'] for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.OfficialQuoted, grammars)
        self.assertIn(
            ['производственный_объединение', '«', 'алмаз-антей', '»'], values)

    def test_education(self):
        results = list(self.combinator.extract(
            'в стенах Санкт-Петербургского государственного университета'))
        grammars = (x[0] for x in results)
        values = ([y.forms[0]['normal_form'] for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.Educational, grammars)
        self.assertEqual(
            list(values), [['санкт-петербургский', 'государственный', 'университет']])

    def test_social(self):
        results = list(self.combinator.extract(
            'в стенах общества андрологии и сексуальной медицины, возле министерства любви и цензуры РФ'))
        grammars = list(x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.Social, grammars)
        self.assertIn(natasha.Location.Object, grammars)
        self.assertEqual(list(values), [
            ['общества', 'андрологии', 'и', 'сексуальной', 'медицины'],
            ['РФ'],
            ['министерства', 'любви', 'и', 'цензуры', 'РФ'],
        ])

        results = list(
            self.combinator.extract('распоряжения правительства РФ'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.Social, grammars)
        self.assertEqual(list(values), [['РФ'], ['правительства', 'РФ']])

        results = list(
            self.combinator.extract('министерством экономического развития РФ'))
        grammars = (x[0] for x in results)
        values = ([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.Social, grammars)
        self.assertEqual(
            list(values), [['РФ'], ['министерством', 'экономического', 'развития', 'РФ']])

        results = list(
            self.combinator.extract('руководству российского парламента'))
        grammars = list(x[0] for x in results)
        values = list([y.value for y in x[1]] for x in results)
        self.assertIn(natasha.Organisation.Social, grammars)
        self.assertIn(['руководству', 'российского', 'парламента'], values)
        self.assertIn(['российского', 'парламента'], values)

class OrganisationInterpretationTestCase(BaseTestCase):

    def setUp(self):
        self.engine = InterpretationEngine(OrganisationObject)
        super(OrganisationInterpretationTestCase, self).setUp()

    def test_get_organisation_object(self):
        matches = self.combinator.resolve_matches(
            self.combinator.extract('ООО "Рога и копыта"')
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].descriptor.value, 'ООО')
        self.assertEqual([x.value for x in objects[0].name], ['Рога', 'и', 'копыта'])

        matches = self.combinator.resolve_matches(
            self.combinator.extract('Санкт-Петербургский государственный университет')
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].descriptor.value, 'университет')
        self.assertEqual([x.value for x in objects[0].name], ['Санкт-Петербургский', 'государственный'])

        matches = self.combinator.resolve_matches(
            self.combinator.extract('филиал ООО "Рога и копыта"')
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 1)
        self.assertEqual([x.value for x in objects[0].descriptor], ['филиал', 'ООО'])
        self.assertEqual([x.value for x in objects[0].name], ['Рога', 'и', 'копыта'])

    def test_coreference_solving(self):
        text = 'ооо "Рога и КаПыта" или общество "рога и копыто"'
        matches = self.combinator.resolve_matches(
            self.combinator.extract(text)
        )
        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 2)

        self.assertEqual(objects[0], objects[1])

        text = 'федеральная служба безопасности (сокращенно, ФСБ)'
        matches = list(
            self.combinator.resolve_matches(
                self.combinator.extract(text)
            )
        )

        objects = list(
            self.engine.extract(matches)
        )
        self.assertEqual(len(objects), 2)
        self.assertEqual(objects[0].abbr, {'фсб'})
        self.assertEqual(objects[1].abbr, {'фсб'})

        self.assertEqual(objects[0], objects[1])
