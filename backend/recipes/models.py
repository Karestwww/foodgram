from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователей"""

    class Role(models.TextChoices):
        USER = 'user', _('User')
        ADMIN = 'admin', _('Admin')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    username = models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'email']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('role', 'id')


class Tag(models.Model):
    '''Модель тега рецепта.'''
    name = models.CharField(
        max_length=256,
        default=None,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('name', 'slug')


class Ingredient(models.Model):
    '''Модель ингредиента.'''
    name = models.CharField(
        max_length=256,
        default=None,
        verbose_name='Название'
    )
    unit_measure = models.CharField(
        max_length=50,
        default=None,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)


class Recipe(models.Model):
    '''Модель рецептов'''

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=256, verbose_name='Название рецепта')
    image = ''
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание блюда'
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Время приготовления в минутах'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)


class Chosen(models.Model):
    '''Модель избранных рецептов.'''
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='chosen',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'избранный'
        verbose_name_plural = 'Избранные'
        ordering = ('recipe', 'author')


class Shopping_list(models.Model):
    '''Модель списка покупок.'''
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='shopping_list',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'избранный'
        verbose_name_plural = 'Избранные'
        ordering = ('recipe', 'author')
