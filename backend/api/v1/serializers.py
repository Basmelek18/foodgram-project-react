from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import FoodgramUser, Subscriptions
from recipes.models import (
    Tags,
    Ingredients,
    Recipes,
    IngredientsInRecipes,
    Favorite,
    ShoppingCart
)
from foodgram import constants


class FoodgramUserSerializer(serializers.ModelSerializer):
    """Serializer for user."""
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
        request = self.context.get('request')
        return bool(
            request
            and request.user.is_authenticated
            and Subscriptions.objects.filter(
                subscriber=request.user,
                followed_user=obj
            ).exists()
        )


class SubscribeWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating subscriptions."""
    class Meta:
        model = Subscriptions
        fields = ('subscriber', 'followed_user')

    def validate(self, data):
        if data['subscriber'] == data['followed_user']:
            raise serializers.ValidationError(
                'You cannot subscribe to yourself'
            )
        subscription = Subscriptions.objects.filter(
            subscriber=data['subscriber'],
            followed_user=data['followed_user']
        ).exists()
        if self.context.get('request').method == 'POST':
            if subscription:
                raise serializers.ValidationError(
                    'You have already subscribed to this user'
                )
        if self.context.get('request').method == 'DELETE':
            if not subscription:
                raise serializers.ValidationError(
                    'You have not subscribed to this user'
                )
        return data

    def destroy(self):
        return Subscriptions.objects.filter(
            subscriber=self.validated_data.get('subscriber'),
            followed_user=self.validated_data.get('followed_user')
        ).delete()

    def to_representation(self, instance):
        return SubscribeSerializer(
            instance.followed_user,
            context={'request': self.context.get('request')}
        ).data


class SubscribeSerializer(FoodgramUserSerializer):
    """Serializer for subscriptions."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(FoodgramUserSerializer.Meta):
        model = FoodgramUser
        fields = FoodgramUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        pararms = self.context['request'].query_params
        if 'recipes_limit' in pararms:
            try:
                recipes = recipes[:int(pararms['recipes_limit'])]
            except ValueError:
                pass
        return RecipesMiniSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagsSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    class Meta:
        model = Tags
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientsSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""
    class Meta:
        model = Ingredients
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientsInRecipesSerializer(serializers.ModelSerializer):
    """Serializer for ingredients in recipes."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsInRecipes
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class CreateIngredientSerializer(serializers.ModelSerializer):
    """Serializer for creating ingredients in recipes."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
    )
    amount = serializers.IntegerField(
        write_only=True,
        min_value=constants.MIN_INGREDIENTS,
        max_value=constants.MAX_INGREDIENTS,
        required=True
    )

    class Meta:
        model = Ingredients
        fields = (
            'id',
            'amount',
        )


class RecipesWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating and editing recipes."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
    )
    cooking_time = serializers.IntegerField(min_value=1)
    ingredients = CreateIngredientSerializer(many=True)
    image = Base64ImageField(required=True)

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
        IngredientsInRecipes.objects.bulk_create(
            [
                IngredientsInRecipes(
                    recipe=obj,
                    ingredient=ingredient_data['id'],
                    amount=ingredient_data.get('amount')
                ) for ingredient_data in ingredients
            ]
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        image = self.initial_data.get('image')
        if not ingredients:
            raise serializers.ValidationError(
                'Ingredients cannot be empty'
            )
        if not tags:
            raise serializers.ValidationError(
                'Tags cannot be empty'
            )
        if not image:
            raise serializers.ValidationError(
                'Image cannot be empty'
            )
        ingredients_count = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_count) != len(set(ingredients_count)):
            raise serializers.ValidationError(
                'Ingredients must be unique'
            )
        tags_count = [tag for tag in tags]
        if len(tags_count) != len(set(tags_count)):
            raise serializers.ValidationError(
                'Tags must be unique'
            )
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(
            author=self.context.get('request').user,
            **validated_data
        )
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
        return RecipesReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class RecipesReadSerializer(serializers.ModelSerializer):
    """Serializer for reading recipes."""
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
        return IngredientsInRecipesSerializer(
            IngredientsInRecipes.objects.filter(recipe=obj),
            many=True
        ).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return bool(
            request
            and request.user.is_authenticated
            and Favorite.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return bool(
            request
            and request.user.is_authenticated
            and ShoppingCart.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
        )


class RecipesMiniSerializer(RecipesReadSerializer):
    """Serializer for custom recipes list."""
    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FavoriteWriteSerializer(serializers.ModelSerializer):
    """Serializer for favorite."""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        favorite = Favorite.objects.filter(
            user=self.context.get('request').user,
            recipe=data['recipe'].id
        )
        if self.context.get('request').method == 'POST':
            if favorite.exists():
                raise serializers.ValidationError(
                    'Recipe already added to favorites.'
                )
        if self.context.get('request').method == 'DELETE':
            if not favorite.exists():
                raise serializers.ValidationError(
                    'Recipe not added to favorites.'
                )
        return data

    def destroy(self):
        return Favorite.objects.filter(
            user=self.validated_data['user'].id,
            recipe=self.validated_data['recipe'].id
        ).delete()

    def to_representation(self, instance):
        return RecipesMiniSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingCartWriteSerializer(serializers.ModelSerializer):
    """Serializer for shopping_cart."""
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data):
        shopping_cart = ShoppingCart.objects.filter(
            user=self.context.get('request').user,
            recipe=data['recipe'].id
        )
        if self.context.get('request').method == 'POST':
            if shopping_cart.exists():
                raise serializers.ValidationError(
                    'Recipe already added to shopping cart.'
                )
        if self.context.get('request').method == 'DELETE':
            if not shopping_cart.exists():
                raise serializers.ValidationError(
                    'Recipe not added to shopping cart.'
                )
        return data

    def destroy(self):
        return ShoppingCart.objects.filter(
            user=self.validated_data['user'].id,
            recipe=self.validated_data['recipe'].id
        ).delete()

    def to_representation(self, instance):
        return RecipesMiniSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
