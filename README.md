# Natasha [![Build Status](https://travis-ci.org/bureaucratic-labs/natasha.svg?branch=master)](https://travis-ci.org/bureaucratic-labs/natasha) [![Documentation Status](https://readthedocs.org/projects/natasha/badge/?version=0.7.0)](http://natasha.readthedocs.io/ru/0.7.0/?badge=0.7.0) [![PyPI](https://img.shields.io/pypi/v/natasha.svg)](https://pypi.python.org/pypi/natasha)

<img align="right" src="http://i.imgur.com/DD2KYS9.png">

Natasha - библиотека для поиска и извлечения именованных сущностей ([Named-entity recognition](https://en.wikipedia.org/wiki/Named-entity_recognition)) в тексте на естественном языке.

На данный момент мы умеем разбирать:

- Упоминания персон
- Названия организаций
- Топонимы и почтовые адреса
- Названия праздников, конференций и т.д.

Из возможностей парсера стоит отметить:

- Снятие морфологической неоднозначности
- Приведение сущностей к нормальной форме и их склонение
- Извлечение атрибутов сущностей: для упоминаний персон это имя, фамилия и т.д.
- Разрешение кореференции для упоминаний персон, организаций и топонимов

# Дополнительная информация

- [Демо поиска упоминаний](https://b-labs.pro/natasha/)
- [Пошаговое руководство](http://natasha.readthedocs.io/ru/latest/quickstart/) и [документация](http://natasha.readthedocs.io/ru/latest/)
- [Telegram-конференция](https://telegram.me/natural_language_processing), где можно найти ответы на все вопросы (на самом деле нет)
- [Результаты FactRuEval-2016](https://github.com/bureaucratic-labs/natasha-factRuEval-2016)

# Лицензия

Исходный код распространяется под лицензией MIT.
