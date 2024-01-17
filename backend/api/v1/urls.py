from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.views import UserViewSet, TagsViewSet, RecipesViewSet, ShoppingCartViewSet, FavoriteViewSet, IngredientsViewSet

router_v1 = DefaultRouter()

router_v1.register(
    'tags',
    TagsViewSet,
    basename='tags'
)

router_v1.register(
    'recipes',
    RecipesViewSet,
    basename='recipes'
)

router_v1.register(
    r'recipes/(?P<recipes_id>\d+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shopping_cart'
)

router_v1.register(
    r'recipes/(?P<recipes_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite'
)

router_v1.register(
    'ingredients',
    IngredientsViewSet,
    basename='ingredients'
)
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
