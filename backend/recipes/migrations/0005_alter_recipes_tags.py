# Generated by Django 3.2.23 on 2024-01-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20240119_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', through='recipes.TagsRecipes', to='recipes.Tags'),
        ),
    ]
