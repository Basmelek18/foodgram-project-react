from rest_framework import serializers

from users.models import FoodgramUser


class FoodgramUserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью user."""
    class Meta:
        model = FoodgramUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )