from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from foodgram import constants


class FoodgramUser(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username', 'password')

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=constants.MAX_LENGTH_USERCHARFIELD,
        validators=[
            UnicodeUsernameValidator()
        ]
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=constants.MAX_LENGTH_USERCHARFIELD,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=constants.MAX_LENGTH_USERCHARFIELD,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=constants.MAX_LENGTH_USERCHARFIELD,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    """Модель подписок."""
    subscriber = models.ForeignKey(
        FoodgramUser,
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    followed_user = models.ForeignKey(
        FoodgramUser,
        related_name='followers',
        on_delete=models.CASCADE,
        verbose_name='Подписка',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'followed_user'],
                name='unique_subscriptions'
            )
        ]
        ordering = ('id',)

    def __str__(self):
        return f'{self.subscriber} {self.followed_user}'
