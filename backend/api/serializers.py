import base64
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import (CurrentUserDefault,
                                        ModelSerializer,
                                        Serializer,
                                        CharField,
                                        IntegerField,
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

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'avatar')
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        user = request.user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author_recipies=obj).exists()
        
class UserCreateSerializer(ModelSerializer):
#    username = RegexField(regex=r'^[\w.@+-]+\Z')

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

    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')
    #ingredient = ReadOnlyField(source='ingredient.name')

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measurement_unit', 'amount')
#        read_only_fields = ('amount',)


class RecipeSerializer(ModelSerializer):

    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer()
    ingredients = AmountSerializer(source='recipe_ingredients', many=True, read_only=True)

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
        return ShoppingList.objects.filter(recipe=obj).exists()


class AmountCreateRecipeSerializer(ModelSerializer):

    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = Amount
        fields = ('id', 'amount')


class CreateRecipeSerializer(ModelSerializer):

    ingredients = AmountCreateRecipeSerializer(many=True, write_only=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'image', 'name', 'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        if self.context.get('request').user:
            return False
        return Chosen.objects.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request').user:
            return False
        return ShoppingList.objects.filter(recipe=obj).exists()

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError(
                {'ingredients': 'Ингридиент, обязательное поле!'})
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(Ingredient, name=item['id'])
            if ingredient in ingredients_list:
                raise ValidationError(
                    {'ingredients': 'Дублирование ингридиентов запрещено!'})
            if int(item['amount']) <= 0:
                raise ValidationError(
                    {'amount': 'Количество не меньше 1!'})
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError(
                {'tags': 'Тег, обязательное поле!'})
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError(
                    {'tags': 'Дублирование тегов запрещено!'})
            tags_list.append(tag)
        return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
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
        return recipe

    
    def update(self, instance, validated_data):
        # Получаем ингредиенты и теги из validated_data
        ingredients_data = validated_data.pop('ingredients', None)
        if not ingredients_data:
            raise ValidationError(
                {'ingredients': 'Ингридиент, обязательное поле!'})
        tags_data = validated_data.pop('tags', None)
        if not tags_data:
            raise ValidationError(
                {'tags': 'Тег, обязательное поле!'})
        # Обновляем остальные поля рецепта
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        # Очищаем текущие ингредиенты и теги
        instance.ingredients.clear()  # данные обязательны, можно перезаписать
        instance.tags.clear()  # данные обязательны, можно перезаписать
        # Устанавливаем новые теги
        instance.tags.set(tags_data)
        # Обновляем ингредиенты
        for ingredient_data in ingredients_data:
            # Получаем id ингредиента и количество
            ingredient_id = ingredient_data['id']
            amount = ingredient_data['amount']
            # Используем update_or_create для обновления или создания новой записи
            Amount.objects.update_or_create(
                recipe=instance,
                ingredient=ingredient_id,
                defaults={'amount': amount}
            )
        instance.save()  # Сохраняем обновленный рецепт
        return instance

    def to_representation(self, instance):
        """Корректировка формата вывода данных."""
        ret  = super().to_representation(instance)
        ret ['ingredients'] = AmountSerializer(
            instance.recipe_ingredients.all(), many=True).data
        ret ['tags'] = TagSerializer(instance.tags.all(), many=True).data
        ret ['author'] = UserSerializer(instance.author).data
        #ret ['is_favorited'] = RecipeSerializer(instance.is_favorited).data
        #ret = RecipeSerializer(instance.all()).data
        return ret


class ChosenSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingListSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeRecipeSerializer(ModelSerializer):
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

class SubscribeSerializer(ModelSerializer):
    
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 
                  'is_subscribed', 'recipes', 'recipes_count', 'avatar')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        user = request.user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author_recipies=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        if not request:
            return []
        #limit_in_shopping_cart = request.GET.get('is_in_shopping_cart')
        recipes_limit = request.GET.get('recipes_limit')
        queryset = obj.recipes.all()
        #breakpoint()
        #if limit_in_shopping_cart:
        #queryset = queryset.filter('is_in_shopping_cart')
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return SubscribeRecipeSerializer(queryset, many=True, context={'request': request}).data

        '''request = self.context.get('request')
        if not request:
            return []
        recipies = obj.recipes.all()
        return SubscribeRecipeSerializer(recipies, many=True, context={'request': request}).data'''

    def get_recipes_count(self, obj):
        return obj.recipes.count()
