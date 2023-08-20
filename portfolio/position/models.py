from django.db import models

from portfolio.common.models import Ticker
from portfolio.stocks_portfolio.models import Portfolio


class Position(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    count = models.FloatField()
    price = models.FloatField()
    date_added = models.DateField(auto_now_add=True)
    to_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def position_total(self):
        return self.price * self.count

    def avg_price(self):
        return self.price / self.count


class PositionHistory(models.Model):
    pass
