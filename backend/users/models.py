from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from foodgram import constants


class FoodgramUser(AbstractUser):
    """Custom user model."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username', 'password')

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Username',
        unique=True,
        max_length=constants.MAX_LENGTH_USERCHARFIELD,
        validators=[
            UnicodeUsernameValidator()
        ]
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=constants.MAX_LENGTH_USERCHARFIELD,
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=constants.MAX_LENGTH_USERCHARFIELD,
    )
    password = models.CharField(
        verbose_name='Password',
        max_length=constants.MAX_LENGTH_USERCHARFIELD,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('email', 'username', 'first_name', 'last_name')

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    """Subscriptions."""
    subscriber = models.ForeignKey(
        FoodgramUser,
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Subscriber',
    )
    followed_user = models.ForeignKey(
        FoodgramUser,
        related_name='followers',
        on_delete=models.CASCADE,
        verbose_name='Followed user',
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'followed_user'],
                name='unique_subscriptions'
            )
        ]
        ordering = ('subscriber', 'followed_user')

    def __str__(self):
        return f'{self.subscriber} {self.followed_user}'
