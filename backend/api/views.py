from django.shortcuts import render
from api.serializers import (TagSerializer,
                             IngredientSerializer,
                             RecipeSerializer,
                             ChosenSerializer,
                             ShoppingListSerializer)
from recipes.models import Tag, Ingredient, Recipe, Chosen, ShoppingList
from rest_framework.viewsets import ModelViewSet


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
