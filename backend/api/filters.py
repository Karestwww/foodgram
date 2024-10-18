from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe, Tag, User


class RecipeFilter(FilterSet):  # взял из док-ции по рекомендуемым типам
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug')
    is_favorited = filters.BooleanFilter()
    is_in_shopping_cart = filters.BooleanFilter()

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_in_shopping_cart']

    def filter_is_in_shopping_cart(self, queryset):
        if not self.request.user.is_authenticated:
            return queryset
        return queryset.filter(in_shopping_cart__user=self.request.user)
    