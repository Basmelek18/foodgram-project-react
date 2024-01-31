from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reportlab.pdfgen import canvas
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import FoodgramUser, Subscriptions
from api.v1.serializers import (
    TagsSerializer,
    IngredientsSerializer,
    RecipesWriteSerializer,
    RecipesReadSerializer,
    SubscribeSerializer,
    RecipesMiniSerializer,
)
from recipes.models import (
    Tags,
    Ingredients,
    Recipes,
    IngredientsInRecipes,
    Favorite,
    ShoppingCart
)
from api.v1.filters import RecipeFilter, IngredientFilter
from api.v1.permissions import IsRecipeOwner


class FoodgramUserViewSet(UserViewSet):
    """Вьюсет для работы с моделью user."""
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
    )
    def get_subscriptions(self, request):
        user = request.user
        subscriptions = self.paginate_queryset(
            Subscriptions.objects.filter(
                subscriber=user
            )
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
        permission_classes=(IsAuthenticated,)
    )
    def get_subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(FoodgramUser, pk=id)
        if user == author:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            subscription, status_sub = Subscriptions.objects.get_or_create(
                subscriber=user,
                followed_user=author
            )
            if not status_sub:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = SubscribeSerializer(
                subscription,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            subscription = Subscriptions.objects.filter(
                subscriber=user,
                followed_user=author
            ).first()
            if subscription is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesReadSerializer
        return RecipesWriteSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = (IsAuthenticated, IsRecipeOwner)
        return super().get_permissions()

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def get_favorite(self, request, pk):
        recipe = Recipes.objects.filter(id=pk).first()
        if recipe is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            favorite, status_favorite = Favorite.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if not status_favorite:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = RecipesMiniSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = get_object_or_404(
                Favorite,
                user=request.user,
                recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        recipe = Recipes.objects.filter(id=pk).first()
        if recipe is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            shopping_cart, status_cart = ShoppingCart.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if not status_cart:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = RecipesMiniSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            shopping_cart = ShoppingCart.objects.filter(
                user=request.user, recipe=recipe
            ).first()
            if shopping_cart is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            shopping_cart.delete()
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
