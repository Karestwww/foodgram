Находясь в папке infra, выполните команду docker compose up. При выполнении этой команды контейнер frontend, описанный в docker-compose.yml, подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу.

По адресу http://localhost изучите фронтенд веб-приложения, а по адресу http://localhost/api/docs/ — спецификацию API.


Проект состоит из следующих страниц: 
главная, - по 6 рецептов, сортировка по дате от новых к старым
страница входа,
страница регистрации, - после регистрации переход на страницу входа
страница рецепта, - отличаются у залогиненного пользователя и гостя
страница пользователя, - все рецепты пользователя и возможность подписаться/отписаться
страница подписок, - только для залогиненного пользователя
избранное, - только для залогиненного пользователя, другим на регистрацию или вход
список покупок, - при клике рецепта добавить в покупки, рецепты добавляются в список покупок 
                - можно скачать уже список продуктов для всех рецептов в формате .txt, .pdf
создание и редактирование рецепта, - только для залогиненного пользователя
страница смены пароля,
статические страницы «О проекте» и «Технологии». - по умолчанию 404, можно настроить



Разграничение прав:
гость (анонимный пользователь), - просмотр пользователей и рецептов
аутентифицированный (залогиненный) пользователь, - функционал проекта
администратор () - то же что и залогиненный плюс администрирование



Должно быть три базовые модели: «Рецепт», «Тег» и «Ингредиент» и еще другие модели

Пользователь (на основе встроенной модели User)
имя,
фамилия,
ник пользователя,
адрес электронной почты,
пароль.

Рецепт (все поля обязательны для заполнения - каскадное удаление от пользователя) состоит из:
Автор публикации.
Название.
Картинка.
Текстовое описание.
Ингредиенты — продукты для приготовления блюда по рецепту. (продумать если ингредиент удалят, то что делать с рецептом)
              Множественное поле с выбором из предустановленного списка и с указанием количества и единицы измерения.
Тег. Можно установить несколько тегов на один рецепт. (продумать, если теги удалят, то стоит ли удалять рецепт?)
Время приготовления в минутах.

Тег (все поля обязательны для заполнения и уникальны) состоит из:
Название.
Slug.

Ингредиент (все поля обязательны для заполнения) состоит из:
Название.
Единица измерения.

Избранное (если рецепт удалят, то удалять из избранного)
Автор публикации.
Рецепт

Список_покупок (если рецепт удалят, то удалять из списка покупок)
Автор публикации.
Рецепт



Админка
В интерфейс админ-зоны нужно вывести необходимые поля моделей и настроить поиск:
- вывести все модели с возможностью редактирования и удаления записей;
- для модели пользователей добавить поиск по адресу электронной почты и имени пользователя;
- для модели рецептов:
    - в списке рецептов вывести название и имя автора рецепта;
    - добавить поиск по автору, названию рецепта, и фильтрацию по тегам;
    - на странице рецепта вывести общее число добавлений этого рецепта в избранное.
- для модели ингредиентов:
    - в список вывести название ингредиента и единицы измерения;
    - добавить поиск по названию.


Проект ()
foodgram_backend

Два приложения
api()
recipes()



Требуемые urls
http://localhost:8000/api/users/ - сделан url - работает, постмен прошел
http://localhost:8000/api/users/{id}/ - сделан url - работает, постмен прошел
http://localhost:8000/api/users/me/ - сделан url - работает, постмен прошел
http://localhost:8000/api/users/me/avatar/ - сделан url - работает, постмен прошел
http://localhost:8000/api/users/set_password/ - сделан url - работает, постмен прошел
http://localhost:8000/api/auth/token/login/ - сделан url  - работает, постмен прошел
http://localhost:8000/api/auth/token/logout/ - сделан url - работает, постмен прошел
http://localhost:8000/api/tags/ - сделан url
http://localhost:8000/api/tags/{id}/ - сделан url
http://localhost:8000/api/recipes/ - сделан url
http://localhost:8000/api/recipes/{id}/ - сделан url
http://localhost:8000/api/recipes/{id}/get-link/ - сделан url
http://localhost:8000/api/recipes/download_shopping_cart/ - сделан url
http://localhost:8000/api/recipes/{id}/shopping_cart/ - сделан url
http://localhost:8000/api/recipes/{id}/favorite/ - сделан url
http://localhost:8000/api/users/subscriptions/ - сделан url
http://localhost:8000/api/users/{id}/subscribe/ - сделан url
http://localhost:8000/api/ingredients/ - сделан url
http://localhost:8000/api/ingredients/{id}/ - сделан url

