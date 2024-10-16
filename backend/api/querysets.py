from recipes.models import Ingredient, ShoppingList, Amount


#Надо вывести список:
#{Ингридиент}" ("{мера измерения}") — "{кол-во}
def shopping_cart_file(self, request, user):
    """Функция формирования файлов ингридиентов."""
    ingridients = Ingredient.objects.filter()
    user=user
    shopping_list = ShoppingList.objects.filter(user=user)  # получаем queryset по списку покупок
    
