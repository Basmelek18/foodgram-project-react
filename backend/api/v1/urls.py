from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.views import FoodgramUserViewSet, TagsViewSet, RecipesViewSet, IngredientsViewSet

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
    'ingredients',
    IngredientsViewSet,
    basename='ingredients'
)
router_v1.register(
    'users',
    FoodgramUserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
