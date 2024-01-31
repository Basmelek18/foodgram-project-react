from django.conf import settings
from django.db import models

from users.models import FoodgramUser


class Ingredients(models.Model):
    """Ингридиенты."""
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=settings.MAX_NAME_LENGTH,
    )
    measurement_unit = models.CharField(
        verbose_name='Размерность',
        max_length=settings.MAX_NAME_LENGTH,
    )

    class Meta:
        verbose_name_plural = 'Ингридиенты'
        verbose_name = 'Ингридиент'

    def __str__(self):
        return self.name


class Tags(models.Model):
    """Тэги."""
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
    """Рецепты."""
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
        default=None,
        verbose_name='Картинка',
    )
    tags = models.ManyToManyField(
        Tags,
        through='TagsRecipes',
        related_name='recipes',
        verbose_name='Тэги',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsInRecipes',
        verbose_name='Ингредиенты',
    )
    author = models.ForeignKey(
        FoodgramUser,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    cooking_time = models.IntegerField()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class TagsRecipes(models.Model):
    """Тэги рецепта."""
    tag = models.ForeignKey(
        Tags,
        related_name='tags_recipes',
        on_delete=models.CASCADE,
        verbose_name='Тэг'
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='tags_recipes',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'{self.tag} {self.recipe}'

    class Meta:
        verbose_name = 'Тэг рецепта'
        verbose_name_plural = 'Тэги рецепта'


class IngredientsInRecipes(models.Model):
    """Ингредиенты в рецептах."""
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Рецепт'
    )
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'Ингредиент в рецептах'
        verbose_name_plural = 'Ингредиенты в рецептах'


class ShoppingCart(models.Model):
    """Список покупок."""
    user = models.ForeignKey(
        FoodgramUser,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]


class Favorite(models.Model):
    """Избранное."""
    user = models.ForeignKey(
        FoodgramUser,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'

    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
