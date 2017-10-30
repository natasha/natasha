
# coding: utf-8

# In[4]:

import natasha
from yargy.labels import (
    label,
    type_required,
    string_type,
    is_capitalized,
)
from yargy.compat import string_type
from yargy import Grammar, Parser


# In[5]:

@label
@type_required(string_type)
def is_bank(bank, token, value):
    return ('банк' in token.value or 'Банк' in token.value or 'БАНК' in token.value) == bank

bank_grammar = Grammar('Bank', [
    {
        'labels': [
            is_bank(False),
            is_capitalized(True),
        ],
        'optional': True,
        'repeatable': True,
    },
    {
        'labels': [
            is_bank(True),
            is_capitalized(True),
        ],
    },
    {
        'labels': [
            is_bank(False),
            is_capitalized(True),
        ],
        'optional': True,
        'repeatable': True,
    },
])

