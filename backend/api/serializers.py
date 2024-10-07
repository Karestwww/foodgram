from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import (CurrentUserDefault,
                                        ModelSerializer,
                                        SlugRelatedField,
                                        ValidationError,
                                        ChoiceField)
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Tag, Ingredient, Recipe, Chosen, ShoppingList, Subscribe

User = get_user_model()

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'avatar')


class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


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
