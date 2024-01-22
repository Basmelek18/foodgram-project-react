from django.conf import settings
from rest_framework import serializers

from users.models import FoodgramUser

from recipes.models import Tags, Ingredients, Recipes


class FoodgramUserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью user."""
    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = FoodgramUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )

    def create(self, validated_data):
        user = FoodgramUser(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipesSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
    )
    author = FoodgramUserSerializer(read_only=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('author',)
