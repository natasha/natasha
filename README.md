# Natasha [![Build Status](https://travis-ci.org/natasha/natasha.svg?branch=master)](https://travis-ci.org/natasha/natasha) [![Build status](https://ci.appveyor.com/api/projects/status/k5pqpvtpb79lhn86/branch/master?svg=true)](https://ci.appveyor.com/project/dveselov/natasha/branch/master) [![Documentation Status](https://readthedocs.org/projects/natasha/badge/?version=latest)](http://natasha.readthedocs.io/) [![PyPI](https://img.shields.io/pypi/v/natasha.svg)](https://pypi.python.org/pypi/natasha)

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
extractor = NamesExtractor()
matches = extractor(text)
for match in matches:
    print(match.span, match.fact)

(69, 75) Name(first='иисус', last=None, middle=None, nick=None)
(86, 95) Name(first='мухаммед', last=None, middle=None, nick=None)
(107, 120) Name(first='иисус', last='христос', middle=None, nick=None)
```

Про атрибуты объекта `match` и другие типы экстракторов написано в [документации](http://natasha.readthedocs.io/ru/latest/).

# Демо поиска упоминаний

https://natasha.github.io/demo/
<img src="https://i.imgur.com/4i4sreZ.png">

# Лицензия

Исходный код распространяется под лицензией MIT.

# Поддержка

- Telegram-конференция — https://telegram.me/natural_language_processing. Там можно найти ответы на все вопросы (на самом деле нет)
- Таск-трекер — https://github.com/natasha/natasha/issues
- Коммерческая поддержка — http://lab.alexkuk.ru/natasha
