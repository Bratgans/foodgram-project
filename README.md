[![foodgram Actions Status](https://github.com/Bratgans/foodgram-project/workflows/foodgram/badge.svg)](https://github.com/Bratgans/foodgram-project/actions)
# foodgram-project
### «Продуктовый помощник» (Дипломный Проект студента Яндекс.Практикум)

Доступен по адресу: http://bratgans.ga/

## Описание
Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии
Python 3.8.10, Django 3.0.5

## Запуск (docker)
Запустить docker-compose:

`docker-compose up`

### При первом запуске для функционирования проекта обязательно: 
Выполнить миграции:

`docker-compose exec web python manage.py migrate`

Создать суперпользователя (админа):

`docker-compose exec web python manage.py createsuperuser`

Собрать статику:

`docker-compose exec web python manage.py collectstatic --no-input`

Загрузить список ингредиентов в БД:

`docker-compose exec web python manage.py load_ingredients static/ingredients/ingredients.json`
