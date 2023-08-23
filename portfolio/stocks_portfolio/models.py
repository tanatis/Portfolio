from django.contrib.auth import get_user_model
from django.db import models
UserModel = get_user_model()


class Portfolio(models.Model):
    name = models.CharField(max_length=50)
    cash = models.FloatField()
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CashTransaction(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    operation = models.CharField(
        choices=[
            ('deposit', 'Deposit'),
            ('withdraw', 'Withdraw'),
        ],
        max_length=8,
    )
    amount = models.FloatField()
    date_added = models.DateField(auto_now_add=True)
