from django.db import models


class Tags(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipes(models.Model):
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class ShoppingCart(models.Model):
    class Meta:
        verbose_name = 'Список покупок'


class Favorite(models.Model):
    class Meta:
        verbose_name = 'Избранное'


class Subscriptions(models.Model):
    class Meta:
        verbose_name = 'Подписки'


class Ingredients(models.Model):
    class Meta:
        verbose_name = 'Ингридиенты'

