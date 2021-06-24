from django.contrib import admin

from .models import (
    Favorite, Follow, Ingredient,
    IngredientRecipe, Purchase, Recipe, Tag
)


class IngredientRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    """
        Настройка админки для рецептов
    """
    list_display = ("pk", "author", "title")
    search_fields = ("text",)
    list_filter = ("author", "title", "tags")
    inlines = [
        IngredientRecipeInline,
    ]


class FavoriteAdmin(admin.ModelAdmin):
    """
        Настройка админки для избранного
    """
    list_display = ('user', 'recipe',)
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    """
        Настройка админки для ингредиентов
    """
    list_display = ("pk", "title", "dimension")
    search_fields = ("title",)
    list_filter = ("title",)


admin.site.register(Purchase)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(IngredientRecipe)

admin.site.site_header = 'FoodGram Admin'

