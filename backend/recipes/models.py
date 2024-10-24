from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.settings import (MAX_AMOUNT, MAX_COOKING_TIME, MIN_AMOUNT,
                              MIN_COOKING_TIME)


class User(AbstractUser):
    """Модель пользователей"""

    class Role(models.TextChoices):
        USER = 'user', _('Пользователь')
        ADMIN = 'admin', _('Администратор')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+\Z',), ],)  # type: ignore
    email = models.EmailField(max_length=254, unique=True)
    avatar = models.ImageField(
        upload_to='avatar/',
        blank=True,
        null=True,
        default=None,
        verbose_name='Фото аватара',
    )
    password = models.CharField(max_length=254)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'
    subscriptions = models.ManyToManyField(
        'self',
        through='Subscribe',
        symmetrical=False,
        related_name='subscribers',
        verbose_name='Подписки'
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        default_related_name = 'user_related_name'

    def __str__(self):
        return self.username


class Tag(models.Model):
    """Модель тега рецепта."""
    name = models.CharField(
        max_length=32,
        verbose_name='Название тега'
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('name', 'slug')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(
        max_length=128,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=64,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', 'measurement_unit')
        default_related_name = 'ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=256, verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Фото блюда',
    )
    text = models.TextField(
        verbose_name='Описание блюда',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Amount',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(MIN_COOKING_TIME),
                    MaxValueValidator(MAX_COOKING_TIME)),
        verbose_name='Время приготовления в минутах'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)
        default_related_name = 'recipes'

    def __str__(self):
        return self.name


class Amount(models.Model):
    """Модель для кол-ва ингридиентов в рецепте"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,)
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(MIN_AMOUNT),
                    MaxValueValidator(MAX_AMOUNT)),
        verbose_name='Кол-во ингридиента'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('amount',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients')]

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'


class Chosen(models.Model):
    """Модель избранных рецептов."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorited'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранный рецепт',
        on_delete=models.CASCADE,
        related_name='favorited'
    )

    class Meta:
        verbose_name = 'избранный'
        verbose_name_plural = 'Избранные'
        ordering = ('id',)

    def __str__(self):
        return f'{self.recipe}'


class Subscribe(models.Model):
    """Модель подписок пользователя."""
    author_recipies = models.ForeignKey(
        User,
        verbose_name='Автор рецептов',
        on_delete=models.CASCADE,
        related_name='author_recipies_subscribe'
    )

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='user_subscribe'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('author_recipies', 'id')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author_recipies'],
                name='unique_subscribes')]

    def __str__(self):
        return f'{self.user} подписан на {self.author_recipies}'


class ShoppingList(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='in_shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='in_shopping_cart'
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe}'
