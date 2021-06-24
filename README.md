![FoodGram](https://github.com/Bratgans/foodgram-project/actions/workflows/yamdb_workflow.yml/badge.svg)
# foodgram-project
###«Продуктовый помощник» (Дипломный Проект студента Яндекс.Практикум)

Доступен по адресу: http://84.252.141.9/

##Описание
Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск (docker)
###prod
Запустить docker-compose:

`docker-compose up`

При первом запуске для функционирования проекта обязательно выполнить миграции:

`docker-compose exec web python manage.py migrate`

Чтобы загрузить список ингредиентов в БД:

`docker-compose exec web python manage.py loaddata ingredients.json`

###local
Запустить docker-compose (файл docker-compose.localhost.yml):

`docker-compose -f ./docker-compose.localhost.yml up`

При первом запуске для функционирования проекта обязательно выполнить миграции:

`docker-compose exec web python manage.py migrate`

Чтобы ззагрузить список ингредиентов в БД:

`docker-compose exec web python manage.py loaddata ingredients.json`