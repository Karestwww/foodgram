from django.contrib import admin
from recipes.models import User, Tag, Ingredient, Recipe, Subscribe, Chosen, ShoppingList
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]


admin.site.register(Ingredient, IngredientAdmin)


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Subscribe)
admin.site.register(Chosen)
admin.site.register(ShoppingList)
