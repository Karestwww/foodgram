from django.shortcuts import get_object_or_404, get_list_or_404, render
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
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from backend.settings import DOMAIN
from recipes.models import User, Tag, Ingredient, Recipe, Chosen, ShoppingList, Subscribe
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api.filters import RecipeFilter
from djoser.serializers import SetPasswordSerializer
from api.querysets import shopping_cart_file


class UsersViewSet(ModelViewSet):
    """Модель пользователя."""
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

    @action(methods=['get'], detail=False, 
             permission_classes=[IsAuthenticated], url_path='subscriptions')
    def user_subscriptions(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            user=self.request.user
            subscribes = user.subscribers.all()
            pages = self.paginate_queryset(subscribes)
            serializer = SubscribeSerializer(pages, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True, 
             permission_classes=[IsAuthenticated], url_path='subscribe')
    def subscribe(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        author_subscribes = get_object_or_404(User, id=pk)
        if self.request.method == 'POST':
            if user == author_subscribes:
                return Response({'detail': 'Подписываться на себя запрещено.'}, status=HTTP_400_BAD_REQUEST)
            elif Subscribe.objects.filter(user=user, author_recipies=author_subscribes).exists():
                return Response({'detail': 'Вы уже подписаны.'}, status=HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(user=user, author_recipies=author_subscribes)
            serializer = SubscribeSerializer(author_subscribes, context={'request': request})
            if serializer.is_valid:
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST)
        # if request.method == 'DELETE'
        subscription = Subscribe.objects.filter(user=user, author_recipies=author_subscribes)
        if not subscription.exists():
            return Response({'detail': 'Вы не подписаны.'}, status=HTTP_400_BAD_REQUEST)
        subscription.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated], url_path='me')
    def get_current_user_info(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user, context={'request': request})
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
    def user_set_password(self, request):  # функция установления пароля
        if request.method == 'POST':  # проверяем на постметод
            serializer = SetPasswordSerializer(context={'request': request}, data=request.data)
            # сериализация встроенным в джойстер сериализатором
            if serializer.is_valid():  # Если данные соответсвуюут, то
                self.request.user.set_password(serializer.data["new_password"])  
                # устанавливаем пользователю пароль переданный в словаре new_password
                self.request.user.save()
                return Response(serializer.data, status=HTTP_204_NO_CONTENT)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST)


'''class UserCreateViewSet(ModelViewSet):
    """Модель пользователя."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer'''


'''class UserInfoViewSet(ModelViewSet):  # неактуально, перекинул в UsersViewSet
    """Информация о пользователе."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated], url_path='me')
    def get_current_user_infos(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user, context={'request': request})
            return Response(serializer.data, status=HTTP_200_OK)'''


'''class UserPasswordViewSet(ModelViewSet):  # неактуально, перекинул в UsersViewSet
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
            return Response(serializer.data, status=HTTP_204_NO_CONTENT)'''


'''class AvatarViewSet(ModelViewSet):  # неактуально, перекинул в UsersViewSet
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
        return Response(status=HTTP_204_NO_CONTENT)'''


class TagsViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']
    filterset_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
#    pagination_class = StandardResultsSetPagination


class IngredientsViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
#    search_fields = ('name',)


class RecipesViewSet(ModelViewSet):
    """По модели Recipe все стандартные виды запросов через viewsets."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
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

    @action(methods=['post', 'delete'], detail=True, 
             permission_classes=[IsAuthenticated], url_path='favorite')
    def favorite(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        #breakpoint()
        if self.request.method == 'POST':
            #если уже в избранном ошибка 400
            if Chosen.objects.filter(user=user, recipe=recipe).exists():
                return Response({'detail': 'Рецепт уже в избранном.'}, status=HTTP_400_BAD_REQUEST)
            Chosen.objects.update_or_create(user=user, recipe=recipe)
            serializer = ChosenSerializer(recipe, context={'request': request})
            if serializer.is_valid:
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST)
        chosen = Chosen.objects.filter(user=user, recipe=recipe)
        if not chosen.exists():
            return Response({'detail': 'Рецепт не в избранном.'}, status=HTTP_400_BAD_REQUEST)
        chosen.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True, 
             permission_classes=[IsAuthenticated], url_path='shopping_cart')
    def shopping_list(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if self.request.method == 'POST':
            if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
                return Response({'detail': 'Рецепт уже в списке покупок.'}, status=HTTP_400_BAD_REQUEST)
            ShoppingList.objects.update_or_create(user=user, recipe=recipe)
            serializer = ShoppingListSerializer(recipe, context={'request': request})
            if serializer.is_valid:
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST)
        shopping_list = ShoppingList.objects.filter(user=user, recipe=recipe)
        if not shopping_list.exists():
            return Response({'detail': 'Рецепт не в списке покупок.'}, status=HTTP_400_BAD_REQUEST)
        shopping_list.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, 
             permission_classes=[IsAuthenticated], url_path='download_shopping_cart')
    def download_shopping_cart(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            user=self.request.user
            if not user.in_shopping_cart.exists():
                return Response('Список покупок пуст.',status=HTTP_404_NOT_FOUND)
            return shopping_cart_file(self, request, user)

            #subscribes = user.subscribers.all()
            #pages = self.paginate_queryset(subscribes)
            #serializer = SubscribeSerializer(pages, many=True, context={'request': request})
            #return self.get_paginated_response(serializer.data)




'''class ChosensViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = Chosen.objects.all()
    serializer_class = ChosenSerializer'''


'''class ShoppingsListViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer'''


'''class SubscribeViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
'''