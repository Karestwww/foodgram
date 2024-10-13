from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from api.views import (TagsViewSet,
                    IngredientsViewSet,
                    RecipesViewSet,
                    UsersViewSet,
                    )

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tag')
router.register('recipes', RecipesViewSet, basename='recipe')
router.register('ingredients', IngredientsViewSet, basename='ingredient')
router.register('users', UsersViewSet, basename='users')


app_name = 'api'


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),  # Работа с пользователями
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # Работа с токенами
]
