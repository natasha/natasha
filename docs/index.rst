
Natasha
=======

Natasha — библиотека для поиска и извлечения именованных сущностей
(`Named-entity
recognition <https://en.wikipedia.org/wiki/Named-entity_recognition>`__)
из текстов на русском языке. В библиотеке собраны грамматики и словари
для парсера `Yargy <https://github.com/natasha/yargy>`__.

Использование
-------------

Natasha имеет лаконичный интерфейс. Доступны экстракторы для имён,
адресов, сумм денег, дат и некоторых других сущностей.

.. code:: python

    from natasha import (
        NamesExtractor,
        DatesExtractor,
        MoneyExtractor,
    )   

Экстрактор принимает на вход текст и возвращается список метчей:

.. code:: python

    extractor = NamesExtractor()
    text = '''
    Простите, еще несколько цитат из приговора. «…Отрицал существование
    Иисуса и пророка Мухаммеда», «наделял Иисуса Христа качествами
    ожившего мертвеца — зомби» [и] «качествами покемонов —
    представителей бестиария японской мифологии, тем самым совершил
    преступление, предусмотренное статьей 148 УК РФ
    '''
    matches = extractor(text)
    matches




.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">
    Простите, еще несколько цитат из приговора. «…Отрицал существование
    <mark>Иисуса</mark> и пророка <mark>Мухаммеда</mark>», «наделял <mark>Иисуса Христа</mark> качествами
    ожившего мертвеца - зомби» [и] «качествами покемонов -
    представителей бестиария японской мифологии, тем самым совершил
    преступление, предусмотренное статьей 148 УК РФ
    </div>



Каждый метч имеет два основных атрибута: ``span`` и ``fact``. ``span``
определяет границы метча:

.. code:: python

    for match in matches:
        start, stop = match.span
        print(start, stop, text[start:stop])


.. parsed-literal::

    69 75 Иисуса
    86 95 Мухаммеда
    107 120 Иисуса Христа


В ``fact`` находится объект с атрибутами:

.. code:: python

    for index, match in enumerate(matches):
        print(index, match.fact)


.. parsed-literal::

    0 Name(first='иисус', middle=None, last=None, nick=None)
    1 Name(first='мухаммед', middle=None, last=None, nick=None)
    2 Name(first='иисус', middle=None, last='христос', nick=None)


Разные экстракторы возвращают разные типы объектов:

.. code:: python

    extractor = DatesExtractor()
    text = '''
    Я посмотрел на инфляцию в России, взял период с декабря 2002 года
    по декабрь 2015 года Инфляция 246%.
    
    14.14 29 июня 2016 года:   Наиболее ожесточенные бои ночью шли под
    Дебальцево
    '''
    matches = extractor(text)
    matches




.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">
    Я посмотрел на инфляцию в России, взял период с <mark>декабря 2002 года</mark>
    по <mark>декабрь 2015 года</mark> Инфляция 246%.
    
    14.14 <mark>29 июня 2016 года</mark>:   Наиболее ожесточенные бои ночью шли под
    Дебальцево
    </div>



.. code:: python

    for index, match in enumerate(matches):
        print(index, match.fact)


.. parsed-literal::

    0 Date(year=2002, month=12, day=None)
    1 Date(year=2015, month=12, day=None)
    2 Date(year=2016, month=6, day=29)


У некоторых сущностей есть дополнительные атрибуты, например, у сумм
есть атрибут ``normalized``:

.. code:: python

    extractor = MoneyExtractor()
    text = 'В 1995 году стоимость 1 доллара была около 800 рублей 50 копеек'''
    matches = extractor(text)
    matches




.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">В 1995 году стоимость <mark>1 доллара</mark> была около <mark>800 рублей 50 копеек</mark></div>



.. code:: python

    for index, match in enumerate(matches):
        print(index, repr(match.fact.normalized))


