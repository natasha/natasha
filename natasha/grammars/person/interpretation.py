# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from functools import partial
from collections import Counter

from yargy.tokenizer import Token
from yargy.normalization import get_normalized_text
from yargy.interpretation import (
    InterpretationObject,
    choice_best_span,
    damerau_levenshtein_distance,
)


class PersonObject(InterpretationObject):

    '''
    Big thanks to @lastveritas for her work on person clustering:
    https://github.com/lasveritas/coreference-resolution
    '''

    NEUTRAL_COEF = (0, 0, 0)
    POSITIVE_COEF = (2.76, 0.49, 3.55)
    NEGATIVE_COEF = (-3.18, -0.006, -3.4)
    GENDER_COEF = (-2.676, 1.257)
    DESCRIPTOR_COEF = (-0.8, -0.6)

    MINIMUM_SIMILARITY_COEFFICIENT = 0

    class Attributes(Enum):

        Firstname = 0  # владимир
        Middlename = 1  # владимирович
        Lastname = 2  # путин
        Nickname = 3 # "володя"
        Descriptor = 4  # президент
        Descriptor_Destination = 5  # российской федерации

    @property
    def gender(self):
        '''
        Very simple gender prediction algorithm
        '''
        counter = Counter()
        for field, token in self.__dict__.items():
            if not isinstance(token, Token):
                continue
            for form in token.forms:
                grammemes = set()
                if ('Ms-f' in form['grammemes']) or ('Fixd' in form['grammemes']):
                    continue
                elif 'femn' in form['grammemes']:
                    grammemes |= {'femn'}
                elif 'masc' in form['grammemes']:
                    grammemes |= {'masc'}
                counter.update(grammemes)
        return counter

    @property
    def normalized_firstname(self):
        if self.firstname:
            return get_normalized_text(
                self.firstname
            ).lower()
        else:
            return None

    @property
    def normalized_middlename(self):
        if self.middlename:
            return get_normalized_text(
                self.middlename
            ).lower()
        else:
            return None

    @property
    def normalized_lastname(self):
        if self.lastname:
            return get_normalized_text(
                self.lastname
            ).lower()
        else:
            return None

    @property
    def normalized_descriptor(self):
        if self.descriptor:
            return get_normalized_text(
                self.descriptor
            ).lower()
        else:
            return None

    def similarity(self, another):
        coefficients = (
            self.similarity_firstname_coef(another),
            self.similarity_middlename_coef(another),
            self.similarity_lastname_coef(another),
            self.similarity_gender_coef(another),
            self.similarity_descriptor_coef(another),
        )
        return round(sum(coefficients), 2)

    def similarity_check(self, a, b, index):

        if not a or not b:
            return self.NEUTRAL_COEF[index]

        if b > a:
            a, b = b, a
        if a.startswith(b):
            return self.POSITIVE_COEF[index]

        similarity = damerau_levenshtein_distance(a, b)

        if similarity <= self.SIMILARITY_THRESHOLD:
            return self.POSITIVE_COEF[index]
        else:
            return self.NEGATIVE_COEF[index]

    def similarity_firstname_coef(self, another):
        return self.similarity_check(
            self.normalized_firstname,
            another.normalized_firstname,
            0,
        )

    def similarity_middlename_coef(self, another):
        return self.similarity_check(
            self.normalized_firstname,
            another.normalized_firstname,
            1,
        )

    def similarity_lastname_coef(self, another):
        return self.similarity_check(
            self.normalized_firstname,
            another.normalized_firstname,
            2,
        )

    def similarity_gender_coef(self, another):
        if not self.gender.most_common(1) or not another.gender.most_common(1):
            return 0
        else:
            return self.GENDER_COEF[
                self.gender.most_common(1)[0] == another.gender.most_common(1)[0]
            ]

    def similarity_descriptor_coef(self, another):
        if not self.normalized_descriptor or not another.normalized_descriptor:
            return 0
        similarity = damerau_levenshtein_distance(
            self.normalized_descriptor,
            another.normalized_descriptor,
        )
        return self.DESCRIPTOR_COEF[similarity <= self.SIMILARITY_THRESHOLD]

    def merge(self, another):
        return PersonObject(**{
            'firstname': choice_best_span(
                self.firstname,
                another.firstname,
            ),
            'middlename': choice_best_span(
                self.middlename,
                another.middlename,
            ),
            'lastname': choice_best_span(
                self.lastname,
                another.lastname,
            ),
            'nickname': choice_best_span(
                self.nickname,
                another.nickname,
            ),
            'descriptor': choice_best_span(
                self.descriptor,
                another.descriptor,
            ),
            'descriptor_destination': choice_best_span(
                self.descriptor_destination,
                another.descriptor_destination,
            ),
            'spans': self.spans + another.spans,
        })

    def __eq__(self, another):
        if self.similarity(another) >= self.MINIMUM_SIMILARITY_COEFFICIENT:
            return True
        else:
            return False
