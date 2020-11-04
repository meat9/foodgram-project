from django.forms import ModelForm, CheckboxSelectMultiple, ModelChoiceField
from posts.models import Recipe, Ingredients


class PostForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'image', 'description', 'tags', 'cooking_time', 'ingredients')
        widgets = {
            'tags': CheckboxSelectMultiple(),
            
        }