.. parsed-literal::

    0 Money(1, 'USD')
    1 Money(800.5, 'RUB')


Справочник
----------

.. code:: python

    from natasha import (
        NamesExtractor,
        SimpleNamesExtractor,
        PersonExtractor,
    
        LocationExtractor,
        AddressExtractor,
    
        OrganisationExtractor,
    
        DatesExtractor,
    
        MoneyExtractor,
        MoneyRateExtractor,
        MoneyRangeExtractor,
    )   
    
    from natasha.markup import (
        show_markup_notebook as show_markup,
        format_json
    )

NamesExtractor
~~~~~~~~~~~~~~

.. code:: python

    extractor = NamesExtractor()
    
    text = """
    Благодарственное письмо   Хочу поблагодарить учителей моего, теперь уже бывшего, одиннадцатиклассника:  Бушуева Вячеслава Владимировича и Бушуеву Веру Константиновну. Они вовлекали сына в интересные внеурочные занятия, связанные с театром и походами.
    
    Благодарю прекрасного учителя 1"А" класса - Волкову Наталью Николаевну, нашего наставника, тьютора - Ларису Ивановну, за огромнейший труд, чуткое отношение к детям, взаимопонимание! Огромное спасибо!
    """
    
    matches = extractor(text)
    spans = [_.span for _ in matches]
    facts = [_.fact.as_json for _ in matches]
    show_markup(text, spans)
    print(format_json(facts))



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">
    Благодарственное письмо   Хочу поблагодарить учителей моего, теперь уже бывшего, одиннадцатиклассника:  <mark>Бушуева Вячеслава Владимировича</mark> и <mark>Бушуеву Веру Константиновну</mark>. Они вовлекали сына в интересные внеурочные занятия, связанные с театром и походами.
    
    Благодарю прекрасного учителя 1"А" класса - <mark>Волкову Наталью Николаевну</mark>, нашего наставника, тьютора - <mark>Ларису Ивановну</mark>, за огромнейший труд, чуткое отношение к детям, взаимопонимание! Огромное спасибо!
    </div>


.. parsed-literal::

    [
      {
        "first": "вячеслав",
        "middle": "владимирович",
        "last": "бушуев"
      },
      {
        "first": "вера",
        "middle": "константиновна",
        "last": "бушуева"
      },
      {
        "first": "наталья",
        "middle": "николаевна",
        "last": "волкова"
      },
      {
        "first": "лариса",
        "middle": "ивановна"
      }
    ]


SimpleNamesExtractor
~~~~~~~~~~~~~~~~~~~~

``NamesExtractor`` на самом деле использует не только правила для
извлечения имён. Предварительно текст прогоняется через CRF-теггер,
правила запускаются только на слов, где сработал теггер. Это сделано,
чтобы учитывать контекст. Например, алгоритм не должен срабатывать на
фразе (сейчас он срабатывает, но не должен, но задумка такая) "5 июля во
Владимире состоит", "Владимир" здесь не имя. Учесть это только с помощью
правил Yargy нельзя.

``SimpleNames`` не использует CRF, его стоит применять, когда известно,
что в строке только имена.

.. code:: python

    extractor = SimpleNamesExtractor()
    
    lines = [
        'Мустафа Джемилев',
        'Егору Свиридову',
        'Стрыжак Алеся',
        'владимир путин',
        'плаксюк саша',
    
        'О. Дерипаска',
        'Ищенко Е.П.',
    ]
    
    for line in lines:
        matches = extractor(line)
        match = matches[0]
        fact = match.fact.as_json
        print(line)
        print(format_json(fact))


