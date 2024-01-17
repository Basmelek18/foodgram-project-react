from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodgramUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username', 'password')

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=settings.MAX_LENGTH_USERCHARFIELD,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.MAX_LENGTH_USERCHARFIELD,
    )
    first_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAX_LENGTH_USERCHARFIELD,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=settings.MAX_LENGTH_USERCHARFIELD,
    )
