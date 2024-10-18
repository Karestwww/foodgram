from recipes.models import Ingredient, ShoppingList, Amount, Recipe
from django.http import HttpResponse
from django.db.models import Sum


#Надо вывести список:
#{Ингридиент}" ("{мера измерения}") — "{кол-во}
def shopping_cart_file(self, request, user):
    """Функция формирования файлов ингридиентов."""
    # для проверки - print(Amount.objects.filter(recipe__in_shopping_cart__user=user).values('ingredient__name', 'ingredient__measurement_unit', 'amount'))
    ingridients = Amount.objects.filter(
        recipe__in_shopping_cart__user=user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(sum_amount=Sum('amount', distinct=True)).order_by('ingredient__name')
    print(ingridients)
    shopping_data_txt = f'Список покупок. Пользователь - {user.first_name} {user.last_name}\n'
    for ingridient in ingridients:
        shopping_data_txt += (f"({ingridient['ingredient__name']} ({ingridient['ingredient__measurement_unit']}) — {str(ingridient['sum_amount'])})\n")
    #print(shopping_data_txt)
    return HttpResponse(shopping_data_txt, content_type='text/plain', charset="utf-8")
