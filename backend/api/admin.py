from django.contrib import admin
from recipes.models import User, Tag, Ingredient, Recipe, Subscribe


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Subscribe)
