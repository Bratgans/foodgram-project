from django import forms
from django.forms import CheckboxSelectMultiple

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'tags',
            'cook_time',
            'description',
            'image'
        ]
        widgets = {
                   'description': forms.Textarea(attrs={'rows': 8}),
                   'tags': CheckboxSelectMultiple()
                   }
