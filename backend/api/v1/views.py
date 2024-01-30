from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from reportlab.pdfgen import canvas
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
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
    RecipesMiniSerializer,
)
from recipes.models import Tags, Ingredients, Recipes, IngredientsInRecipes, Favorite, ShoppingCart

from api.v1.filters import RecipeFilter, IngredientFilter


class FoodgramUserViewSet(UserViewSet):
    """
    Получение списка всех пользователей.
    """
    queryset = FoodgramUser.objects.all()
    pagination_class = LimitOffsetPagination

    @action(
        methods=['GET'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
    )
    def get_current_user_info(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK, )

    @action(
        methods=['GET'],
        detail=False,
        url_path='subscriptions',
        permission_classes=(IsAuthenticated,),
        pagination_class=LimitOffsetPagination
    )
    def get_subscriptions(self, request):
        user = request.user
        subscriptions = self.paginate_queryset(
            Subscriptions.objects.filter(
                subscriber=user
            )
        )
        serializer = SubscribeSerializer(subscriptions, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='subscribe',
        permission_classes=(IsAuthenticated,)
    )
    def get_subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(FoodgramUser, pk=id)
        if request.method == 'POST':
            subscription, status_sub = Subscriptions.objects.get_or_create(
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
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesReadSerializer
        return RecipesWriteSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def get_favorite(self, request, pk):
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
            ShoppingCart.objects.get_or_create(user=request.user, recipe=recipe)
            serializer = RecipesMiniSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            shopping_cart = get_object_or_404(ShoppingCart, user=request.user, recipe=recipe)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientsInRecipes.objects.filter(recipe__shopping_cart__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.pdf"'

        pdf = canvas.Canvas(response)
        pdf.drawString(100, 800, "Shopping Cart")

        y_position = 780
        for ingredient in ingredients:
            ingredient_line = f"{ingredient['ingredient__name']}, {ingredient['ingredient__measurement_unit']}, {ingredient['amount']}"
            pdf.drawString(100, y_position, ingredient_line)
            y_position -= 20

        pdf.showPage()
        pdf.save()

        return response


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
