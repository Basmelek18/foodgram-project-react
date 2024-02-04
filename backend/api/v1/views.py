from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reportlab.pdfgen import canvas
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from users.models import FoodgramUser, Subscriptions
from api.v1.serializers import (
    TagsSerializer,
    IngredientsSerializer,
    RecipesWriteSerializer,
    RecipesReadSerializer,
    SubscribeSerializer,
    SubscribeWriteSerializer,
    FavoriteWriteSerializer,
    ShoppingCartWriteSerializer
)
from recipes.models import (
    Tags,
    Ingredients,
    Recipes,
    IngredientsInRecipes
)
from api.v1.filters import RecipeFilter, IngredientFilter
from api.v1.permissions import IsRecipeOwner


class FoodgramUserViewSet(UserViewSet):
    """Вьюсет для работы с моделью user."""
    queryset = FoodgramUser.objects.all()
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated(), ]
        return super().get_permissions()

    @action(
        methods=['GET'],
        detail=False,
        url_path='subscriptions',
        permission_classes=(IsAuthenticated,),
    )
    def get_subscriptions(self, request):
        user = request.user
        queryset = FoodgramUser.objects.filter(
            followers__in=Subscriptions.objects.select_related('followed_user').filter(
                subscriber=user
            )
        )
        subscriptions = self.paginate_queryset(
            queryset
        )
        serializer = SubscribeSerializer(
            subscriptions,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='subscribe',
        permission_classes=(IsAuthenticated, )
    )
    def get_subscribe(self, request, id):
        user = request.user
        data = {'subscriber': user.id, 'followed_user': id}
        get_object_or_404(FoodgramUser, id=id)
        serializer = SubscribeWriteSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'POST':
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            serializer.destroy()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с моделью tags."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделью recipes."""
    queryset = Recipes.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsRecipeOwner, IsAuthenticatedOrReadOnly,)

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
    def get_favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavoriteWriteSerializer(
            data=data,
            context={'request': request}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(Recipes, id=pk)
            serializer.is_valid(raise_exception=True)
            serializer.destroy()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingCartWriteSerializer(
            data=data,
            context={'request': request}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(Recipes, id=pk)
            serializer.is_valid(raise_exception=True)
            serializer.destroy()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientsInRecipes.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; '
            'filename="shopping_cart.pdf"'
        )

        pdf = canvas.Canvas(response)
        pdf.setFont('Helvetica', 14)
        pdf.drawString(100, 800, 'Shopping Cart')

        y_position = 780
        for ingredient in ingredients:
            ingredient_line = (
                f'{ingredient["ingredient__name"]},'
                f'{ingredient["ingredient__measurement_unit"]},'
                f'{ingredient["amount"]}'
            )
            pdf.drawString(100, y_position, ingredient_line)
            y_position -= 20

        pdf.showPage()
        pdf.save()

        return response


class IngredientsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделью ingredients."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
