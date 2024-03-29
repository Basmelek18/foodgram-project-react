# Generated by Django 3.2.23 on 2024-02-03 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20240203_0225'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'default_related_name': 'favorite', 'ordering': ('user', 'recipe'), 'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='ingredientsinrecipes',
            options={'ordering': ('ingredient', 'recipe'), 'verbose_name': 'Ингредиент в рецептах', 'verbose_name_plural': 'Ингредиенты в рецептах'},
        ),
        migrations.AlterModelOptions(
            name='recipes',
            options={'ordering': ('name', 'author'), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'default_related_name': 'shopping_cart', 'ordering': ('user', 'recipe'), 'verbose_name': 'Список покупок', 'verbose_name_plural': 'Список покупок'},
        ),
        migrations.AlterModelOptions(
            name='tagsrecipes',
            options={'ordering': ('tag', 'recipe'), 'verbose_name': 'Тэг рецепта', 'verbose_name_plural': 'Тэги рецепта'},
        ),
    ]
