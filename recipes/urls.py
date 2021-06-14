from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shopping_list', views.shopping_list, name='shopping_list'),
    path('create_recipe', views.create_recipe, name='create_recipe'),
    path('subscriptions', views.subscriptions, name='subscriptions'),
    path('favorites', views.favorites, name='favorites'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
]
