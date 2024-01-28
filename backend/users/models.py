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
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAX_LENGTH_USERCHARFIELD,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=settings.MAX_LENGTH_USERCHARFIELD,
    )


class Subscriptions(models.Model):
    subscriber = models.ForeignKey(
        FoodgramUser,
        related_name='subscriptions',
        on_delete=models.CASCADE)
    followed_user = models.ForeignKey(
        FoodgramUser,
        related_name='followers',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'followed_user'],
                name='unique_subscriptions'
            )
        ]
