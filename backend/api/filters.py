from django_filters.rest_framework import FilterSet, Filter, filters

from recipes.models import Recipe, Tag, User


class RecipeFilter(FilterSet):  # взял из док-ции по рекомендуемым типам
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug')
    is_favorited = filters.NumberFilter(method='filter_is_favorited')  # field_name='favorited', lookup_expr='exact')
    is_in_shopping_cart = filters.NumberFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['tags', 'author']

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if not self.request.user.is_authenticated:
            return queryset
        if value == 0:
            queryset = queryset.exclude(in_shopping_cart__user=self.request.user)
        else:
            queryset = queryset.filter(in_shopping_cart__user=self.request.user)
        return queryset
    
    def filter_is_favorited(self, queryset, name, value):
        if not self.request.user.is_authenticated:
            return queryset
        if value == 0:
            queryset = queryset.exclude(favorited__user=self.request.user)
        else:
            queryset = queryset.filter(favorited__user=self.request.user)
        return queryset
    