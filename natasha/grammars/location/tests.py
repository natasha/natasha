# coding: utf-8
from __future__ import unicode_literals


import natasha
import unittest

from natasha.tests import BaseTestCase
from natasha.grammars.location import LocationObject, AddressObject

from yargy.normalization import get_normalized_text
from yargy.interpretation import InterpretationEngine


class LocationTestCase(BaseTestCase):

    def test_federal_district(self):
        grammar, match = list(
            self.combinator.extract('северо-западный федеральный округ'))[0]
        self.assertEqual(grammar, natasha.Location.FederalDistrict)
        self.assertEqual(
            ['северо-западный', 'федеральный', 'округ'], [x.value for x in match])

    def test_autonomous_district(self):
        grammar, match = list(
            self.combinator.extract('Ямало-Ненецкого автономного округа'))[0]
        self.assertEqual(grammar, natasha.Location.AutonomousDistrict)
        self.assertEqual(
            ['Ямало-Ненецкого', 'автономного', 'округа'], [x.value for x in match])

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
        self.assertEqual(grammar, natasha.Location.AdjfFederation)
        self.assertEqual(['Донецкой', 'народной', 'республике'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Соединенными Штатами Америки')
            )
        )[0]
        self.assertEqual(grammar, natasha.Location.AdjxFederation)
        self.assertEqual(['Соединенными', 'Штатами', 'Америки'], [x.value for x in match])

