from rest_framework import viewsets

from api.v1.serializers import FoodgramUserSerializer
from users.models import FoodgramUser


class UserViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех пользователей.
    """
    queryset = FoodgramUser.objects.all()
    serializer_class = FoodgramUserSerializer


class TagsViewSet(viewsets.ModelViewSet):
    pass


class RecipesViewSet(viewsets.ModelViewSet):
    pass


class ShoppingCartViewSet(viewsets.ModelViewSet):
    pass


class FavoriteViewSet(viewsets.ModelViewSet):
    pass


class SubscriptionsViewSet(viewsets.ModelViewSet):
    pass


class IngredientsViewSet(viewsets.ModelViewSet):
    pass
