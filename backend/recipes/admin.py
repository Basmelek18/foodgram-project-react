from django.contrib import admin

from .models import (
    Tags,
    Ingredients,
    IngredientsInRecipes,
    ShoppingCart,
    Recipes,
    TagsRecipes,
    Favorite
)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    filter_fields = ('name',)


class TagsRecipesInline(admin.TabularInline):
    model = TagsRecipes


class IngredientsInRecipesInline(admin.TabularInline):
    model = IngredientsInRecipes


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = ('name',)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    inlines = [
        IngredientsInRecipesInline,
        TagsRecipesInline
    ]
    list_display = (
        'pk',
        'name',
        'author',
        'image',
        'text',
        'cooking_time',
    )
    search_fields = ('name',)
    filter_fields = ('author', 'name', 'tags')


@admin.register(Favorite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = ('name',)


@admin.register(TagsRecipes)
class TagsRecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'tag',
        'recipe',
    )
    search_fields = ('name',)


@admin.register(IngredientsInRecipes)
class IngredientsInRecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredient',
        'recipe',
    )
    search_fields = ('name',)
