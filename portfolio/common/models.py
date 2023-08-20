from django.db import models


class Ticker(models.Model):
    symbol = models.CharField(max_length=5)
    company_name = models.CharField(max_length=100)
    #index = models.CharField(choices=Index.choices(), max_length=Index.length())

    def __str__(self):
        return self.symbol
