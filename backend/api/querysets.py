from django.db.models import Sum
from django.http import HttpResponse
from recipes.models import Amount


def shopping_cart_file(self, request, user):
    """Функция формирования файлов ингридиентов."""
    ingridients = Amount.objects.filter(
        recipe__in_shopping_cart__user=user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
                sum_amount=Sum(
                    'amount', distinct=True)).order_by('ingredient__name')
    shopping_txt = 'Список покупок. Пользователь - '
    shopping_txt += (f"{user.first_name} {user.last_name}\n")
    for ingridient in ingridients:
        shopping_txt += (f"({ingridient['ingredient__name']} "
                         f"({ingridient['ingredient__measurement_unit']}) — "
                         f"{str(ingridient['sum_amount'])})\n")
    return HttpResponse(shopping_txt,
                        content_type='text/plain',
                        charset="utf-8")
