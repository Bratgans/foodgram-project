from django import template

from recipes.models import Favorite, Follow, Purchase
from recipes.views import get_all_tags

register = template.Library()


RECIPE = 'рецепт'
FEW_RECIPE = 'рецепта'
RECIPES = 'рецептов'


@register.filter()
def recipe_plural(value):
    """
        Изменение слова в зависимости от кол-ва
    """
    value -= 3
    word = RECIPES
    if (value % 100 == 1) or (value % 100 > 20) and (value % 10 == 1):
        word = RECIPE
    if (value % 100 == 2) or (value % 100 > 20) and (value % 10 == 2):
        word = FEW_RECIPE
    if (value % 100 == 3) or (value % 100 > 20) and (value % 10 == 3):
        word = FEW_RECIPE
    if (value % 100 == 4) or (value % 100 > 20) and (value % 10 == 4):
        word = FEW_RECIPE
    return f'Еще {value} {word}...'


@register.filter()
def url_with_get(request, number):
    """
        Получение номера страницы
    """
    query = request.GET.copy()
    query['page'] = number
    return query.urlencode()


@register.filter(name='get_filter_tags')
def get_filter_tags(request, tag):
    """
        Получение тэгов
    """
    new_request = request.GET.copy()
    tags_list = new_request.getlist('tags')
    if not tags_list:
        tags_list = get_all_tags(request)
    if tag.title in tags_list:
        tags_list.remove(tag.title)
        new_request.setlist('tags', tags_list)
    else:
        new_request.appendlist('tags', tag.title)
    return new_request.urlencode()


@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    """
        Проверка наличия рецепта в избранном
    """
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='is_follow')
def is_follow(author, user):
    """
        Проверка наличия подписки на автора
    """
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter(name='in_purchases')
def in_purchases(recipe, user):
    """
        Проверка налиция рецепта в покупках
    """
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='purchase_count')
def purchase_count(request, user_id):
    """
        Считает количество покупок для синего счетчика
    """
    return Purchase.objects.filter(user=user_id).count()
