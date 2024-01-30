from django.conf import settings
from django.db import models

from users.models import FoodgramUser


class Ingredients(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=settings.MAX_NAME_LENGTH,
    )
    measurement_unit = models.CharField(
        verbose_name='Размерность',
        max_length=settings.MAX_NAME_LENGTH,
    )

    class Meta:
        verbose_name = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(
        verbose_name='Название тэга',
        max_length=settings.MAX_NAME_LENGTH,
        unique=True,
        null=False,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=settings.COLOR_LENGTH,
        unique=True,
        null=False,
    )
    slug = models.CharField(
        verbose_name='Slug',
        max_length=settings.MAX_NAME_LENGTH,
        unique=True,
        null=False,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipes(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.MAX_NAME_LENGTH,
    )
    text = models.CharField(
        verbose_name='Описание',
        max_length=settings.MAX_NAME_LENGTH,
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=False,
        default=None
    )
    tags = models.ManyToManyField(
        Tags,
        through='TagsRecipes',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsInRecipes',
    )
    author = models.ForeignKey(
        FoodgramUser,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    cooking_time = models.IntegerField()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class TagsRecipes(models.Model):
    tag = models.ForeignKey(
        Tags,
        related_name='tags_recipes',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipes,
        related_name='tags_recipes',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientsInRecipes(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe'
    )
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'ингредиенты в рецептах'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        related_name='favorite',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipes,
        related_name='favorite',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранное'
