from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from recipes.models import (Amount, Chosen, Ingredient, Recipe, ShoppingList,
                            Subscribe, Tag, User)


class IngredientResource(resources.ModelResource):
    """Админ настройка ресурсов для поля ингридиентов."""

    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    """Админ настройка ингридиентов."""
    resource_classes = [IngredientResource]
    list_display = ('id', 'name', 'measurement_unit',)
    list_editable = ('name', 'measurement_unit',)
    search_fields = ('name',)


class UserAdmin(ImportExportModelAdmin):
    """Админ настройка пользователей."""
    list_display = ('id', 'role', 'first_name', 'last_name',
                    'username', 'email', 'avatar',)
    list_editable = ('role', 'first_name', 'last_name',
                     'username', 'email', 'avatar',)
    search_fields = ('email', 'username',)


class TagAdmin(ImportExportModelAdmin):
    """Админ настройка Тэгов."""
    list_display = ('id', 'name', 'slug',)
    list_editable = ('name', 'slug',)


class ChosenInline(admin.StackedInline):
    """Админ настройка доступа из рецептов к избранному."""
    model = Chosen
    extra = 0


class AmountInline(admin.StackedInline):
    """Админ настройка доступа из рецептов к избранному."""
    model = Amount
    extra = 0


class RecipeAdmin(ImportExportModelAdmin):
    """Админ настройка рецептов."""
    inlines = (ChosenInline, AmountInline)
    list_display = ('id', 'name', 'author', 'in_сhosen',)
    list_edittable = ('name', 'author',)
    filter_horizontal = ('tags',)
    search_fields = ('name', 'author__username',)
    list_filter = ('tags',)
    search_help_text = 'Рецепты'

    def in_сhosen(self, obj):
        return obj.favorited.all().count()
    in_сhosen.short_description = 'В избранном'


class SubscribeAdmin(ImportExportModelAdmin):
    """Админ настройка подписки."""
    list_display = ('id', 'author_recipies', 'user',)
    list_editable = ('author_recipies', 'user',)


class ChosenAdmin(ImportExportModelAdmin):
    """Админ настройка избранного."""
    list_display = ('id', 'user', 'recipe',)
    list_editable = ('user', 'recipe',)


class ShoppingListAdmin(ImportExportModelAdmin):
    """Админ настройка списка покупок."""
    list_display = ('id', 'user', 'recipe',)
    list_editable = ('user', 'recipe',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Chosen, ChosenAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
