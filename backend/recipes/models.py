from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import FoodgramUser
from foodgram import constants


class Ingredients(models.Model):
    """Ingredients."""
    name = models.CharField(
        verbose_name='Ingredient name',
        max_length=constants.MAX_NAME_LENGTH,
    )
    measurement_unit = models.CharField(
        verbose_name='Measurement unit',
        max_length=constants.MAX_NAME_LENGTH,
    )

    class Meta:
        verbose_name_plural = 'Ingredients'
        verbose_name = 'Ingredient'
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
    """Tags."""
    name = models.CharField(
        verbose_name='Tag name',
        max_length=constants.MAX_NAME_LENGTH,
        unique=True,
    )
    color = ColorField(
        verbose_name='Color',
        unique=True,
    )
    slug = models.CharField(
        verbose_name='Slug',
        max_length=constants.MAX_NAME_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Recipes."""
    name = models.CharField(
        verbose_name='Recipe name',
        max_length=constants.MAX_NAME_LENGTH,
    )
    text = models.TextField(
        verbose_name='Decription',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        default=None,
        verbose_name='Image',
    )
    tags = models.ManyToManyField(
        Tags,
        through='TagsRecipes',
        related_name='recipes',
        verbose_name='Tags',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsInRecipes',
        verbose_name='Ingredients',
    )
    author = models.ForeignKey(
        FoodgramUser,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Author',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time',
        validators=[
            MinValueValidator(
                constants.MIN_TIME,
                message=(
                    'Cooking time cannot be less '
                    f'{constants.MIN_TIME} minute'
                ),
            ),
            MaxValueValidator(
                constants.MAX_TIME,
                message=(
                    'Cooking time cannot be more '
                    f'{constants.MAX_TIME} minutes'
                ),
            ),
        ],

    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('name', 'author',)

    def __str__(self):
        return self.name


class TagsRecipes(models.Model):
    """Recipe's tags."""
    tag = models.ForeignKey(
        Tags,
        related_name='tags_recipes',
        on_delete=models.CASCADE,
        verbose_name='Tag'
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='tags_recipes',
        on_delete=models.CASCADE,
        verbose_name='Recipe'
    )

    class Meta:
        verbose_name = 'Recipe tag'
        verbose_name_plural = 'Recipe tags'
        ordering = ('tag', 'recipe',)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientsInRecipes(models.Model):
    """Ingredients in recipes."""
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Ingredient'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Recipe'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Amount',
        validators=[
            MinValueValidator(
                constants.MIN_INGREDIENTS,
                message=(
                    'Amount of ingredient cannot be less '
                    f'{constants.MIN_INGREDIENTS}'
                )
            ),
            MaxValueValidator(
                constants.MAX_INGREDIENTS,
                message=(
                    'Amount of ingredient cannot be more '
                    f'{constants.MAX_INGREDIENTS}'
                )
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецептах'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ('ingredient', 'recipe',)

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
        ordering = ('user', 'recipe')
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
        ordering = ('user', 'recipe')
        default_related_name = 'favorite'
