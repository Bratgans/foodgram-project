from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title =
    dimension =
    quantity =

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        help_text='Укажите название рецепта',
        unique=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Опишите Ваш рецепт',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        help_text='Выберите один или несколько ингридиентов',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    image = models.ImageField(
        upload_to='static/images/',
    )
    tag = models.ManyToManyField(

    )
    cook_time = models.IntegerField(
        verbose_name='Время приготовления в минутах'
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.name
