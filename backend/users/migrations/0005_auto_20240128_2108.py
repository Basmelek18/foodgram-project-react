# Generated by Django 3.2.23 on 2024-01-28 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_subscriptions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptions',
            options={'verbose_name': 'Подписки', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AddConstraint(
            model_name='subscriptions',
            constraint=models.UniqueConstraint(fields=('subscriber', 'followed_user'), name='unique_subscriptions'),
        ),
    ]
