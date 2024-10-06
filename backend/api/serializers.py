from django.contrib.auth import get_user_model
from rest_framework.serializers import (CurrentUserDefault,
                                        ModelSerializer,
                                        SlugRelatedField,
                                        ValidationError)
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Tag, Ingredient, Recipe, Chosen, ShoppingList, Subscribe

User = get_user_model()


class TagSerializer(ModelSerializer):
    pass


class IngredientSerializer(ModelSerializer):
    pass


class RecipeSerializer(ModelSerializer):
    pass


class ChosenSerializer(ModelSerializer):
    pass


class ShoppingListSerializer(ModelSerializer):
    pass


class SubscribeSerializer(ModelSerializer):
    pass
