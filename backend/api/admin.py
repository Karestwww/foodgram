from django.contrib import admin
from recipes.models import User, Tag, Ingredient


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Ingredient)
