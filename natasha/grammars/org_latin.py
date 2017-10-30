
# coding: utf-8

# In[4]:

import natasha
from yargy.labels import (
    gram_any,
    dictionary,
    dictionary_not,
    label,
    is_capitalized,
    type_required,
    string_type,
)
from yargy.compat import string_type
from natasha.grammars.organisation.interpretation import OrganisationObject
from yargy import Grammar, Parser


# In[5]:

#Google Inc, EG Capital Partners

ORGN_COMMERCIAL_LATIN = {
    "ag",
    "co",
    "corp",
    "eg",
    "gmbh",
    "ibc",
    "inc",
    "kg",
    "llc",
    "lp",
    "llp",
    "ltd",
    "plc",
    "s.a.",
    "corporation",
    "incorporated",
    "limited",
}

latin_abbr_grammar = Grammar('OfficialLatin', [
    {
        'labels': [
            dictionary_not(ORGN_COMMERCIAL_LATIN),
            is_capitalized(True),
            gram_any({
                    'LATN',
                    'NUMBER',
            }),
            
        ],
        'optional': True,
        'repeatable': True,
    },
    {
        'labels': [
            dictionary(ORGN_COMMERCIAL_LATIN),
        ],
    },
    {
        'labels': [
            dictionary_not(ORGN_COMMERCIAL_LATIN),
            is_capitalized(True),
            gram_any({
                    'LATN',
                    'NUMBER',
            }),
            
        ],
        'optional': True,
        'repeatable': True,
    },
])

