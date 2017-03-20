# Natasha [![Build Status](https://travis-ci.org/bureaucratic-labs/natasha.svg?branch=master)](https://travis-ci.org/bureaucratic-labs/natasha) [![Documentation Status](https://readthedocs.org/projects/natasha/badge/?version=latest)](http://natasha.readthedocs.io/ru/latest/?badge=latest) [![PyPI](https://img.shields.io/pypi/v/natasha.svg)](https://pypi.python.org/pypi/natasha)


![](http://i.imgur.com/nGwT8IG.png)

Наташа извлекает именованные сущности (имена людей, адреса, топонимы и т.д.) из текста на русском языке.

Алгоритм работы похож на [Томита-парсер от Яндекса](https://tech.yandex.ru/tomita/).

# Установка

*Важно:* `natasha` поддерживает версии Python 2.7+ и 3.3+, включая интерпретаторы PyPy и PyPy3.

```bash
$ pip install natasha==0.5.0
```

# Использование

Для первого знакомства можно использовать [онлайн версию](https://bureaucratic-labs.github.io/natasha/).

```python
from natasha import (
    Combinator,
    DEFAULT_GRAMMARS,
)
from natasha.grammars import Location, Date

# DEFAULT_GRAMMARS содержит стандартный набор правил:
# [
#    <enum 'Brand'>,
#    <enum 'Date'>,
#    <enum 'Event'>
#    <enum 'Location'>,
#    <enum 'Money'>,
#    <enum 'Organisation'>,
#    <enum 'Person'>,
# ]

# Можно использовать их частично или использовать свои правила
MY_GRAMMARS_LIST = [
    Location,
    Date,
]

text = "23 августа в Нижнем Новгороде пройдет очередной день"

combinator = Combinator(
    MY_GRAMMARS_LIST

)

for grammar, tokens in combinator.extract(text):
    print("Правило:", grammar)
    print("Токены:", tokens)
```

# Лицензия

Исходный код распространяется под лицензией MIT.

# У меня остались вопросы
[Telegram-конференция](https://telegram.me/natural_language_processing), где можно найти ответы на все вопросы (на самом деле нет)

