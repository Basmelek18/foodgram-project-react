import base64

from django.conf import settings
import webcolors
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from users.models import FoodgramUser, Subscriptions

from recipes.models import Tags, Ingredients, Recipes, IngredientsInRecipes, TagsRecipes, Favorite, ShoppingCart


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CreateFoodgramUserSerializer(serializers.ModelSerializer):
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


class FoodgramUserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью user."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = FoodgramUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return Subscriptions.objects.filter(
            subscriber=self.context['request'].user,
            followed_user=obj
        ).exists()


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью подписок."""
    id = serializers.ReadOnlyField(source='followed_user.id')
    username = serializers.ReadOnlyField(source='followed_user.username')
    email = serializers.ReadOnlyField(source='followed_user.email')
    first_name = serializers.ReadOnlyField(source='followed_user.first_name')
    last_name = serializers.ReadOnlyField(source='followed_user.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscriptions
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return Subscriptions.objects.filter(
            subscriber=obj.subscriber,
            followed_user=obj.followed_user
        ).exists()

    def get_recipes(self, obj):
        recipes = obj.followed_user.recipes.all()
        return RecipesMiniSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.followed_user.recipes.count()

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя."
            )
        return value


class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

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


class IngredientsInRecipesSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsInRecipes
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class CreateIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
    )
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredients
        fields = (
            'id',
            'amount',
        )


class RecipesWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
    )
    cooking_time = serializers.IntegerField(min_value=1)
    ingredients = CreateIngredientSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipes
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('author',)

    @staticmethod
    def create_or_update_ingredients(ingredients, obj):
        for ingredient_data in ingredients:
            amount = ingredient_data.get('amount')
            pk = ingredient_data.get('id').id
            current_ingredient = get_object_or_404(
                Ingredients,
                pk=pk
            )
            IngredientsInRecipes.objects.create(
                ingredient=current_ingredient,
                recipe=obj,
                amount=amount
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        self.create_or_update_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        super().update(instance, validated_data)
        instance.ingredients.clear()
        self.create_or_update_ingredients(ingredients, instance)
        instance.tags.set(tags)
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tags'] = TagsSerializer(instance.tags.all(), many=True).data
        return response


class RecipesReadSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    author = FoodgramUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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
            'is_favorited',
            'is_in_shopping_cart'
        )

    @staticmethod
    def get_ingredients(obj):
        return IngredientsInRecipesSerializer(IngredientsInRecipes.objects.filter(recipe=obj), many=True).data

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            user=self.context['request'].user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(
            user=self.context['request'].user,
            recipe=obj
        ).exists()


class RecipesMiniSerializer(RecipesReadSerializer):
    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
