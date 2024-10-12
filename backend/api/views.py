from django.shortcuts import render
from api.serializers import (TagSerializer,
                             IngredientSerializer,
                             RecipeSerializer,
                             ChosenSerializer,
                             SubscribeSerializer,
                             UserSerializer,
                             AvatarSerializer,
                             UserCreateSerializer,
                             CreateRecipeSerializer,
                             UserPasswordSerializer,
                             ShoppingListSerializer)
from api.paginators import StandardResultsSetPagination
from api.permissions import IsAdminOrReadOnly
from recipes.models import User, Tag, Ingredient, Recipe, Chosen, ShoppingList, Subscribe
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_204_NO_CONTENT
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api.filters import RecipeFilter


class UsersViewSet(ModelViewSet):
    """Модель пользователя."""
    queryset = User.objects.all()
    http_method_names = ['get', 'post']
    pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        else:
            return UserCreateSerializer


class UserCreateViewSet(ModelViewSet):
    """Модель пользователя."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserInfoViewSet(ModelViewSet):
    """Информация о пользователе."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated], url_path='me')
    def get_current_user_info(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=HTTP_200_OK)


class UserPasswordViewSet(ModelViewSet):
    """Установить новый пароль."""

    queryset = User.objects.all()
    serializer_class = UserPasswordSerializer
    http_method_names = ['post']

    @action(methods=['post'], detail=False,
            permission_classes=[IsAuthenticated], url_path='set_password')
    def user_set_password(self, request):
        if request.method == 'POST':
            serializer = UserPasswordSerializer(request.user, data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=HTTP_204_NO_CONTENT)


class AvatarViewSet(ModelViewSet):
    """Аватар."""

    queryset = User.objects.all()
    serializer_class = AvatarSerializer
    http_method_names = ['put', 'delete']

    @action(methods=['put', 'delete'], detail=False,
            permission_classes=[IsAuthenticated], url_path='me/avatar')
    def current_user_avatar(self, request):

        if request.method == 'PUT':
            serializer = AvatarSerializer(request.user, data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        request.user.avatar.delete()
        request.user.avatar = None
        request.user.save()
        return Response(status=HTTP_204_NO_CONTENT)


class TagsViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']
    filterset_fields = ('name',)
#    permission_classes = (IsAdminOrReadOnly, )
#    pagination_class = StandardResultsSetPagination


class IngredientsViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
#    search_fields = ('name',)


class RecipesViewSet(ModelViewSet):
    """По модели Recipe все стандартные виды запросов через viewsets."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer


class ChosensViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = Chosen.objects.all()
    serializer_class = ChosenSerializer


class ShoppingsListViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer


class SubscribeViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
