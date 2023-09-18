from django.contrib.auth import get_user_model
from django.db import models
from portfolio.common.models import Ticker
UserModel = get_user_model()


class Watchlist(models.Model):
    tickers = models.ManyToManyField(Ticker)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
