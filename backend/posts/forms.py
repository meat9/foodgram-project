from django.forms import ModelForm
from posts.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'image', 'text', 'ingredient', 'tag', 'time_to_made']