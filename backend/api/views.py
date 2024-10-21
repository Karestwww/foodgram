from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.paginators import StandardResultsSetPagination
from api.permissions import IsAuthorOrReadOnly
from api.querysets import shopping_cart_file
from api.serializers import (AvatarSerializer, CreateRecipeSerializer,
                             IngredientSerializer, RecipeSerializer,
                             SimpleRecipeSerializer, SubscribeSerializer,
                             TagSerializer, UserCreateSerializer,
                             UserSerializer)
from backend.settings import DOMAIN
from recipes.models import (Chosen, Ingredient, Recipe, ShoppingList,
                            Subscribe, Tag, User)


class UsersViewSet(ModelViewSet):
    """По модели пользователя запросы get, post, put, delete."""
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        else:
            return UserCreateSerializer

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated],
            url_path='subscriptions')
    def user_subscriptions(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            user = self.request.user
            subscribes = user.subscribers.all()
            pages = self.paginate_queryset(subscribes)
            serializer = SubscribeSerializer(pages, many=True,
                                             context={'request': request})
            return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='subscribe')
    def subscribe(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        author_subscribes = get_object_or_404(User, id=pk)
        if self.request.method == 'POST':
            if user == author_subscribes:
                return Response({'detail': 'Не подписывайся на себя.'},
                                status=HTTP_400_BAD_REQUEST)
            elif Subscribe.objects.filter(user=user,
                                          author_recipies=author_subscribes
                                          ).exists():
                return Response({'detail': 'Вы уже подписаны.'},
                                status=HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(user=user,
                                     author_recipies=author_subscribes)
            serializer = SubscribeSerializer(author_subscribes,
                                             context={'request': request})
            if serializer.is_valid:
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST)
        subscription = Subscribe.objects.filter(
            user=user,
            author_recipies=author_subscribes)
        if not subscription.exists():
            return Response({'detail': 'Вы не подписаны.'},
                            status=HTTP_400_BAD_REQUEST)
        subscription.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated], url_path='me')
    def get_current_user_info(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user,
                                        context={'request': request})
            return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['put', 'delete'], detail=False,
            permission_classes=[IsAuthenticated], url_path='me/avatar')
    def current_user_avatar(self, request):
        if request.method == 'PUT':
            serializer = AvatarSerializer(request.user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST)
        request.user.avatar.delete()
        request.user.avatar = None
        request.user.save()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False,
            permission_classes=[IsAuthenticated], url_path='set_password')
    def user_set_password(self, request):
        serializer = SetPasswordSerializer(context={'request': request},
                                           data=request.data)
        if serializer.is_valid():
            self.request.user.set_password(serializer.data["new_password"])
            self.request.user.save()
            return Response(serializer.data, status=HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=HTTP_400_BAD_REQUEST)


class TagsViewSet(ModelViewSet):
    """Модель get запросов для получения списка тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']
    filterset_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientsViewSet(ModelViewSet):
    """Модель get запросов для получения списка ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = (IngredientFilter,)
    filterset_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class RecipesViewSet(ModelViewSet):
    """По модели Recipe стандартные виды запросов через viewsets."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        url = f"{DOMAIN}/recipes/{recipe.id}/"
        return Response({'short-link': url}, status=HTTP_200_OK)

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='favorite')
    def favorite(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if self.request.method == 'POST':
            if Chosen.objects.filter(user=user, recipe=recipe).exists():
                return Response({'detail': 'Рецепт уже в избранном.'},
                                status=HTTP_400_BAD_REQUEST)
            Chosen.objects.update_or_create(user=user, recipe=recipe)
            serializer = SimpleRecipeSerializer(recipe,
                                                context={'request': request})
            if serializer.is_valid:
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST)
        chosen = Chosen.objects.filter(user=user, recipe=recipe)
        if not chosen.exists():
            return Response({'detail': 'Рецепт не в избранном.'},
                            status=HTTP_400_BAD_REQUEST)
        chosen.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='shopping_cart')
    def shopping_list(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if self.request.method == 'POST':
            if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
                return Response({'detail': 'Рецепт уже в списке покупок.'},
                                status=HTTP_400_BAD_REQUEST)
            ShoppingList.objects.update_or_create(user=user, recipe=recipe)
            serializer = SimpleRecipeSerializer(recipe,
                                                context={'request': request})
            if serializer.is_valid:
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST)
        shopping_list = ShoppingList.objects.filter(user=user, recipe=recipe)
        if not shopping_list.exists():
            return Response({'detail': 'Рецепт не в списке покупок.'},
                            status=HTTP_400_BAD_REQUEST)
        shopping_list.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated],
            url_path='download_shopping_cart')
    def download_shopping_cart(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            user = self.request.user
            if not user.in_shopping_cart.exists():
                return Response('Список покупок пуст.',
                                status=HTTP_404_NOT_FOUND)
            return shopping_cart_file(self, request, user)
