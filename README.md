# Natasha [![Build Status](https://travis-ci.org/bureaucratic-labs/natasha.svg?branch=master)](https://travis-ci.org/bureaucratic-labs/natasha) [![Documentation Status](https://readthedocs.org/projects/natasha/badge/?version=0.7.0)](http://natasha.readthedocs.io/ru/0.7.0/?badge=0.7.0) [![PyPI](https://img.shields.io/pypi/v/natasha.svg)](https://pypi.python.org/pypi/natasha)

<img align="right" src="http://i.imgur.com/DD2KYS9.png">

Natasha - библиотека для поиска и извлечения именованных сущностей ([Named-entity recognition](https://en.wikipedia.org/wiki/Named-entity_recognition)) из текстов на русском языке. На данный момент разбираются упоминания персон, даты и суммы денег.

# Установка

Natasha поддерживает Python 2.7+ / 3.3+ и PyPy.

```bash
$ pip install natasha
```

Если вы используете CPython, рекомендуется также поставить `pymorphy2[fast]`:

```bash
$ pip install pymorphy2[fast]
```

# Использование

```python

from natasha import NamesExtractor
	

text = '''
Простите, еще несколько цитат из приговора. «…Отрицал существование
Иисуса и пророка Мухаммеда», «наделял Иисуса Христа качествами
ожившего мертвеца — зомби» [и] «качествами покемонов —
представителей бестиария японской мифологии, тем самым совершил
преступление, предусмотренное статьей 148 УК РФ
'''
matches = extractor(text)
for match in matches:
    print(match.span, match.fact)

(69, 75) Name(first='иисус', last=None, middle=None, nick=None)
(86, 95) Name(first='мухаммед', last=None, middle=None, nick=None)
(107, 120) Name(first='иисус', last='христос', middle=None, nick=None)
```

Про атрибуты объекта `match` и другие типы экстракторов написано в [документации](http://natasha.readthedocs.io/ru/latest/).

# Дополнительная информация

- [Демо поиска упоминаний](https://b-labs.pro/natasha/)
- [Telegram-конференция](https://telegram.me/natural_language_processing), где можно найти ответы на все вопросы (на самом деле нет)

# Лицензия

Исходный код распространяется под лицензией MIT.
