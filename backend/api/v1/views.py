from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import FoodgramUser

from api.v1.serializers import TagsSerializer, IngredientsSerializer, FoodgramUserSerializer, RecipesSerializer
from recipes.models import Tags, Ingredients, Recipes


class UserViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех пользователей.
    """
    queryset = FoodgramUser.objects.all()
    serializer_class = FoodgramUserSerializer

    @action(
        methods=['GET'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_current_user_info(self, request):
        serializer = FoodgramUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    pass


class FavoriteViewSet(viewsets.ModelViewSet):
    pass


class SubscriptionsViewSet(viewsets.ModelViewSet):
    pass


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
