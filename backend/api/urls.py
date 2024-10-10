from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from api.views import (TagsViewSet,
                    IngredientsViewSet,
                    RecipesViewSet,
                    ChosensViewSet,
                    UsersViewSet,
                    UserInfoViewSet,
                    AvatarViewSet,
                    SubscribeViewSet,
                    UserCreateViewSet,
                    UserPasswordViewSet,
                    ShoppingsListViewSet)

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tag')
router.register('recipes', RecipesViewSet, basename='recipe')
router.register('ingredients', IngredientsViewSet, basename='ingredient')
router.register('users', UsersViewSet, basename='users')


app_name = 'api'


patterns_user = [
#    path('', UsersViewSet.as_view({'get': 'list'}), name='users'),  # удалить, скорее всего дублирование пути
#    path('', UserCreateViewSet.as_view({'post': 'create'}), name='users_create'),  # удалить, скорее всего дублирование пути
    path('me/avatar/',
         AvatarViewSet.as_view({'put': 'current_user_avatar',
                                  'delete': 'current_user_avatar'}), name='current_user_avatar'),
    path('me/', UserInfoViewSet.as_view({'get': 'get_current_user_info',}), name='current_user'),
#    re_path(r'^subscri\B', SubscribeViewSet.as_view(), name='subscribe'),
#    path('set_password/', UserPasswordViewSet.as_view({'post': 'user_set_password',}), name='set_password'),
] 

urlpatterns = [
#    path('recipes/<int:id>/get-link/', RecipesViewSet.as_view(), name='get-link'),
#    path('recipes/<int:id>/favorite/', ShoppingsListViewSet.as_view(), name='favorite'),
#    path('recipes/<int:id>/shopping_cart/', ShoppingsListViewSet.as_view(), name='shopping_cart'),
#    path('recipes/download_shopping_cart/', ShoppingsListViewSet.as_view(), name='download_shopping_cart'),
    path('users/', include(patterns_user)),
    path('', include('djoser.urls')),  # Работа с пользователями
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # Работа с токенами
    path('', include(router.urls)),
]
