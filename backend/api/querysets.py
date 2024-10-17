from recipes.models import Ingredient, ShoppingList, Amount, Recipe


#Надо вывести список:
#{Ингридиент}" ("{мера измерения}") — "{кол-во}
def shopping_cart_file(self, request, user):
    """Функция формирования файлов ингридиентов."""
    ingridients = Amount.objects.filter(
        recipe__in_shopping_cart__user=user).values(
            'ingredient__name', 'ingredient__measurement_unit', 'amount', 'recipe__name'
            )
    for ingridient in ingridients:
        print (ingridient['ingredient__name'] + " (" + ingridient['ingredient__measurement_unit'] + ") — " + str(ingridient['amount']))
    breakpoint()
    print(user)
