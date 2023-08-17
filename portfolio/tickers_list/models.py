from enum import Enum
from django.db import models


# class Index(Enum):
#     sp500 = 'S&P 500'
#     dow = 'Dow Jones'
#     nasdaq = 'Nasdaq 100'
#
#     @classmethod
#     def choices(cls):
#         return [(x.value, x.name) for x in cls]
#
#     @classmethod
#     def length(cls):
#         return max(len(name) for name, _ in cls.choices())


class Ticker(models.Model):
    symbol = models.CharField(max_length=5)
    company_name = models.CharField(max_length=100)
    #index = models.CharField(choices=Index.choices(), max_length=Index.length())

    def __str__(self):
        return self.symbol
