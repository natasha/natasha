# Natasha [![Build Status](https://travis-ci.org/bureaucratic-labs/natasha.svg?branch=master)](https://travis-ci.org/bureaucratic-labs/natasha) [![Documentation Status](https://readthedocs.org/projects/natasha/badge/?version=latest)](http://natasha.readthedocs.io/ru/latest/?badge=latest)


![](http://i.imgur.com/nGwT8IG.png)

Наташа извлекает именованные сущности из текста на русском языке.

Алгоритм работы похож на [Томита-парсер от Яндекса](https://tech.yandex.ru/tomita/).

# Зачем?

При всех хороших качествах существующих решений для выделения сущностей, большинство из них трудно использовать в python-проектах, многие имеют закрытый исходный код, неудобную лицензию, бедную документацию и словари.
`Natasha` призвана решить эту проблему - код написан исключительно на python, все используемые библиотеки имеют открытый исходный код, а [морфологический анализатор](https://github.com/kmike/pymorphy2) использует свободный словарь [OpenCorpora](http://opencorpora.org/).  
Если вдаваться в технические детали, `natasha` - всего лишь набор частоиспользуемых грамматик для [GLR-парсера](https://github.com/bureaucratic-labs/yargy). Это позволяет избавить разработчика, желающего научить своё приложение понимать натуральный язык, от необходимости писать лингвистические правила, ведь это скучно.
Из более глобальных целей - создать **простой в использовании** и **полезный** инструмент для извлечения и интерпретации именованных сущностей (для уточнения полезности мы используем тестовые наборы данных конкурса FactRuEval-2016, проходящего в рамках конференции Диалог-21, результаты разбора первой дорожки которого представлены на рисунке ниже). 

![factRuEval-2016-results](http://i.imgur.com/cy9a9d1.png)

# Установка

*Важно:* `natasha` поддерживает версии Python 2.7+ и 3.3+, включая интерпретаторы PyPy и PyPy3.

```bash
$ pip install natasha==0.4.0
```

# Использование

Для первого знакомства можно использовать [онлайн версию](https://bureaucratic-labs.github.io/natasha/).

```python
from natasha import (
    Combinator,
    DEFAULT_GRAMMARS,
)
from natasha.grammars import Geo, Date

# DEFAULT_GRAMMARS содержит стандартный набор правил:
# [
#    <enum 'Brand'>,
#    <enum 'Date'>,
#    <enum 'Event'>
#    <enum 'Geo'>,
#    <enum 'Money'>,
#    <enum 'Organisation'>,
#    <enum 'Person'>,
# ]

# Можно использовать их частично или использовать свои правила
MY_GRAMMARS_LIST = [
    Geo,
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

Иногда бывает так: некоторые словосочетания попадают под несколько грамматик, например, в предложении `иван иванович иванов меняет...` `natasha` найдет четыре результата - `Person.Full`, `Person.Firstname`, `Person.Middlename`, `Person.Lastname`.
Если необходимо получить только один результат, можно использовать метод `resolve_matches`, который вернет правило, включившее в себя наибольшее количество слов, т.е. в данном случае - `Person.Full`:

```python
from natasha import Combinator
from natasha.grammars import Person

text = "Иван иванович иванов меняет..."

combinator = Combinator([Person])

matches = combinator.extract(text)

for grammar, tokens in combinator.resolve_matches(matches):
   print(grammar, tokens)

```

Также метод `resolve_matches` принимает дополнительный именной аргумент - `strict`, который определяет разрешение совпадений по классу грамматики, например:

```python
from natasha import Combinator
from natasha.grammars import Person, Organisation


text = 'представитель администрации президента россии федор смирнов'

combinator = Combinator([
    Person,
    Organisation,
])
matches = combinator.resolve_matches(combinator.extract(text), strict=False)
matches = ((grammar, [t.value for t in tokens]) for (grammar, tokens) in matches)

assert list(matches) == [
    (Person.WithPosition, ['представитель', 'администрации', 'президента', 'россии', 'федор', 'смирнов']),
    (Organisation.Social, ['администрации', 'президента', 'россии']),
]
```

# Лицензия

Исходный код распространяется под лицензией MIT.

# У меня остались вопросы
[Telegram-конференция](https://telegram.me/natural_language_processing), где можно найти ответы на все вопросы (на самом деле нет)

