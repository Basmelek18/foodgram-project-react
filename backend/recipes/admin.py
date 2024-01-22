from django.contrib import admin

from .models import Tags, Ingredients


@admin.register(Tags)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)