.. parsed-literal::

    Мустафа Джемилев
    {
      "first": "мустафа",
      "last": "джемилев"
    }
    Егору Свиридову
    {
      "first": "егор",
      "last": "свиридов"
    }
    Стрыжак Алеся
    {
      "first": "алеся",
      "last": "стрыжак"
    }
    владимир путин
    {
      "first": "владимир",
      "last": "путин"
    }
    плаксюк саша
    {
      "first": "саша",
      "last": "плаксюк"
    }
    О. Дерипаска
    {
      "first": "О",
      "last": "дерипаск"
    }
    Ищенко Е.П.
    {
      "first": "Е",
      "middle": "П",
      "last": "ищенко"
    }


PersonExtractor
~~~~~~~~~~~~~~~

.. code:: python

    extractor = PersonExtractor()
    
    lines = [
        'президент Николя Саркози',
        'Вице-премьер правительства РФ Дмитрий Козак',
        'Вице-президент Генадий Рушайло',
    ]
    
    for line in lines:
        matches = extractor(line)
        match = matches[0]
        fact = match.fact.as_json
        print(line)
        print(format_json(fact))


.. parsed-literal::

    президент Николя Саркози
    {
      "position": "президент",
      "name": {
        "first": "николя",
        "last": "саркози"
      }
    }
    Вице-премьер правительства РФ Дмитрий Козак
    {
      "position": "Вице-премьер правительства РФ",
      "name": {
        "first": "дмитрий",
        "last": "козак"
      }
    }
    Вице-президент Генадий Рушайло
    {
      "position": "Вице-президент",
      "name": {
        "first": "генадий",
        "last": "рушайло"
      }
    }


LocationExtractor
~~~~~~~~~~~~~~~~~

**WARN!** формат результатов скорее всего будет меняться, и вообще
качество сейчас не очень

.. code:: python

    extractor = LocationExtractor()
    
    lines = [
        'В Чеченской республике на день рождения ...',
        'Донецкая народная республика провозгласила ...',
        'Российская Федерация',
        'в Соединенных Штатах Америки',
        'речь шла о Обьединенных Арабских Эмиратах',
        'Соединённые Штаты',
    ]
    
    for line in lines:
        matches = extractor(line)
        match = matches[0]
        fact = match.fact.as_json
        print(line)
        print(format_json(fact))


.. parsed-literal::

    В Чеченской республике на день рождения ...
    {
      "name": "чеченская республика"
    }
    Донецкая народная республика провозгласила ...
    {
      "name": "донецкая народная республика"
    }
    Российская Федерация
    {
      "name": "российская федерация"
    }
    в Соединенных Штатах Америки
    {
      "name": "соединённый штат америка"
    }
    речь шла о Обьединенных Арабских Эмиратах
    {
      "name": "обьединённый арабский эмират"
    }
    Соединённые Штаты
    {
      "name": "соединённый штат"
    }


AddressExtractor
~~~~~~~~~~~~~~~~

