from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (TagsViewSet,
                    IngredientsViewSet,
                    RecipesViewSet,
                    ChosensViewSet,
                    ShoppingsListViewSet)

router = DefaultRouter()
router.register(r'tags', TagsViewSet)
router.register(r'recipes', RecipesViewSet)
router.register(r'ingredients', IngredientsViewSet)


app_name = 'api'

urlpatterns = [
    path('', include(router.urls, 'app_name')),
    path('', include('djoser.urls')),  # Работа с пользователями
    path('', include('djoser.urls.authtoken')),  # Работа с токенами
]
