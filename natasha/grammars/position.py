
# coding: utf-8

# In[4]:

import natasha
from yargy.labels import (
    dictionary,
    label,
    type_required,
    string_type,
)
from yargy.compat import string_type
from natasha.grammars.organisation.interpretation import OrganisationObject
from yargy import Grammar, Parser


# In[5]:

#президент НАПФ

POSITION = {
    "президент",
    "сопрезидент",
    "вице-президент",
    "экс-президент",
    "председатель",
    "руководитель",
    "директор",
    "глава",
}

@label
@type_required(string_type)
def is_abbr(case, token, value):
    return token.value.isupper() == case

prob_org_grammar = Grammar('NonQuoted', [
        {
            'labels': [
                dictionary(POSITION),
            ],
        },
        {
            'labels': [
                is_abbr(True),
            ],
            'interpretation': {
                'attribute': OrganisationObject.Attributes.Name,
            },
        },
    ]
)

