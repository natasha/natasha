# coding: utf-8
from __future__ import unicode_literals

from collections import OrderedDict

from natasha.utils import Record


EURO = 'EUR'
DOLLARS = 'USD'
RUBLES = 'RUB'

DAY = 'DAY'
HOUR = 'HOUR'
SHIFT = 'SHIFT'


class Money(Record):
    __attributes__ = ['amount', 'currency']

    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    @property
    def as_json(self):
        return OrderedDict([
            ('amount', self.amount),
            ('currency', self.currency)
        ])

    def __str__(self):
        return '{self.amount} {self.currency}'.format(
            self=self
        )


class Rate(Record):
    __attributes__ = ['money', 'period']

    def __init__(self, money, period):
        self.money = money
        self.period = period

    @property
    def as_json(self):
        return OrderedDict([
            ('money', self.money.as_json),
            ('period', self.period)
        ])

    def __str__(self):
        return '{self.money}/{self.period}'.format(
            self=self
        )


class Range(Record):
    __attributes__ = ['min', 'max']

    def __init__(self, min, max):
        self.min = min
        self.max = max

    @property
    def as_json(self):
        return OrderedDict([
            ('min', self.min.as_json),
            ('max', self.max.as_json)
        ])

    def __str__(self):
        return '{self.min}-{self.max}'.format(
            self=self
        )
