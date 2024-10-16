from recipes.models import Ingredient, ShoppingList, Amount, Recipe


#Надо вывести список:
#{Ингридиент}" ("{мера измерения}") — "{кол-во}
def shopping_cart_file(self, request, user):
    """Функция формирования файлов ингридиентов."""
    ingridients = Ingredient.objects.filter()
    user = user
    recipes = Recipe.objects.filter(author=user)
    shopping_list = ShoppingList.objects.filter(user=user)  # получаем queryset по списку покупок
    #asd = recipes.in_shopping_cart
    breakpoint()
    print(user)