.. code:: python

    extractor = AddressExtractor()
    
    lines = '''Офис и шоу-рум в Красноярске работает с 14.00 до 17.00 по адресу г.Красноряск ул.Парижской Коммуны,14 оф.14.
    Юридический адрес: 129344, г. Москва, ул. Искры, дом 31, корпус 1, пом. II комната 7А.
    г. Пятигорск, ул. Февральская, д. 54
    Дмитровское шоссе, д.157, стр.9
    603070, г. Нижний Новгород, ул. Акимова 22 «А»
    Адрес: | г. Санкт-Петербург, ул. Шамшева, д. 8 (ДК им.В.А.Шелгунова)
    Факт. и юр. адрес: 426052, г. Ижевск, ул. Лесозаводская 23/110
    Адрес: Россия г. Санкт-Петербург ул. Чехова 14 оф23
    129085, Москва, ул.Годовикова д.9  (Бизнес-центр "Калибр").
    Почтовый адрес: Россия, 693010 г. Южно-Сахалинск, Комсомольская, 154, оф. 600
    ул. Менжинского, 4г ст. А
    344010, РФ, г. Ростов-на-Дону, ул. Красноармейская д.208, офис 302.
    Юридический адрес 308000, Белгородская обл., г.Белгород, ул.Н.Островского, д.5
    Юридический, физический и фактический адрес: 350072, г. Краснодар, ул. Московская, 5.
    Российская Федерация, Тверская область, Кимрский район, пгт.  Белый Городок, улица Заводская дом 11
    Свердловская обл., г. Екатеринбург, Барвинка 21'''.splitlines()
    
    for line in lines:
        matches = extractor(line)
        spans = [_.span for _ in matches]
        facts = [_.fact.as_json for _ in matches]
        show_markup(line, spans)
        print(format_json(facts))



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">Офис и шоу-рум в Красноярске работает с 14.00 до 17.00 по адресу <mark>г.Красноряск ул.Парижской Коммуны,14 оф.14</mark>.</div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "name": "Красноряск",
            "type": "город"
          },
          {
            "name": "Парижской Коммуны",
            "type": "улица"
          },
          {
            "number": "14"
          },
          {
            "number": "14",
            "type": "офис"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">Юридический адрес: <mark>129344, г. Москва, ул. Искры, дом 31, корпус 1</mark>, пом. II комната 7А.</div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "value": "129344"
          },
          {
            "name": "Москва",
            "type": "город"
          },
          {
            "name": "Искры",
            "type": "улица"
          },
          {
            "number": "31",
            "type": "дом"
          },
          {
            "number": "1",
            "type": "корпус"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore"><mark>г. Пятигорск, ул. Февральская, д. 54</mark></div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "name": "Пятигорск",
            "type": "город"
          },
          {
            "name": "Февральская",
            "type": "улица"
          },
          {
            "number": "54",
            "type": "дом"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore"><mark>Дмитровское шоссе, д.157, стр.9</mark></div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "name": "Дмитровское",
            "type": "шоссе"
          },
          {
            "number": "157",
            "type": "дом"
          },
          {
            "number": "9",
            "type": "строение"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore"><mark>603070, г. Нижний Новгород, ул. Акимова 22 «А»</mark></div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "value": "603070"
          },
          {
            "name": "Нижний Новгород",
            "type": "город"
          },
          {
            "name": "Акимова",
            "type": "улица"
          },
          {
            "number": "22 «А»"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">Адрес: | <mark>г. Санкт-Петербург, ул. Шамшева, д. 8</mark> (ДК им.В.А.Шелгунова)</div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "name": "Санкт-Петербург",
            "type": "город"
          },
          {
            "name": "Шамшева",
            "type": "улица"
          },
          {
            "number": "8",
            "type": "дом"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">Факт. и юр. адрес: <mark>426052, г. Ижевск, ул. Лесозаводская 23/110</mark></div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "value": "426052"
          },
          {
            "name": "Ижевск",
            "type": "город"
          },
          {
            "name": "Лесозаводская",
            "type": "улица"
          },
          {
            "number": "23/110"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">Адрес: <mark>Россия г. Санкт-Петербург ул. Чехова 14 оф23</mark></div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "name": "Россия"
          },
          {
            "name": "Санкт-Петербург",
            "type": "город"
          },
          {
            "name": "Чехова",
            "type": "улица"
          },
          {
            "number": "14"
          },
          {
            "number": "23",
            "type": "офис"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore"><mark>129085, Москва, ул.Годовикова д.9</mark>  (Бизнес-центр "Калибр").</div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "value": "129085"
          },
          {
            "name": "Москва"
          },
          {
            "name": "Годовикова",
            "type": "улица"
          },
          {
            "number": "9",
            "type": "дом"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">Почтовый адрес: Россия, 693010 г. Южно-Сахалинск, Комсомольская, 154, оф. 600</div>


.. parsed-literal::

    []



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore"><mark>ул. Менжинского, 4г</mark> ст. А</div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "name": "Менжинского",
            "type": "улица"
          },
          {
            "number": "4г"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore"><mark>344010, РФ, г. Ростов-на-Дону, ул. Красноармейская д.208, офис 302</mark>.</div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "value": "344010"
          },
          {
            "name": "РФ"
          },
          {
            "name": "Ростов-на-Дону",
            "type": "город"
          },
          {
            "name": "Красноармейская",
            "type": "улица"
          },
          {
            "number": "208",
            "type": "дом"
          },
          {
            "number": "302",
            "type": "офис"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">Юридический адрес <mark>308000, Белгородская обл., г.Белгород, ул.Н.Островского, д.5</mark></div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "value": "308000"
          },
          {
            "name": "Белгородская",
            "type": "область"
          },
          {
            "name": "Белгород",
            "type": "город"
          },
          {
            "name": "Н.Островского",
            "type": "улица"
          },
          {
            "number": "5",
            "type": "дом"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">Юридический, физический и фактический адрес: <mark>350072, г. Краснодар, ул. Московская, 5</mark>.</div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "value": "350072"
          },
          {
            "name": "Краснодар",
            "type": "город"
          },
          {
            "name": "Московская",
            "type": "улица"
          },
          {
            "number": "5"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">Российская Федерация, <mark>Тверская область, Кимрский район, пгт.  Белый Городок, улица Заводская дом 11</mark></div>


.. parsed-literal::

    [
      {
        "parts": [
          {
            "name": "Тверская",
            "type": "область"
          },
          {
            "name": "Кимрский",
            "type": "район"
          },
          {
            "name": "Белый Городок",
            "type": "посёлок"
          },
          {
            "name": "Заводская",
            "type": "улица"
          },
          {
            "number": "11",
            "type": "дом"
          }
        ]
      }
    ]



.. raw:: html

    <style>
    
    .markup {
        white-space: pre-wrap;
    }
    
    .markup > mark {
        line-height: 1;
        display: inline-block;
        border-radius: 0.25em;
        border: 1px solid #fdf07c;
        background: #ffffc2;
    }
        </style><div class="markup tex2jax_ignore">Свердловская обл., г. Екатеринбург, Барвинка 21</div>


.. parsed-literal::

    []


OrganisationExtractor
~~~~~~~~~~~~~~~~~~~~~

**WARN!** формат результатов скорее всего будет меняться, и вообще
качество сейчас не очень

.. code:: python

    extractor = OrganisationExtractor()
    
    lines = [
        'ПАО «Газпром»',
        'публичное акционерное общество "Газпром"',
        'историческое общество "Мемориал"',
        'коммерческое производственное объединение "Вектор"',
        'правозащитный центр «Мемориал»',
    ]
    
    for line in lines:
        matches = extractor(line)
        match = matches[0]
        fact = match.fact.as_json
        print(line)
        print(format_json(fact))


.. parsed-literal::

    ПАО «Газпром»
    {
      "name": "ПАО «Газпром»"
    }
    публичное акционерное общество "Газпром"
    {
      "name": "публичное акционерное общество \"Газпром\""
    }
    историческое общество "Мемориал"
    {
      "name": "историческое общество \"Мемориал\""
    }
    коммерческое производственное объединение "Вектор"
    {
      "name": "коммерческое производственное объединение \"Вектор\""
    }
    правозащитный центр «Мемориал»
    {
      "name": "правозащитный центр «Мемориал»"
    }


DatesExtractor
~~~~~~~~~~~~~~

.. code:: python

    extractor = DatesExtractor()
    
    lines = [
        '24.01.2017',
        '27. 05.99',
        '2015 год',
        '1 апреля',
        'май 2017 г.',
        '9 мая 2017 года',
    ]
    
    for line in lines:
        matches = extractor(line)
        match = matches[0]
        fact = match.fact.as_json
        print(line)
        print(format_json(fact))


.. parsed-literal::

    24.01.2017
    {
      "year": 2017,
      "month": 1,
      "day": 24
    }
    27. 05.99
    {
      "year": 1999,
      "month": 5,
      "day": 27
    }
    2015 год
    {
      "year": 2015
    }
    1 апреля
    {
      "month": 4,
      "day": 1
    }
    май 2017 г.
    {
      "year": 2017,
      "month": 5
    }
    9 мая 2017 года
    {
      "year": 2017,
      "month": 5,
      "day": 9
    }


MoneyExtractor
~~~~~~~~~~~~~~

.. code:: python

    extractor = MoneyExtractor()
    
    lines = [
        '1 599 059, 38 Евро',
        '2 134 472,44 рубля',
        '420 долларов',
        '20 млн руб',
        '2,2 млн.руб.',
        '20 тыс руб',
        '124 451 рубль 50 копеек',
        '881 913 (Восемьсот восемьдесят одна тысяча девятьсот тринадцать) руб. 98 коп.',
    ]
    
    for line in lines:
        matches = extractor(line)
        match = matches[0]
        fact = match.fact.normalized.as_json
        print(line)
        print(format_json(fact))


.. parsed-literal::

    1 599 059, 38 Евро
    {
      "amount": 1599059.38,
      "currency": "EUR"
    }
    2 134 472,44 рубля
    {
      "amount": 2134472.44,
      "currency": "RUB"
    }
    420 долларов
    {
      "amount": 420,
      "currency": "USD"
    }
    20 млн руб
    {
      "amount": 20000000,
      "currency": "RUB"
    }
    2,2 млн.руб.
    {
      "amount": 2020000.0,
      "currency": "RUB"
    }
    20 тыс руб
    {
      "amount": 20000,
      "currency": "RUB"
    }
    124 451 рубль 50 копеек
    {
      "amount": 124451.5,
      "currency": "RUB"
    }
    881 913 (Восемьсот восемьдесят одна тысяча девятьсот тринадцать) руб. 98 коп.
    {
      "amount": 881913.98,
      "currency": "RUB"
    }


MoneyRateExtractor
~~~~~~~~~~~~~~~~~~

**WARN!** формат результатов скорее всего будет меняться, и вообще
качество сейчас не очень

.. code:: python

    extractor = MoneyRateExtractor()
    
    lines = [
        '2000 руб. / сутки',
        '2000 руб./смена',
        '2000 руб. в час',
    ]
    
    for line in lines:
        matches = extractor(line)
        match = matches[0]
        fact = match.fact.normalized.as_json
        print(line)
        print(format_json(fact))


.. parsed-literal::

    2000 руб. / сутки
    {
      "money": {
        "amount": 2000,
        "currency": "RUB"
      },
      "period": "DAY"
    }
    2000 руб./смена
    {
      "money": {
        "amount": 2000,
        "currency": "RUB"
      },
      "period": "SHIFT"
    }
    2000 руб. в час
    {
      "money": {
        "amount": 2000,
        "currency": "RUB"
      },
      "period": "HOUR"
    }


MoneyRangeExtractor
~~~~~~~~~~~~~~~~~~~

**WARN!** формат результатов скорее всего будет меняться, и вообще
качество сейчас не очень

.. code:: python

    extractor = MoneyRangeExtractor()
    
    lines = [
        '20000-30000 рублей',
        'от 80 тысяч до 2 миллионов рублей',
    ]
    
    for line in lines:
        matches = extractor(line)
        match = matches[0]
        fact = match.fact.normalized.as_json
        print(line)
        print(format_json(fact))


.. parsed-literal::

    20000-30000 рублей
    {
      "min": {
        "amount": 20000,
        "currency": "RUB"
      },
      "max": {
        "amount": 30000,
        "currency": "RUB"
      }
    }
    от 80 тысяч до 2 миллионов рублей
    {
      "min": {
        "amount": 80000,
        "currency": "RUB"
      },
      "max": {
        "amount": 2000000,
        "currency": "RUB"
      }
    }

