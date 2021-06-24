import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import RecipeForm
from .models import (Favorite, Follow, Ingredient, IngredientRecipe, Purchase,
                     Recipe, Tag, User)


def get_ingredients(request):
    """
        Получение ингредиентов
    """
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = int(
                request.POST[f'valueIngredient_{_[1]}']
            )
    return ingredients


def index(request):
    """
        Главная страница
    """
    tags_list = request.GET.getlist('tags')
    if not tags_list:
        tags_list = ['breakfast', 'lunch', 'dinner']
    recipe_list = Recipe.objects.filter(
        tags__title__in=tags_list
    ).select_related('author').prefetch_related('tags').distinct()
    paginator = Paginator(recipe_list, settings.RECIPE_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags_list': tags_list,
    }
    return render(request, 'index.html', context)


@login_required
def create_recipe(request):
    """
        Создание рецепта
    """
    author = get_object_or_404(User, username=request.user)
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = RecipeForm(
            request.POST or None, files=request.FILES or None
        )
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = author
            recipe.save()
            for title, value in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                recipe_ingredient = IngredientRecipe(
                    value=value,
                    ingredient=ingredient,
                    recipe=recipe
                )
                recipe_ingredient.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm()
    return render(
        request,
        'form_recipe.html',
        {
            'form': form,
            'tags': tags,
            'new': True
        }
    )


def recipe_view(request, recipe_id):
    """
        Просмотр рецепта
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe,
    }
    return render(request, 'recipe.html', context)


@login_required()
def recipe_edit(request, recipe_id):
    """
        Редактирование рецепта
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('index')
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)
    tags = recipe.tags.all()
    ingredients = get_ingredients(request)
    if form.is_valid():
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        for title, value in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            recipe_ingredient = IngredientRecipe(
                value=value,
                ingredient=ingredient,
                recipe=recipe
            )
            recipe_ingredient.save()
        form.save_m2m()
        return redirect('recipe', recipe_id=recipe.id)
    return render(request,
                  'form_recipe.html',
                  {'form': form,
                   'recipe': recipe,
                   'tags': tags,
                   'new': False,
                   }
                  )


@login_required
def recipe_delete(request, recipe_id):
    """
        Удаление рецепта
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')


def profile(request, username):
    """
        Страница автора рецептов
    """
    profile = get_object_or_404(User, username=username)
    tags_list = request.GET.getlist('tags')
    if not tags_list:
        tags_list = ['breakfast', 'lunch', 'dinner']
    recipes = Recipe.objects.filter(
        author=profile, tags__title__in=tags_list
    ).prefetch_related('tags').distinct()
    paginator = Paginator(recipes, settings.RECIPE_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {
        'page': page,
        'paginator': paginator,
        'profile': profile,
        'recipes': recipes,
        'tags_list': tags_list,
    })


@login_required()
def favorites(request):
    """
        Страница избранных рецептов
    """
    tags_list = request.GET.getlist('tags')
    if not tags_list:
        tags_list = ['breakfast', 'lunch', 'dinner']
    recipes = Recipe.objects.select_related('author').prefetch_related(
        'tags',
    ).filter(favorite_recipe__user=request.user)
    paginator = Paginator(recipes, settings.RECIPE_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html', {
        'page': page,
        'paginator': paginator,
        'profile': profile,
        'recipes': recipes,
        'tags_list': tags_list,
    })


@login_required()
def purchase_list(request):
    """
        Страница покупок по рецептам
    """
    recipes = request.user.purchases.all()
    return render(request, 'purchase_list.html', {'recipes': recipes})


@login_required()
def purchase_recipe_delete(request, recipe_id):
    """
        Удаление рецепта из покупок
    """
    recipe = get_object_or_404(Purchase, user=request.user, recipe=recipe_id)
    recipe.delete()
    return redirect('purchase_list')


@login_required()
def purchase_list_download(request):
    """
        Скачивание списка ингредиентов для покупки
    """
    user = request.user
    shopping = user.purchases.all().values_list('recipe_id', flat=True)
    ingredients = IngredientRecipe.objects.values(
        'ingredient_id__title', 'ingredient_id__dimension').filter(
        recipe_id__in=list(shopping)).annotate(
        total=Sum('value')).order_by('ingredient')
    file_data = 'Список покупок с сайта FoodGram. \n'
    for item in ingredients:
        line = ' '.join(str(value) for value in item.values())
        file_data += line + '\n'
    response = HttpResponse(
        file_data, content_type='application/text charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response


@login_required()
def follow_list(request):
    """
        Страница подписок на авторов рецептов
    """
    follows = Follow.objects.select_related(
        'user', 'author'
    ).filter(user=request.user)
    paginator = Paginator(follows, settings.RECIPE_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'my_follow.html', {
        'page': page,
        'paginator': paginator,
    })


class Favorites(View):
    """
        Добавление рецепта в избранное
        и удаление из избранного
    """
    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        Favorite.objects.get_or_create(
            user=request.user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite = get_object_or_404(
            Favorite,
            user=request.user,
            recipe=recipe)
        favorite.delete()
        return JsonResponse({'success': True})


class Following(View):
    """
        Добавление профиля автора в подписки
        и удаление профиля из подписок
    """
    def post(self, request):
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)
        Follow.objects.get_or_create(user_id=request.user.id, author=author)
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        user = get_object_or_404(User, username=request.user.username)
        author = get_object_or_404(User, id=author_id)
        following = get_object_or_404(Follow, user=user, author=author)
        following.delete()
        return JsonResponse({'success': True})


class Ingredients(View):
    """
        Фильтрация ингредиентов по GET запросу
    """
    def get(self, request):
        ingredient = request.GET['query']
        ingredients = list(Ingredient.objects.filter(
            title__icontains=ingredient).values('title', 'dimension'))
        return JsonResponse(ingredients, safe=False)


class Purchases(View):
    """
        Добавление рецепта в список покупок
        и удаление из списка
    """
    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Purchase.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = get_object_or_404(User, username=request.user.username)
        purchase = get_object_or_404(Purchase, user=user, recipe=recipe)
        purchase.delete()
        return JsonResponse({'success': True})


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
