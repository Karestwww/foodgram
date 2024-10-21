from django_filters.rest_framework import CharFilter, FilterSet
from django_filters.rest_framework.filters import (ModelChoiceFilter,
                                                   ModelMultipleChoiceFilter,
                                                   NumberFilter)
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag, User


class RecipeFilter(FilterSet):
    """Фильтр для рецептов."""
    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug')
    ingredients__name = CharFilter(lookup_expr='icontains')
    is_favorited = NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = NumberFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'ingredients']

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        if value == 0:
            queryset = queryset.exclude(in_shopping_cart__user=user)
        else:
            queryset = queryset.filter(in_shopping_cart__user=user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        if value == 0:
            queryset = queryset.exclude(favorited__user=user)
        else:
            queryset = queryset.filter(favorited__user=user)
        return queryset


class IngredientFilter(SearchFilter):
    """Фильтр ингридиентов"""
    name = CharFilter(lookup_expr='icontains', field_name='name')
