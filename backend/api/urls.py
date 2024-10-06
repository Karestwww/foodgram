from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (TagsViewSet,
                    IngredientsViewSet,
                    RecipesViewSet,
                    ChosensViewSet,
                    UsersViewSet,
                    UserInfoViewSet,
                    SubscribeViewSet,
                    ShoppingsListViewSet)

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tag')
router.register('recipes', RecipesViewSet, basename='recipe')
router.register('ingredients', IngredientsViewSet, basename='ingredient')
router.register('users', UsersViewSet, basename='users')


app_name = 'api'


patterns_user = [
    path('users/me/', UserInfoViewSet.as_view({'get': 'get_current_user_info',}), name='current_user'),
    path('users/me/avatar/',
         UserInfoViewSet.as_view({'put': 'current_user_avatar',
                                  'delete': 'current_user_avatar'}), name='current_user_avatar'),
    path(r'^subscri\B', SubscribeViewSet.as_view(), name='subscribe'),
] 

urlpatterns = [
    path('recipes/<int:id>/get-link/', RecipesViewSet.as_view(), name='get-link'),
    path('recipes/<int:id>/favorite/', ShoppingsListViewSet.as_view(), name='favorite'),
    path('recipes/<int:id>/shopping_cart/', ShoppingsListViewSet.as_view(), name='shopping_cart'),
    path('recipes/download_shopping_cart/', ShoppingsListViewSet.as_view(), name='download_shopping_cart'),
    path('users/', include(patterns_user)),
    path('', include(router.urls, 'app_name')),
    path('', include('djoser.urls')),  # Работа с пользователями
    path('', include('djoser.urls.authtoken')),  # Работа с токенами
]
