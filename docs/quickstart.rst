Пошаговое руководство
=====================

Введение
--------

Natasha - библиотека для поиска и извлечения именованных сущностей (`Named-entity recognition <https://en.wikipedia.org/wiki/Named-entity_recognition>`_) в тексте на естественном языке.

На данный момент мы умеем разбирать:

- Упоминания персон
- Названия организаций
- Топонимы и почтовые адреса
- Названия праздников, конференций и т.д.

Из возможностей парсера стоит отметить:

- Снятие морфологической неоднозначности
- Приведение сущностей к нормальной форме и их склонение
- Извлечение аттрибутов сущностей: для упоминаний персон это имя, фамилия и т.д.
- Разрешение кореференции для упоминаний персон, организаций и топонимов

Подготовка
----------

Прежде всего, необходимо установить необходимые пакеты. Это можно сделать следующим образом:

.. code-block:: text

  $ pip install natasha==0.6.0


Если вы используете CPython, рекомендуем также поставить "быструю" версию pymorphy2 - морфологического анализатора, который лежит в основе нашей библиотеки:

.. code-block:: text

  $ pip install pymorphy2[fast]

Извлекаем упоминания
--------------------

Первым шагом в этом руководстве является извлечение упоминаний - определенных частей текста, которые попадают под заданные правила.

.. code-block:: python

  from natasha import Combinator, DEFAULT_GRAMMARS

  # DEFAULT_GRAMMARS содержит стандартный набор правил:
  # [
  #    <enum 'Person'>,
  #    <enum 'Location'>,
  #    <enum 'Organisation'>,
  #           ...
  # ]

  text = "Василий Иванович родился в Нижнем Новгороде"

  # Создаем экземпляр парсера
  combinator = Combinator(DEFAULT_GRAMMARS)

  # Передаем разбираемый текст в метод extract
  # и перебираем полученные результаты
  for grammar, tokens in combinator.extract(text):
      print("Правило:", grammar)
      print("Токены:", tokens)
      print("---")

В результате можно увидеть что-то похожее:

.. code-block:: text

  Правило: Person.Firstname
  Токены: [
    Token('Василий', (0, 7), [
      {
        'grammemes': {
          'sing',
          'anim',
          'nomn',
          'masc',
          'Name',
          'NOUN',
        },
        'normal_form': 'василий',
      },
    ])
  ]
  ---
  Правило: Person.FirstnameAndMiddlename
  Токены: [
    Token('Василий', (0, 7), [
      {
        'grammemes': {
          'sing',
          'anim',
          'nomn',
          'masc',
          'Name',
          'NOUN',
        },
        'normal_form': 'василий',
      },
    ]),
    Token('Иванович', (8, 16), [
      {
        'grammemes': {
          'sing',
          'Patr',
          'anim',
          'nomn',
          'masc',
          'NOUN',
        },
        'normal_form': 'иван',
      }
    ])]
  ---

Рассмотрим полученный результат подробнее.

На каждую найденную сущность, парсер возвращает два объекта:

- Правило по которому произошел разбор
- Список токенов, подходящих под правило

Каждый токен имеет несколько аттрибутов:

- Оригинальное содержимое - `token.value`
- Позиция в тексте, в формате **(start, end)** - `token.position`
- Список словоформ с морфологической информацией - `token.forms`

Как можно заметить, для одного упоминания персоны, парсер вернул несколько результатов.
Это связанно с особенностью алгоритма, лежащего в основе парсера - GLR, который параллельно обрабатывает все объявленные правила.

Для того, чтобы отсеять неполные разборы, необходимо использовать метод `resolve_matches`:

.. code-block:: python

  from natasha import Combinator, DEFAULT_GRAMMARS

  text = "иван васильевич"
  combinator = Combinator(DEFAULT_GRAMMARS)

  # метод resolve_matches выбирает наиболее полный разбор
  # из нескольких пересекающихся вариантов
  results = combinator.resolve_matches(
      combinator.extract(text)
  )

  for grammar, tokens in results:
      # т.к. мы заранее знаем, что сначала по тексту идет имя,
      # а потом фамилия, можно обращаться к токенам напрямую
      print("Имя:", tokens[0].value)
      print("Фамилия:", tokens[1].value)

