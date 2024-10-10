import base64
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.serializers import (CurrentUserDefault,
                                        ModelSerializer,
                                        SlugRelatedField,
                                        ValidationError,
                                        SerializerMethodField,
                                        ImageField,
                                        RegexField,
                                        PrimaryKeyRelatedField,
                                        ReadOnlyField,
                                        ChoiceField)
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import User, Tag, Ingredient, Recipe, Chosen, ShoppingList, Subscribe, Amount

#User = get_user_model()

class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]  # формат рисунка изымается
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class AvatarSerializer(ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)


class ImageRecipieSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('image',)


class UserPasswordSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('password',)


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'avatar')


class UserCreateSerializer(ModelSerializer):
    username = RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True,
        help_text='Тербуется  не более 150 символов. '
                  'Только буквы, цифры и @/./+/-/_.',
        error_messages={
            'invalid': ('Значение должны состоять только из буквы или '
                        'цифры или символов подчёркивания или дефисов.'),
        }
    )

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        user_with_same_username = (User.objects
                                   .filter(username=username).first())
        user_with_same_email = (User.objects
                                .filter(email=email).first())
        messege_error = {}
        if user_with_same_username and user_with_same_username.email != email:
            messege_error['username'] = username
        if user_with_same_email and user_with_same_email.username != username:
            messege_error['email'] = email
        if len(messege_error) > 0:
            raise serializers.ValidationError(messege_error)
        return data


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
        read_only_fields = ('name', 'slug')


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class AmountSerializer(ModelSerializer):

    id = ReadOnlyField(source='ingredients.id')
    name = ReadOnlyField(source='ingredients.name')
    measurement_unit = ReadOnlyField(source='ingredients.measurement_unit')
    ingredients = ReadOnlyField(source='ingredients.name')

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measurement_unit', 'ingredients')
#        read_only_fields = ('amounts',)


class RecipeSerializer(ModelSerializer):

    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer()
    ingredients = AmountSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
#        read_only_fields = ('id', 'author', 'name', 'image', 'text', 'ingredients', 'tags', 'cooking_time')

    def get_is_favorited(self, obj):
        if self.context.get('request').user:
            return False
        return Chosen.objects.filter(recipe=obj).exists()
        
    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request').user:
            return False
        return Chosen.objects.filter(recipe=obj).exists()


class ChosenSerializer(ModelSerializer):
    pass


class ShoppingListSerializer(ModelSerializer):
    pass


class SubscribeSerializer(ModelSerializer):
    pass
