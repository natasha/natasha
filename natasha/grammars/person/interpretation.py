# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from collections import Counter

from yargy.tokenizer import Token
from yargy.normalization import get_normalized_text
from yargy.interpretation import (
    InterpretationObject,
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
        Descriptor = 3  # президент
        Descriptor_Destination = 4  # российской федерации

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

    def similarity_firstname_coef(self, another):
        if not self.normalized_firstname or not another.normalized_firstname:
            return self.NEUTRAL_COEF[0]

        similarity = damerau_levenshtein_distance(
            self.normalized_firstname,
            another.normalized_firstname,
        )

        if similarity <= self.SIMILARITY_THRESHOLD:
            return self.POSITIVE_COEF[0]
        else:
            return self.NEGATIVE_COEF[0]

    def similarity_middlename_coef(self, another):
        if not self.normalized_middlename or not another.normalized_middlename:
            return self.NEUTRAL_COEF[1]

        similarity = damerau_levenshtein_distance(
            self.normalized_middlename,
            another.normalized_middlename,
        )

        if similarity <= self.SIMILARITY_THRESHOLD:
            return self.POSITIVE_COEF[1]
        else:
            return self.NEGATIVE_COEF[1]

    def similarity_lastname_coef(self, another):
        if not self.normalized_lastname or not another.normalized_lastname:
            return self.NEUTRAL_COEF[2]

        similarity = damerau_levenshtein_distance(
            self.normalized_lastname,
            another.normalized_lastname,
        )

        if similarity <= self.SIMILARITY_THRESHOLD:
            return self.POSITIVE_COEF[2]
        else:
            return self.NEGATIVE_COEF[2]

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
            'firstname': self.firstname or another.firstname,
            'middlename': self.middlename or another.middlename,
            'lastname': self.lastname or another.lastname,
            'descriptor': self.descriptor or another.descriptor,
            'descriptor_destination': self.descriptor_destination or another.descriptor_destination,
            'spans': self.spans + another.spans,
        })

    def __eq__(self, another):
        if self.similarity(another) >= self.MINIMUM_SIMILARITY_COEFFICIENT:
            return True
        else:
            return False
