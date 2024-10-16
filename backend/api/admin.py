from django.contrib import admin
from recipes.models import User, Tag, Ingredient, Recipe, Subscribe, Chosen, ShoppingList


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Subscribe)
admin.site.register(Chosen)
admin.site.register(ShoppingList)
