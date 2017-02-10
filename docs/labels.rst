Лейблы
==============

Лейбл - функция, проверяющая совпадает ли токен (передаваемый из токенизатора в парсер) заданным правилам.
Лейблы используются при определении правил, в специальной секции - `labels`. 

.. code-block:: python

   from enum import Enum
   from yargy.labels import gram

   class MyGrammar(Enum):

       NounAndVerb = [
           {
               'labels': [
                   gram('NOUN'), # токен разбирается как существительное
               ],
           },
           {
               'labels': [
                   gram('VERB'), # а этот - как глагол
               ],
           },
       ]
