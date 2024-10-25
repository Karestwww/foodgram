import base64

from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import (ImageField, IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField, ValidationError)
from rest_framework.status import HTTP_400_BAD_REQUEST

from recipes.models import Amount, Ingredient, Recipe, Tag, User


class Base64ImageField(ImageField):
    """Поверка рисунков по Base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]  # формат рисунка изымается
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class AvatarSerializer(ModelSerializer):
    """Сериализатор аватаров."""
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя при выводе о не информации."""
    is_subscribed = SerializerMethodField()
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'avatar')
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        user = request.user
        if user.is_anonymous:
            return False
        return user.user_subscribe.filter(author_recipies=obj).exists()


class UserCreateSerializer(ModelSerializer):
    """Сериализатор пользователия при его создании."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
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
    """Сериализатор тэгов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
        read_only_fields = ('name', 'slug')


class IngredientSerializer(ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class AmountSerializer(ModelSerializer):
    """Вспомогательный сериализатор кол-ва ингредиентов."""
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ModelSerializer):
    """Сериализатор для вывода информации о рецепте."""
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer()
    image = Base64ImageField()
    ingredients = AmountSerializer(source='recipe_ingredients',
                                   many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.favorited.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.in_shopping_cart.filter(recipe=obj).exists()


class AmountCreateRecipeSerializer(ModelSerializer):
    """Вспомогательный сериализатор для CreateRecipeSerializer."""
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = IntegerField(min_value=settings.MIN_AMOUNT,
                          max_value=settings.MAX_AMOUNT)

    class Meta:
        model = Amount
        fields = ('id', 'amount')


class CreateRecipeSerializer(ModelSerializer):
    """Сериализатор рецептов для их создания."""
    ingredients = AmountCreateRecipeSerializer(many=True, write_only=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    cooking_time = IntegerField(min_value=settings.MIN_COOKING_TIME,
                                max_value=settings.MAX_COOKING_TIME)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'image', 'name', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        return obj.favorited.exists()

    def get_is_in_shopping_cart(self, obj):
        return obj.in_shopping_cart.exists()

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError(
                {'ingredients': 'Ингредиент, обязательное поле!'})
        ingredients_set = set()
        for item in ingredients:
            ingredient = get_object_or_404(Ingredient, name=item['id'])
            if ingredient in ingredients_set:
                raise ValidationError(
                    {'ingredients': 'Дублирование ингредиентов запрещено!'})
            ingredients_set.add(ingredient)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError(
                {'tags': 'Тег, обязательное поле!'})
        tags_set = set()
        for tag in tags:
            if tag in tags_set:
                raise ValidationError(
                    {'tags': 'Дублирование тегов запрещено!'})
            tags_set.add(tag)
        return value

    def add_ingredients_or_tags(self, recipe, ingredients_data, tags_data):
        recipe.tags.set(tags_data)
        ingredients_to_create = [
            Amount(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients_data
        ]
        Amount.objects.bulk_create(ingredients_to_create)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.add_ingredients_or_tags(recipe, ingredients_data, tags_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        if not ingredients_data:
            raise ValidationError(
                {'ingredients': 'Ингредиент, обязательное поле!'})
        tags_data = validated_data.pop('tags', None)
        if not tags_data:
            raise ValidationError(
                {'tags': 'Тег, обязательное поле!'})
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.ingredients.clear()
        instance.tags.clear()
        self.add_ingredients_or_tags(instance, ingredients_data, tags_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        """Корректировка формата вывода данных."""
        ret = super().to_representation(instance)
        ret['ingredients'] = AmountSerializer(
            instance.recipe_ingredients.all(), many=True).data
        ret['tags'] = TagSerializer(instance.tags.all(), many=True).data
        ret['author'] = UserSerializer(instance.author).data
        return ret


class FavoriteRecipeSerializer(ModelSerializer):
    """Сериализатор избранных рецептов."""
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('name', 'cooking_time')

    def validate(self, data):
        recipe = self.context['recipe']
        user = self.context['request'].user
        if user.favorited.filter(recipe=recipe).exists():
            raise ValidationError(
                detail='Рецепт уже в избранном.',
                code=HTTP_400_BAD_REQUEST)
        return recipe


class ShoppingListSerializer(ModelSerializer):
    """Сериализатор рецептов для списка покупок."""
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('name', 'cooking_time')

    def validate(self, data):
        recipe = self.context['recipe']
        user = self.context['request'].user
        if user.in_shopping_cart.filter(recipe=recipe).exists():
            raise ValidationError(
                detail='Рецепт уже в списке покупок.',
                code=HTTP_400_BAD_REQUEST)
        return recipe


class SimpleRecipeSerializer(ModelSerializer):
    """Сериализатор рецептов краткий."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(ModelSerializer):
    """Сериализатор подписок."""
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()
    avatar = Base64ImageField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count', 'avatar')
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        user = request.user
        if user.is_anonymous:
            return False
        return user.user_subscribe.filter(author_recipies=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        if not request:
            return []
        recipes_limit = request.GET.get('recipes_limit')
        queryset = obj.recipes.all()
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return SimpleRecipeSerializer(queryset, many=True,
                                      context={'request': request}).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def validate(self, data):
        author = self.context['author']
        user = self.context['request'].user
        if user.user_subscribe.filter(author_recipies=author).exists():
            raise ValidationError(
                detail='Вы уже подписаны.',
                code=HTTP_400_BAD_REQUEST)
        if user == author:
            raise ValidationError(
                detail='Не подписывайся на себя.',
                code=HTTP_400_BAD_REQUEST)
        return author
