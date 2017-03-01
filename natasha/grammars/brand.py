# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    in_,
    is_capitalized,
)
from yargy.normalization import NormalizationType

from natasha.grammars.organisation import OrganisationObject


class Brand(Enum):

    Latin = [
        {
            'labels': [
                gram('LATN'),
                is_capitalized(True),
            ],
            'repeatable': True,
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': [
                    OrganisationObject.Attributes.Name,
                ]
            },
        },
        {
            'labels': [
                gram('INT'),
            ],
            'optional': True,
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': [
                    OrganisationObject.Attributes.Name,
                ]
            },
        }
    ]

    WithConj = [
        Latin[0],
        {
            'labels': [
                in_({
                    '&',
                    '/',
                }),
            ],
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': [
                    OrganisationObject.Attributes.Name,
                ]
            },
        },
        Latin[0],
    ]

    Trademark = [
        {
            'labels': [
                gram('Trad'),
            ],
            'normalization': NormalizationType.Original,
            'interpretation': {
                'attribute': [
                    OrganisationObject.Attributes.Name,
                ]
            },
        }
    ]
