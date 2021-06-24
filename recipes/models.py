from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from sorl.thumbnail import ImageField

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента',
        help_text='Укажите название ингредиента',
        db_index=True,
    )
    dimension = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
        help_text='Укажите единицу измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        db_table = 'recipes_ingredients'

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Tag(models.Model):
    title = models.CharField(
        max_length=20,
        verbose_name='Тэг',
        db_index=True,
        unique=True,
    )
    display_name = models.CharField(
        verbose_name='Имя тэга',
        max_length=20,
    )
    color = models.CharField(
        verbose_name='Цвет тэга',
        max_length=20,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.display_name


class Recipe(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Укажите название рецепта',
        unique=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Опишите Ваш рецепт',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        help_text='Выберите один или несколько ингридиентов',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    image = ImageField(
        upload_to='static/images/',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тэги',
    )
    cook_time = models.PositiveIntegerField(
        verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент в рецепте',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe',
        verbose_name='Рецепт',
    )
    value = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(1)],
        verbose_name='Кол-во',
        help_text='Введите кол-во продукта',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_recipe_ingredient'
            )
        ]
        verbose_name = 'Ингредиент в рецептах'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'{self.ingredient}, {self.value}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )
    in_bookmarks = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}, {self.recipe.title}, {self.in_bookmarks}'

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    def __str__(self):
        return f'follower - {self.user} | following - {self.author}'

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchase_recipe',
        verbose_name='Список рецептов'
    )

    def __str__(self):
        return self.recipe.title

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
