from django.contrib.auth.models import UserManager
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from django.utils import timezone

#UserModel = get_user_model()


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = 'username'

    objects = UserManager()

    username = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True
    )

    date_joined = models.DateTimeField(
        default=timezone.now
    )


class Profile(models.Model):
    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=30,
    )

    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=30,
    )

    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,  # pk на UserModel става pk на Profile (т.е. Profile вече няма pk в базата)
    )


class AppUserHistory(models.Model):
    to_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    operation_type = models.CharField(
        choices=[
            ('buy', 'Buy'),
            ('sell', 'Sell'),
            ('deposit', 'Deposit'),
            ('withdraw', 'Withdraw'),
            ('dividend', 'Dividend'),
        ],
        max_length=8
    )
    ticker = models.CharField(blank=True, null=True, max_length=5)
    date_added = models.DateField(auto_now_add=True)
    count = models.FloatField(blank=True, null=True)
    price = models.FloatField()
