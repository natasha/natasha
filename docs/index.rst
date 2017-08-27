
Natasha
=======

Natasha — библиотека для поиска и извлечения именованных сущностей
(`Named-entity
recognition <https://en.wikipedia.org/wiki/Named-entity_recognition>`__)
из текстов на русском языке. В библиотеке собраны грамматики и словари
для парсера `Yargy <https://github.com/bureaucratic-labs/yargy>`__. На
данный момент разбираются упоминания персон, даты и суммы денег.

Использование
-------------

Natasha имеет лаконичный интерфейс. Доступно три типа экстракторов:

.. code:: python

    from natasha import NamesExtractor, DatesExtractor, MoneyExtractor

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
    
    .markup > mark > .index {
        font-size: 0.7em;
        vertical-align: top;
        margin-left: 0.1em;
    }
        </style><div class="markup tex2jax_ignore">
    Простите, еще несколько цитат из приговора. «…Отрицал существование
    <mark>Иисуса<span class="index">0</span></mark> и пророка <mark>Мухаммеда<span class="index">1</span></mark>», «наделял <mark>Иисуса Христа<span class="index">2</span></mark> качествами
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

    0 Name(first='иисус', last=None, middle=None, nick=None)
    1 Name(first='мухаммед', last=None, middle=None, nick=None)
    2 Name(first='иисус', last='христос', middle=None, nick=None)


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
    
    .markup > mark > .index {
        font-size: 0.7em;
        vertical-align: top;
        margin-left: 0.1em;
    }
        </style><div class="markup tex2jax_ignore">
    Я посмотрел на инфляцию в России, взял период с <mark>декабря 2002 года<span class="index">0</span></mark>
    по <mark>декабрь 2015 года<span class="index">1</span></mark> Инфляция 246%.
    
    14.14 <mark>29 июня 2016 года<span class="index">2</span></mark>:   Наиболее ожесточенные бои ночью шли под
    Дебальцево
    </div>



.. code:: python

    for index, match in enumerate(matches):
        print(index, match.fact)


.. parsed-literal::

    0 Date(year=2002, month='декабрь', day=None)
    1 Date(year=2015, month='декабрь', day=None)
    2 Date(year=2016, month='июнь', day=29)


.. code:: python

    extractor = MoneyExtractor()
    text = 'В 1995 году стоимость 1 доллара была около 800 рублей'''
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
    
    .markup > mark > .index {
        font-size: 0.7em;
        vertical-align: top;
        margin-left: 0.1em;
    }
        </style><div class="markup tex2jax_ignore">В 1995 году стоимость <mark>1 доллара<span class="index">0</span></mark> была около <mark>800 рублей<span class="index">1</span></mark></div>



.. code:: python

    for index, match in enumerate(matches):
        print(index, match.fact)


.. parsed-literal::

    0 Money(amount=1, currency='доллара')
    1 Money(amount=800, currency='рублей')