Иногда бывает так, что сущности разных типов пересекаются - например, должность персоны содержит название организации, и если необходимо правильно обрабатывать такие случаи, можно передать аргумент `strict=False` в метод `resolve_matches`:

.. code-block:: python

  from natasha import Combinator
  from natasha.grammars import Person, Organisation


  text = "представитель администрации президента россии федор смирнов"

  combinator = Combinator([
      Person,
      Organisation,
  ])

  # при strict=False, resolve_matches не отбрасывает
  # пересекающиеся грамматики разных классов,
  # например, упоминание персоны с должностью,
  # содержащее название организации, как в этом примере

  matches = combinator.resolve_matches(
      combinator.extract(text), strict=False
  )
  matches = (
      # преобразуем результат парсера в более читаемый формат:
      # (правило, [список, оригинальных, совпадений])
      (grammar, [t.value for t in tokens]) for (grammar, tokens) in matches
  )

  assert list(matches) == [
      # персона
      (Person.WithPosition, [
          "представитель",
          "администрации",
          "президента",
          "россии",
          "федор",
          "смирнов",
      ]),
      # организация
      (Organisation.Social, [
          "администрации",
          "президента",
          "россии",
      ]),
  ]

Извлекаем объекты
-----------------

Так как оперировать токенами или, проще говоря, кусками текста - не так-то удобно (например, для упоминания персоны - имя может быть как на первом месте в тексте, так и идти после фамилии), в этом разделе мы рассмотрим другую ключевую возможность парсера - извлечение объектов.

Парсер строит объект из заранее извлеченных упоминаний, в правилах которых были объявлены специальные поля с информацией о принадлежности тех или иных слов к аттрибутам результирующего класса. Если вы не собираетесь писать свои грамматики - это не имеет значения, иначе мы рассмотрим это чуть позже.

.. code-block:: python

  from yargy.interpretation import InterpretationEngine

  from natasha import Combinator
  from natasha.grammars import Person
  from natasha.grammars.person import PersonObject

  text = 'василия петровича на заводе уважали все'

  combinator = Combinator([
      Person,
  ])

  matches = combinator.resolve_matches(
      combinator.extract(text),
  )

  # InterpretationEngine создает экземпляры получаемого класса
  # из извлеченных упоминаний
  engine = InterpretationEngine(PersonObject)

  persons = list(
      engine.extract(matches)
  )

  assert len(persons) == 1

  print('Аттрибуты (оригинальное значение)')
  print('Имя:', persons[0].firstname)
  print('Отчество:', persons[0].middlename)
  print('Фамилия:', persons[0].lastname)

В результате можно увидеть: 

.. code-block:: text

  Аттрибуты (оригинальное значение)
  Имя: Token('василия', (0, 7), ...)
  Отчество: Token('петровича', (8, 17), ...)
  Фамилия: None

Дополнительно, для объектов персон, существуют специальные методы упрощающие нормализацию:

.. code-block:: python

  print('Аттрибуты (нормализованное значение)')
  print('Имя:', persons[0].normalized_firstname)
  print('Отчество:', persons[0].normalized_middlename)
  print('Фамилия:', persons[0].normalized_lastname)

.. code-block:: text

  Аттрибуты (нормализованное значение)
  Имя: василий
  Отчество: петрович
  Фамилия: None

На данный момент доступны следующие типы объектов с извлекаемыми аттрибутами:

- Персона `(natasha.grammars.person.PersonObject)`
    - **firstname** - имя
    - **middlename** - отчество
    - **lastname** - фамилия
    - **descriptor** - должность, например, `президент`
    - **descriptor_destination** - несклоняемая часть должности, например, `президент [российской федерации]` 
- Организация `(natasha.grammars.organisation.OrganisationObject)`
    - **name** - название, `Санкт-Петербургский государственный`
    - **descriptor** - дескриптор, `университет`
- Топоним `(natasha.grammars.location.LocationObject)`
    - **name** - название, `Российская`
    - **descriptor** - дескриптор, `Федерация`
- Почтовый адрес `(natasha.grammars.location.AddressObject)`
    - **street_name** - название улицы, `Реки Фонтанки`
    - **street_descriptor** - дескриптор улицы, `набережная`
    - **house_number** - номер дома, `33`
    - **house_number_letter** - литера дома, `А / Б и т.д.`
