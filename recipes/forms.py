from django import forms

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'cook_time',
            'description',
            'image',
            'tag'
        ]
        widgets = {
                   'description': forms.Textarea(attrs={'rows': 8}),
                   }
