from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Recipe, Tag


def index(request):
    tags_list = request.GET.getlist('filters')
    if not tags_list:
        tags_list = ['breakfast', 'lunch', 'dinner']
    recipes_list = Recipe.objects.filter(tag__title__in=tags_list).\
        select_related('author').prefetch_related('tag').distinct()
    all_tags = Tag.objects.all()
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'all_tags': all_tags,
        'tags_list': tags_list
    }
    return render(request, 'index.html', context)
