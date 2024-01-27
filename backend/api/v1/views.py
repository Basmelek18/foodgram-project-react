from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import FoodgramUser, Subscriptions

from api.v1.serializers import (
    TagsSerializer,
    IngredientsSerializer,
    FoodgramUserSerializer,
    RecipesWriteSerializer,
    RecipesReadSerializer,
    IngredientsInRecipesSerializer,
    SubscribeSerializer,
    CreateFoodgramUserSerializer,
    RecipesMiniSerializer
)
from recipes.models import Tags, Ingredients, Recipes, IngredientsInRecipes, Favorite, ShoppingCart


class UserViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех пользователей.
    """
    queryset = FoodgramUser.objects.all()
    serializer_class = CreateFoodgramUserSerializer

    @action(
        methods=['GET'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        pagination_class=PageNumberPagination
    )
    def get_current_user_info(self, request):
        serializer = CreateFoodgramUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['GET'],
        detail=False,
        url_path='subscriptions',
        permission_classes=(IsAuthenticated,)
    )
    def get_subscriptions(self, request):
        user = request.user
        subscriptions = user.subscriptions.all()
        serializer = SubscribeSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='subscribe',
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(FoodgramUser, id=pk)
        if request.method == 'POST':
            subscription = Subscriptions.objects.create(
                subscriber=user,
                followed_user=author
            )
            serializer = SubscribeSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscriptions,
                subscriber=user,
                followed_user=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesWriteSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesReadSerializer
        return RecipesWriteSerializer

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipes, id=pk)
        if request.method == 'POST':
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = RecipesMiniSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = get_object_or_404(Favorite, user=request.user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipes, id=pk)
        if request.method == 'POST':
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            serializer = RecipesMiniSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            shopping_cart = get_object_or_404(ShoppingCart, user=request.user, recipe=recipe)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
