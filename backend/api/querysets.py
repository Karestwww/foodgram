from recipes.models import Ingredient, ShoppingList, Amount, Recipe


#Надо вывести список:
#{Ингридиент}" ("{мера измерения}") — "{кол-во}
def shopping_cart_file(self, request, user):
    """Функция формирования файлов ингридиентов."""
    ingridients = Amount.objects.filter(
        recipe__in_shopping_cart__user=user).values(
            'ingredient__name', 'ingredient__measurement_unit'
            )
    user = user
    recipes = Recipe.objects.filter(author=user)
    shopping_list = ShoppingList.objects.filter(user=user)  # получаем queryset по списку покупок
    #asd = recipes.in_shopping_cart
    breakpoint()
    print(user)
