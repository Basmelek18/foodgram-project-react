from django.contrib import admin

from .models import FoodgramUser, Subscriptions


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    filter_fields = ('username', 'email',)


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'subscriber',
        'followed_user'
    )
    filter_fields = ('subscriber', 'followed_user')
