from django.contrib.auth import get_user_model
from django.db import models
UserModel = get_user_model()


class Portfolio(models.Model):
    name = models.CharField(max_length=50)
    cash = models.FloatField()
    #position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