class StreetTestCase(BaseTestCase):

    def test_adj_full(self):
        grammar, match = list(self.combinator.extract('на зеленой улице'))[0]
        self.assertEqual(grammar, natasha.Street.AdjFull)
        self.assertEqual(['зеленой', 'улице'], [x.value for x in match])

        grammar, match = list(self.combinator.extract('около красной площади'))[0]
        self.assertEqual(grammar, natasha.Street.AdjFull)
        self.assertEqual(['красной', 'площади'], [x.value for x in match])

        # TODO: this grammar fails on pypy
        # grammar, match = list(
        #     self.combinator.resolve_matches(
        #         self.combinator.extract('улица Красная Набережная')
        #     )
        # )[0]
        # self.assertEqual(grammar, natasha.Street.AdjFull)
        # self.assertEqual(['Красная', 'Набережная'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('вторая московская улица')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjFull)
        self.assertEqual(['вторая', 'московская', 'улица'], [x.value for x in match])

    def test_adj_short(self):
        grammar, match = list(self.combinator.extract('ул. Нижняя Красносельская'))[0]
        self.assertEqual(grammar, natasha.Street.AdjShort)
        self.assertEqual(['ул', '.', 'Нижняя', 'Красносельская'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пл. Ленина')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjShort)
        self.assertEqual(['пл', '.', 'Ленина'], [x.value for x in match])

    def test_adj_short_reversed(self):

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('московская ул.')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjShortReversed)
        self.assertEqual(['московская', 'ул', '.'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Настасьинский пер.')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjShortReversed)
        self.assertEqual(['Настасьинский', 'пер', '.'], [x.value for x in match])

    def test_adj_full_reversed(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Зеленая')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjFullReversed)
        self.assertEqual(['улица', 'Зеленая'], [x.value for x in match])

    def test_adj_noun_full(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Красной Гвардии')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjNounFull)
        self.assertEqual(['улица', 'Красной', 'Гвардии'], [x.value for x in match])

    def test_adj_noun_short(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. Брянской пролетарской дивизии')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjNounShort)
        self.assertEqual(['ул', '.', 'Брянской', 'пролетарской', 'дивизии'], [x.value for x in match])

    def test_gent_full(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Николая Ершова улица')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentFull)
        self.assertEqual(['Николая', 'Ершова', 'улица'], [x.value for x in match])

    def test_gent_short(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('Обуховской Обороны пр-кт')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentShort)
        self.assertEqual(['Обуховской', 'Обороны', 'пр-кт'], [x.value for x in match])

    def test_gent_full_reversed(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('проспект Юрия Гагарина')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentFullReversed)
        self.assertEqual(['проспект', 'Юрия', 'Гагарина'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Богомягкова')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentFullReversed)
        self.assertEqual(['улица', 'Богомягкова'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица Федосеенко')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentFullReversed)
        self.assertEqual(['улица', 'Федосеенко'], [x.value for x in match])

    def test_gent_full_reversed_with_shortcut(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица К. Маркса')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentFullReversedWithShortcut)
        self.assertEqual(['улица', 'К', '.', 'Маркса'], [x.value for x in match])

    def test_gent_full_reversed_with_extended_shortcut(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица В. В. Ленина')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentFullReversedWithExtendedShortcut)
        self.assertEqual(['улица', 'В', '.', 'В', '.', 'Ленина'], [x.value for x in match])

    def test_gent_short_reversed(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр. Маршала Жукова')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentShortReversed)
        self.assertEqual(['пр', '.', 'Маршала', 'Жукова'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пл. Металлургов')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentShortReversed)
        self.assertEqual(['пл', '.', 'Металлургов'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр-т Культуры')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentShortReversed)
        self.assertEqual(['пр-т', 'Культуры'], [x.value for x in match])

        # TODO:
        # grammar, match = list(
        #     self.combinator.resolve_matches(
        #         self.combinator.extract('ул. Розы Люксембург')
        #     )
        # )[0]
        # self.assertEqual(grammar, natasha.Street.GentShortReversed)
        # self.assertEqual(['ул', '.', 'Розы', 'Люксембург'], [x.value for x in match])

    def test_gent_short_reversed_with_shortcut(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр. М. Жукова')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentShortReversedWithShortcut)
        self.assertEqual(['пр', '.', 'М', '.', 'Жукова'], [x.value for x in match])

    def test_gent_short_reversed_with_extended_shortcut(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр. В. В. Ленина')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentShortReversedWithExtendedShortcut)
        self.assertEqual(['пр', '.', 'В', '.', 'В', '.', 'Ленина'], [x.value for x in match])

    def test_numeric_adj_full(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('2-я новорублевская улица')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjFullWithNumericPart)
        self.assertEqual([2, '-', 'я', 'новорублевская', 'улица'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('1-й бадаевский проезд')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjFullWithNumericPart)
        self.assertEqual([1, '-', 'й', 'бадаевский', 'проезд'], [x.value for x in match])

    def test_numeric_adj_full_reversed(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('улица 1-я промышленная')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjFullReversedWithNumericPart)
        self.assertEqual(['улица', 1, '-', 'я', 'промышленная'], [x.value for x in match])

    def test_numeric_adj_short(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('1-я промышленная ул.')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjShortWithNumericPart)
        self.assertEqual([1, '-', 'я', 'промышленная', 'ул', '.'], [x.value for x in match])

        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('1-й басманный пер.')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjShortWithNumericPart)
        self.assertEqual([1, '-', 'й', 'басманный', 'пер', '.'], [x.value for x in match])

    def test_numeric_adj_short_reversed(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('ул. 1-я промышленная')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.AdjShortReversedWithNumericPart)
        self.assertEqual(['ул', '.', 1, '-', 'я', 'промышленная'], [x.value for x in match])

    def test_numeric_gent_full_reversed_with_numeric_prefix(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('проспект 50 лет октября')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentFullReversedWithNumericPrefix)
        self.assertEqual(['проспект', 50, 'лет', 'октября'], [x.value for x in match])

        # TODO:
        # grammar, match = list(
        #     self.combinator.resolve_matches(
        #         self.combinator.extract('площадь 1905 года')
        #     )
        # )[0]
        # self.assertEqual(grammar, natasha.Street.GentFullReversedWithNumericPrefix)
        # self.assertEqual(['площадь', 1905, 'года'], [x.value for x in match])


    def test_numeric_gent_short_reversed_with_numeric_prefix(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('пр-т. 50 лет советской власти')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentShortReversedWithNumericPrefix)
        self.assertEqual(['пр-т', '.', 50, 'лет', 'советской', 'власти'], [x.value for x in match])

        # TODO:        
        # grammar, match = list(
        #     self.combinator.resolve_matches(
        #         self.combinator.extract('ул. 9 мая')
        #     )
        # )[0]
        # self.assertEqual(grammar, natasha.Street.GentShortReversedWithNumericPrefix)
        # self.assertEqual(['ул', '.', 9, 'мая'], [x.value for x in match])

    def test_numeric_gent_splitted_by_full_descriptor(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('7-я улица текстильщиков')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentNumericSplittedByFullDescriptor)
        self.assertEqual([7, '-', 'я', 'улица', 'текстильщиков'], [x.value for x in match])

    def test_numeric_gent_splitted_by_short_descriptor(self):
        grammar, match = list(
            self.combinator.resolve_matches(
                self.combinator.extract('7-я ул. текстильщиков')
            )
        )[0]
        self.assertEqual(grammar, natasha.Street.GentNumericSplittedByShortDescriptor)
        self.assertEqual([7, '-', 'я', 'ул', '.', 'текстильщиков'], [x.value for x in match])


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


ADDRESS_TESTS = '''
# Главная-Контакты-Магазины-Касторама Краснодар, ул. Стасова/ул. Сормовская, д. 178-180/1, лит. Е
# 	Сормовская улица
# 	178-180/1

# Ростов-на-Дону ул.Варфоломеева д.222а/108а.
# 	улица Варфоломеева
# 	222А/108А

105066 г. Москва. Ул. Нижняя Красносельская д. 40/12 к. 20 офис 610
	Нижняя Красносельская улица
	40/12к20

420030, г. Казань, ул. Восстания, д. 100, корп. 266 ДК, офис 510
	улица Восстания
	100к266

105066, г. Москва, ул. Нижняя Красносельская д.40/12 , корп.10
	Нижняя Красносельская улица
	40/12к10

ул. 1-я Бухвостова, д.12/11, корп. 12
	1-я улица Бухвостова
	12/11к12

# г. Пермь, ул. Героев Хасана, 105, корпус 17/2,
# 	улица Героев Хасана
# 	105к17/2

Адрес: 620141, г.Екатеринбург, ул. Артинская, д. 12-Б, офис 41
	Артинская улица
	12Б

Адрес: 107076, Москва, 1-я ул. Бухвостова, д.12/11 к.12, оф103 Схема проезда
	1-я улица Бухвостова
	12/11к12

620141, г.Екатеринбург, ул. Артинская, д. 12-Б, офис 41
	Артинская улица
	12Б

Юридический адрес: 105066, г. Москва, ул. Нижняя красносельская д.40/12, корп. 20
	Нижняя Красносельская улица
	40/12к20

Юр. Адрес:107045 г. Москва, ул. Садовая-Спасская, д. 12/23, стр.2
	Садовая-Спасская улица
	12/23с2

Москва, ул. Садовническая, д. 76/71, стр.1
	Садовническая улица
	76/71с1

Адрес: 410002 г.Саратов, ул. Мичурина 144/148
	улица Мичурина
	144/148

# 115035, г. Москва, Космодамианская наб., д. 40-42, стр. 3 (помещение ТАРП ЦАО)
# 	Космодамианская набережная
# 	40/42с3

Почтовый адрес 450005, Республика Башкортостан, г.Уфа, ул. Цюрупы, 100/102
	улица Цюрупы
	100/102

# Почтовый адрес: 127055, г. Москва, ул. Бутырский Вал д. 68/70, стр. 1, офис 38
# 	улица Бутырский Вал
# 	68/70с1

# Россия, г. Москва, ул. Бакунинская, дом. 26/30, 105082
# 	Бакунинская улица
# 	26/30

# 119017, г. Москва, ул. Пятницкая, дом 40-42, строение 1.
# 	Пятницкая улица
# 	40-42с1

1. Для отправки писем по России просьба пользоваться адресом: Россия, 117997, г. Москва, улица Миклухо-Маклая, д.16/10, офис 74-413
	улица Миклухо-Маклая
	16/10

Адрес: 105064, г. Москва, Яковоапостольский пер, д. 11/13, стр. 4, оф. 9
	Яковоапостольский переулок
	11/13с4

# Россия , 350059, г. Краснодар, ул. Стасова, 178-180/1 (ТК «Галактика»)
# 	улица Стасова
# 	178-180/1

(C) ФГБОУ ДПО РМАПО 2016   I   125993, г. Москва, ул. Баррикадная, д.2/1, стр.1   I   +7 (499) 252-21-04   I
	Баррикадная улица
	2/1с1

115114, Россия, г. Москва, ул. Летниковская, д.11/10 стр.1
	Летниковская улица
	11/10с1

2.Высшая школа Экономики по адресу:г. Москва, Покровский бульвар, д.11
	Покровский бульвар
	11

г. Пермь, шоссе Космонавтов, 316/16а
	шоссе Космонавтов
	316/16А

Адрес: 443068, Россия, г. Самара, ул. Ново-Садовая, д. 106, корп. 155
	Ново-Садовая улица
	106к155

2-ой Силикатный пр-д, д.14, кор.1, стр.20
	2-й Силикатный проезд
	14к1с20

# Адрес: ул.Ленинский проспект дом 121/1 корпус 3
# 	Ленинский проспект
# 	121/1к3

# Адрес: 105613, Москва, Измайловское шоссе, д.71, корпус 4ГД, офис 3Д3. Гостиничный комплекс "Измайлово", корпус "Дельта"
# 	Измайловское шоссе
# 	71к4Г-Д

# 125047\. г. Москва, ул. Миусская 1-я. д.24/22,стр.3 оф. 7Д
# 	1-я Миусская улица
# 	24/22с3

Адрес: 129223, г. Москва, проспект Мира, д. 119, стр. 559, 2й этаж
	проспект Мира
	119с559

109147, г. Москва, ул. Воронцовская, д 13/14, стр.1
	Воронцовская улица
	13/14с1

Адрес офиса ООО НПП "Ирвис": Казань, ул. Восстания, д. 100, корпус 214, офис 15, проезд и проход через Северную проходную Технополиса "Химград".
	улица Восстания
	100к214

# 127055, г.Москва, ул.Новослободская (ст. м. Савеловская) д.73/68 стр.1, оф. 21
# 	Новослободская улица
# 	73/68с1

Адрес: 117218, г. Москва, ул. Кржижановского, д. 21/33, корп. 1
	улица Кржижановского
	21/33к1

г. Самара, ул. Ново-Садовая, 106, корп. 170
	Ново-Садовая улица
	106к170

# Адрес: 190020, Санкт - Петербург, Набережная обводного канала., д.223-225
# 	набережная Обводного канала
# 	223-225

# 109012, г. Москва, ул. Никольская, д. 10/2, стр 2Б, станция метро Лубянка.
# 	Никольская улица
# 	10/2с2Б

# Адрес: Санкт-Петербург, ул. Садовая, д. 28-30, к. 5
# 	Садовая улица
# 	28-30к5

Наш адрес: Россия, 107497, г. Москва, ул. Амурская 9/6
	Амурская улица
	9/6

г.Москва, Щелковское шоссе, д.100, корп.108
	Щёлковское шоссе
	100к108

г. Саратов, ул. Советская, д. 83/89
	Советская улица
	83/89

# 119002, г. Москва, ул. Сивцев Вражек, 29/16, офис 416
# 	переулок Сивцев Вражек
# 	29/16

ул. Ново-Садовая, дом 106, корп. 155, офис 605Б, ТЦ "Захар"
	Ново-Садовая улица
	106к155

105043, г.Москва, ул.Измайловский б-р, д.12/31, стр.1
	Измайловский бульвар
	12/31с1

# г. Казань, ул. Восстания, 100, 41а
# 	улица Восстания
# 	100к43А

# Адрес:  123317, г. Москва, Пресненская наб., д.10, блок С, «Москва-Сити», Башня на набережной, 5 этаж
# 	Пресненская набережная
# 	10блокС

Готовый.сайт, ООО • Проспект Победы, дом 290, офис 501, Челябинск
	проспект Победы
	290

123557, Москва, Электрический пер., д.3/10, офис 539    тел. (499)255-58-05       e-mail: stroytir@mail.ru   |  С т р о и т е л ь с т в о
	Электрический переулок
	3/10

# г. Краснодар, ул. Бородинская, 150, 11 показать на карте
# 	Бородинская улица
# 	150/11

Пермь, ул.Г. Хасана, 105, к.19
	улица Героев Хасана
	105к19

# ул. Волочаевская, д.12А, стр. 1А, ТЦ "РТС"
# 	Волочаевская улица
# 	12Ас1А

Наш адрес: Москва, м. Братиславская, ул. Верхние поля, д. 11, корп. 1
	улица Верхние Поля
	11к1

РФ, 117418, г. Москва, ул. Новочеремушкинская д. 44, корп. 1, комн.115
	Новочерёмушкинская улица
	44к1

Адрес: 193015, г. Санкт-Петербург, ул .Кавалергардская, д.14, пом. 1 Н
	Кавалергардская улица
	14

656056, Россия, г. Барнаул, ул. Л. Толстого, 16
	улица Льва Толстого
	16

# Адрес: улица Достоевского 44, корпус Е 191119 Санкт-Петербург,
# 	улица Достоевского
# 	40кЕ

# Для корреспонденции: 107031, г. Москва, ул. Большая Дмитровка, д. 12/1, стр. 3
# 	улица Большая Дмитровка
# 	12/1с3

Адрес местонахождения органа по сертификации продукции: 115093, Москва, Партийный переулок, дом 1, корпус 58, строение 1, офис 331
	Партийный переулок
	1к58с1

+7 (495) 229-89-80Москва, Зеленый пр-кт., д. 5/12, офис 236
	Зелёный проспект
	5/12

м. Чистые пруды, ул. Мясницкая, 24/7, стр. 1
	Мясницкая улица
	24/7с1

Юр. адрес: 414000, г. Астрахань, ул. Бакинская д.149
	Бакинская улица
	149

ул. Садовая д.11,
	Садовая улица
	11

Адрес: 350000, Россия, г. Краснодар, ул. Октябрьская, 135
	Октябрьская улица
	135

Адрес: г. Москва, Рязанский проспект, д. 86/1, оф. 3
	Рязанский проспект
	86/1

# Адрес: 443080, г. Самара, ул. Санфировой, д. 95, литер 4
# 	улица Санфировой
# 	95лит4

117587, г. Москва, Варшавское шоссе, дом 125Ж, корпус 6
	Варшавское шоссе
	125Жк6

г.Сызрань, ул.К. Маркса 67,  тел. 8 (8464) 98-43-67
	улица Карла Маркса
	67

(C) 2011-2014, ООО «Компания Энергоремонт». | 107140, г. Москва, ул. Краснопрудная, д. 12/1, стр. 1, пом. 15-17
	Краснопрудная улица
	12/1с1

Адрес: 344022, Ростов-на-Дону, Социалистическая ул. 197
	Социалистическая улица
	197

© 2016 Компания ООО «СУАР-Групп»             СПб., пр. Обуховской Обороны, д. 112, к 2, оф. 204
	проспект Обуховской Обороны
	112к2

Наш адрес: г. Ростов-на-Дону, пр. Театральный, д. 97 (угол с ул. Малюгиной)
	Театральный проспект
	97

г. Санкт-Петербург, ул. Салова 27А, бизнес-центр "СтартСервис", 3-й этаж
	улица Салова
	27А

# г. Пермь, ул. Героев Хасана, 105, корпус 71
# 	улица Героев Хасана
# 	105к71

344014, г.Ростов-на-Дону, ул. Красноармейская 298/81
	Красноармейская улица
	298/81

445007, РФ, Самарская обл, Тольятти, Новозаводская улица, дом 2А, строение 326
	Новозаводская улица
	2Ас326

# ул. Героев Танкограда, 71п, ст.10
# 	улица Героев Танкограда
# 	71Пс10

Общество с ограниченной ответственностью «Управляющая компания «Энергия» Директор: Ким Сон Ок Адрес: 664033, г. Иркутск, ул. Лермонтова, д. 279/10 ИНН/КПП 3808226131/381201001, ОГРН 1123850040027 40702810600350000849...
	улица Лермонтова
	279/10

# 350000, г.Краснодар, ул. Красноармейская, д. 64, лит. В, офис 4.
# 	Красноармейская улица
# 	64В

634024, г. Томск, ул.Профсоюзная, 28/1 стр. 3, пом. 1001
	Профсоюзная улица
	28/1с3

Адрес: г. Москва, Волгоградский проспект, 183
	Волгоградский проспект
	183

117587, г. Москва, Варшавское шоссе, д. 125 Д, корп. 1
	Варшавское шоссе
	125Дк1

# Наш адрес: г. Москва,  ул. Старокирочный пер.,  д. 16/2, стр. 2
# 	Старокирочный переулок
# 	16/2с2

Санкт-Петербург, Лиговский пр. д.10 оф.212
	Лиговский проспект
	10

м.Выхино, Москва, Рязанский проспект, д.86/1, 9 этаж.
	Рязанский проспект
	86/1

344032, г. Ростов-на-Дону, ул. Красноармейская, 298/81
	Красноармейская улица
	298/81

344091, Россия, г. Ростов-на-Дону, ул. 2-я Краснодарская, 145/11
	2-я Краснодарская улица
	145/11

Адрес: Россия, Москва, Рязанский проспект, д. 86/1, стр. 2
	Рязанский проспект
	86/1с2

Адрес: Россия 680038 г. Хабаровск ул. Серышева 22
	улица Серышева
	22

Адрес: г.Ростов-на-Дону, ул.Варфоломеева, 261/81
	улица Варфоломеева
	261/81

г. Новосибирск, ул. Станционная, д. 38, корпус 28
	Станционная улица
	38к28

394087, г. Воронеж, ул. Ломоносова, д. 114/13, оф. 2
	улица Ломоносова
	114/13

Почт адрес: 610035, г. Киров, ул. Производственная, д. 28.
	Производственная улица
	28

г. Москва, ул. Угрешская д.18/1 на территории ГУП МОСГОРТРАНС
	Угрешская улица
	18/1

115093 г.Москва, Партийный пер., д.1, корп.58, стр.3, офис 405, офис 406
	Партийный переулок
	1к58с3

г. Москва, Варшавское шоссе, д. 141, стр. 80.
	Варшавское шоссе
	141с80

Адрес: 109542, г. Москва, Рязанский проспект, д.86/1, стр.3, офис 416
	Рязанский проспект
	86/1с3

# г. Краснодар, ул. Онежская, 60, Б
# 	Онежская улица
# 	60Б

# ул. Пестеля, 13/15, лит. Б, пом. 6
# 	улица Пестеля
# 	13/15Б

Юридический адрес: РФ, 105082, г. Москва, Спартаковская площадь, д. 1/7, стр. 10
	Спартаковская площадь
	1/7с10

Юридический адрес: 620017, город Екатеринбург, проспект Космонавтов, 18, корпус 101, пом. 301
	проспект Космонавтов
	18к101

# 107031, город Москва, улица Большая Дмитровка, дом 32, строение 7-8
# 	улица Большая Дмитровка
# 	32с7-8

# Адпксс: 190020 Санкт-Петербург, набережная Обводного канала, д.134, корп.12 литер А
# 	набережная Обводного канала
# 	134Ак12

ЖСК "Лазурь",115580 Москва, Задонский проезд, д. 15 корп. 2, кв.421
	Задонский проезд
	15к2

119991, Москва, ГСП-1, 5-й Донской проезд, д. 21Б, корп. 2, офис 37.
	5-й Донской проезд
	21Бк2

Адрес: 115093, г.Москва, Партийный пер., д.1, корп.57, стр.3, офис 35
	Партийный переулок
	1к57с3

г. Москва 109202, ул. 1-ая Фрезерная, д. 2/1 стр. 10
	1-я Фрезерная улица
	2/1с10

г.Павловский Посад, ул.Городковская, д.73А
	Городковская улица
	73А

Юридический адрес: 125190, г. Москва, Ленинградский проспект, д. 45Г, корп. 14
	Ленинградский проспект
	45Гк14

Адрес: г. Москва, Рязанский проспект, д. 81/1, стр. 2
	Рязанский проспект
	81/1с2

Адрес склада: Россия, Московская область, Люберецкий район, п. Томилино, ул. Гоголя, д. 39/1
	улица Гоголя
	39/1

Адрес: г. Сургут, ул. Островского, 37/1 к3
	улица Островского
	37/1к3

# Адрес: Россия, 129085, г.Москва, ул. Проспект Мира, д.101В стр.2 (м. Алексеевская)
# 	проспект Мира
# 	101Вс2

# по адресу: ул. Пречистенка 12/2, С.9, вход с Чертольского переулка!
# 	улица Пречистенка
# 	12/2с9

# 115088, г. Москва, ул. Рязанский проспект, д. 86, ст. метро Выхино (15 мин. пешком, рядом - 100 метров МКАД)
# 	Рязанский проспект
# 	86

Москва, ул. Яузская, д.1/15 стр.6
	Яузская улица
	1/15с6

# г. Рязань, ул. Связи, стр. 29 "Б"
# 	улица Связи
# 	с29Б

664050, г. Иркутск, ул. Байкальская, 295/14
	Байкальская улица
	295/14

Склад находится по адресу: г.Москва ,ул.Угрешская 18/1с1,  складской комплекс ГУП "Мосгортранс".
	Угрешская улица
	18/1с1

г. Санкт-Петербург, ул. Садовая, д. 11
	Садовая улица
	11

пер. Журавлева, д. 40.
	переулок Журавлева
	40

Юридический адрес: 101000, город Москва , ул.Мясницкая , д. 22, стр. 1
	Мясницкая улица
	22с1

# Офис компании расположен по адресу: 109542, г.Москва, ул.Рязанский проспект, д.86/1, офис 507 (5 этаж). Это последниий дом по Рязанскому проспекту, перед МКАД.
# 	Рязанский проспект
# 	86/1

Юридический адрес Ассоциации «СЦ НАСТХОЛ»: Россия, 125315, г. Москва, 1-й Балтийский пер., д.6/21, корп.3
	1-й Балтийский переулок
	6/21к3

# 115054, Москва, ул. Валовая, 2-4/44, стр. 1
# 	Валовая улица
# 	2-4/44с1

Центр оперативной печати: г. Казань, ул. Х. Такташа, д.105 (На карте)
	улица Хади Такташа
	105

123423 г. Москва, ул. Народного Ополчения, д. 11, 143
	улица Народного Ополчения
	11

Юридический адрес: | 107023, г. Москва, Семеновский пер., д.11, стр.1, офис 423
	Семёновский переулок
	11с1

117587, г. Москва, Варшавское шоссе, 125Ж к. 6
	Варшавское шоссе
	125Жк6

354008, г.Сочи, ул. Виноградная, 43/2, корп.3
	Виноградная улица
	43/2к3

ул.А. Матросова 30л, стр.21
	улица Александра Матросова
	30Лс21

Москва, ул. Бауманская, д. 68/8, строение 1
	Бауманская улица
	68/8с1

# 660061, город Красноярск, ул. Геологическая 2-я, д. 32, офис 1-06
# 	2-я Геологическая улица
# 	32

127055, г. Москва, ул. Новослободская, д. 50/1, стр.1, кв.12
	Новослободская улица
	50/1с1

101999, Москва, Балаклавский пр-т, д. 28 стр.1, офис 6
	Балаклавский проспект
	28с1

127495, г. Москва, Дмитровское шоссе, д.163А, корп.2, БЦ «SK PLAZA», офис 15.4
	Дмитровское шоссе
	163Ак2

Фактический адрес: | 125130 , г. Москва, Старопетровский пр-д, д. 7А, стр. 30
	Старопетровский проезд
	7Ас30

129223, г.Москва, пр-кт Мира, д.119/70(атх)
	проспект Мира
	119/70

Москва, Кировоградская улица, дом 23А, корпус 1 (Южное Чертаново, Южный округ)
	Кировоградская улица
	23Ак1

Москва, Пятницкая ул., д. 65 на карте
	Пятницкая улица
	65

450001, г Уфа, ул Пархоменко, д. 153/1
	улица Пархоменко
	153/1

город Москва, Профсоюзная улица, д. 152к3
	Профсоюзная улица
	152к3

Адрес: г. Астрахань, ул. Бабушкина, 68, офис 307
	улица Бабушкина
	68

199155, г. Санкт-Петербург, ул. Уральская, д. 10, к. 1
	Уральская улица
	10к1

142200, Московская обл, г. Серпухов, ул. Советская, д. 31/21
	Советская улица
	31/21

423800 г. Набережные Челны, 7/01, пр. Мира, д. 20/18
	проспект Мира
	20/18

Адрес: 424003, Россия, РМЭ, г. Йошкар-Ола, ул. Лобачевского, д. 12
	улица Лобачевского
	12

Дата и место проведения: 16 февраля, 15:00, г. Уфа, ул. Менделеева 215/4
	улица Менделеева
	215/4

"Двери Зодчий"Санкт-Петербург, пр.Энгельса, д.138, ТК "СтройДвор" цок. этаж
	проспект Энгельса
	138

г. Тольятти, ул. Новозаводская, 2А, строение 58, оф.1
	Новозаводская улица
	2Ас58

119435, г. Москва, Большой Саввинский пер., д. 12, стр. 12
	Большой Саввинский переулок
	12с12

Тургоякское шоссе, 13/23, г. Миасс,
	Тургоякское шоссе
	13/23

ул.Дмитровское шоссе д.100 корп.2
	Дмитровское шоссе
	100к2

г.Москва, Смоленская-Сенная площадь, д.23/ 25.
	Смоленская-Сенная площадь
	23/25

Адрес: г.Москва, 5-й Донской проезд д.15 стр. 11.
	5-й Донской проезд
	15с11

пер. Братский, д. 46/16
	Братский переулок
	46/16

2-й Южнопортовый пр-д, д.20А, стр.4
	2-й Южнопортовый проезд
	20Ас4

Адрес: ул. Чапаева, 39/14, Берёзовский, Свердловская обл., Россия, 623704
	улица Чапаева
	39/14

Адрес в Нижнем Новгороде: 603000, Россия, г. Нижний Новгород, ул. Белинского, д. 58/60 (вход со двора).
	улица Белинского
	58/60

121170, Кутузовский проспект, д.36, строение 11, м. Кутузовская
	Кутузовский проспект
	36с11

Адрес: 623704, Свердловская область, г. Берёзовский, ул. Чапаева, 39 корп.22, оф.1
	улица Чапаева
	39к22

Россия 105187, Москва, ул. Вольная д.28, стр. 16
	Вольная улица
	28с16

г. Чебоксары, ул. Декабристов, дом 43
	улица Декабристов
	43

129343, Россия, г. Москва, Серебрякова проезд, дом № 14, строение 23.
	проезд Серебрякова
	14с23

Наш адрес: 142200, МО, г. Серпухов, ул. Красноармейская, д. 35/60
	Красноармейская улица
	35/60

129343 г. Москва, Серебрякова проезд, дом 14, строение 14.
	проезд Серебрякова
	14с14

Россия, 125315, г. Москва, ул. Усиевича 31 А, стр 2
	улица Усиевича
	31Ас2

ул. Индустриальная, 107, стр.7,
	Индустриальная улица
	107с7

105120, г. Москва, 3-й Сыромятнический переулок, дом 3/9, строение 2
	3-й Сыромятнический переулок
	3/9с2

ул. Островского, д.109/2
	улица Островского
	109/2

117105, г.Москва, Варшавское шоссе, д.26, стр.11, эт.5    ®    ЗАО «УФЛЕКУ и Партнeры»
	Варшавское шоссе
	26с11

Дмитровское шоссе, д. 157 стр. 9, этаж 2, офис 92101
	Дмитровское шоссе
	157с9

Адрес: 195197, Россия, Г. Санкт-Петербург, Ул. Минеральная, д. 13, корпус 28
	Минеральная улица
	13к28

г. Москва, Духовской переулок, 17/15 (2 этаж, офис 5)
	Духовской переулок
	17/15

Ярославское шоссе д. 190 к.2
	Ярославское шоссе
	190к2

Адрес | г.Санкт-Петербург, Пискаревский проспект д.150 литер О.
	Пискарёвский проспект
	150О

ул. Чернышевского, д. 147, с. 1
	улица Чернышевского
	147с1

660079, г.Красноярск, ул.Лесопильщиков, 177, ст.4
	улица Лесопильщиков
	177с4

г.Ростов-на-Дону ул.Доватора 154к5
	улица Доватора
	154к5

ул. Лобова, д. 39,
	улица Лобова
	39

Наш офис: 119454, Москва, пр-т Вернадского, 62а, стр. 2
	проспект Вернадского
	62Ас2

Адрес: 344082, г. Ростов-на-Дону, ул. Красноармейская, 36/62.
	Красноармейская улица
	36/62

Наш адрес:  127486, г. Москва, Бульвар Бескудниковский дом №59А, строение 7
	Бескудниковский бульвар
	59Ас7

# Россия, Московская обл., Мытищинский р-н, Сельское поселение Федоскинское, д. Красная горка, ул. Промышленная, вл. 8.
# 	Промышленная улица
# 	вл4

Адрес: 456313, Россия, Челябинская область, г. Миасс, Тургоякское шоссе, дом 11/64.
	Тургоякское шоссе
	11/64

г. Уфа, ул. Революционная 154/1
	Революционная улица
	154/1

Московская область, г. Серпухов, ул. Центральная, д. 142
	Центральная улица
	142

# 390000, г. Рязань, ул. Южный Промузел, д. 13В, строение 12.
# 	улица Южный Промузел
# 	13Вс7

Адрес: 344025, Россия, г. Ростов-на-Дону, ул. В.Черевичкина, 106/2
	улица Черевичкина
	106/2

ул. Автомоторная, д. 4А, стр. 21
	Автомоторная улица
	4Ас21

# Служба по эксплуатации газового хозяйства г. Благовещенска, Благовещенского района 675000 Благовещенск, ул. Зейская , 245\1
# 	Зейская улица
# 	245/1

Автономная некоммерческая организация «Судебная Экспертиза Недвижимости и Бизнеса» |  г. Москва  117534, г. Москва, ул. Кировоградская, д. 44А, корп. 2  Вельгоша Ангелина Юрьевна
	Кировоградская улица
	44Ак2

г. Мурманск, пр-т Кольский, д. 158/1
	Кольский проспект
	158/1

Адрес: 194354, Россия, Санкт-Петербург, пр.Энгельса, д.115, корп. 2
	проспект Энгельса
	115к2

# Адрес: 350063, г. Краснодар, ул. Кубанская Набережная 37/11, этаж 3
# 	Кубанская набережная
# 	37/11

Адрес: ул. Толмаческая 19, корп. 12.
	Толмачёвская улица
	19к12

# Санкт-Петербург, проспект Энгельса, дом 27, корпус 12В
# 	проспект Энгельса
# 	27к12В

Москва, Дмитровское шоссе, д. 100, стр. 2, офис № 2240
	Дмитровское шоссе
	100с2

г. Москва, Ленинский проспект, дом 1/2, корпус 1, офис 1211 (12 этаж) (5 минут пешком от метро «Октябрьская»)
	Ленинский проспект
	1/2к1

'''


class AddressTestRecord(object):
    def __init__(self, skip, address, street, house):
        self.skip = skip
        self.address = address
        self.street = street
        self.house = house


def parse(data):
    lines = iter(data.lstrip().splitlines())
    for line in lines:
        address = line
        skip = address[0] == '#'
        street = next(lines).lstrip('#\t')
        house = next(lines).lstrip('#\t')
        assert next(lines) == ''
        yield AddressTestRecord(skip, address, street, house)


class AddressTestCase(unittest.TestCase):

    def setUp(self):
        self.combinator = natasha.Combinator([natasha.Address])
        self.engine = InterpretationEngine(AddressObject)


def generate(test):
    def function(self):
        matches = self.combinator.extract(test.address)
        matches = list(self.combinator.resolve_matches(matches))
        records = list(self.engine.extract(matches))
        
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertTrue(record.street_name)
        self.assertEqual(record.normalized_house, test.house)
    return function


for index, test in enumerate(parse(ADDRESS_TESTS)):
    name = 'test_address_%d' % index
    function = generate(test)

    if test.skip:
        function = unittest.skip('just skip')(function)

    function.__name__ = name
    setattr(AddressTestCase, name, function)

del function
