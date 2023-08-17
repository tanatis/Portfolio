from django.db import models


class Portfolio(models.Model):
    name = models.CharField(max_length=50)
    cash = models.FloatField()
    #position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    # TODO: user


