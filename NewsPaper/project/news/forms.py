from django.forms import ModelForm, BooleanField
from .models import Post
from django.contrib.auth.models import User

# Создаём модельную форму
class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title',
                  'text',
                  'postCategory',
                  'author'
                  ]
