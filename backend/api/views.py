from django.shortcuts import render
from api.serializers import (TagSerializer,
                             IngredientSerializer,
                             RecipeSerializer,
                             ChosenSerializer,
                             SubscribeSerializer,
                             ShoppingListSerializer)
from recipes.models import User, Tag, Ingredient, Recipe, Chosen, ShoppingList, Subscribe
from rest_framework.viewsets import ModelViewSet


class UsersViewSet(ModelViewSet):
    """Модель пользователя."""
    queryset = User.objects.all()


class UserInfoViewSet(ModelViewSet):
    """Информация о пользователе."""
    queryset = User.objects.all()

    def get_current_user_info(self, request):
        pass

    def current_user_avatar(self, request):
        pass


class TagsViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipesViewSet(ModelViewSet):
    """По модели POST все стандартные виды запросов через viewsets."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


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
