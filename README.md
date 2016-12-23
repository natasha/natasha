# Natasha [![Build Status](https://travis-ci.org/bureaucratic-labs/natasha.svg?branch=master)](https://travis-ci.org/bureaucratic-labs/natasha)

![](http://i.imgur.com/jQtaSTV.png)

Наташа извлекает именованные сущности из текста на русском языке, включая (но не ограничиваясь):

**Физ. лица**: `Иванов Иван Иванович`, `Иван Иванов`, `Иван Петрович`, `Ваня`  
**Организации**: `ПАО «Газпром»`, `ИП Иванов Иван Иванович`, `агентство Bloomberg`  
**События**: `фестиваль «Ковчег спасения»`, `шоу «Пятая империя»`  
**Гео-объекты**: `Москва`, `Ленинградская область`, `Российская Федерация`, `Северо-Кавказский ФО`  
**Объекты времени**: `21 мая 1996 года`, `21.05.1996`, `21 мая`, `сегодня`, `в конце года`  
**Денежные единицы**: `200 рублей`, `1 млрд. долларов`,  `семьдесят пять тысяч рублей`  

Алгоритм работы (выделение сущностей по заданным правилам, используя морфологический разбор) похож на [Томита-парсер от Яндекса](https://tech.yandex.ru/tomita/).

# Зачем?

При всех хороших качествах существующих решений для выделения сущностей, большинство из них трудно использовать в python-проектах, многие имеют закрытый исходный код, неудобную лицензию, бедную документацию и словари.
`Natasha` призвана решить эту проблему - код написан исключительно на python, все используемые библиотеки имеют открытый исходный код, а [морфологический анализатор](https://github.com/kmike/pymorphy2) использует свободный словарь [OpenCorpora](http://opencorpora.org/).
Если вдаваться в технические детали, `natasha` - всего лишь набор частоиспользуемых грамматик для [GLR-парсера](https://github.com/bureaucratic-labs/yargy). Это позволяет избавить разработчика, желающего научить своё приложение понимать натуральный язык, от необходимости писать лингвистические правила, ведь это скучно.

# Установка

*Важно:* `natasha` поддерживает версии Python 2.7+ и 3.3+, включая интерпретаторы PyPy и PyPy3.

```bash
$ pip install natasha==0.4.0
```

# Использование

Для первого знакомства можно использовать [онлайн версию](https://bureaucratic-labs.github.io/natasha/).

```python
from natasha import Combinator, DEFAULT_GRAMMARS
from natasha.grammars import Geo, Date

# DEFAULT_GRAMMARS содержит стандартный набор правил:
# [
#    <enum 'Money'>,
#    <enum 'Person'>,
#    <enum 'Geo'>,
#    <enum 'Date'>,
#    <enum 'Brand'>,
#    <enum 'Event'>
# ]

# Можно использовать их частично или использовать свои правила
MY_GRAMMARS_LIST = [
    Geo,
    Date,
]

text = "23 августа в Нижнем Новгороде пройдет очередной день"

combinator = Combinator(MY_GRAMMARS_LIST)
for grammar, tokens in combinator.extract(text):
    print("Правило:", grammar)
    print("Токены:", tokens)
```

Иногда бывает так: некоторые словосочитания попадают под несколько грамматик, например, в предложении `иван иванович иванов меняет...` `natasha` найдет четыре результата - `Person.Full`, `Person.Firstname`, `Person.Middlename`, `Person.Lastname`. Если необходимо получить только один результат, можно использовать метод `resolve_matches`, который вернет правило, включившее в себя наибольшее количество слов, т.е. в данном случае - `Person.Full`:

```python
from natasha import Combinator
from natasha.grammars import Person

text = "Иван иванович иванов меняет..."

combinator = Combinator([Person])

matches = combinator.extract(text)

for grammar, tokens in combinator.resolve_matches(matches):
   print(grammar, tokens)

```

# Лицензия

Исходный код распространяется под лицензией MIT.

# У меня остались вопросы
[Telegram-конференция](https://telegram.me/natural_language_processing), где можно найти ответы на все вопросы (на самом деле нет)

