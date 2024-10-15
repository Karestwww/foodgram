from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


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
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+\Z',),],
        )
    email = models.EmailField(max_length=254, unique=True)
    #is_subscribed = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to='media/avatar/',
        null=True,
        default=None,
        verbose_name='Фото аватара',
    )
    password = models.CharField(max_length=254)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)


class Tag(models.Model):
    '''Модель тега рецепта.'''
    name = models.CharField(
        max_length=32,
        verbose_name='Название тега'
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        verbose_name='Слаг'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('name', 'slug')


class Ingredient(models.Model):
    '''Модель ингредиента.'''
    name = models.CharField(
        max_length=128,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=64,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', 'measurement_unit')


class Recipe(models.Model):
    '''Модель рецептов'''

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
#        related_name='recipes'
    )
    name = models.CharField(max_length=256, verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='media/recipes/',
        verbose_name='Фото блюда',
    )
    text = models.TextField(
        verbose_name='Описание блюда',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Amount',
#        related_name='recipes',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        Tag,
#        related_name='recipes',
        verbose_name='Тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Время приготовления в минутах'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('id', 'name')
        default_related_name = 'recipes'


class Amount(models.Model):
    '''Модель для кол-ва ингридиентов в рецепте'''
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,)
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Кол-во ингридиента'
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients')]


class Chosen(models.Model):
    '''Модель избранных рецептов.'''
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='favorited'
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='favorited',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'избранный'
        verbose_name_plural = 'Избранные'
        ordering = ('author',)


class Subscribe(models.Model):
    '''Модель подписок пользователя.'''
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='user_subscribe'
    )

    author_recipies = models.ForeignKey(
        User,
        verbose_name='Автор рецептов',
        on_delete=models.CASCADE,
        related_name='author_recipies_subscribe'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('author_recipies', 'id')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author_recipies'],
                name='unique_subscribes')]


class ShoppingList(models.Model):
    '''Модель списка покупок.'''
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='in_shopping_cart'
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='in_shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'избранный'
        verbose_name_plural = 'Избранные'
        ordering = ('author',)
