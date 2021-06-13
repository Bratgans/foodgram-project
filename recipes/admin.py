from django.contrib import admin

from .models import Ingredient, Recipe, Tag, UserRecipeRelation


class IngredientRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientRecipeInline,
    ]
    ordering = ['title']


admin.site.register(UserRecipeRelation)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)

admin.site.site_header = 'FoodGram Admin'

