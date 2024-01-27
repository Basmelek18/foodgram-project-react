from django.contrib import admin

from .models import Tags, Ingredients, IngredientsInRecipes


@admin.register(Tags)
class CategoryAdmin(admin.ModelAdmin):
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


@admin.register(IngredientsInRecipes)
class IngredientsInRecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredient',
        'recipe',
    )
    search_fields = ('name',)

