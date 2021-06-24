from django import template

from recipes.models import Favorite, Follow, Purchase
from recipes.views import get_all_tags

register = template.Library()


@register.filter()
def url_with_get(request, number):
    query = request.GET.copy()
    query['page'] = number
    return query.urlencode()


@register.filter(name='get_filter_tags')
def get_filter_tags(request, tag):
    new_request = request.GET.copy()
    if not request.GET.getlist('tags'):
        tags_list = get_all_tags()
    else:
        tags_list = new_request.getlist('tags')
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
    Проверка наличия рецепта в избранном
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
    count = Purchase.objects.filter(user=user_id).count()
    return count
