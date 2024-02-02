from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import FoodgramUser
from foodgram import constants


class Ingredients(models.Model):
    """Ингридиенты."""
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=constants.MAX_NAME_LENGTH,
    )
    measurement_unit = models.CharField(
        verbose_name='Размерность',
        max_length=constants.MAX_NAME_LENGTH,
    )

    class Meta:
        verbose_name_plural = 'Ингридиенты'
        verbose_name = 'Ингридиент'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            )
        ]

    def __str__(self):
        return self.name


class Tags(models.Model):
    """Тэги."""
    name = models.CharField(
        verbose_name='Название тэга',
        max_length=constants.MAX_NAME_LENGTH,
        unique=True,
    )
    color = ColorField(
        verbose_name='Цвет',
        unique=True,
    )
    slug = models.CharField(
        verbose_name='Slug',
        max_length=constants.MAX_NAME_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Рецепты."""
    name = models.CharField(
        verbose_name='Название',
        max_length=constants.MAX_NAME_LENGTH,
    )
    text = models.CharField(
        verbose_name='Описание',
        max_length=constants.MAX_TEXT_LENGTH,
    )
    image = models.ImageField(
        upload_to='recipes/images/',
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
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                constants.MIN_TIME,
                message=(
                    'Время приготовления не '
                    f'может быть меньше {constants.MIN_TIME} минуты'
                ),
            ),
            MaxValueValidator(
                constants.MAX_TIME,
                message=(
                    'Время приготовления не '
                    f'может быть больше {constants.MAX_TIME} минут'
                ),
            ),
        ],

    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('id',)

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = 'Тэг рецепта'
        verbose_name_plural = 'Тэги рецепта'
        ordering = ('id',)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


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
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                constants.MIN_INGREDIENTS,
                message=(
                    'Количество ингредиента не '
                    f'может быть меньше {constants.MIN_INGREDIENTS}'
                )
            ),
            MaxValueValidator(
                constants.MAX_INGREDIENTS,
                message=(
                    'Количество ингредиента не '
                    f'может быть больше {constants.MAX_INGREDIENTS}'
                )
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецептах'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ('id',)

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class BaseForFavoriteAndShoppingCart(models.Model):
    """Базовый класс для списка покупок и избранного."""
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(BaseForFavoriteAndShoppingCart):
    """Список покупок."""
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]
        ordering = ('id',)
        default_related_name = 'shopping_cart'


class Favorite(BaseForFavoriteAndShoppingCart):
    """Избранное."""
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]
        ordering = ('id',)
        default_related_name = 'favorite'
